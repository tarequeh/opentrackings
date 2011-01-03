import urllib2

from xml.etree.ElementTree import _escape_cdata, _raise_serialization_error, _encode, _escape_attrib, fixtag
from xml.etree.ElementTree import ElementTree, Comment, QName, ProcessingInstruction, XMLTreeBuilder

class PrintableElementTree(ElementTree):
    def print_tree(self, encoding="us-ascii"):
        assert self._root is not None
        if not encoding:
            encoding = "us-ascii"        
        return self._print_node(self._root, encoding)

    def _print_node(self, node, encoding):
        tree_string = ""

        tag = node.tag
        if tag is Comment:
            tree_string += "<!-- %s -->" % _escape_cdata(node.text, encoding)
        elif tag is ProcessingInstruction:
            tree_string += "<?%s?>" % _escape_cdata(node.text, encoding)
        else:
            items = node.items()
            xmlns_items = [] # new namespaces in this scope
            try:
                if isinstance(tag, QName) or tag[:1] == "{":
                    tag, xmlns = fixtag(tag, namespaces)
                    if xmlns: xmlns_items.append(xmlns)
            except TypeError:
                _raise_serialization_error(tag)
            tree_string += "<" + _encode(tag, encoding)
            if items or xmlns_items:
                items.sort() # lexical order
                for k, v in items:
                    try:
                        if isinstance(k, QName) or k[:1] == "{":
                            k, xmlns = fixtag(k, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(k)
                    try:
                        if isinstance(v, QName):
                            v, xmlns = fixtag(v, namespaces)
                            if xmlns: xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(v)
                    tree_string += " %s=\"%s\"" % (_encode(k, encoding),
                                               _escape_attrib(v, encoding))
                for k, v in xmlns_items:
                    tree_string += " %s=\"%s\"" % (_encode(k, encoding),
                                               _escape_attrib(v, encoding))

            tree_string += ">"
            if node.text:
                tree_string += _escape_cdata(node.text, encoding).replace('"', '&quot;')
            for n in node:
                tree_string += self._print_node(n, encoding)
            tree_string += "</" + _encode(tag, encoding) + ">"
            for k, v in xmlns_items:
                del namespaces[v]

        if node.tail:
            tree_string += _escape_cdata(node.tail, encoding)

        return tree_string

    def parse_xml(self, raw_xml, parser=None):
        if not parser:
            parser = XMLTreeBuilder()

        parser.feed(raw_xml)

        self._root = parser.close()
        return self._root

def get_element_text(element, default_text=''):
    try:
        element_text = element.text
        return element_text
    except:
        return default_text
