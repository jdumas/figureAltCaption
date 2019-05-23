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
# from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from markdown import util as md_util
import re  # regex

import logging
logger = logging.getLogger('MARKDOWN')


NOBRACKET = r'[^\]\[]*'
BRK = (
    r'\[(' +
    (NOBRACKET + r'(\[') * 6 +
    (NOBRACKET + r'\])*') * 6 +
    NOBRACKET + r')\]'
)
IMAGE_LINK_RE = r'\!' + BRK + r'\s*\(\s*(<.*?>|([^"\)\s]+\s*"[^"]*"|[^\)\s]*))\s*\)'
IMAGE_REFERENCE_RE = r'\!' + BRK + r'\s?\[([^\]]*)\]'

# is: linestart, any whitespace (even none), image, any whitespace (even none), line ends.
FIGURES = [u'^\s*' + IMAGE_LINK_RE + u'\s*$',
           u'^\s*' + IMAGE_REFERENCE_RE + u'\s*$']


# This is the core part of the extension
class OldFigureCaptionProcessor(BlockProcessor):
    FIGURES_RE = re.compile('|'.join(f for f in FIGURES))

    def test(self, parent, block):  # is the block relevant
        # If there is an image and the image is alone in the paragraph, and the image doesn't already have a figure parent, return True
        isImage = bool(self.FIGURES_RE.search(block))
        isOnlyOneLine = (len(block.splitlines()) == 1)
        isInFigure = (parent.tag == 'figure')

        # print(block, isImage, isOnlyOneLine, isInFigure, "T,T,F")
        if (isImage and isOnlyOneLine and not isInFigure):
            return True
        else:
            return False

    def run(self, parent, blocks):  # how to process the block?
        raw_block = blocks.pop(0)
        captionText = self.FIGURES_RE.search(raw_block).group(1)

        # create figure
        figure = etree.SubElement(parent, 'figure')

        # render image in figure
        figure.text = raw_block

        # create caption
        figcaptionElem = etree.SubElement(figure, 'figcaption')
        # no clue why the text itself turns out as html again and not raw. Anyhow, it suits me, the blockparsers annoyingly wrapped everything into <p>.
        figcaptionElem.text = captionText


class FigureCaptionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        """ Add an instance of FigcaptionProcessor to BlockParser. """
        md.parser.blockprocessors.register(OldFigureCaptionProcessor(md.parser), 'figureAltcaption', 200)
        # md.inlinePatterns.register(FigureCaptionProcessor(IMAGE_LINK_RE, md), 'figureAltcaption', 190)
        md.registerExtension(self)


def makeExtension(**kwargs):
    return FigureCaptionExtension(**kwargs)
