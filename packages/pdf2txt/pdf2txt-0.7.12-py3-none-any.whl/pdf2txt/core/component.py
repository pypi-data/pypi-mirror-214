from itertools import chain
from pdf2txt import  utils
from pdf2txt.settings import DEFAULT_X_TOLERANCE, DEFAULT_Y_TOLERANCE



class Component(object):
    cached_properties = ["_rect_edges", "_edges", "_objects"]
    objects=None
    _horizontal_lines=None
    _vertical_lines=None
    def flush_cache(self, properties=None):
        props = self.cached_properties if properties is None else properties
        for p in props:
            if hasattr(self, p):
                delattr(self, p)

    @property
    def rects(self):
        _rects=[utils.BoundingBox(**rect) for rect in self.objects.get("rect", []) if rect["height"]>0 and rect["width"]>0]#+[c for c in self.curves if c.width<100 and c.height<100]

        return [r for r in _rects if r.width/r.height >0.01 and r.height/r.width>0.01]

    @property
    def lines(self):
        if hasattr(self, "__lines"):
            return self.__lines

        h_lines=[rect for rect in self.rects+self.curves if rect.height<1 and rect.width>10]+[utils.BoundingBox(**line) for line in self.objects.get("line", []) if line["width"]>line["height"]]
        v_lines=[rect for rect in self.rects+self.curves if rect.width<1 and rect.height>10]+[utils.BoundingBox(**line) for line in self.objects.get("line", []) if line["width"]<line["height"]]


        h_lines=utils.join_collated_h_edges(h_lines)
        v_lines=utils.join_collated_v_edges(v_lines)



        self.__lines=h_lines+v_lines
        return self.__lines

    def get_non_text_objects(self):
        return self.lines+self.rects+self.curves
    @property
    def curves(self):
        return  [utils.BoundingBox(**curve) for curve in self.objects.get("curve", [])]

    @property
    def images(self):
        return [utils.BoundingBox(**curve) for curve in self.objects.get("image", [])]


    @property
    def chars(self):
        chars_= utils.dedupe_chars(self.objects.get("char", []))
        for c in chars_:
            if c["text"]=='\xad':
                c["text"]='-'
            elif c["text"]=="’":
                c["text"]="'"
        return chars_

    @property
    def horizontal_lines(self):
        if self._horizontal_lines is None:
            self._horizontal_lines=[line for line in self.lines if line.height<1 and line.width>10]
            return self._horizontal_lines
        return self._horizontal_lines

    @property
    def vertical_lines(self):
        if self._vertical_lines is None:
            self._vertical_lines=[line for line in self.lines if line.width<1 and line.height>10]
            return self._vertical_lines
        return self._vertical_lines


    @property
    def rect_edges(self):
        if hasattr(self, "_rect_edges"):
            return self._rect_edges
        rect_edges_gen = (utils.rect_to_edges(r) for r in self.rects)

        self._rect_edges = list(chain(*rect_edges_gen))
        return self._rect_edges

    @property
    def edges(self):
        if hasattr(self, "_edges"):
            return self._edges
        line_edges = list(map(utils.line_to_edge, self.lines))
        self._edges = self.rect_edges + line_edges
        return self._edges

    @property
    def horizontal_edges(self):
        def test(x):
            return x.orientation == "h"

        return list(filter(test, self.edges))

    @property
    def vertical_edges(self):
        def test(x):
            return x.orientation == "v"

        return list(filter(test, self.edges))
