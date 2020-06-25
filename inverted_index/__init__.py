__version__ = "0.1.0"


from inverted_index.inverted_index import (
    InvertedIndex,
    FromDiskInvertedIndex,
    LevenshteinRankingInvertedIndex,
)

try:
    from inverted_index.prompt import SearchCompleter
except ImportError:
    pass
