"""
PyPDF2 is a free and open-source pure-python PDF library capable of splitting,
merging, cropping, and transforming the pages of PDF files. It can also add
custom data, viewing options, and passwords to PDF files. PyPDF2 can retrieve
text and metadata from PDFs as well.

You can read the full docs at https://pypdf2.readthedocs.io/.
"""

import warnings

from ._encryption import PasswordType
from ._page import PageObject, Transformation
from ._reader import DocumentInformation, PdfFileDocument, PdfDocument
from ._version import __version__
from .pagerange import PageRange, parse_filename_page_ranges


__all__ = [
    "__version__",
    "PageRange",
    "DocumentInformation",
    "parse_filename_page_ranges",
    "PdfFileDocument",  # will be removed in PyPDF2 3.0.0; use PdfDocument instead
    "PdfDocument",
    "Transformation",
    "PageObject",
    "PasswordType",
]
