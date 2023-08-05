import re
from typing import List, Callable, Tuple

import pandas as pd
import textdistance
from rank_bm25 import BM25Okapi
from rich import box
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel

from edgar._markdown import convert_table
from edgar._rich import repr_rich

PUNCTUATION = re.compile('[%s]' % re.escape(r"""!"#&'()*+,-/:;<=>?@[\]^`{|}~"""))

__all__ = [
    'SimilaritySearchIndex',
    'SearchResults',
    'BM25Search',
    'RegexSearch',
    'preprocess'
]


class SimilaritySearchIndex:

    def __init__(self,
                 data: pd.DataFrame,
                 search_column: str):
        self.data: pd.DataFrame = data
        self._search_column = search_column

    def similar(self,
                query: str,
                threshold=0.6,
                topn=20):
        query = query.lower()
        df = (self
              .data.assign(match=self.data[self._search_column].apply(textdistance.jaro, s2=query).round(2))
              )
        df = df[df.match > threshold]
        df['matches_start'] = df[self._search_column].str.startswith(query[0])
        df = (df.sort_values(['match'], ascending=[False]).head(topn)
              .sort_values(['matches_start', 'match'], ascending=[False, False]))
        cols = [col for col in df if col not in [self._search_column, 'matches_start']]
        return df[cols]

    def __repr__(self):
        return f"SimilaritySearchIndex(search_column='{self.search_column}')"


Corpus = List[str]


def tokenize(text):
    return text.split()


def lowercase_filter(tokens):
    return [token.lower() for token in tokens]


def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


STOPWORDS = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                 'do', 'at', 'this', 'but', 'his', 'by', 'from'])


def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]


def convert_items_to_tokens(text: str):
    """Change 'Item 4.' to item_4. This keeps this in the filnal text"""
    return re.sub(r"item\s+(\d+\.\d+|\d+)\.?", r"item_\1", text, flags=re.IGNORECASE)


def numeric_shape(tokens: List[str]) -> List[str]:
    """Replace numbers with xx.x """
    toks = []
    for token in tokens:
        if re.fullmatch(r"(\d+[\d,.]*)%?|([,.]\d+)%?", token):
            toks.append(re.sub(r'\d', 'x', token))
        else:
            toks.append(token)
    return toks


def return_spaces_to_items(tokens: List[str]) -> List[str]:
    toks = []
    pattern = r"item_(\d+(\.\d+)?)"
    for token in tokens:
        if re.fullmatch(pattern, token):
            toks += re.sub(pattern, r"item \1", token).split(" ")
        else:
            toks.append(token)
    return toks


def preprocess(text: str):
    text = text.lower()
    text = convert_items_to_tokens(text)
    tokens = tokenize(text)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = numeric_shape(tokens)
    tokens = return_spaces_to_items(tokens)
    return tokens


def preprocess_documents(documents: List[str]) -> Corpus:
    return [preprocess(document) for document in documents]


LocAndDoc = Tuple[str, int]


class SearchResults:

    def __init__(self,
                 query: str,
                 sections: LocAndDoc,
                 tables: bool = True
                 ):
        self.query: str = query
        self.sections: LocAndDoc = sections
        self._show_tables = tables

    def __len__(self):
        return len(self.sections)

    def __rich__(self):
        _md = ""
        renderables = []
        title = f"Search results for '{self.query}'"
        for loc, doc in self.sections:
            if doc.startswith("|  |") and self._show_tables:
                table = convert_table(doc)
                renderables.append(table)
            else:
                renderables.append(Markdown(doc + "\n\n---"))
        return Panel(
            Group(*renderables), title=title, subtitle=title, box=box.ROUNDED
        )

    def __repr__(self):
        return repr_rich(self.__rich__())


class BM25Search:

    def __init__(self,
                 document_objs: List[object],
                 text_fn: Callable = None):
        if text_fn:
            self.corpus: Corpus = [BM25Search.preprocess(text_fn(doc)) for doc in document_objs]
        else:
            self.corpus: Corpus = [BM25Search.preprocess(doc) for doc in document_objs]
        self.document_objs = document_objs
        self.bm25: BM25Okapi = BM25Okapi(self.corpus)

    def __len__(self):
        return len(self.document_objs)

    @staticmethod
    def preprocess(text: str):
        text = text.lower()
        text = convert_items_to_tokens(text)
        tokens = tokenize(text)
        tokens = punctuation_filter(tokens)
        tokens = stopword_filter(tokens)
        tokens = numeric_shape(tokens)
        tokens = return_spaces_to_items(tokens)
        return tokens

    def search(self,
               query: str,
               tables: bool = True):
        preprocessed_query = preprocess(query)
        scores = self.bm25.get_scores(preprocessed_query)
        doc_scores = zip(self.document_objs, scores)
        doc_scores_sorted = sorted([doc for doc in doc_scores if doc[1] > 0], key=lambda t: t[1])[::-1]
        # Return the list of location and document
        return SearchResults(query=query,
                             sections=[(loc, doc_score[0])
                                       for loc, doc_score in enumerate(doc_scores_sorted)
                                       if doc_score[1] > 0],
                             tables=tables)


class RegexSearch:

    def __init__(self,
                 documents: List[object]):
        self.document_objs = [RegexSearch.preprocess(document) for document in documents]

    def __len__(self):
        return len(self.document_objs)

    @staticmethod
    def preprocess(text: str):
        text = text.replace("&#160;", " ")
        return text

    def search(self,
               query: str,
               tables: bool = True):
        return SearchResults(
            query=query,
            sections=[(loc, doc)
                      for loc, doc in enumerate(self.document_objs)
                      if re.search(query, doc, flags=re.IGNORECASE)],
            tables=tables
        )
