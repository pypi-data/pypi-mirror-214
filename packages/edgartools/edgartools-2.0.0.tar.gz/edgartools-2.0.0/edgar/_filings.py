import itertools
import os.path
import re
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache, partial
from io import BytesIO
from typing import Tuple, List, Dict, Union, Optional

import httpx
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pa_csv
import pyarrow.parquet as pq
from bs4 import BeautifulSoup
from fastcore.basics import listify
from fastcore.parallel import parallel
from rich.console import Group, Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

from edgar._markdown import MarkdownContent
from edgar._markdown import html_to_markdown
from edgar._rich import df_to_rich_table, repr_rich
from edgar._xbrl import FilingXbrl
from edgar._party import Address
from edgar.core import (http_client, download_text, download_file, log, display_size, sec_edgar, get_text_between_tags,
                        filter_by_date, sec_dot_gov, InvalidDateException, IntString, DataPager, text_extensions)
from edgar.fundreports import FUND_FORMS
from edgar.search import BM25Search, RegexSearch

""" Contain functionality for working with SEC filing indexes and filings

The module contains the following functions

- `get_filings(year, quarter, index)`

"""

__all__ = [
    'Filing',
    'Filings',
    'get_filings',
    'get_funds',
    'FilingXbrl',
    'SECHeader',
    'FilingsState',
    'Attachment',
    'Attachments',
    'FilingHomepage',
    'get_fund_filings',
    'available_quarters',
    'get_by_accession_number',
    'get_restricted_stock_filings',
    'get_insider_transaction_filings'
]

full_index_url = "https://www.sec.gov/Archives/edgar/full-index/{}/QTR{}/{}.{}"

filing_homepage_url_re = re.compile(f"{sec_edgar}/data/[0-9]{1,}/[0-9]{10}-[0-9]{2}-[0-9]{4}-index.html")

headers = {'User-Agent': 'Dwight Gunning dgunning@gmail.com'}

full_or_daily = ['daily', 'full']
index_types = ['form', 'company', 'xbrl']
file_types = ['gz', 'idx']

form_index = "form"
xbrl_index = "xbrl"
company_index = "company"

max_concurrent_http_connections = 10
quarters_in_year: List[int] = list(range(1, 5))

YearAndQuarter = Tuple[int, int]
YearAndQuarters = List[YearAndQuarter]
Years = Union[int, List[int], range]
Quarters = Union[int, List[int], range]

accession_number_re = re.compile(r"\d{10}\-\d{2}\-\d{6}$")

xbrl_document_types = ['XBRL INSTANCE DOCUMENT', 'XBRL INSTANCE FILE', 'EXTRACTED XBRL INSTANCE DOCUMENT']


def current_year_and_quarter() -> Tuple[int, int]:
    now = datetime.now()
    current_year, current_quarter = now.year, (now.month - 1) // 3 + 1
    return current_year, current_quarter


@lru_cache(maxsize=1)
def available_quarters() -> YearAndQuarters:
    """
    Get a list of year and quarter tuples
    :return:
    """
    current_year, current_quarter = current_year_and_quarter()
    start_quarters = [(1994, 3), (1994, 4)]
    in_between_quarters = list(itertools.product(range(1995, current_year), range(1, 5)))
    end_quarters = list(itertools.product([current_year], range(1, current_quarter + 1)))
    return start_quarters + in_between_quarters + end_quarters


def expand_quarters(year: Years,
                    quarter: int = None) -> YearAndQuarters:
    """
    Expand the list of years and a list of quarters to a full list of tuples covering the full range
    :param year: The year or years
    :param quarter: The quarter or quarters
    :return:
    """
    years = listify(year)
    quarters = listify(quarter) if quarter else quarters_in_year
    return [yq
            for yq in itertools.product(years, quarters)
            if yq in available_quarters()
            ]


class FileSpecs:
    """
    A specification for a fixed width file
    """

    def __init__(self, specs: List[Tuple[str, Tuple[int, int], pa.lib.DataType]]):
        self.splits = list(zip(*specs))[1]
        self.schema = pa.schema(
            [
                pa.field(name, datatype)
                for name, _, datatype in specs
            ]
        )


form_specs = FileSpecs(
    [("form", (0, 12), pa.string()),
     ("company", (12, 74), pa.string()),
     ("cik", (74, 82), pa.int32()),
     ("filing_date", (85, 97), pa.string()),
     ("accession_number", (97, 141), pa.string())
     ]
)
company_specs = FileSpecs(
    [("company", (0, 62), pa.string()),
     ("form", (62, 74), pa.string()),
     ("cik", (74, 82), pa.int32()),
     ("filing_date", (85, 97), pa.string()),
     ("accession_number", (97, 141), pa.string())
     ]
)


def read_fixed_width_index(index_text: str,
                           file_specs: FileSpecs) -> pa.Table:
    """
    Read the index text as a fixed width file
    :param index_text: The index text as downloaded from SEC Edgar
    :param file_specs: The file specs containing the column definitions
    :return:
    """
    # Treat as a single array
    array = pa.array(index_text.rstrip('\n').split('\n')[10:])

    # Then split into separate arrays by file specs
    arrays = [
        pc.utf8_trim_whitespace(
            pc.utf8_slice_codeunits(array, start=start, stop=stop))
        for start, stop,
        in file_specs.splits
    ]

    # Change the CIK to int
    arrays[2] = pa.compute.cast(arrays[2], pa.int32())

    # Convert filingdate from string to date
    # Some files have %Y%m-%d other %Y%m%d
    date_format = '%Y-%m-%d' if len(arrays[3][0].as_py()) == 10 else '%Y%m%d'
    arrays[3] = pc.cast(pc.strptime(arrays[3], date_format, 'us'), pa.date32())

    # Get the accession number from the file path
    arrays[4] = pa.compute.utf8_slice_codeunits(
        pa.compute.utf8_rtrim(arrays[4], characters=".txt"), start=-20)

    return pa.Table.from_arrays(
        arrays=arrays,
        names=list(file_specs.schema.names),
    )


def read_pipe_delimited_index(index_text: str) -> pa.Table:
    """
    Read the index file as a pipe delimited index
    :param index_text: The index text as read from SEC Edgar
    :return: The index data as a pyarrow table
    """
    index_table = pa_csv.read_csv(
        BytesIO(index_text.encode()),
        parse_options=pa_csv.ParseOptions(delimiter="|"),
        read_options=pa_csv.ReadOptions(skip_rows=10,
                                        column_names=['cik', 'company', 'form', 'filing_date', 'accession_number'])
    )
    index_table = index_table.set_column(
        0,
        "cik",
        pa.compute.cast(index_table[0], pa.int32())
    ).set_column(4,
                 "accession_number",
                 pc.utf8_slice_codeunits(index_table[4], start=-24, stop=-4))
    return index_table


