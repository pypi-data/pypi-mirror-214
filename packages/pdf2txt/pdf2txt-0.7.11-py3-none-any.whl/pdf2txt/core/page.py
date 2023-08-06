import re

from pandas import DataFrame

from pdf2txt import utils
from pdf2txt.core import Component
from pdf2txt.core.paragraph import ContentType
from pdf2txt.core.paragraph import extract
from pdf2txt.core.token import Token, TokenExtractor
from pdf2txt.core.word import WordExtractor, Word
from pdf2txt.doc_analyzer.image_analyzer import PageAnalyzer
from pdf2txt.charts import extract_charts
from pdf2txt.settings import ALL_ATTRS
from pdf2txt.settings import DEFAULT_WORD_EXTRACTION_SETTINGS, DEFAULT_TOKEN_EXTRACTION_SETTINGS
from pdf2txt.table import TableFinder, extract_table_from_rects  # , Table
from pdf2txt.table import Table, guess_tables_from_lines
from pdf2txt.utils import BoundingBox
from pdf2txt.core.paragraph import guess_titles
from pdf2txt.charts import Chart
from pdf2txt.utils import resolve_all
from pdf2txt.doc_analyzer.img import show_rects_and_wait, show_and_wait
import cv2
from math import isclose
from poppdf.pdf import xml_ocr_from_image
import numpy as np
from kdmt.geometry import rectangle_intersect

lt_pat = re.compile(r"^LT")

PAGE_HEIGHT = 1260
PAGE_WIDTH = 890


