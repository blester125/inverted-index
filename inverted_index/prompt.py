from prompt_toolkit.completion import Completer, Completion
from inverted_index.inverted_index import InvertedIndex


class SearchCompleter(Completer):
    def __init__(self, inverted_index: InvertedIndex):
        self.inverted_index = inverted_index

    def get_completions(self, document, complete_event):
        if complete_event.completion_requested:
            for match in self.inverted_index.search(document.text):
                yield Completion(match.ljust(document.cursor_position), start_position=-document.cursor_position)
