# Twitter Name Finagler

This bot facilitates automatic adjustments to Twitter account information.

# Usage
Place a `profile.properties` file at the root with the following keys (may be
empty or nonexistent)::

    name=
    url=
    location=
    description=

Embed tokens like `${<token>}` in the values; they will be replaced as
appropriate. Supported `<token>`s:

  - `character`: A random Unicode character (U+0000—U+10FFFF; not in the M* or
    C* categories)
  - `adjective`: A random adjective
  - `indefinite_adjective`: A random adjective prepended with an appropriate
    indefinite article ("a" or "an")
  - `enclosing_character`: A random Unicode character of category "mark, enclosing (`Me`)

# Requirements

- Python 2.7

# License

MIT

# Acknowledgments

This project uses word lists derived from [WordNet](http://wordnet.princeton.edu).