class Page(Component):
    cached_properties = Component.cached_properties + ["_layout"]
    is_original = True
    _text_lines = None

    def __init__(self, parent, page_obj, page_number=None, page_image=None, bbox=None, fix_with_ocr=False):
        self.document = parent
        self.page_obj = page_obj
        self.page_number = page_number
        self.title = []
        self._words = None
        self.token_start = None
        self.token_end = None

        self.page_image = page_image
        #        self._tokens=None

        mediabox = page_obj.attrs.get("MediaBox")

        self.mediabox = resolve_all(mediabox)
        m = self.mediabox

        if bbox is None:
            self.bbox = BoundingBox(
                min(m[0], m[2]),
                min(m[1], m[3]),
                max(m[0], m[2]),
                max(m[1], m[3]),
            )
        self._left_margin = None
        self._right_margin = None
        self._top_margin = None
        self._bottom_margin = None
        size = (PAGE_WIDTH, PAGE_HEIGHT)
        # high resolution image foe OCR

        if not isinstance(self, Region):
            self.alto = None
            if fix_with_ocr:
                self.alto = xml_ocr_from_image(self.page_image, size=size, options='--psm 3', thresholding='simple')

            self.page_image = cv2.cvtColor(np.asarray(self.page_image), code=cv2.COLOR_RGB2BGR)
            # reduce image size for region analysis
            self.page_image = cv2.resize(self.page_image, size, interpolation=cv2.INTER_AREA)
            self.set_page_layout()

            # used to extract regions
            nb_regions = len(self.regions)
        self.table_finder = TableFinder(self)
        self.root_page = self

    def detect_semantic_structure_bk(self, debug=True):

        self.regions.sort(key=lambda re: (re.left, re.top))

        paragraph_number = 0
        font_body = {}
        page_font_statistics = self.font_statistics
        for region_number, region in enumerate(self.regions):
            font_statistics = region.font_statistics
            if self.page_number == 0 and region_number <= 1:
                if region_number == 0:
                    self.find_header(region, region_number == 1)
                elif region_number == 1 and region.height < self.bbox.height / 8:
                    self.find_header(region, region_number == 1)
            elif self.page_number > 0 and region_number == 0 and region.height < self.bbox.height / 8:
                self.find_header(region, region_number == 1)

            title_font = {}
            paragraphs = []
            if len(region.text_lines) > 0:
                paragraphs = self.extract_paragraph(region)
            for p in paragraphs:
                check_title = True
                paragraph_number += 1
                paragraph = self.document._paragraphs.get_last_paragraph()

                for n, tl in enumerate(p):
                    if isinstance(tl, Table) or isinstance(tl, DataFrame):
                        if paragraph is not None and len(paragraph.content) > 0:
                            t = paragraph.content[-1]["content"]
                            if not isinstance(t, DataFrame) and check_title and t is not None and self.is_title2(t,
                                                                                                                 font_statistics,
                                                                                                                 page_font_statistics,
                                                                                                                 title_font={}):
                                del paragraph.content[-1]
                                paragraph = self.document._paragraphs.create_paragraph()
                                paragraph.title = t
                                check_title = False
                            else:
                                if isinstance(tl, Table):
                                    columns = tl.to_pandas().columns.tolist()
                                else:  # Dataframe
                                    columns = tl.columns.tolist()
                                if len(columns) > 0:

                                    if paragraph is not None and len(paragraph.content) > 0 and len(columns) > 0:
                                        first = columns[0]
                                        t = self.get_token_with_value(first)
                                        if check_title and t is not None and self.is_title2([t], page_font_statistics,
                                                                                            page_font_statistics,
                                                                                            title_font):
                                            paragraph = self.document._paragraphs.create_paragraph()
                                            paragraph.title = [t]
                                        if paragraph is None:
                                            paragraph = self.document._paragraphs.create_paragraph()
                        elif paragraph is None:
                            paragraph = self.document._paragraphs.create_paragraph()
                        paragraph.add_content(tl, ContentType.Table)

                    elif check_title and (
                            paragraph is None or self.is_title2(tl, font_statistics, page_font_statistics, title_font,
                                                                font_body)):
                        #                        existing_title=self.document._paragraphs.filter_by_title_equal(tl)
                        paragraph = self.document._paragraphs.create_paragraph()
                        paragraph.title = tl
                        title_font['name'] = tl[0].font + str(tl[0].Text.isupper() or tl[0].is_bold)
                        title_font['size'] = tl[0].font_size
                        check_title = False
                    else:
                        paragraph.add_content(tl, ContentType.Text)
                        if tl[0].font_size <= self.font_statistics['average']:
                            font_body['name'] = tl[0].font + str(tl[0].is_bold)
                            font_body['size'] = tl[0].font_size

                        check_title = True

    def detect_semantic_structure(self, debug=False):
        text_lines = []
        for region in self.regions:
            text_lines.extend(region.text_lines)

        titles=guess_titles(text_lines, self.font_statistics)
        title_font={}

        if debug:
            show_rects_and_wait(self.regions, self.page_image.copy())

        for region_number, region in enumerate(self.regions):
            if region.top < 10:
                self.find_header(region, region_number == 1, titles)
            if len(region.text_lines) > 0:
                paragraphs = self.extract_paragraph(region)
                doc_paragraph=None
                for paragraph in paragraphs:
                    last_paragraph=self.document._paragraphs.get_last_paragraph()
                    if last_paragraph is None:
                        doc_paragraph = self.document._paragraphs.create_paragraph()
                    if isinstance(paragraph, Chart):
                        if doc_paragraph is not None:
                            doc_paragraph.add_content(paragraph, ContentType.Chart)
                        elif last_paragraph is not None:
                            last_paragraph.add_content(paragraph, ContentType.Chart)
                        continue
                    elif isinstance(paragraph, Table):
                        if doc_paragraph is not None:
                            doc_paragraph.add_content(paragraph, ContentType.Table)
                        elif last_paragraph is not None:
                            last_paragraph.add_content(paragraph, ContentType.Table)
                        continue
                    for line in paragraph:
                        if self.is_title(line, title_font, self.font_statistics):