def fetch_filing_index(year_and_quarter: YearAndQuarter,
                       client: Union[httpx.Client, httpx.AsyncClient],
                       index: str
                       ):
    year, quarter = year_and_quarter
    url = full_index_url.format(year, quarter, index, "gz")
    index_text = download_text(url=url, client=client)
    if index == "xbrl":
        index_table: pa.Table = read_pipe_delimited_index(index_text)
    else:
        # Read as a fixed width index file
        file_specs = form_specs if index == "form" else company_specs
        index_table: pa.Table = read_fixed_width_index(index_text,
                                                       file_specs=file_specs)
    return (year, quarter), index_table


def get_filings_for_quarters(year_and_quarters: YearAndQuarters,
                             index="form") -> pa.Table:
    """
    Get the filings for the quarters
    :param year_and_quarters:
    :param index: The index to use - "form", "company", or "xbrl"
    :return:
    """
    with http_client() as client:
        if len(year_and_quarters) == 1:
            _, final_index_table = fetch_filing_index(year_and_quarter=year_and_quarters[0],
                                                      client=client,
                                                      index=index)
        else:
            quarters_and_indexes = parallel(fetch_filing_index,
                                            items=year_and_quarters,
                                            client=client,
                                            index=index,
                                            threadpool=True,
                                            progress=True
                                            )
            quarter_and_indexes_sorted = sorted(quarters_and_indexes, key=lambda d: d[0])
            index_tables = [fd[1] for fd in quarter_and_indexes_sorted]
            final_index_table: pa.Table = pa.concat_tables(index_tables, promote=False)
    return final_index_table


@dataclass
class FilingsState:
    page_start: int
    num_filings: int


class Filings:
    """
    A container for filings
    """

    def __init__(self,
                 filing_index: pa.Table,
                 original_state: FilingsState = None):
        self.data: pa.Table = filing_index
        self.data_pager = DataPager(self.data)
        # This keeps track of where the index should start in case this is just a page in the Filings
        self._original_state = original_state or FilingsState(0, len(self.data))

    def to_pandas(self, *columns) -> pd.DataFrame:
        """Return the filing index as a python dataframe"""
        df = self.data.to_pandas()
        return df.filter(columns) if len(columns) > 0 else df

    def save_parquet(self, location: str):
        """Save the filing index as parquet"""
        pq.write_table(self.data, location)

    def save(self, location: str):
        """Save the filing index as parquet"""
        self.save_parquet(location)

    def get_filing_at(self, item: int):
        """Get the filing at the specified index"""
        return Filing(
            cik=self.data['cik'][item].as_py(),
            company=self.data['company'][item].as_py(),
            form=self.data['form'][item].as_py(),
            filing_date=self.data['filing_date'][item].as_py(),
            accession_no=self.data['accession_number'][item].as_py(),
        )

    @property
    def date_range(self) -> Tuple[datetime]:
        """Return a tuple of the start and end dates in the filing index"""
        min_max_dates = pc.min_max(self.data['filing_date']).as_py()
        return min_max_dates['min'], min_max_dates['max']

    @property
    def start_date(self) -> str:
        """Return the start date for the filings"""
        return str(self.date_range[0])

    @property
    def end_date(self) -> str:
        """Return the end date for the filings"""
        return str(self.date_range[1])

    def latest(self, n: int = 1) -> int:
        """Get the latest n filings"""
        sort_indices = pc.sort_indices(self.data, sort_keys=[("filing_date", "descending")])
        sort_indices_top = sort_indices[:min(n, len(sort_indices))]
        latest_filing_index = pc.take(data=self.data, indices=sort_indices_top)
        filings = Filings(latest_filing_index)
        if len(filings) == 1:
            return filings[0]
        return filings

    def filter(self,
               form: Union[str, List[IntString]] = None,
               amendments: bool = None,
               filing_date: str = None,
               date: str = None):
        """
        Filter the filings
        :param form: The form or list of forms to filter by
        :param amendments: Whether to include amendments to the forms e.g include "10-K/A" if filtering for "10-K"
        :param filing_date: The filing date
        :param date: An alias for the filing date
        :return: The filtered filings
        """
        filing_index = self.data
        forms = form
        if forms:
            # Ensure that forms is a list of strings ... it can accept int like form 3, 4, 5
            forms = [str(el) for el in listify(forms)]
            # If amendments then add amendments
            if amendments:
                forms = list(set(forms + [f"{val}/A" for val in forms]))
            filing_index = filing_index.filter(pc.is_in(filing_index['form'], pa.array(forms)))

        # filing_date and date are aliases
        filing_date = filing_date or date
        if filing_date:
            try:
                filing_index = filter_by_date(filing_index, filing_date, 'filing_date')
            except InvalidDateException as e:
                log.error(e)
                return None

        return Filings(filing_index)

    def __head(self, n):
        assert n > 0, "The number of filings to select - `n`, should be greater than 0"
        return self.data.slice(0, min(n, len(self.data)))

    def head(self, n: int):
        """Get the first n filings"""
        selection = self.__head(n)
        return Filings(selection)

    def __tail(self, n):
        assert n > 0, "The number of filings to select - `n`, should be greater than 0"
        return self.data.slice(max(0, len(self.data) - n), len(self.data))

    def tail(self, n: int):
        """Get the last n filings"""
        selection = self.__tail(n)
        return Filings(selection)

    def _sample(self, n: int):
        assert len(self) > n > 0, "The number of filings to select - `n`, should be greater than 0"
        return self.data.take(np.random.choice(len(self), n, replace=False)).sort_by([("filing_date", "descending")])

    def sample(self, n: int):
        """Get a random sample of n filings"""
        selection = self._sample(n)
        return Filings(selection)

    @property
    def empty(self) -> bool:
        return len(self.data) == 0

    def current(self):
        """Display the current page .. which is the default for this filings object"""
        return self

    def next(self) -> Optional[pa.Table]:
        """Show the next page"""
        data_page = self.data_pager.next()
        if data_page is None:
            log.warning("End of data .. use prev() \u2190 ")
            return None
        start_index, _ = self.data_pager._current_range
        filings_state = FilingsState(page_start=start_index, num_filings=len(self))
        return Filings(data_page, original_state=filings_state)

    def previous(self) -> Optional[pa.Table]:
        """
        Show the previous page of the data
        :return:
        """
        data_page = self.data_pager.previous()
        if data_page is None:
            log.warning(" No previous data .. use next() \u2192 ")
            return None
        start_index, _ = self.data_pager._current_range
        filings_state = FilingsState(page_start=start_index, num_filings=len(self))
        return Filings(data_page, original_state=filings_state)

    def prev(self):
        """Alias for self.previous()"""
        return self.previous()

    def get(self, index_or_accession_number: IntString):
        """
        Get the Filing at that index location or that has the accession number
        >>> filings.get(100)

        >>> filings.get("0001721868-22-000010")

        :param index_or_accession_number:
        :return:
        """
        if isinstance(index_or_accession_number, int) or index_or_accession_number.isdigit():
            return self.get_filing_at(int(index_or_accession_number))
        else:
            accession_number = index_or_accession_number.strip()
            mask = pc.equal(self.data['accession_number'], accession_number)
            idx = mask.index(True).as_py()
            if idx > -1:
                return self.get_filing_at(idx)
            if not accession_number_re.match(accession_number):
                log.warning(
                    f"Invalid accession number [{accession_number}]"
                    "\n  valid accession number [0000000000-00-000000]"
                )

    def find(self,
             company_search_str: str):
        from edgar._companies import find_company

        # Search for the company
        search_results = find_company(company_search_str)
        cik_match_lookup = search_results.cik_match_lookup()

        # Filter filings that are in the search results
        ciks = search_results.data.cik.tolist()
        filing_index = self.data.filter(pc.is_in(self.data['cik'], pa.array(ciks)))

        # Sort by the match score
        score_values = pa.array([cik_match_lookup.get(cik.as_py()) for cik in filing_index.column("cik")])
        filing_index = filing_index.append_column("match", score_values)
        filing_index = filing_index.sort_by([('match', 'descending'), ('company', 'ascending')]).drop(['match'])

        # Need to sort by
        return Filings(filing_index)

    def __getitem__(self, item):
        return self.get_filing_at(item)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.data):
            filing: Filing = self[self.n]
            self.n += 1
            return filing
        else:
            raise StopIteration

    @property
    def summary(self):
        return (f"Showing {self.data_pager.page_size} of "
                f"{self._original_state.num_filings:,} filings")

    def _page_index(self) -> range:
        """Create the range index to set on the page dataframe depending on where in the data we are
        """
        if self._original_state:
            return range(self._original_state.page_start,
                         self._original_state.page_start
                         + min(self.data_pager.page_size, len(self.data)))  # set the index to the size of the page
        else:
            return range(*self.data_pager._current_range)

    def __rich__(self) -> Panel:
        page = self.data_pager.current().to_pandas()
        page.index = self._page_index()

        # Show paging information
        page_info = f"Showing {len(page)} of {self._original_state.num_filings:,} filings"

        return Panel(
            Group(
                df_to_rich_table(page, max_rows=len(page)),
                Text(page_info)
            ), title="Filings"
        )

    def __repr__(self):
        return repr_rich(self.__rich__())


