import itertools
from operator import itemgetter
from collections import Counter
from pdf2txt.core.token import Token
import numpy as np
import re
from pdf2txt.table_ml import extract_table
import pandas as pd
from . import utils
from pdf2txt.doc_analyzer.img import show_rects_and_wait, show_and_wait
from itertools import chain, zip_longest
from .exceptions import (
    TableExtractionError,
    NoTokenFoundError,
    MultipleTokensFoundError,
    InvalidTableError,
    InvalidTableHeaderError,
)
from copy import deepcopy

DEFAULT_SNAP_TOLERANCE = 3
DEFAULT_JOIN_TOLERANCE = 3
DEFAULT_MIN_WORDS_VERTICAL = 3
DEFAULT_MIN_WORDS_HORIZONTAL = 3

from copy import copy


class Table(object):
    def __init__(self, region, textlines=None, rect=None, paragraph=None, settings={}):

        if textlines == None and rect == None:
            raise Exception(
                "Incomplete infromation for the table. You should give either a list of tokens or a bounding box coordinates")
        self.region = region
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)
        self.interline = -1
        self.area = rect
        self.paragraph = paragraph
        self.from_table_region_only = False
        if textlines:
            self.textlines = textlines
            self.settings["edge_min_length"] = max(l[-1].right - l[0].left for l in self.textlines)
        else:

            self.textlines = utils.find_line_structure(utils.get_widthin_BoundingBox(region.tokens, rect))
            self.from_table_region_only = True

        self._data = []
        self.df = None

        self._nb_headers = 1
        self.get_edges()

    @property
    def bbox(self):
        if self.area is not None:
            return self.area
        return utils.get_BoundingBox_from_objects([t for line in self.textlines for t in line])

    @property
    def top(self):
        return self.bbox.top

    @property
    def left(self):
        return self.bbox.left

    @property
    def right(self):
        return self.bbox.right

    @property
    def bottom(self):
        return self.bbox.bottom

    def vertically_in_line_with(self, token, linelist, tolerance: float = 0.0):

        tolerance = min(token.width / 2, tolerance)
        bounding_box = utils.BoundingBox(
            left=token.left - tolerance,
            right=token.right + tolerance,
            top=self.region.top,
            bottom=self.region.bottom,
        )
        results = set()

        for line in linelist:
            for tok in line:
                if tok.partially_within(bounding_box):
                    results.add(tok)
        return frozenset(results)

    def get_edges(self):

        v = utils.filter_edges(self.region.edges, "v")

        hh = self.region.horizontal_edges
        #show_rects_and_wait(hh, self.region.parent_page.page_image.copy())
        hh = utils.join_collated_h_edges(hh)

        if self.area is not None and self.paragraph is not None:
            hh = [l for l in hh if l.top >= min(self.paragraph[0][0].top, self.area.top) and l.bottom <= max(
                self.paragraph[-1][0].bottom, self.area.bottom)]

        #       show_rects_and_wait(hh, self.page.parent_page.image.copy())

        left_right = utils.cluster_objects2(hh, ["left", "right"], rel_tol=0, abs_tol=1)
        h = []
        if left_right:
            h = max(left_right, key=lambda x: len(x))
        #        if len(utils.get_partially_overlapping_objects(utils.get_BoundingBox_from_objects([t for line in self.textlines for t in line]), h)) >= max(1, len(self.textlines)-3):
        self._edges_h = sorted(h, key=lambda e: e.top)
        split_index = -1
        if len(self._edges_h) > len(self.textlines) + 2:  # we may have been too agressive and selected too many lines.
            nb_tokens = [len(l) for l in self.region.text_lines]
            for i in range(0, len(nb_tokens) - 2):
                if nb_tokens[i] == 1 and nb_tokens[i + 1] == 1:  # ugly fix
                    split_index = i
                    break
            if split_index > 0:
                y_cut_off = self.region.text_lines[i][0].top
                self._edges_h = [l for l in self._edges_h if l.bottom < y_cut_off]
        self._edges_v = v

    def horizontally_in_line(self, row, rows):

        if len(rows) == 0:
            return None

        bounding_box = utils.BoundingBox(
            left=self.region.left,
            right=self.region.right,
            top=row.top,
            bottom=row.bottom,
        )

        for r in rows:
            for token in list(r):
                if token.partially_within(bounding_box):
                    return frozenset(r)
        return None

    def horizontally_within_lines(self, line_bottom, line_top, nbcols):

        if line_top is not None:
            bounding_box = utils.BoundingBox(
                left=self.region.left,
                right=self.region.right,
                top=line_top.top,
                bottom=line_bottom.bottom,
            )

            ll = [line for line in self.textlines if line[0].within(bounding_box)]

            if ll == []:
                ll = [self.textlines[0]]
            if len(ll) > 1 and all([len(a) == nbcols for a in ll]):
                return ll

        else:
            ll = [line for line in self.textlines if line[0].top > line_bottom.bottom]
        return [[item for sublist in ll for item in sublist]]

    def extract(self):
        if self.region is not None:
            self._data = extract_table_from_rects(self.region)
            if self._data:
                objects = [c for row in self._data for c in row]
                objects = [o for l in objects for o in l]

                self.area = utils.get_BoundingBox_from_objects(objects)
                self._data = [[tokens_to_string(c) for c in row] for row in self._data]
                return self
        if not self._data:
            if 2 < len(self._edges_h) < 2 * (len(self.textlines) + 1):
                return self.extract_from_lines()
            elif len(self._edges_h) > 2 * (len(self.textlines) + 1) and self.area is not None:
                self._edges_h = [e for e in self._edges_h if e.top >= self.area.top and e.bottom <= self.area.bottom]
                if len(self._edges_h) > len(self.textlines):
                    return self.extract_from_lines()

            return self.extract_from_text()

    def extract_from_text(self):
        """
        Returns tokens structured as a table.

        Given an TokenList, tries to extract a structured table by examining which
        tokens are aligned. There must be a clear gap between each row and between each
        column which contains no tokens, and a single cell cannot contain multiple
        tokens.

        If you fail to satisfy any of the other conditions listed above, that case is not
        yet supported.

        Returns:
            list[list]: a list of rows, which are lists of PDFTokens or strings
                (depending on the value of as_text).
        """

        guess_nb_cols_most_common = Counter(len(l) for l in self.textlines if len(l) > 1).most_common(1)

        nb_cols_cutoff = int(len(self.textlines) / 2) if len(self.textlines) >= 4 else 2

        if guess_nb_cols_most_common == [] or guess_nb_cols_most_common[0][1] < nb_cols_cutoff:
            return None

        else:
            ncols = guess_nb_cols_most_common[0][0]

        if ncols == 1:
            return None

        if len(self.textlines[-1]) == 1:
            self.textlines = self.textlines[:-1]

        while len(self.textlines[0]) == 1:
            self.textlines = self.textlines[1:]

        self._data = extract_table(self.textlines)

        #        self._validate_table_shape()
        return self

    def post_process_token(self, line):

        # split list of dates into separate tokens:
        regex = r"(\d{2}[\/\.-]\d{2}[\/\.-]\d{2}\s?)"
        new_line = []
        for token in line:
            text = token.Text
            matches = re.finditer(regex, text)

            indices = []
            nb_matches = 0
            for matchNum, match in enumerate(matches, start=1):
                nb_matches += 1

            if nb_matches > 1:
                words = [w for w in token.original_words]

                new_line.extend([Token(w, token.page) for w in words])
            else:
                new_line.append(token)
        return new_line

    def extract_from_textlines(self, rows, token_lines):
        self._data = extract_table(rows)
        return self

    def fix_text_lines(self, textlines):

        for line in textlines:
            if len(line) <= self.ncols:
                continue
            while len(line) > self.ncols:
                separations = []
                for i in range(0, len(line) - 1):
                    separations.append(line[i + 1].left - line[i].right)
                    to_combine = separations.index(min(separations))
                line[to_combine].combine(line[to_combine + 1])
                line[to_combine].right = line[to_combine + 1].right
                del line[to_combine + 1]
        return textlines

    def extract_from_lines(self):
        bbox = utils.get_BoundingBox_from_objects(self._edges_h)
        bbox.bottom += 10

        if (self.textlines is not None and len(self.textlines) > 0) and self._edges_h[0].top > self.textlines[0][0].top:
            bbox.top = self.textlines[0][0].top
        if not self.from_table_region_only:
            self.textlines = [self.post_process_token(line) for line in self.region.text_lines if
                              line[0].bottom >= bbox.top and line[0].top <= bbox.bottom]
            self._edges_h = [e for e in self._edges_h if
                             e.top > self.textlines[0][0].top - 10 and e.bottom < self.textlines[-1][0].bottom + 10]
        if self.textlines == []:
            return None

        if len(self._edges_h) <= 2:
            return self.extract_from_text()
        col_sizes = [len(line) for line in self.textlines if len(line) > 1]
        if len(col_sizes) > 1:
            self.ncols = Counter([len(line) for line in self.textlines if len(line) > 1]).most_common(1)[0][0]
        else:
            return None
        if self.ncols == 1:
            return None
        self.textlines = self.fix_text_lines(self.textlines)
        while len(self.textlines[0]) == 1:
            self.textlines = self.textlines[1:]

        while len(self.textlines[-1]) == 1:
            self.textlines = self.textlines[:-1]

        rows = []

        z = zip(self._edges_h[1:], self._edges_h[:-1])
        header = []
        for i, (b, t) in enumerate(z):
            #            show_rects_and_wait([b, t], self.page.parent_page.image.copy())
            if header == []:
                if t.top > self.textlines[0][0].bottom:
                    header = [tl for tl in self.textlines if tl[0].top < self._edges_h[0].top]

                    rows.extend(self._fix_header_rows(header, self.ncols))
                elif b.top > (self.textlines[0][0].bottom + self.textlines[0][0].top) / 2:
                    header = self.horizontally_within_lines(b, t, self.ncols)
                    rows.extend(self._fix_header_rows(header, self.ncols))
            else:
                row = self.horizontally_within_lines(b, t, self.ncols)
                if row and row not in rows:
                    rows.extend(row)

        last_row = self.horizontally_within_lines(b, None, self.ncols)
        if last_row != [[]] and len(last_row[0]) >= (int(self.ncols * 0.7) if self.ncols >= 3 else self.ncols - 1):
            rows.extend(last_row)
        elif last_row != [[]]:
            self.textlines = self.textlines[:-1]

        return self.extract_from_textlines(rows, self.textlines)

    def _validate_table_shape(self):
        """
        Checks that all rows (and therefore all columns) are the same length.
        """
        if len(self._data) < 1:
            return
        first_row_len = len(self._data[0])
        for idx, row in enumerate(self._data[1:]):
            if not len(row) == first_row_len:
                raise InvalidTableError(
                    f"Table not rectangular, row 0 has {first_row_len} tokens but row "
                    f"{idx + 1} has {len(row)}."
                )

    @staticmethod
    def extract_table_lines_from_paragaraph(paragraph):
        if len(paragraph) < 3:
            return False

        guess_nb_cols_most_common = Counter(len(l) for l in paragraph if len(l) > 1).most_common(1)

        if not guess_nb_cols_most_common:
            return False
        if guess_nb_cols_most_common[0][1] < 2:
            return False

        else:
            guess_nb_cols = guess_nb_cols_most_common[0][0]

        if guess_nb_cols < 2:
            return False

        # only a subset of columns in a pragraph form a table
        rows = []

        rows_idx = [i for i, r in enumerate(paragraph) if max(guess_nb_cols - 2, 2) <= len(r) <= guess_nb_cols + 1]

        table_lines = paragraph[min(rows_idx):max(rows_idx) + 1]

        return table_lines

    def _fix_rows(self, rows, pdflines) -> None:
        """
        Sometimes a token may span over multiple rows. For example:
        ---------
        | A | B |
        ----|   |
        | C |   |
        ---------
        In this, case, when extract_table scans for token in line with A it will pick up
        A and B. When it scans B it will get A, B and C, and when it scans C it will get B
        and C. This results in three distinct rows, AB, ABC, BC. This function will fix
        this by putting any merged cells into the top row, resulting in one row AB and the
        other with just C.

        To do this, we check which token is in multiple rows, get which rows it is in,
        and then remove it from the lower rows. This should fix the problem. It can result
        in empty rows (since in my example we begin with 3 'rows' when there are only
        really 2), but these can simply be removed.
        """

        sorted_rows = sorted(
            rows,
            key=lambda row: (max(-(elem.right) for elem in row)))

        #    sorted_rows = [row for row in sorted_rows if not all(utils.get_type(token.Text) == 'Literal' for token in row)]
        for line in pdflines:
            for token in line:
                num_rows = sum(token in row for row in rows)
                if num_rows == 1:
                    continue
                # If we reach here, we've found an token in multiple rows.

                rows_with_token = [row for row in rows if token in row]
                sorted_rows_with_token = sorted(
                    rows_with_token, key=lambda row: sorted_rows.index(row)
                )
                # Remove the token from all but the first row.
                for row in sorted_rows_with_token[1:]:
                    rows.remove(row)
                    new_row = set(row).remove(token)
                    if new_row:
                        rows.add(new_row)
                        # Update sorted rows
                        sorted_rows = [
                            new_row if some_row == row else some_row for some_row in sorted_rows
                        ]
                    else:
                        sorted_rows.remove(row)

    def _fix_cols(self, cols, tokenlines) -> None:
        """
        The same as _fix_rows, but when an token is in multiple columns, for example
        ---------
        | A | B |
        --------|
        |   C   |
        ---------
        """

        if sum([len(col) for col in cols]) == len(set(chain.from_iterable(cols))):
            # No elements are in multiple cols, return.
            return cols

        # We sort by looking at all the elements and choosing the element which starts
        # most to the right. The ones with elements which start most to the right
        # will be later on in the sorted list.
        sorted_columns = sorted(
            cols, key=lambda col: (max([elem.left for elem in col]), -len([e for e in col]))
        )
        for element in [token for line in tokenlines for token in line]:
            num_cols = sum(element in col for col in cols)
            if num_cols == 1:
                continue
            # If we reach here, we've found an element in multiple cols.

            cols_with_element = [col for col in cols if element in col]
            sorted_cols_with_element = sorted(
                cols_with_element, key=lambda col: sorted_columns.index(col)
            )
            # Remove the element from all but the first col.
            for col in sorted_cols_with_element[1:]:
                cols.remove(col)
                new_col = set(copy(col))
                new_col.remove(element)
                if new_col:
                    cols.add(frozenset(new_col))
                    # Update sorted columns
                    sorted_columns = [
                        new_col if some_col == col else some_col
                        for some_col in sorted_columns
                    ]
                else:
                    sorted_columns.remove(col)

        return cols

    def _fix_header_rows(self, header, ncols, tolerance=5):
        """
        First row in a table my contain several sub rows that  typically span multiple columns
        -------------------------
        | A                     |
        ------------------------|
        | B | C | D | E | F | G |
        -------------------------
        """

        if not isinstance(header[0], list):
            return header
        if len(header) == 1:
            return header

        header2 = []
        start_index = 0
        header2.append([Token.copy(h) for h in header[-1]])
        if len(header2[0]) == ncols:
            start_index = 1

        # if the first row is right justified than the first row is not a header row otherwise it is considered as header row
        for i in reversed(range(1, len(header))):
            next_row_used = False
            for token in header[i - 1][start_index:]:
                if len(header[i][start_index:]) > 2 and token.left - tolerance > min(
                        t.left for t in header[i][start_index:]) and (
                        len(header[i - 1]) == len(header2[-1]) or len(header[i - 1]) == len(
                        header[i])):  # not left justified or as many header as the last row
                    for t in header[i - 1]:
                        for j in range(start_index, len(header2[-1])):
                            if t.left + tolerance >= header2[-1][j].left and t.right - tolerance <= header2[-1][
                                j].right:
                                t_c = Token.copy(t)
                                header2[-1][j] = t_c.combine(header2[-1][j])
                                next_row_used = True
                    break
                else:
                    break
            if not next_row_used:
                h2 = []
                for t in range(start_index, len(header[i - 1]) - 1):
                    for h in header2[-1][start_index:]:
                        if h.right < header[i - 1][t + 1].left:
                            h_item = Token.copy(header[i - 1][t])

                            h_item.left = h.left
                            h_item.right = h.right
                            h2.append(h_item)
                for h in header2[-1]:
                    if h.left >= header[i - 1][-1].left:
                        h_item = Token.copy(header[i - 1][-1])

                        h_item.left = h.left
                        h_item.right = h.right
                        h2.append(h_item)
                if len(h2) <= len(header2[-1]):
                    header2.insert(0, h2)
                else:
                    header2.insert(0, header[i - 1])
        self._nb_headers = len(header2)
        return header2

    def __repr__(self):
        return f"<{self.__class__.__name__} shape={self.shape}>"

    def __lt__(self, other):
        if self.region == other.region:
            if self.order < other.order:
                return True
        if self.region < other.region:
            return True

    @property
    def shape(self):
        if len(self._data) == 0:
            return (0, 0)
        return (len(self.data), len(self._data[0]) if len(self._data[0]) else 0)

    @property
    def data(self):
        """Returns two-dimensional list of strings in table.
        """
        d = []
        for row in self._data:
            d.append([' '.join([c.Text for c in cell]) for cell in row])
        return d

    def to_pandas(self):
        if self.df is not None:
            return self.df
        else:
            self.df = Table.to_dataframe(self._data, self._nb_headers)
            return self.df

    @staticmethod
    def to_dataframe(data, nb_headers=1):

        df = pd.DataFrame(data)

        if not df.empty and len(df.index) > 2:
            if nb_headers == 1:
                headers = df.iloc[0]

                df = pd.DataFrame(df.values[1:], columns=headers)
            else:
                tuple_index = [(i, *j) for i, *j in zip(*data[0:nb_headers])]

                pd.MultiIndex.from_tuples(tuple_index)
                df = pd.DataFrame(data[nb_headers:])
                try:
                    df.columns = pd.MultiIndex.from_tuples(tuple_index)
                except:
                    pass

        if not df.empty:
            df.iloc[:, 0].replace("", np.NaN, inplace=True)
            df.iloc[:, 0].fillna(method='ffill', inplace=True)
        return df

    def to_text(self):
        if self.df is not None:
            return self.df.to_string()
        else:
            ""

    def to_json(self, path, **kwargs):
        """Writes Table to a JSON file.
        For kwargs, check :meth:`pandas.DataFrame.to_json`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {"orient": "records"}
        kw.update(kwargs)
        json_string = self.df.to_json(**kw)
        with open(path, "w") as f:
            f.write(json_string)

    def to_excel(self, path, **kwargs):
        """Writes Table to an Excel file.
        For kwargs, check :meth:`pandas.DataFrame.to_excel`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        kw = {
            "sheet_name": f"page-{self.region}-table-{self.order}",
            "encoding": "utf-8",
        }
        kw.update(kwargs)
        writer = pd.ExcelWriter(path)
        self.df.to_excel(writer, **kw)
        writer.save()

    def to_html(self, path, **kwargs):
        """Writes Table to an HTML file.
        For kwargs, check :meth:`pandas.DataFrame.to_html`.
        Parameters
        ----------
        path : str
            Output filepath.
        """
        html_string = self.df.to_html(**kwargs)
        with open(path, "w") as f:
            f.write(html_string)


