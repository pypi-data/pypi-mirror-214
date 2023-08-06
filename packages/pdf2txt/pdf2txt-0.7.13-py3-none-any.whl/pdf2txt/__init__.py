
from pdf2txt.simple_reader._encryption import PasswordType
from pdf2txt.simple_reader._page import PageObject, Transformation
from pdf2txt.simple_reader._reader import DocumentInformation, PdfFileDocument, PdfDocument
from pdf2txt.simple_reader._version import __version__
from pdf2txt.simple_reader.pagerange import PageRange, parse_filename_page_ranges


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