def get_filings(year: Years = None,
                quarter: Quarters = None,
                form: Union[str, List[IntString]] = None,
                amendments: bool = True,
                filing_date: str = None,
                index="form") -> Filings:
    """
    Downloads the filing index for a given year or list of years, and a quarter or list of quarters.

    So you can download for 2020, [2020,2021,2022] or range(2020, 2023)

    Examples

    >>> from edgar import get_filings

    >>> filings = get_filings(2021) # Get filings for 2021

    >>> filings = get_filings(2021, 4) # Get filings for 2021 Q4

    >>> filings = get_filings(2021, [3,4]) # Get filings for 2021 Q3 and Q4

    >>> filings = get_filings([2020, 2021]) # Get filings for 2020 and 2021

    >>> filings = get_filings([2020, 2021], 4) # Get filings for Q4 of 2020 and 2021

    >>> filings = get_filings(range(2010, 2021)) # Get filings between 2010 and 2021 - does not include 2021

    >>> filings = get_filings(2021, 4, form="D") # Get filings for 2021 Q4 for form D

    >>> filings = get_filings(2021, 4, filing_date="2021-10-01") # Get filings for 2021 Q4 on "2021-10-01"

    >>> filings = get_filings(2021, 4, filing_date="2021-10-01:2021-10-10") # Get filings for 2021 Q4 between
                                                                            # "2021-10-01" and "2021-10-10"


    :param year The year of the filing
    :param quarter The quarter of the filing
    :param form The form or forms as a string e.g. "10-K" or a List ["10-K", "8-K"]
    :param amendments If True will expand the list of forms to include amendments e.g. "10-K/A"
    :param filing_date The filing date to filter by in YYYY-MM-DD format
                e.g. filing_date="2022-01-17" or filing_date="2022-01-17:2022-02-28"
    :param index The index type - "form" or "company" or "xbrl"
    :return:
    """
    # Get the year or default to the current year
    if not year:
        year, quarter = current_year_and_quarter()

    year_and_quarters: YearAndQuarters = expand_quarters(year, quarter)
    if len(year_and_quarters) == 0:
        log.warning(f"""
    Provide a year between 1994 and {datetime.now().year} and optionally a quarter (1-4) for which the SEC has filings. 
    
        e.g. filings = get_filings(2023) OR
             filings = get_filings(2023, 1)
    
    (You specified the year {year} and quarter {quarter})   
        """)
        return None
    filing_index = get_filings_for_quarters(year_and_quarters, index=index)

    filings = Filings(filing_index)

    if form or filing_date:
        filings = filings.filter(form=form, amendments=amendments, filing_date=filing_date)

    # Finally sort by filing date
    filings = Filings(filings.data.sort_by([("filing_date", "descending")]))
    return filings


# Fund filings
get_fund_filings = partial(get_filings, form=FUND_FORMS)
get_funds = get_fund_filings

# Restricted stock sales
get_restricted_stock_filings = partial(get_filings, form=[144])

# Insider transaction filings
get_insider_transaction_filings = partial(get_filings, form=[3, 4, 5])


def parse_filing_header(content):
    data = {}
    current_key = None

    lines = content.split('\n')
    for line in lines:
        if line.endswith(':'):
            current_key = line[:-1]  # Remove the trailing colon
            data[current_key] = {}
        elif current_key and ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            data[current_key][key] = value

    return data


@dataclass(frozen=True)
class CompanyInformation:
    name: str
    cik: str
    sic: str
    irs_number: str
    state_of_incorporation: str
    fiscal_year_end: str