#                            print(line)
                            if last_paragraph is not None and last_paragraph.title==line:
                                continue

                            doc_paragraph = self.document._paragraphs.create_paragraph()
                            doc_paragraph.title=line
                        else:
                            if doc_paragraph is not None:
                                doc_paragraph.add_content(line, ContentType.Text)
                            elif last_paragraph is not None:
                                last_paragraph.add_content(line, ContentType.Text)


    def extract_paragraph_bk(self, region):
        returned_paragraphs = []

        g_paragraph = self.extract_paragaph_from_graph(region)

        if g_paragraph:
            returned_paragraphs = g_paragraph
        else:
            txt_paragraphs = extract(region.text_lines)

            for p in txt_paragraphs:
                paragraph = []
                table_region = None
                text_lines = Table.extract_table_lines_from_paragaraph(p)
                table_regions = utils.get_partially_overlapping_objects(
                    utils.get_BoundingBox_from_objects([t for l in p for t in l]), region.tables)
                if table_regions:
                    table_region = utils.get_BoundingBox_from_objects(table_regions)

                if text_lines or table_region:
                    i = 0
                    table = Table(region, textlines=text_lines if text_lines else p, rect=table_region,
                                  paragraph=p).extract()
                    while i < len(p):
                        line = p[i]
                        if table is None or line not in table.textlines:
                            paragraph.append(line)
                            i += 1
                        else:
                            paragraph.append(table)
                            i += len(table.textlines)
                else:
                    paragraph = p

                returned_paragraphs.append(paragraph)
        return returned_paragraphs

    def extract_paragraph(self, region):

        returned_paragraphs = []
        g_paragraph=self.extract_paragaph_from_graph(region)
        t_paragraph=self.extract_paragaph_from_table(region)

        if g_paragraph:
            returned_paragraphs.extend(g_paragraph)
        elif t_paragraph:
            returned_paragraphs.extend(t_paragraph)
        else:
            returned_paragraphs.extend(extract(region.text_lines))

        return returned_paragraphs

    def extract_paragaph_from_graph(self, region):

        if len(region.charts) == 0:
            return []
        else:
            top = region.top
            paragraphs = []
            for graph in sorted(region.charts, key=lambda g: g.top):
                top_paragraph = extract([tl for tl in region.text_lines if top < tl[0].bottom <= graph.top])
                if len(top_paragraph[0]) > 0:
                    paragraphs.extend(top_paragraph)
                # graph_paragraph = []
                # graph_data = graph.extract_chart_data()
                # if 'text' in graph_data and len(graph_data['text']) > 0:
                #     graph_paragraph.append(graph_data['text'])
                # if 'dataframe' in graph_data and graph_data['dataframe'] is not None:
                #     graph_paragraph.append(graph_data['dataframe'])
                paragraphs.append(graph)

                top = graph.bottom
            last_paragraph = extract([tl for tl in region.text_lines if tl[0].top > top])
            if len(last_paragraph[0]) > 0:
                paragraphs.extend(last_paragraph)

        return paragraphs

    def extract_paragaph_from_table(self, region):

        if len(region.tables) == 0:
            return []
        else:
            top = region.top
            paragraphs = []
            if len(region.tables)>1:
                txt_paragraphs=extract(region.text_lines)
                for p in txt_paragraphs:
                    table_region = utils.get_partially_overlapping_objects(
                        utils.get_BoundingBox_from_objects([t for l in p for t in l]), region.tables)
                    if table_region:
                        text_lines = Table.extract_table_lines_from_paragaraph(p)
                        table = Table(region, textlines=text_lines, rect=table_region[0], paragraph=p).extract()
                        if table:
                            paragraphs.append(table)
                    else:
                        paragraphs.append(p)
            else:
                table=region.tables[0]
                top_paragraph = extract([tl for tl in region.text_lines if top < tl[0].bottom <= table.top])
                if len(top_paragraph[0]) > 0:
                    paragraphs.extend(top_paragraph)
                text_lines = Table.extract_table_lines_from_paragaraph(region.text_lines)
                table = Table(region, textlines= text_lines, rect=table).extract()
                if table:
                    paragraphs.append(table)

                    top = table.bottom
                last_paragraph = extract([tl for tl in region.text_lines if tl[0].top > top])
                if len(last_paragraph[0]) > 0:
                    paragraphs.extend(last_paragraph)

        return paragraphs

    def is_title2(self, textline, font_stat, page_font_stat, title_font={}, font_body={}):

        if len(textline) == 0:
            return False
        if font_body and textline[0].font + str(textline[0].Text.isupper() or textline[0].is_bold) == font_body[
            'name'] and textline[0].font_size == font_body['size']:
            return False

        if utils.get_type(textline[0].Text.replace('M€', '').replace('€', '').replace('/', '').strip()) == "Numeric":
            return False
        if title_font and textline[0].font + str(textline[0].Text.isupper() or textline[0].is_bold) == title_font[
            'name']:
            return True
        elif title_font and textline[0].font_size > title_font['size']:
            return True
        elif title_font:
            return False
        if (len(font_stat["name_by_frequency"]) > 1 or len(font_stat["size_by_frequency"]) > 1) and (
                textline[0].font_size >= font_stat['second_largest'] and font_stat['second_largest'] > -1):
            title_font['name'] = textline[0].font + str(textline[0].Text.isupper() or textline[0].is_bold)
            title_font['size'] = textline[0].font_size
            return True
        elif len(font_stat["name_by_frequency"]) == 1 and len(font_stat["size_by_frequency"]) == 1:
            if font_stat['most_frequent'] < page_font_stat["largest"]:
                return False
            elif font_stat['most_frequent'] == page_font_stat["largest"] and (
                    textline[0].Text.isupper() or textline[0].is_bold):
                title_font['name'] = textline[0].font + str(textline[0].Text.isupper() or textline[0].is_bold)
                title_font['size'] = textline[0].font_size
                return True
            elif font_stat['most_frequent'] == page_font_stat["largest"]:
                return False
        return False

    def find_header(self, region, first_page=False, titles=None):
        font_stat = region.parent_page.font_statistics
        for i, l in enumerate(region.text_lines[:5]):
            if (l[0].top >= self.root_page.height / 8 and i > 2) or l in titles:
                continue
            if l[0].font_size == font_stat["largest"] or l[0].font_size >= font_stat['second_largest']:
                self.title.append(l)
                if first_page or l[0].font_size == font_stat["largest"]:
                    region.text_lines.remove(l)

        return False

    def find_header_bk(self, region, largest_only=False):
        font_stat = region.parent_page.font_statistics
        first_horizontal_separator = None
        horizontal_separators = [line for line in region.horizontal_lines + region.horizontal_edges if
                                 line.width > self.width * 0.7]
        if len(horizontal_separators) > 0:
            first_horizontal_separator = horizontal_separators[0]
        for l in region.text_lines[:5]:
            if first_horizontal_separator and l[0].top > first_horizontal_separator.top and len(self.title) > 0:
                return

            if not largest_only and (
                    l[0].font_size == font_stat["largest"] or l[0].font_size > font_stat["most_frequent"]):
                self.title.append(l)
                region.text_lines.remove(l)
            elif largest_only and l[0].font_size == font_stat["largest"]:
                self.title.append(l)
                region.text_lines.remove(l)
        return False

    def is_title(self, line, title_font, font_stat={}):

