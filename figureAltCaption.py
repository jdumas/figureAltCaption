"""
Generates a Caption for Figures for each Image which stands alone in a paragraph,
similar to pandoc#s handling of images/figures

--------------------------------------------

Licensed under the GPL 2 (see LICENSE.md)

Copyright 2015 - Jan Dittrich by
building upon the markdown-figures Plugin by
Copyright 2013 - [Helder Correia](http://heldercorreia.com) (GPL2)

--------------------------------------------

Examples:
    Bla bla bla

    ![this is the caption](http://lorempixel.com/400/200/)

    Next paragraph starts here

would generate a figure like this:

    <figure>
        <img src="http://lorempixel.com/400/200/">
        <figcaption>this is the caption</figcaption>
    </figure>
"""


from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import LinkInlineProcessor, IMAGE_LINK_RE
from markdown.util import etree


class FigureCaptionInlineProcessor(LinkInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        figure = etree.Element('figure')
        img = etree.SubElement(figure, "img")
        caption = etree.SubElement(figure, "figcaption")

        img.set("src", src)

        if title is not None:
            img.set("title", title)

        caption.text = text
        return figure, m.start(0), index


class FigureCaptionExtension(Extension):
    def extendMarkdown(self, md, __md_globals):
        """ Add an instance of AltCaptionInlineProcessor to InlinePatterns. """
        md.inlinePatterns.register(FigureCaptionInlineProcessor(IMAGE_LINK_RE, md), 'figureAltcaption', 155)
        md.registerExtension(self)


def makeExtension(**kwargs):
    return FigureCaptionExtension(**kwargs)