@dataclass(frozen=True)
class FilingInformation:
    form: str
    file_number: str
    sec_act: str
    film_number: str


@dataclass(frozen=True)
class FormerCompany:
    name: str
    date_of_change: str


@dataclass(frozen=True)
class Filer:
    company_information: CompanyInformation
    filing_information: FilingInformation
    business_address: Address
    mailing_address: Address
    former_company_names: Optional[List[FormerCompany]] = None


@dataclass(frozen=True)
class Owner:
    name: str
    cik: str


@dataclass(frozen=True)
class ReportingOwner:
    owner: Owner
    company_information: CompanyInformation
    filing_information: FilingInformation
    business_address: Address
    mailing_address: Address

@dataclass(frozen=True)
class SubjectCompany:
    company_information: CompanyInformation
    filing_information: FilingInformation
    business_address: Address
    mailing_address: Address
    former_company_names: Optional[List[FormerCompany]] = None


@dataclass(frozen=True)
class Issuer:
    company_information: CompanyInformation
    business_address: Address
    mailing_address: Address


# Title text
mailing_address_title = "\U0001F4EC Mailing Address"
business_address_title = "\U0001F4EC Business Address"
company_title = "\U0001F3E2 Company"
reporting_owner_title = "\U0001F468 REPORTING OWNER"
issuer_title = "\U0001F4B5 ISSUER"
filing_title = "\U0001F4D1 FILING"


def _create_address_table(address: Address, title: str):
    address_table = Table("Street1", "Street2", "City", "State", "Zipcode",
                          title=title, box=box.SIMPLE)
    address_table.add_row(address.street1,
                          address.street2,
                          address.city,
                          address.state_or_country,
                          address.zipcode)
    return address_table

