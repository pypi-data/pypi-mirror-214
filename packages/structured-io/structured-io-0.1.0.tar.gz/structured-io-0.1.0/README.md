# structio

A proof of concept for an experimental structured concurrency framework written in Python

## Disclaimer

This library is highly experimental and currently in alpha stage (it doesn't even have a proper version
number yet, that's how alpha it is), so it's not production ready (and probably never will be). If you
want the fancy structured concurrency paradigm in a library that works today, consider [trio](https://trio.readthedocs.org),
from which structio is heavily inspired ([curio](https://github.com/dabeaz/curio) is also worth looking into, although
technically it doesn't implement SC).

## Why?

This library (and [its](https://git.nocturn9x.space/nocturn9x/giambio) [predecessors](https://git.nocturn9x.space/nocturn9x/aiosched)) is just a way for me to test my knowledge and make sure I understand the basics of structured concurrency
and building solid coroutine runners so that I can implement the paradigm in my own programming language. For more info, see [here](https://git.nocturn9x.space/nocturn9x/peon).