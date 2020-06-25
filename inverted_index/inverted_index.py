from operator import itemgetter
from typing import Dict, List, Callable, Any


def white_space_tokenize(string: str) -> List[str]:
    return string.split()


def lowercase(string: str) -> str:
    return string.lower()


class InvertedIndex:
    def __init__(
        self, tokenize: Callable[[str], List[str]] = white_space_tokenize, preprocess: Callable[[str], str] = lowercase,
    ):
        self.tokenize = tokenize
        self.preprocess = preprocess
        self.posting_list: Dict[str, List[int]] = {}
        self.documents: List[str] = []
        self.document_features: List[Any] = []

    @staticmethod
    def intersect(posting_1: List[int], posting_2: List[int]) -> List[int]:
        intersection = []
        if not (posting_1 and posting_2):
            return intersection
        p1, p2 = 0, 0
        while p1 < len(posting_1) and p2 < len(posting_2):
            doc_1 = posting_1[p1]
            doc_2 = posting_2[p2]
            if doc_1 == doc_2:
                intersection.append(doc_1)
                p1 += 1
                p2 += 1
            elif doc_1 < doc_2:
                p1 += 1
            else:
                p2 += 1
        return intersection

    def index(self, documents: List[str]):
        for idx, document in enumerate(documents, len(self.documents)):
            # These indices work because we always append but it would be nicer if there
            # were explicit inserts?
            self.documents.append(document)
            self.index_document(document, idx)
            self.document_features.append(self.featurize_document(document))

    def index_document(self, document: str, document_index: int) -> None:
        for token in self.tokenize_document(document):
            posting = self.posting_list.setdefault(token, [])
            posting.append(document_index)

    def get_document(self, index: int) -> str:
        return self.documents[index]

    def tokenize_document(self, document: str) -> List[str]:
        return list(map(self.preprocess, self.tokenize(document)))

    def tokenize_query(self, query: str) -> List[str]:
        return list(map(self.preprocess, self.tokenize(query)))

    def featurize_document(self, document: str) -> Any:
        pass

    def featurize_query(self, query: str) -> Any:
        pass

    def retrieve(self, query: List[str]) -> List[int]:
        posting_list = []
        for token in query:
            posting = self.posting_list.get(token, [])
            if posting_list and posting:
                posting_list = InvertedIndex.intersect(posting_list, posting)
            else:
                posting_list = posting
        return posting_list

    def rank(self, query: Any, document_ids: List[int]) -> List[int]:
        return document_ids

    def search(self, query: str) -> List[str]:
        proc_query = self.tokenize_query(query)
        document_ids = self.retrieve(proc_query)
        return [self.get_document(i) for i in self.rank(self.featurize_query(query), document_ids)]


class FromDiskInvertedIndex(InvertedIndex):
    def index_document(self, document: str, document_index: int) -> None:
        with open(documenet) as f:
            document = f.read()
            super().index_document(document, document_index)

    def get_document(self, index: int) -> str:
        with open(self.documents[index]) as f:
            return f.read()


class LevenshteinRankingInvertedIndex(InvertedIndex):
    def featurize_document(self, document: str) -> str:
        return " ".join(self.tokenize_document(document))

    def featurize_query(self, query: str) -> str:
        return " ".join(self.tokenize_query(query))

    def rank(self, query: str, document_ids: List[int]) -> List[int]:
        from string_distance import levenshteins

        if not document_ids:
            return document_ids
        documents = [self.document_features[i] for i in document_ids]
        distances = levenshteins(query, documents)
        ranks = list(zip(distances, document_ids))
        ranks = sorted(ranks, key=itemgetter(0))
        document_ids = list(zip(*ranks))[1]
        return document_ids