class SECHeader:
    """
    Contains the parsed representation of the SEC-HEADER text at the top of the full submission text
    <SEC-HEADER>

    </SEC-HEADER>
    """

    def __init__(self,
                 header_text: str,
                 filing_metadata: Dict[str, str],
                 filers: List[Filer] = None,
                 reporting_owners: List[ReportingOwner] = None,
                 issuers: List[Issuer] = None,
                 subject_companies: List[SubjectCompany] = None):
        self.header_text:str = header_text
        self.filing_metadata: Dict[str, str] = filing_metadata
        self.filers: List[Filer] = filers
        self.reporting_owners: List[ReportingOwner] = reporting_owners
        self.issuers: List[Issuer] = issuers
        self.subject_companies = subject_companies

    @property
    def accession_number(self):
        return self.filing_metadata.get("ACCESSION NUMBER")

    @property
    def form(self):
        return self.filing_metadata.get("CONFORMED SUBMISSION TYPE")

    @property
    def filing_date(self):
        return self.filing_metadata.get("FILED AS OF DATE")

    @property
    def date_as_of_change(self):
        return self.filing_metadata.get("DATE AS OF CHANGE")

    @property
    def document_count(self):
        return self.filing_metadata.get("PUBLIC DOCUMENT COUNT", 0)

    @property
    def acceptance_datetime(self):
        acceptance = self.filing_metadata.get("ACCEPTANCE-DATETIME")
        if acceptance:
            return datetime.strptime(acceptance, "%Y%m%d%H%M%S")

    @classmethod
    def parse(cls, header_text:str):
        data = {}
        current_header = None
        current_subheader = None

        # Read the lines in the content. This starts with <ACCEPTANCE-DATETIME>20230606213204
        for line in header_text.split('\n'):
            if not line:
                continue

            # The line ends with a ':' meaning nested content follows e.g. "REPORTING-OWNER:"
            if line.rstrip('\t').endswith(':'):

                # Nested line means a subheader e.g. "OWNER DATA:"
                if line.startswith('\t'):
                    current_subheader = line.strip().split(':')[0]
                    if current_subheader == "FORMER COMPANY":  # Special case. This is a list of companies
                        if current_subheader not in data[current_header][-1]:
                            data[current_header][-1][current_subheader] = []
                        data[current_header][-1][current_subheader].append({})
                    else:
                        data[current_header][-1][current_subheader] = {}  # Expect only one record per key

                # Top level header
                else:
                    current_header = line.strip().split(':')[0]
                    if current_header not in data:
                        data[current_header] = []
                    data[current_header].append({})
            else:
                if line.strip().startswith("<"):
                    # The line looks like this <KEY>VALUE
                    key, value = line.split('>')
                    # Strip the leading '<' from the key
                    data[key[1:]] = value
                elif ':' in line:
                    key, value = line.strip().split(':')
                    value = value.strip()
                    if not current_header:
                        data[key] = value
                    elif not current_subheader:
                        continue
                    else:
                        if current_subheader == "FORMER COMPANY":
                            data[current_header][-1][current_subheader][-1][key.strip()] = value
                        else:
                            data[current_header][-1][current_subheader][key.strip()] = value

        # The filer
        filers = []
        for filer_values in data.get('FILER', []):
            filer_company_values = filer_values.get('COMPANY DATA')
            company_obj = None
            if filer_company_values:
                    company_obj = CompanyInformation(
                        name=filer_company_values.get('COMPANY CONFORMED NAME'),
                        cik=filer_company_values.get('CENTRAL INDEX KEY'),
                        sic=filer_company_values.get('STANDARD INDUSTRIAL CLASSIFICATION'),
                        irs_number=filer_company_values.get('IRS NUMBER'),
                        state_of_incorporation=filer_company_values.get('STATE OF INCORPORATION'),
                        fiscal_year_end=filer_company_values.get('FISCAL YEAR END')
                )
            # Filing Values
            filing_values_text_section = filer_values.get('FILING VALUES')
            filing_values_obj = None
            if filing_values_text_section:
                    filing_values_obj = FilingInformation(
                        form=filing_values_text_section.get('FORM TYPE'),
                        sec_act=filing_values_text_section.get('SEC ACT'),
                        file_number=filing_values_text_section.get('SEC FILE NUMBER'),
                        film_number=filing_values_text_section.get('FILM NUMBER')
                    )
             # Now create the filer
            filer = Filer(
                    company_information=company_obj,
                    filing_information=filing_values_obj,
                    business_address=Address(
                        street1=filer_values['BUSINESS ADDRESS'].get('STREET 1'),
                        street2=filer_values['BUSINESS ADDRESS'].get('STREET 2'),
                        city=filer_values['BUSINESS ADDRESS'].get('CITY'),
                        state_or_country=filer_values['BUSINESS ADDRESS'].get('STATE'),
                        zipcode=filer_values['BUSINESS ADDRESS'].get('ZIP'),

                    ) if 'BUSINESS ADDRESS' in filer_values else None,
                    mailing_address=Address(
                        street1=filer_values['MAIL ADDRESS'].get('STREET 1'),
                        street2=filer_values['MAIL ADDRESS'].get('STREET 2'),
                        city=filer_values['MAIL ADDRESS'].get('CITY'),
                        state_or_country=filer_values['MAIL ADDRESS'].get('STATE'),
                        zipcode=filer_values['MAIL ADDRESS'].get('ZIP'),

                    ) if 'MAIL ADDRESS' in filer_values else None,
                    former_company_names=[FormerCompany(date_of_change=record.get('DATE OF NAME CHANGE'),
                                                        name=record.get('FORMER CONFORMED NAME'))
                                          for record in filer_values['FORMER COMPANY']
                                          ]
                    if 'FORMER COMPANY' in filer_values else None
            )
            filers.append(filer)

        # Reporting Owner

        reporting_owners = []

        for reporting_owner_values in data.get('REPORTING-OWNER', []):
            reporting_owner = None
            if reporting_owner_values:
                reporting_owner = ReportingOwner(
                    owner=Owner(
                        name=reporting_owner_values.get('OWNER DATA').get('COMPANY CONFORMED NAME'),
                        cik=reporting_owner_values.get('OWNER DATA').get('CENTRAL INDEX KEY'),
                    ) if "OWNER DATA" in reporting_owner_values else None,
                    company_information=CompanyInformation(
                        name=reporting_owner_values.get('COMPANY DATA').get('COMPANY CONFORMED NAME'),
                        cik=reporting_owner_values.get('COMPANY DATA').get('CENTRAL INDEX KEY'),
                        sic=reporting_owner_values.get('COMPANY DATA').get('STANDARD INDUSTRIAL CLASSIFICATION'),
                        irs_number=reporting_owner_values.get('COMPANY DATA').get('IRS NUMBER'),
                        state_of_incorporation=reporting_owner_values.get('COMPANY DATA').get('STATE OF INCORPORATION'),
                        fiscal_year_end=reporting_owner_values.get('COMPANY DATA').get('FISCAL YEAR END')
                    ) if "COMPANY DATA" in reporting_owner_values else None,
                    filing_information=FilingInformation(
                        form=reporting_owner_values.get('FILING VALUES').get('FORM TYPE'),
                        sec_act=reporting_owner_values.get('FILING VALUES').get('SEC ACT'),
                        file_number=reporting_owner_values.get('FILING VALUES').get('SEC FILE NUMBER'),
                        film_number=reporting_owner_values.get('FILING VALUES').get('FILM NUMBER')
                    ) if 'FILING VALUES' in reporting_owner_values else None,
                    business_address=Address(
                        street1=reporting_owner_values.get('BUSINESS ADDRESS').get('STREET 1'),
                        street2=reporting_owner_values.get('BUSINESS ADDRESS').get('STREET 2'),
                        city=reporting_owner_values.get('BUSINESS ADDRESS').get('CITY'),
                        state_or_country=reporting_owner_values.get('BUSINESS ADDRESS').get('STATE'),
                        zipcode=reporting_owner_values.get('BUSINESS ADDRESS').get('ZIP'),
                    ) if 'BUSINESS ADDRESS' in reporting_owner_values else None,
                    mailing_address=Address(
                        street1=reporting_owner_values.get('MAIL ADDRESS').get('STREET 1'),
                        street2=reporting_owner_values.get('MAIL ADDRESS').get('STREET 2'),
                        city=reporting_owner_values.get('MAIL ADDRESS').get('CITY'),
                        state_or_country=reporting_owner_values.get('MAIL ADDRESS').get('STATE'),
                        zipcode=reporting_owner_values.get('MAIL ADDRESS').get('ZIP'),
                    ) if 'MAIL ADDRESS' in reporting_owner_values else None
                )
            reporting_owners.append(reporting_owner)

        # Issuer
        issuers = []
        for issuer_values in data.get('ISSUER', []):
            issuer = Issuer(
                    company_information=CompanyInformation(
                        name=issuer_values.get('COMPANY DATA').get('COMPANY CONFORMED NAME'),
                        cik=issuer_values.get('COMPANY DATA').get('CENTRAL INDEX KEY'),
                        sic=issuer_values.get('COMPANY DATA').get('STANDARD INDUSTRIAL CLASSIFICATION'),
                        irs_number=issuer_values.get('COMPANY DATA').get('IRS NUMBER'),
                        state_of_incorporation=issuer_values.get('COMPANY DATA').get('STATE OF INCORPORATION'),
                        fiscal_year_end=issuer_values.get('COMPANY DATA').get('FISCAL YEAR END')
                    ) if 'COMPANY DATA' in issuer_values else None,
                    business_address=Address(
                        street1=issuer_values.get('BUSINESS ADDRESS').get('STREET 1'),
                        street2=issuer_values.get('BUSINESS ADDRESS').get('STREET 2'),
                        city=issuer_values.get('BUSINESS ADDRESS').get('CITY'),
                        state_or_country=issuer_values.get('BUSINESS ADDRESS').get('STATE'),
                        zipcode=issuer_values.get('BUSINESS ADDRESS').get('ZIP'),
                    ) if 'BUSINESS ADDRESS' in issuer_values else None,
                    mailing_address=Address(
                        street1=issuer_values.get('MAIL ADDRESS').get('STREET 1'),
                        street2=issuer_values.get('MAIL ADDRESS').get('STREET 2'),
                        city=issuer_values.get('MAIL ADDRESS').get('CITY'),
                        state_or_country=issuer_values.get('MAIL ADDRESS').get('STATE'),
                        zipcode=issuer_values.get('MAIL ADDRESS').get('ZIP'),
                    ) if 'MAIL ADDRESS' in issuer_values else None
                )
            issuers.append(issuer)

        subject_companies = []
        for subject_company_values in data.get('SUBJECT COMPANY', []):
            subject_company = SubjectCompany(
                company_information=CompanyInformation(
                    name=subject_company_values.get('COMPANY DATA').get('COMPANY CONFORMED NAME'),
                    cik=subject_company_values.get('COMPANY DATA').get('CENTRAL INDEX KEY'),
                    sic=subject_company_values.get('COMPANY DATA').get('STANDARD INDUSTRIAL CLASSIFICATION'),
                    irs_number=subject_company_values.get('COMPANY DATA').get('IRS NUMBER'),
                    state_of_incorporation=subject_company_values.get('COMPANY DATA').get('STATE OF INCORPORATION'),
                    fiscal_year_end=subject_company_values.get('COMPANY DATA').get('FISCAL YEAR END')
                ) if 'COMPANY DATA' in subject_company_values else None,
                filing_information=FilingInformation(
                    form=subject_company_values.get('FILING VALUES').get('FORM TYPE'),
                    sec_act=subject_company_values.get('FILING VALUES').get('SEC ACT'),
                    file_number=subject_company_values.get('FILING VALUES').get('SEC FILE NUMBER'),
                    film_number=subject_company_values.get('FILING VALUES').get('FILM NUMBER')
                ) if 'FILING VALUES' in subject_company_values else None,
                business_address=Address(
                    street1=subject_company_values.get('BUSINESS ADDRESS').get('STREET 1'),

                    street2=subject_company_values.get('BUSINESS ADDRESS').get('STREET 2'),
                    city=subject_company_values.get('BUSINESS ADDRESS').get('CITY'),
                    state_or_country=subject_company_values.get('BUSINESS ADDRESS').get('STATE'),
                    zipcode=subject_company_values.get('BUSINESS ADDRESS').get('ZIP'),
                ) if 'BUSINESS ADDRESS' in subject_company_values else None,
                mailing_address=Address(
                    street1=subject_company_values.get('MAIL ADDRESS').get('STREET 1'),
                    street2=subject_company_values.get('MAIL ADDRESS').get('STREET 2'),
                    city=subject_company_values.get('MAIL ADDRESS').get('CITY'),
                    state_or_country=subject_company_values.get('MAIL ADDRESS').get('STATE'),
                    zipcode=subject_company_values.get('MAIL ADDRESS').get('ZIP'),
                ) if 'MAIL ADDRESS' in subject_company_values else None,
                former_company_names=[FormerCompany(date_of_change=record.get('DATE OF NAME CHANGE'),
                                                    name=record.get('FORMER CONFORMED NAME'))
                                      for record in subject_company_values['FORMER COMPANY']
                                      ]
                if 'FORMER COMPANY' in subject_company_values else None
            )
            subject_companies.append(subject_company)

        # Create a dict of the values in data that are not nested dicts
        filing_metadata = {key: value for key, value in data.items() if isinstance(value, str)}

        # The header text contains <ACCEPTANCE-DATETIME>20230612172243. Replace with the formatted date
        header_text = re.sub(r'<ACCEPTANCE-DATETIME>(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})',
               r'ACCEPTANCE-DATETIME:            \1-\2-\3 \4:\5:\6', header_text)

        # Remove empty lines from header_text
        header_text = '\n'.join([line for line in header_text.split('\n') if line.strip()])

        # Create the Filing object
        return cls(
            header_text=header_text,
            filing_metadata=filing_metadata,
            filers=filers,
            reporting_owners=reporting_owners,
            issuers=issuers,
            subject_companies=subject_companies
        )

    def __rich__(self):
        return Panel(Text(self.header_text))

    def __repr__(self):
        return repr_rich(self.__rich__())