class CellGroup(object):
    def __init__(self, cells):
        self.cells = cells
        self.bbox = (
            min(map(itemgetter(0), filter(None, cells))),
            min(map(itemgetter(1), filter(None, cells))),
            max(map(itemgetter(2), filter(None, cells))),
            max(map(itemgetter(3), filter(None, cells))),
        )


class Row(CellGroup):
    pass


TABLE_STRATEGIES = ["lines", "lines_strict", "text", "explicit"]
DEFAULT_TABLE_SETTINGS = {

    "edge_min_length": 3,
    "y_tolerance": 1,
    "min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
    "min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
}


class TableFinder(object):
    """
    Given a PDF page, find plausible table structures.
    """

    def __init__(self, page, settings={}):
        for k in settings.keys():
            if k not in DEFAULT_TABLE_SETTINGS:
                raise ValueError(f"Unrecognized table setting: '{k}'")
        self.page = page
        self.settings = dict(DEFAULT_TABLE_SETTINGS)
        self.settings.update(settings)

    def find_tables(self):
        table_areas = self.guess_tables()
        for table_area in table_areas:
            text_tokens = utils.get_widthin_BoundingBox(self.page.tokens, table_area)
            line_clusters = utils.cluster_objects(text_tokens, "bottom", self.settings["y_tolerance"])

            if line_clusters is not None:
                text_lines = [line for line in line_clusters]
            else:
                text_lines = []

            table = Table(self.page, text_lines)
            yield table

    def words_to_edges_h(self, word_threshold=DEFAULT_MIN_WORDS_HORIZONTAL, max_words=10):
        """
        Find (imaginary) horizontal lines that connect the tops
        of at least `word_threshold` words.
        """
        by_top = utils.cluster_objects(self.page.tokens, "bottom", 2)
        if by_top is None:
            return []
        #        by_top=[c for c in by_top for t in c if len(t.Text)< 100]

        large_clusters = []
        for c in by_top:

            c = [t for t in c if t.Text != '–']

            c = [t for t in c if len(t.Text) < 40]

            if len(c) >= word_threshold:
                large_clusters.append(c)

        #        large_clusters = list(filter(lambda x: len(x) >= word_threshold, by_top))
        rects = list(map(utils.get_BoundingBox_from_objects, large_clusters))
        if len(rects) == 0:
            return []
        edges = [
            {
                "left": r.left,
                "right": r.right,
                "top": r.bottom,
                "bottom": r.bottom,
                "width": r.right - r.left,
                "orientation": "h",
            }
            for r in rects
        ]

        return [utils.BoundingBox(**e) for e in edges]

    def guess_tables(self):

        tables = []
        all_tables = self._guess_tables_from_rectangles()

        horizontal_lines = [line for line in self.page.horizontal_edges if
                            line.width < self.page.root_page.content_width * 0.95]

        #show_rects_and_wait(horizontal_lines, self.page.page_image.copy())
        if len(horizontal_lines) >= 2:
            tables = self._guess_tables_from_lines(horizontal_lines)
            for table in tables:
                if not utils.is_ovarlaping_with_objects(table, all_tables):
                    all_tables.append(table)