#        return line in titles
        if len(line)>1 or not line[0].Text.istitle():
            return False

        if line[0].font_size >= font_stat["second_largest"]:
            title_font['font']=line[0].font
            return True

        if title_font:
            if line[0].font == title_font['font']:
                return True
            else:
                return False

        if len(line)==1 and utils.get_type(line[0].Text)=="Numeric":
            return False

        if len(font_stat["size_by_frequency"])==1 and line[0].is_bold:
            title_font['font']=line[0].font
            return True

        if len(font_stat["size_by_frequency"])==1 and len(font_stat["name_by_frequency"])==1:
            return False

        if id==0:
            title_font['font'] = line[0].font
            return True

        return False

    def _has_match(self, sorted_list, item):
        #       show_rects_and_wait(sorted_list, self.page_image)
        i = 0
        while i < len(sorted_list) and not isclose(sorted_list[i].top, item.top, abs_tol=item.height / 3):
            i += 1

        return_set = []
        if i < len(sorted_list):
            while i < len(sorted_list) and isclose(sorted_list[i].top, item.top, abs_tol=item.height / 3):
                return_set.append(sorted_list[i])
                i += 1
        if return_set == []:
            return False
        else:
            for t in return_set:
                intersection = rectangle_intersect((item.left, item.top, item.right, item.bottom),
                                                   (t.left, t.top, t.right, t.bottom), norm_intersect_area='a')
                if intersection and intersection > 0.5:
                    return True
        return False

    def set_page_layout(self):

        mediabox = self.page_obj.attrs.get("MediaBox")

        self.mediabox = resolve_all(mediabox)

        self.image_width = self.page_image.shape[1]
        self.image_height = self.page_image.shape[0]
        self.x_scaler = self.image_width / float(self.mediabox[2])
        self.y_scaler = self.image_height / float(self.mediabox[3])

    def get_token_with_value(self, val):
        for t in self.tokens:
            if t.Text == val:
                return t

    @property
    def regions(self):
        if hasattr(self, "_regions"):
            return self._regions

        self._regions = []
        for chart in self.charts:
            cv2.line(self.page_image, (int(chart.left) + 5, int(chart.top) + 5),
                     (int(chart.right) - 5, int(chart.bottom) - 5), (0, 0, 255), 3)


        _regions_ = PageAnalyzer(self).extract_regions()

        # recombine small regions horizontally
        all_regions = []
        for sub_region in _regions_:

            for region in sorted(sub_region, key=lambda x: (x.top, x.left)):
                texts1 = utils.get_widthin_BoundingBox(self.text_lines, region)
                texts2 = utils.get_widthin_BoundingBox(self.text_lines, all_regions[-1]) if len(all_regions) else 3

                if len(all_regions) == 0 or len(texts1) > 2 and len(texts2) > 2:
                    all_regions.append(region)
                elif all_regions[-1].top == region.top and all_regions[-1].bottom == region.bottom:
                    all_regions[-1].right = region.right
                else:
                    all_regions.append(region)

        all_regions_ = []
        for region in sorted(all_regions, key=lambda x: (x.left, x.top)):
            texts1 = utils.get_widthin_BoundingBox(self.tokens, region)
            texts2 = utils.get_widthin_BoundingBox(self.tokens, all_regions_[-1]) if len(all_regions_) else 4

            if len(all_regions_) == 0 or len(texts1) > 3 and len(texts2) > 3:
                all_regions_.append(region)
            elif all_regions_[-1].left == region.left and all_regions_[-1].right == region.right:
                all_regions_[-1].bottom = region.bottom
            else:
                all_regions_.append(region)

        all_regions_ = [Region(self, r) for r in all_regions_]
        self._regions = sorted([r for r in all_regions_ if len(r.text_lines) > 0], key=lambda re: (re.left, re.top))

        #        self._regions=sorted(self._regions, key=lambda re: (re.left, re.top))
        return self._regions

    @property
    def width(self):
        return self.bbox.right - self.bbox.left

    @property
    def height(self):
        return self.bbox.bottom - self.bbox.top

    @property
    def layout(self):
        if hasattr(self, "_layout"):
            return self._layout
        self._layout = self.document.get_page(self.page_obj)
        return self._layout

    @property
    def font_statistics(self):
        if hasattr(self, "_font_statistics"):
            return self._font_statistics

        self._font_statistics = utils.get_fonts_statistics(self.text_lines)
        return self._font_statistics

    @property
    def objects(self):
        if hasattr(self, "_objects"):
            return self._objects
        self._objects = self.parse_objects()
        return self._objects

    def process_object(self, obj):
        kind = re.sub(lt_pat, "", obj.__class__.__name__).lower()

        def process_attr(item):
            k, v = item
            if k in ALL_ATTRS:
                res = resolve_all(v)
                return (k, res)
            else:
                return None

        attr = dict(filter(None, map(process_attr, obj.__dict__.items())))

        attr["object_type"] = kind
        attr["page_number"] = self.page_number

        if hasattr(obj, "graphicstate"):
            gs = obj.graphicstate
            attr["stroking_color"] = gs.scolor
            attr["non_stroking_color"] = gs.ncolor
            attr["linewidth"] = gs.linewidth

        if hasattr(obj, "get_text"):
            attr["text"] = obj.get_text()

        if kind == "curve":
            def point2coord(pt):
                x, y = pt
                return (x, self.height - y)

            attr["points"] = list(map(point2coord, obj.pts))

        if attr.get("y0") is not None:
            attr["top"] = (self.height - attr["y1"]) * self.y_scaler
            attr["bottom"] = (self.height - attr["y0"]) * self.y_scaler
        if attr.get("x0") is not None:
            attr["left"] = attr["x0"] * self.x_scaler
        if attr.get("x1") is not None:
            attr["right"] = attr["x1"] * self.x_scaler

        return attr

    def iter_layout_objects(self, layout_objects):
        for obj in layout_objects:
            # If object is, like LTFigure, a higher-level object
            # then iterate through it's children
            if hasattr(obj, "_objs"):
                yield from self.iter_layout_objects(obj._objs)
            else:
                yield self.process_object(obj)

    def parse_objects(self):
        objects = {}
        for obj in self.iter_layout_objects(self.layout._objs):
            kind = obj["object_type"]

            if objects.get(kind) is None:
                objects[kind] = []
            objects[kind].append(obj)
        return objects

    def within_bbox(self, bbox, relative=False):
        """
        Same as .crop, except only includes objects fully within the bbox
        """
        return Region(self, bbox)

    @property
    def tables(self):
        if hasattr(self, "_tables"):
            return self._tables

        self._tables = self.table_finder.guess_tables()
        return self._tables

    @property
    def charts(self):
        if hasattr(self, "_charts"):
            return self._charts

        self._charts = extract_charts(page=self, rect_threshold=2)

        return self._charts

    @property
    def words(self):
        settings = dict(DEFAULT_WORD_EXTRACTION_SETTINGS)
        if self._words:
            return self._words
        if not self.chars:
            return []
        chars = self.chars

        if "linewidth" in self.chars[0]:
            chars = [char for char in self.chars if
                     (char["upright"] and (char["left"] > 0 and char["linewidth"] > 0) or (
                             char["linewidth"] == 0 and char["non_stroking_color"] not in [(1, 0, 1)]))]
        self._words = WordExtractor(self, **settings).extract(chars)
        if self.alto is not None:
            return [w for w in self._words if
                    self._has_match(sorted([t for t in self.alto.extract_text_lines()], key=lambda x: x.top), w)]
        return self._words

    @property
    def tokens(self):
        if self.token_start is not None and self.token_end is not None:
            return self.document._token_list[self.token_start:self.token_end]

        settings = dict(DEFAULT_TOKEN_EXTRACTION_SETTINGS)

        self.token_start = len(self.document._token_list)
        if self.words != []:
            _tokens = TokenExtractor(self, **settings).extract(self.words)
        else:
            _tokens = []

        not_tokens = [t for t in _tokens if t.left < 1 or t.right < 1 or t.top < 1 or t.bottom < 1]

        for i, token in enumerate(_tokens):
            if hasattr(token.original_words[0], "font_color"):
                print(token.Text)
            if token in not_tokens:
                continue
            token.index = self.token_start + i
            self.document._token_list.append(token)

        self.token_end = len(self.document._token_list)
        return self.document._token_list[self.token_start:self.token_end]

    @property
    def text_lines(self):

        if self._text_lines is not None:
            return self._text_lines
        if len(self.tokens) == 0:
            return []
            #       doctop_clusters = cluster_objects(self.tokens, "bottom", self.tokens[0].font_size/3)

            #        if doctop_clusters is not None:
        self._text_lines = utils.find_line_structure(
            self.tokens)  # [sorted(line, key=lambda x: x.left) for line in doctop_clusters]
        if not isinstance(self, Region):
            for i in range(1, len(self._text_lines)):
                for token in self._text_lines[i]:
                    token.space_above = self._text_lines[i][0].bottom - self._text_lines[i - 1][0].bottom

            if len(self._text_lines)>=2:
                for token in self._text_lines[0]:
                    token.space_above=max(a[0].space_above for a in self._text_lines[1:])


        return self._text_lines

    def __repr__(self):
        return f"<Page:{self.page_number}>"

    @property
    def top(self):
        return self.bbox.top

    @property
    def bottom(self):
        return self.bbox.bottom

    @property
    def left(self):
        return self.bbox.left

    @property
    def right(self):
        return self.bbox.right

    @property
    def left_margin(self):
        if self._left_margin is None:
            if len(self.tokens) == 0:
                self._left_margin = 0
            else:
                self._left_margin = min([t.left for t in self.tokens])

        return self._left_margin

    @property
    def content_width(self):
        return self.right_margin - self.left_margin

    @property
    def right_margin(self):
        if self._right_margin is None:
            if len(self.tokens) == 0:
                self._right_margin = self.width
            else:
                self._right_margin = max([t.right for t in self.tokens])
            if self._right_margin >= self.bbox.right:
                self._right_margin = self.bbox.right - self.left_margin / 2
        return self._right_margin

    @property
    def top_margin(self):
        if self._top_margin is None:
            if len(self.tokens) == 0:
                self._top_margin = 0
            else:
                self._top_margin = min([t.top for t in self.tokens])
        return self._top_margin

    @property
    def bottom_margin(self):
        if self._bottom_margin is None:
            if len(self.tokens) == 0:
                self._bottom_margin = self.height
            else:
                self._bottom_margin = max([t.bottom for t in self.tokens])
        return self._bottom_margin


class Region(Page):
    is_original = False

    def __init__(self, parent_page, bbox):

        self.parent_page = parent_page
        self.page_number = parent_page.page_number

        super().__init__(parent_page, parent_page.page_obj, bbox=bbox)
        self.flush_cache(Component.cached_properties)
        self.page_image = self.parent_page.page_image[bbox.top:bbox.bottom, bbox.left:bbox.right]
        self.bbox = bbox

        if type(parent_page) == Page:
            self.root_page = parent_page
        else:
            self.root_page = parent_page.root_page
        self.sections = []

    def __repr__(self):
        return f"<Region:{self.page_number}>"

    @property
    def rects(self):
        return utils.get_widthin_BoundingBox(self.parent_page.rects, self.bbox)

    @property
    def words(self):
        return utils.get_widthin_BoundingBox(self.parent_page.words, self.bbox)

    @property
    def tokens(self):
        return utils.get_widthin_BoundingBox(self.parent_page.tokens, self.bbox)

    @property
    def charts(self):
        return utils.get_widthin_BoundingBox(self.parent_page.charts, self.bbox)

    @property
    def objects(self):
        return utils.get_widthin_BoundingBox(self.parent_page.objects, self.bbox)

