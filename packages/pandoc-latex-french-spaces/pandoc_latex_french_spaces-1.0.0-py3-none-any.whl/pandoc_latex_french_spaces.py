#!/usr/bin/env python3

"""
Pandoc filter for converting spaces to non-breakable spaces.

This filter is for use in LaTeX for french ponctuation.
"""

from panflute import RawInline, Space, Str, run_filter  # type: ignore


def spaces(elem, doc):
    """
    Add LaTeX spaces when needed.

    Arguments
    ---------
    elem
        A tree element
    doc
        The pandoc document

    Returns
    -------
        A RawInLine or None.
    """
    # Is it in the right format and is it a Space?
    if doc.format in ("latex", "beamer") and isinstance(elem, Space):
        if isinstance(elem.prev, Str) and elem.prev.text in ("«", "“", "‹"):
            return RawInline("\\thinspace{}", "tex")
        if isinstance(elem.next, Str):
            if elem.next.text == ":":
                return RawInline("~", "tex")
            if elem.next.text in (";", "?", "!", "»", "”", "›"):
                return RawInline("\\thinspace{}", "tex")
    return None


def main(doc=None):
    """
    Process conversion.

    Arguments
    ---------
    doc
        The pandoc document
    """
    run_filter(spaces, doc=doc)


if __name__ == "__main__":
    main()