#        if tables:
            #show_rects_and_wait(all_tables, self.page.root_page.page_image.copy())
        tables = self._guess_tables_from_lines(self.guess_table_lines())
        for table in tables:
            if not utils.is_ovarlaping_with_objects(table, all_tables):
                all_tables.append(table)

        return_tables = []
        for t in sorted(all_tables, key=lambda x: (x.top, x.left)):
            if not return_tables:
                return_tables = [t]
            found_overlap = False
            for i in range(0, len(return_tables)):
                table = return_tables[i]
                if utils.has_overlap_with_bbox(table, t, allow_touching=True):
                    table_ = utils.get_BoundingBox_from_objects([t, table])
                    return_tables[i] = table_
                    found_overlap = True
                    break
            if not found_overlap:
                return_tables.append(t)

        return [t for t in return_tables if not utils.is_ovarlaping_with_objects(t, self.page.charts)]

    def snap_edges(self, edges, tolerance=DEFAULT_SNAP_TOLERANCE):
        """
        Given a list of edges, snap any within `tolerance` pixels of one another
        to their positional average.
        """
        v, h = [list(filter(lambda x: x.orientation == o, edges)) for o in ("v", "h")]

        snap = utils.snap_objects
        snapped = snap(v, "left", tolerance) + snap(h, "top", tolerance)
        return snapped

    def join_edge_group(self, edges, orientation, tolerance=DEFAULT_JOIN_TOLERANCE):
        """
        Given a list of edges along the same infinite line, join those that
        are within `tolerance` pixels of one another.
        """
        if orientation == "h":
            min_prop, max_prop = "left", "right"
        elif orientation == "v":
            min_prop, max_prop = "top", "bottom"
        else:
            raise ValueError("Orientation must be 'v' or 'h'")

        sorted_edges = list(sorted(edges, key=lambda e: getattr(e, min_prop)))
        joined = [sorted_edges[0]]
        for e in sorted_edges[1:]:
            last = joined[-1]
            if getattr(e, min_prop) <= (getattr(last, max_prop) + tolerance):
                if getattr(e, max_prop) > getattr(last, max_prop):
                    # Extend current edge to new extremity
                    joined[-1] = utils.resize_object(last, max_prop, getattr(e, max_prop))
            else:
                # Edge is separate from previous edges
                joined.append(e)

        return joined

    def merge_edges(self, edges, snap_tolerance, join_tolerance):
        """
        Using the `snap_edges` and `join_edge_group` methods above,
        merge a list of edges into a more "seamless" list.
        """

        def get_group(edge):
            if edge.orientation == "h":
                return ("h", edge.top)
            else:
                return ("v", edge.left)

        if snap_tolerance > 0:
            edges = self.snap_edges(edges, snap_tolerance)

        if join_tolerance > 0:
            _sorted = sorted(edges, key=get_group)
            edge_groups = itertools.groupby(_sorted, key=get_group)
            edge_gen = (
                self.join_edge_group(items, k[0], join_tolerance) for k, items in edge_groups
            )
            edges = list(itertools.chain(*edge_gen))
        return edges

    def _guess_tables_from_rectangles(self, threshold=2):
        #        show_and_wait()
        rects = [rect for rect in self.page.rects if rect.width > rect.height and rect.height > 2]
        left_right = utils.cluster_objects2(rects, ["left", "right"], rel_tol=0, abs_tol=0.2)
        if left_right is not None:
            left_right = list(filter(lambda x: len(x) >= threshold, left_right))
        if left_right is None:
            return []

        groups = []
        for group in left_right:
            sorted(group, key=lambda g: g.top)
            new_group = [group[0]]
            for i in range(0, len(group) - 1):
                if np.isclose(group[i].bottom, group[i + 1].top, atol=0.1) or np.isclose(group[i].top, group[i + 1].top,
                                                                                         atol=0.1):
                    new_group.append(group[i + 1])
                else:
                    groups.append(new_group)
                    new_group = [group[i + 1]]
            if new_group:
                groups.append(new_group)
        return [utils.get_BoundingBox_from_objects(g) for g in groups if len(g) >= threshold]

    def _guess_tables_from_lines(self, lines, threshold=3):
        lines = utils.join_collated_h_edges(lines)

        max_row_height = 40
        left_right = utils.cluster_objects2(lines, ["left", "right"], abs_tol=10)

        if left_right is not None:
            left_right = list(filter(lambda x: (len(x) >= threshold and x[0].width > 20), left_right))
        if left_right is None:
            return []
        tables = []
        for group in left_right:
            group = sorted(group, key=lambda x: x.bottom)
            for i in range(0, len(group) - 1):
                group[i].space_bellow = group[i + 1].bottom - group[i].bottom
                if i > 0:
                    group[i].space_above = group[i].bottom - group[i - 1].bottom
            group[-1].space_bellow = group[-2].space_bellow
            group[0].space_above = group[1].space_above

            i = 0
            while i < len(group):
                line = group[i]
                if line.space_bellow <= max_row_height:
                    subgroup = [line]
                else:
                    subgroup = []
                i += 1
                while i < len(group) and np.isclose(line.space_bellow, group[i].space_bellow,
                                                    atol=min(line.space_above, line.space_bellow)):
                    if group[i].space_bellow <= max_row_height:
                        subgroup.append(group[i])
                    line = group[i]
                    i += 1
                # if i < len(group):
                #     if len(subgroup)>0:
                #         subgroup.append(group[i])
                #     i += 1
                if len(subgroup) >= threshold:
                    bbox = utils.get_BoundingBox_from_objects(subgroup)
                    txts = utils.get_widthin_BoundingBox(self.page.text_lines, bbox)
                    if len(txts) > 1:
                        tables.append(bbox)

        return tables

    def guess_table_lines(self, token_threshold_v=2, token_threshold_h=2, pruning_cut_off=2):

        h_edges = self.words_to_edges_h(word_threshold=token_threshold_h)
        h_edges = utils.cluster_objects2(h_edges, ["left", "right"], rel_tol=0, abs_tol=5)
        if h_edges is not None:
            h_edges = list(filter(lambda x: len(x) >= token_threshold_v, h_edges))
        if h_edges is not None:
            return [e for g in h_edges for e in g]
        else:
            return []

    def get_intersections_for_edge(self, edge, intersections):
        intersection_points = []
        for pt, edges in intersections.items():
            edge_v = edges['v'][0]
            edge_h = edges['h'][0]
            if edge == edge_h or edge == edge_v:
                intersection_points.append(pt)

        return intersection_points

    def words_to_edges_v(self, word_threshold=DEFAULT_MIN_WORDS_VERTICAL):
        """
        Find (imaginary) vertical lines that connect the left, right, or
        center of at least `word_threshold` words.
        """
        # Find words that share the same left, right, or centerpoints
        by_left = utils.cluster_objects(self.page.tokens, "left", 0.5)
        if by_left is None:
            by_left = []
        else:
            by_left = list(filter(lambda x: len(x) >= word_threshold, by_left))
        by_right = utils.cluster_objects(self.page.tokens, "right", 0.5)
        if by_right is None:
            by_right = []
        else:
            by_right = list(filter(lambda x: len(x) >= word_threshold, by_right))
        #    by_center = utils.cluster_objects(words, lambda x: (x.left + x.right) / 2,  0.5)
        #    by_center = list(filter(lambda x: len(x) >= word_threshold, by_center))

        by_left_copy = copy(by_left)
        by_right_copy = copy(by_right)

        # for left in by_left:
        #     for right in by_right:
        #         inetersection = set(left).intersection(set(right))
        #         if len(inetersection) >= 2:
        #             if len(set(right)) >= len(set(left)):
        #                 if left in by_left_copy:
        #                     by_left_copy.remove(left)
        #             else:
        #                 if right in by_right_copy:
        #                     by_right_copy.remove(right)

        rects = list(map(utils.get_BoundingBox_from_objects, by_left_copy))

        edges = [
            {
                "left": r.left,
                "right": r.left,
                "top": r.top,
                "bottom": r.bottom,
                "height": r.bottom - r.top,
                "justification": "left",
                "orientation": "v",
            }
            for r in rects
        ]

        rects = list(map(utils.get_BoundingBox_from_objects, by_right_copy))

        edges = edges + [
            {
                "left": r.right,
                "right": r.right,
                "top": r.top,
                "bottom": r.bottom,
                "height": r.bottom - r.top,
                "justification": "right",
                "orientation": "v",
            }
            for r in rects
        ]
        # rects= list(map(utils.get_BoundingBox_from_objects, by_center))
        #
        # edges = edges + [
        #     {
        #         "left": (r.right+r.left)/2,
        #         "right": (r.right+r.left)/2,
        #         "top": r.top,
        #         "bottom": r.bottom,
        #         "height": r.bottom - r.top,
        #         "justification": "center",
        #         "orientation": "v",
        #     }
        #     for r in rects
        # ]

        rects = [utils.BoundingBox(**e) for e in edges]

        return rects

    def edges_to_intersections(self, edges, x_tolerance=1, y_tolerance=1):
        """
        Given a list of edges, return the points at which they intersect
        within `tolerance` pixels.
        """
        intersections = {}
        v_edges, h_edges = [
            list(filter(lambda x: x.orientation == o, edges)) for o in ("v", "h")
        ]
        for v in sorted(v_edges, key=lambda e: (getattr(e, "left"), getattr(e, "top"))):
            for h in sorted(h_edges, key=lambda e: (getattr(e, "top"), getattr(e, "left"))):
                if (
                        (v.top <= (h.top + y_tolerance))
                        and (v.bottom >= (h.top - y_tolerance))
                        and (v.left >= (h.left - x_tolerance))
                        and (v.left <= (h.right + x_tolerance))
                ):
                    vertex = (v.left, h.top)
                    if vertex not in intersections:
                        intersections[vertex] = {"v": [], "h": []}
                    intersections[vertex]["v"].append(v)
                    intersections[vertex]["h"].append(h)
        return intersections

    def intersections_to_cells(self, intersections):
        """
        Given a list of points (`intersections`), return all rectangular "cells"
        that those points describe.

        `intersections` should be a dictionary with (x0, top) tuples as keys,
        and a list of edge objects as values. The edge objects should correspond
        to the edges that touch the intersection.
        """

        def edge_connects(p1, p2):
            def edges_to_set(edges):
                return set([(e.left, e.top, e.right, e.bottom) for e in edges])

            if p1[0] == p2[0]:
                common = edges_to_set(intersections[p1]["v"]).intersection(
                    edges_to_set(intersections[p2]["v"])
                )
                if len(common):
                    return True

            if p1[1] == p2[1]:
                common = edges_to_set(intersections[p1]["h"]).intersection(
                    edges_to_set(intersections[p2]["h"])
                )
                if len(common):
                    return True
            return False

        points = list(sorted(intersections.keys()))
        n_points = len(points)

        def find_smallest_cell(points, i):
            if i == n_points - 1:
                return None
            pt = points[i]
            rest = points[i + 1:]
            # Get all the points directly below and directly right
            below = [x for x in rest if x[0] == pt[0]]
            right = [x for x in rest if x[1] == pt[1]]
            for below_pt in below:
                if not edge_connects(pt, below_pt):
                    continue

                for right_pt in right:
                    if not edge_connects(pt, right_pt):
                        continue

                    bottom_right = (right_pt[0], below_pt[1])

                    if (
                            (bottom_right in intersections)
                            and edge_connects(bottom_right, right_pt)
                            and edge_connects(bottom_right, below_pt)
                    ):
                        return (pt[0], pt[1], bottom_right[0], bottom_right[1])

        cell_gen = (find_smallest_cell(points, i) for i in range(len(points)))
        return list(filter(None, cell_gen))

    def cells_to_tables(self, cells):
        """
        Given a list of bounding boxes (`cells`), return a list of tables that
        hold those cells most simply (and contiguously).
        """

        def bbox_to_corners(bbox):
            x0, top, x1, bottom = bbox
            return list(itertools.product((x0, x1), (top, bottom)))

        cells = [
            {"available": True, "bbox": bbox, "corners": bbox_to_corners(bbox)}
            for bbox in cells
        ]

        # Iterate through the cells found above, and assign them
        # to contiguous tables

        def init_new_table():
            return {"corners": set([]), "cells": []}

        def assign_cell(cell, table):
            table["corners"] = table["corners"].union(set(cell["corners"]))
            table["cells"].append(cell["bbox"])
            cell["available"] = False

        n_cells = len(cells)
        n_assigned = 0
        tables = []
        current_table = init_new_table()
        while True:
            initial_cell_count = len(current_table["cells"])
            for i, cell in enumerate(filter(itemgetter("available"), cells)):
                if len(current_table["cells"]) == 0:
                    assign_cell(cell, current_table)
                    n_assigned += 1
                else:
                    corner_count = sum(
                        c in current_table["corners"] for c in cell["corners"]
                    )
                    if corner_count > 0 and cell["available"]:
                        assign_cell(cell, current_table)
                        n_assigned += 1
            if n_assigned == n_cells:
                break
            if len(current_table["cells"]) == initial_cell_count:
                tables.append(current_table)
                current_table = init_new_table()

        if len(current_table["cells"]):
            tables.append(current_table)

        _sorted = sorted(tables, key=lambda t: min(t["corners"]))
        filtered = [t["cells"] for t in _sorted if len(t["cells"]) > 1]
        return filtered

    def get_edges(self):
        settings = self.settings

        v_base = utils.filter_edges(self.page._edges, "v")

        v_base_text = self.words_to_edges_v()

        v = v_base + v_base_text

        h_base = utils.filter_edges(self.page._edges, "h")
        h_base_text = self.words_to_edges_h()

        h = h_base + h_base_text

        edges = list(v) + list(h)

        if settings["snap_tolerance"] > 0 or settings["join_tolerance"] > 0:
            edges = self.merge_edges(
                edges,
                snap_tolerance=settings["snap_tolerance"],
                join_tolerance=settings["join_tolerance"],
            )
        return utils.filter_edges(edges, min_length=settings["edge_min_length"])