class Filing:
    """
    A single SEC filing. Allow you to access the documents and data for that filing
    """

    def __init__(self,
                 cik: int,
                 company: str,
                 form: str,
                 filing_date: str,
                 accession_no: str):
        self.cik = cik
        self.company = company
        self.form = form
        self.filing_date = filing_date
        self.accession_no = accession_no
        self._filing_homepage = None

    @property
    def document(self):
        """
        :return: The primary display document on the filing, generally HTML but can be XHTML
        """
        return self.homepage.primary_html_document

    @property
    def primary_documents(self):
        """
        :return: a list of the primary documents on the filing, generally HTML or XHTML and optionally XML
        """
        return self.homepage.primary_documents

    @property
    def attachments(self):
        # Return all the attachments on the filing
        return self.homepage.attachments

    def html(self) -> Optional[str]:
        """Returns the html contents of the primary document if it is html"""
        return self.document.download(text=True)

    def xml(self) -> Optional[str]:
        """Returns the xml contents of the primary document if it is xml"""
        xml_document: Attachment = self.homepage.primary_xml_document
        if xml_document:
            return xml_document.download(text=True)

    def text(self) -> str:
        """Return the complete text submission file"""
        return download_file(self.text_url)

    def markdown(self) -> str:
        """return the markdown version of this filing html"""
        return html_to_markdown(self.html())

    def view(self):
        """Preview this filing's primary document as markdown. This should display in the console"""
        console = Console()
        console.print(MarkdownContent(self.html(), title=f"Form {self.form} for {self.company}"))

    def xbrl(self) -> Optional[FilingXbrl]:
        """
        Get the XBRL document for the filing, parsed and as a FilingXbrl object
        :return: Get the XBRL document for the filing, parsed and as a FilingXbrl object, or None
        """
        xbrl_document = self.homepage.xbrl_document
        if xbrl_document:
            xbrl_text = xbrl_document.download(text=True)
            return FilingXbrl.parse(xbrl_text)

    @property
    @lru_cache(maxsize=1)
    def header(self):
        sec_header_content = get_text_between_tags(self.text_url, "SEC-HEADER")
        return SECHeader.parse(sec_header_content)

    def data_object(self):
        """ Get this filing as the data object that it might be"""
        from edgar import obj
        return obj(self)

    def obj(self):
        """Alias for data_object()"""
        return self.data_object()

    def open_homepage(self):
        """Open the homepage in the browser"""
        webbrowser.open(self.homepage_url)

    def open(self):
        """Open the main filing document"""
        webbrowser.open(self.document.url)

    @lru_cache(maxsize=1)
    def sections(self) -> List[str]:
        return re.split(r"\n\s*\n", self.markdown())

    @lru_cache(maxsize=1)
    def __get_bm25_search_index(self):
        return BM25Search(self.sections())

    @lru_cache(maxsize=1)
    def __get_regex_search_index(self):
        return RegexSearch(self.sections())

    def search(self,
               query: str,
               regex=False):
        """Search for the query string in the filing HTML"""
        if regex:
            return self.__get_regex_search_index().search(query)
        return self.__get_bm25_search_index().search(query)

    @property
    def homepage_url(self) -> str:
        return f"{sec_edgar}/data/{self.cik}/{self.accession_no}-index.html"

    @property
    def text_url(self) -> str:
        return f"{sec_edgar}/data/{self.cik}/{self.accession_no.replace('-', '')}/{self.accession_no}.txt"

    @property
    def url(self) -> str:
        return self.homepage_url

    @property
    def homepage(self):
        """
        Get the homepage for the filing
        :return: the FilingHomepage
        """
        if not self._filing_homepage:
            homepage_html = download_text(self.homepage_url)
            self._filing_homepage = FilingHomepage.from_html(homepage_html,
                                                             url=self.homepage_url,
                                                             filing=self)
        return self._filing_homepage

    @lru_cache(maxsize=1)
    def get_entity(self):
        """Get the company to which this filing belongs"""
        "Get the company for cik. Cache for performance"
        from edgar._companies import CompanyData
        return CompanyData.for_cik(self.cik)

    @lru_cache(maxsize=1)
    def as_company_filing(self):
        """Get this filing as a company filing. Company Filings have more information"""
        company = self.get_entity()
        filings = company.get_filings(accession_number=self.accession_no)
        if not filings.empty:
            return filings[0]

    @lru_cache(maxsize=1)
    def related_filings(self):
        """Get all the filings related to this one
        There is no file number on this base Filing class so first get the company,

        then this filing then get the related filings
        """
        company = self.get_entity()
        filings = company.get_filings(accession_number=self.accession_no)
        if not filings.empty:
            file_number = filings[0].file_number
            return company.get_filings(file_number=file_number,
                                       sort_by=[("filing_date", "ascending"), ("accession_number", "ascending")])

    def __hash__(self):
        return hash(self.accession_no)

    def __eq__(self, other):
        return isinstance(other, Filing) and self.accession_no == other.accession_no

    def __ne__(self, other):
        return not self == other

    def summary(self) -> pd.DataFrame:
        """Return a summary of this filing as a dataframe"""
        return pd.DataFrame([{"accession_no": self.accession_no,
                              "Filed on": self.filing_date,
                              "Company": self.company,
                              "CIK": self.cik}]).set_index("accession_no")

    def __str__(self):
        """
        Return a string version of this filing e.g.

        Filing(form='10-K', filing_date='2018-03-08', company='CARBO CERAMICS INC',
              cik=1009672, accession_no='0001564590-18-004771')
        :return:
        """
        return (f"Filing(form='{self.form}', filing_date='{self.filing_date}', company='{self.company}', "
                f"cik={self.cik}, accession_no='{self.accession_no}')")

    def __rich__(self):
        """
        Produce a table version of this filing e.g.
        ┌──────────────────────┬──────┬────────────┬────────────────────┬─────────┐
        │                      │ form │ filing_date│ company            │ cik     │
        ├──────────────────────┼──────┼────────────┼────────────────────┼─────────┤
        │ 0001564590-18-004771 │ 10-K │ 2018-03-08 │ CARBO CERAMICS INC │ 1009672 │
        └──────────────────────┴──────┴────────────┴────────────────────┴─────────┘
        :return: a rich table version of this filing
        """
        summary_table = Table(box=box.SIMPLE)
        summary_table.add_column("Accession Number", style="bold", header_style="bold")
        summary_table.add_column("Filing Date")
        summary_table.add_column("Company")
        summary_table.add_column("CIK")
        summary_table.add_row(self.accession_no, str(self.filing_date), self.company, str(self.cik))

        links_table = Table(box=box.SIMPLE)
        links_table.add_column("Link", style="bold", header_style="bold")
        links_table.add_column("URL")
        links_table.add_row("\U0001F3E0 Homepage", self.homepage_url)
        links_table.add_row("\U0001F4C4 Primary Document", self.document.url)
        links_table.add_row("\U0001F4D2 Full Submission Text", self.text_url)

        return Panel(
            Group(summary_table, links_table),
            title=f"{self.form} {unicode_for_form(self.form)} filing for {self.company}",
            box=box.ROUNDED
        )

    def __rich__repr__(self):
        yield "accession_no", self.accession_no
        yield "form", self.form
        yield "filing_date", self.filing_date
        yield "company", self.company
        yield "cik", self.cik

    def __repr__(self):
        return repr_rich(self.__rich__())


