from pdf2txt.core import Component
from .page import Page
import pytesseract
from poppdf import poppler
import pathlib
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.psparser import PSLiteral
from pdf2txt.core.paragraph import Paragraphs
import regex as re
from pdf2txt.utils import extract_text, TemporaryDirectory, get_page_layout
from pdf2txt.utils import convert_pdf_to_image
from collections import defaultdict
from pdf2txt.core.filtering import TokenList
from  collections import Counter



class Document(Component):
    cached_properties = Component.cached_properties + ["_pages"]

    def __init__(self, stream, path, pages=None, laparams=None, password="", fix_with_ocr=False):
        self.laparams = None if laparams is None else LAParams(**laparams)
        self.stream = stream
        self.pages_to_parse = pages
        self._pdf_file_path=path
        rsrcmgr = PDFResourceManager()
        self.doc = PDFDocument(PDFParser(stream), password=password)
        self.metadata = {}
        self._paragraphs=Paragraphs(self)
        self.fix_with_ocr=fix_with_ocr
        self._token_list = []
        self._element_indexes_by_font = defaultdict(set)
        for info in self.doc.info:
            self.metadata.update(info)
        for k, v in self.metadata.items():
            if hasattr(v, "resolve"):
                v = v.resolve()
            if type(v) == list:
                self.metadata[k] = list(v)
            elif isinstance(v, PSLiteral):
                self.metadata[k] = v.name
            elif isinstance(v, bool):
                self.metadata[k] = v
            else:
                self.metadata[k] = v
        self.device = PDFPageAggregator(rsrcmgr, laparams=self.laparams)
        self.interpreter = PDFPageInterpreter(rsrcmgr, self.device)


    @classmethod
    def open(cls, path_or_fp, **kwargs):
        if isinstance(path_or_fp, (str, pathlib.Path)):
            return cls(open(path_or_fp, "rb"),path_or_fp, **kwargs)
        else:
            return cls(path_or_fp, path_or_fp, **kwargs)

    def get_page(self, page):
        try:
            self.interpreter.process_page(page)
        except:
            return None
        return self.device.get_result()

    @property
    def pages(self):
        if hasattr(self, "_pages"):
            return self._pages


        pp = self.pages_to_parse
        self._pages = []
        for i, page in enumerate(PDFPage.create_pages(self.doc)):
            page_number = i
            if pp is not None and page_number not in pp:
                continue


            page_image = poppler.image_from_path(pdf_path=self._pdf_file_path, first_page=page_number+1, last_page=page_number+1,dpi=500)[0]
            p = Page(self, page, page_number=page_number, page_image=page_image,fix_with_ocr=self.fix_with_ocr)


            self._pages.append(p)

        return self._pages

    # @property
    # def tokens(self):
    #     return [token for page in self.pages for token in page.tokens]

    def close(self):
        self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.flush_cache()
        self.close()

    @property
    def objects(self):
        if hasattr(self, "_objects"):
            return self._objects
        all_objects = {}
        for p in self.pages:
            for kind in p.objects.keys():
                all_objects[kind] = all_objects.get(kind, []) + p.objects[kind]
        self._objects = all_objects
        return self._objects

    @property
    def Title(self):
        largest_fonts=None
        candidates=sorted([token[0] for p in self.pages for token in p.title], key=lambda x: -x.font_size)
        candidates=[c.Text for c in candidates]

        if candidates!=[]:
            most_common=Counter(candidates).most_common(1)[0]
            if most_common[1]>1:
                return most_common[0]
            else:
                candidates = [t[0] for p in self.pages for t in p.title]
                max_size=max([c.font_size for c in candidates])
                largest_fonts = [x.Text for x in candidates if x.font_size == max_size]

        if largest_fonts is not None:
            return ' '.join(largest_fonts)

    @property
    def tokens(self):
        """
        A TokenList containing all tokens in the document.

        Returns:
            TokenList: All tokens in the document.
        """
        return TokenList(self)

    @property
    def paragraphs(self):
        return self._paragraphs.paragraphs

    def pretty_print(self):
        for p in self.paragraphs:
            print(p.Text)
    @property
    def Text(self):
        return '\n'.join([p.Text for p in self._paragraphs.paragraphs])

    def get_text_matches_regex(self, regex_str, case_sensitive=True):
        """
        Filter for tokens whose text contains the given string.

        Args:
            text (str): The text to filter for.

        Returns:
            LineList: The filtered list.
        """
        flags = re.MULTILINE
        if not case_sensitive:
            flags |= re.IGNORECASE

        regex = re.compile(regex_str, flags=flags)

        matches=regex.finditer(self.Text)



        matched=[]
        for matchNum, match in enumerate(matches, start=1):
            m={'matchNum':matchNum, 'start':match.start(),'end':match.end(), 'match':match.group(), 'groups':[]}

            for groupNum in range(0, len(match.groups())):
                groupNum +=1

                m['groups'].append({'groupNum':groupNum, 'start': match.start(groupNum), 'end':match.end(groupNum),  'group':match.group(groupNum)})
            matched.append(m)
        return matched