def guess_table_from_token_lines(region, token_lines, has_table=None):
    if len(token_lines) < 3:
        return None

    guess_nb_cols_most_common = Counter(len(l) for l in token_lines).most_common(1)

    if guess_nb_cols_most_common[0][1] < 3:
        return False

    else:
        guess_nb_cols = guess_nb_cols_most_common[0][0]

    if guess_nb_cols < 3:
        return False

    table_lines = []
    rows_added = False
    for l in token_lines:
        if guess_nb_cols + 1 >= len(l) >= guess_nb_cols - 1:
            table_lines.append(l)
            rows_added = True
        elif rows_added:
            break
    if len(table_lines) >= 3:
        first_row = table_lines[0]
        for t in range(0, len(first_row) - 1):
            h = (first_row[t + 1].left + first_row[t].right) / 2
            for row in table_lines[1:]:
                if t >= len(row) - 1:
                    continue
                if (h > row[t].right and h < row[t + 1].left) or row[t + 1].right < h:
                    continue
                else:
                    return None

        table = Table(region, textlines=table_lines, rect=utils.get_BoundingBox_from_objects(has_table),
                      paragraph=token_lines).extract()
        #            print(table.to_pandas().to_string())
        return table
    return None


def guess_tables_from_lines(lines, threshold=3):
    lines = utils.join_collated_h_edges(lines)

    left_right = utils.cluster_objects2(lines, ["left", "right"], abs_tol=10)

    if left_right is not None:
        left_right = list(filter(lambda x: (len(x) >= threshold and x[0].width > 20), left_right))
    if left_right is None:
        return []
    tables = []
    for group in left_right:
        group = sorted(group, key=lambda x: x.bottom)
        for i in range(0, len(group) - 1):
            group[i].space_bellow = group[i + 1].bottom - group[i].bottom
            if i > 0:
                group[i].space_above = group[i].bottom - group[i - 1].bottom
        group[-1].space_bellow = group[-2].space_bellow
        group[0].space_above = group[1].space_above

        i = 0

        group_bot = utils.cluster_objects(group, "space_bellow", tolerance=5)

    return tables