class Attachments:

    def __init__(self, files: pd.DataFrame):
        self.files = files
        # Replace \xa0 with '-' in the Seq
        self.files['Seq'] = self.files['Seq'].str.replace('\xa0', '-')

    def __getitem__(self, item):
        if isinstance(item, str):
            res = self.files[self.files['Document'] == item]
            if not res.empty:
                return Attachment.from_dataframe_row(res.iloc[0])
        elif isinstance(item, int):
            if 0 <= item < len(self.files):
                return Attachment.from_dataframe_row(self.files.iloc[item])

    def get(self, item):
        return self.__getitem__(item)

    def __len__(self):
        return len(self.files)

    def __rich__(self):
        return df_to_rich_table(self.files
                                .assign(Size=lambda df: df.Size.apply(display_size))
                                .filter(['Description', 'Document', 'Type', 'Size']), max_rows=100)

    def __repr__(self):
        return repr_rich(self.__rich__())


@dataclass(frozen=True)
class Attachment:
    """
    A document on the filing

    """
    seq: int
    description: str
    document: str
    form: str
    size: int
    path: str

    @property
    def extension(self):
        """The actual extension of the filing document
         Usually one of .xml or .html or .pdf or .txt or .paper
         """
        return os.path.splitext(self.path)[1]

    @property
    def display_extension(self) -> str:
        """This is the extension displayed in the html e.g. "es220296680_4-davis.html"
        The actual extension would be "es220296680_4-davis.xml", that displays as html in the browser

        >>> .html

        """
        return os.path.splitext(self.document)[1]

    @property
    def url(self) -> str:
        """
        :return: The full sec url
        """
        # Never use the ixbrl viewer
        return f"{sec_dot_gov}{self.path}".replace("ix?doc=/", "")

    def open(self):
        """Open the filing document"""
        webbrowser.open(self.url)

    @property
    def name(self) -> str:
        return os.path.basename(self.path)

    @classmethod
    def from_dataframe_row(cls, dataframe_row: pd.Series):

        try:
            size = int(dataframe_row.Size)
        except ValueError:
            size = 0
        return cls(seq=dataframe_row.Seq,
                   description=dataframe_row.Description,
                   document=dataframe_row.Document,
                   form=dataframe_row.Type,
                   size=size,
                   path=dataframe_row.Url)

    def is_text(self):
        """Is this a text document"""
        return self.extension in text_extensions

    def download(self,
                 text: bool = None):
        return download_file(self.url, as_text=self.is_text())

    def summary(self) -> pd.DataFrame:
        """Return a summary of this filing as a dataframe"""
        return pd.DataFrame([{'seq': self.seq,
                              'form': self.form,
                              'document': self.document,
                              'description': self.description}]).set_index("seq")

    def __rich__(self):
        return df_to_rich_table(self.summary(), index_name="seq")

    def __repr__(self):
        return repr_rich(self.__rich__())


