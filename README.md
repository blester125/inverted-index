# Inverted Index

[![PyPi Version](https://img.shields.io/pypi/v/inverted-index)](https://pypi.org/project/inverted-index/) [![Actions Status](https://github.com/blester125/inverted-index/workflows/Unit%20Test/badge.svg)](https://github.com/blester125/inverted-index/actions) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A small extensiable python inverted index. It supports retevial by boolean `AND`s and ranking of the returned results. The point is a skeleton to add
quick and dirty search to a script.

It also includes a `prompt_toolkit` completer that can each the inverted index as you type. When you select a auto-suggest option it will replace your prompt.
The best way I have found to use this is to set it up to trigger only when you ask by hitting tab like so:

```python
from prompt_toolkit import prompt
from inverted_index.prompt import SearchCompleter
from inverted_index.inverted_index import InvertedIndex


# Create your index
ii = InvertedIndex(...)
ii.index(my_documents)

user_input = prompt("> ", completer=SearchCompleter(ii), complete_while_typing=False)
# Do things with user_input
print(user_input)
```