def does_it_intersect(x, xmin, xmax):
    return (x <= xmax and x >= xmin)


def find_bounding_rectangle(x, y, h_lines, v_lines):
    """
    Given a collection of lines, and a point, try to find the rectangle
    made from the lines that bounds the point. If the point is not
    bounded, return None.
    """

    v_intersects = [l for l in v_lines
                    if does_it_intersect(y, l.top, l.bottom)]

    h_intersects = [l for l in h_lines
                    if does_it_intersect(x, l.left, l.right)]

    if len(v_intersects) < 2 or len(h_intersects) < 2:
        return None

    v_left = [v.left for v in v_intersects
              if v.left < x]

    if len(v_left) == 0:
        v_left = [v.left for v in h_intersects
                  if v.left < x]

    v_right = [v.left for v in v_intersects
               if v.left > x]

    if len(v_right) == 0:
        v_right = [v.right for v in h_intersects
                   if v.right > x]

    if len(v_left) == 0 or len(v_right) == 0:
        return None

    x0, x1 = max(v_left), min(v_right)

    h_down = [h.top for h in h_intersects
              if h.top < y]
    if len(h_down) == 0:
        h_down = [h.bottom for h in v_intersects
                  if h.bottom > y]

    h_up = [h.top for h in h_intersects
            if h.top > y]

    if len(h_up) == 0:
        h_up = [h.top for h in v_intersects
                if h.top > y]

    if len(h_down) == 0 or len(h_up) == 0:
        return None

    y0, y1 = max(h_down), min(h_up)

    return (x0, y0, x1, y1)