# These are the columns on the table on the filing homepage
filing_file_cols = ['Seq', 'Description', 'Document', 'Type', 'Size', 'Url']


class FilingHomepage:
    """
    A class that represents the homepage for the filing allowing us to get the documents and datafiles
    """

    def __init__(self,
                 files: pd.DataFrame,
                 url: str,
                 filing: Filing):
        self._files: pd.DataFrame = files
        self.url: str = url
        self.filing: Filing = filing

    def get_file(self,
                 *,
                 seq: int) -> Attachment:
        """ get the filing document that matches the seq"""
        res = self._files.query(f"Seq=='{seq}'")
        if not res.empty:
            return Attachment.from_dataframe_row(res.iloc[0])

    def open(self):
        webbrowser.open(self.url)

    def min_seq(self) -> str:
        """Get the minimum document sequence from the Seq column"""
        return str(min([int(seq) for seq in self.documents.Seq.tolist() if seq and seq.isdigit()]))

    @property
    @lru_cache(maxsize=2)
    def primary_documents(self) -> List[Attachment]:
        """
        Get the documents listed as primary for the filing
        :return:
        """
        min_seq = self.min_seq()
        doc_results = self.documents.query(f"Seq=='{min_seq}'")
        return [
            Attachment.from_dataframe_row(self.documents.iloc[index])
            for index in doc_results.index
        ]

    @property
    def primary_xml_document(self) -> Optional[Attachment]:
        """Get the primary xml document on the filing"""
        for doc in self.primary_documents:
            if doc.display_extension == ".xml":
                return doc

    @property
    def text_document(self) -> Attachment:
        "Get the full text submission file"
        res = self._files[self._files.Description == "Complete submission text file"]
        return Attachment.from_dataframe_row(res.iloc[0])

    @property
    def primary_html_document(self) -> Optional[Attachment]:
        """Get the primary xml document on the filing"""
        for doc in self.primary_documents:
            if doc.display_extension == ".html" or doc.display_extension == '.htm':
                return doc
        # Shouldn't get here but just open the first document
        return self.primary_documents[0]

    @property
    def xbrl_document(self):
        """Find and return the xbrl document."""

        # Change from .query syntax due to differences in how pandas executes queries on online environmments
        matching_files = self._files[self._files.Description.isin(xbrl_document_types)]
        if not matching_files.empty:
            rec = matching_files.iloc[0]
            return Attachment.from_dataframe_row(rec)

    def get_matching_files(self,
                           query: str) -> pd.DataFrame:
        """ return the files that match the query"""
        return self._files.query(query, engine="python").reset_index(drop=True).filter(filing_file_cols)

    @property
    def documents(self) -> pd.DataFrame:
        """ returns the files that are in the "Document Format Files" table of the homepage"""
        return self.get_matching_files("table=='Document Format Files'")

    @property
    def datafiles(self):
        """ returns the files that are in the "Data Files" table of the homepage"""
        return self.get_matching_files("table=='Data Files'")

    @property
    @lru_cache(maxsize=2)
    def attachments(self) -> Attachments:
        return Attachments(self._files)

    @classmethod
    def from_html(cls,
                  homepage_html: str,
                  url: str,
                  filing: Filing):
        """Parse the HTML and create the Homepage from it"""

        # It is html so use "html.parser" (instead of "xml", or "lxml")
        soup = BeautifulSoup(homepage_html, features="html.parser")

        # Keep track of the tables as dataframes so we can append later
        dfs = []

        tables = soup.find_all("table", class_="tableFile")
        for table in tables:
            summary = table.attrs.get("summary")
            rows = table.find_all("tr")
            column_names = [th.text for th in rows[0].find_all("th")] + ["Url"]
            records = []

            # Add the rows from the table
            for row in rows[1:]:
                cells = row.find_all("td")
                link = cells[2].a
                cell_values = [cell.text for cell in cells] + [link["href"] if link else None]
                records.append(cell_values)

            # Now create the dataframe
            table_as_df = (pd.DataFrame(records, columns=column_names)
                           .filter(filing_file_cols)
                           .assign(table=summary)
                           )
            dfs.append(table_as_df)

        # Now concat into a single dataframe
        files = pd.concat(dfs, ignore_index=True)

        return cls(files,
                   url=url,
                   filing=filing)

    def __str__(self):
        return f"Homepage for {self.description}"

    def __repr__(self):
        return repr_rich(self.__rich__())

    def __rich__(self):
        return Group(
            Text(f"{self.filing.form} filing", style="bold"),
            df_to_rich_table(self.filing.summary(), index_name="accession_no"),
            Group(Text("Documents", style="bold"),
                  df_to_rich_table(summarize_files(self.documents), index_name="Seq")
                  ),
            Group(Text("Datafiles", style="bold"),
                  df_to_rich_table(
                      summarize_files(self.datafiles), index_name="Seq"),
                  ) if self.datafiles is not None else Text(""),

        )


def summarize_files(data: pd.DataFrame) -> pd.DataFrame:
    return (data
            .filter(["Seq", "Document", "Description", "Size"])
            .assign(Size=data.Size.apply(display_size))
            .set_index("Seq")
            )


def get_by_accession_number(accession_number: str):
    """Find the filing using the accession number"""
    assert re.match(r"\d{10}-\d{2}-\d{6}", accession_number), \
        f"{accession_number} is not a valid accession number .. should be 10digits-2digits-6digits"
    year = int("19" + accession_number[11:13]) if accession_number[11] == 9 else int("20" + accession_number[11:13])
    for quarter in range(1, 5):
        filings = get_filings(year=year, quarter=quarter)
        if filings:
            filing = filings.get(accession_number)
            if filing:
                return filing


def form_with_amendments(*forms: str):
    return list(forms) + [f"{f}/A" for f in forms]


barchart = '\U0001F4CA'
ticket = '\U0001F3AB'
page_facing_up = '\U0001F4C4'
classical_building = '\U0001F3DB'


def unicode_for_form(form: str):
    if form in ['10-K', '10-Q', '10-K/A', '10-Q/A', '6-K', '6-K/A']:
        return barchart
    elif form in ['3', '4', '5', '3/A', '4/A', '5/A']:
        return ticket
    elif form in ['MA-I', 'MA-I/A', 'MA', 'MA/A']:
        return classical_building
    return page_facing_up