from collections import defaultdict
import math


def map_tokens(tokens, h_lines, v_lines):
    box_token_dict = {}

    for token in tokens:
        # choose the bounding box that occurs the majority of times for each of these:
        bboxes = defaultdict(int)
        l_x, l_y = token.left, token.top
        bbox_l = find_bounding_rectangle(l_x, l_y, h_lines, v_lines)
        bboxes[bbox_l] += 1

        c_x, c_y = math.floor((token.left + token.right) / 2), math.floor((token.top + token.bottom) / 2)
        bbox_c = find_bounding_rectangle(c_x, c_y, h_lines, v_lines)
        bboxes[bbox_c] += 1

        u_x, u_y = token.top, token.bottom
        bbox_u = find_bounding_rectangle(u_x, u_y, h_lines, v_lines)
        bboxes[bbox_u] += 1

        # if all values are in different boxes, default to character center.
        # otherwise choose the majority.
        if max(bboxes.values()) == 1:
            bbox = bbox_c
        else:
            bbox = max(bboxes.items(), key=lambda x: x[1])[0]

        if bbox is None:
            continue

        if bbox in box_token_dict.keys():
            box_token_dict[bbox].append(token)
            continue

        box_token_dict[bbox] = [token]

    return box_token_dict


def boxes_to_table(box_record_dict):
    """
    Converts a dictionary of cell:characters mapping into a python list
    of lists of strings. Tries to split cells into rows, then for each row
    breaks it down into columns.
    """
    boxes = box_record_dict.keys()
    rows = sorted(list(set(b[1] for b in boxes)), reverse=True)
    table = []
    if len(rows) < 2:
        return table
    for row in sorted(rows):
        sorted_row = sorted([b for b in boxes if b[1] == row], key=lambda b: b[0])
        table.append([box_record_dict[b] for b in sorted_row])

    return sanitise_table(table)


def sanitise_table(table):
    if len(table) < 3:
        return []

    guess_nb_cols_most_common = Counter(len(l) for l in table if len(l) > 1).most_common(1)

    if not guess_nb_cols_most_common:
        return []
    if guess_nb_cols_most_common[0][1] < 2:
        return []

    else:
        guess_nb_cols = guess_nb_cols_most_common[0][0]

    if guess_nb_cols < 2:
        return []

    # only a subset of columns in a pragraph form a table
    rows = []

    rows_idx = [i for i, r in enumerate(table) if max(guess_nb_cols - 2, 2) <= len(r) <= guess_nb_cols + 1]

    table = table[min(rows_idx):max(rows_idx) + 1]

    return table


def tokens_to_string(tokens):
    text = ' '.join([t.Text for t in tokens])
    return text


def extract_table_from_rects(region):
    table = boxes_to_table(map_tokens(region.tokens, region.horizontal_edges, region.vertical_edges))
    return table
    # if table!=[]:
    #     return Table.to_dataframe(table)
