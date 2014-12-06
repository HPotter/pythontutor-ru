import re

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


# TODO refactor all this shit
class CodeSampleProcessor(BlockProcessor):
    """
    Process code sample blocks:

    ````[lang]
    [code]
    ````
    [sample input]
    ````
    """
    RE = re.compile(r'^@@@@(?P<lang>[\w\-_]*?)\n(?P<code>.*?)@@@@\n(?P<input>.*?)@@@@$', re.DOTALL)  # TODO [at] looks weird

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)

        data = self.RE.match(block).groupdict()

        pre = etree.SubElement(parent, 'pre', {
            'class': '{0}-code'.format(data['lang']) if data['lang'] else 'code',
        })

        code = etree.SubElement(pre, 'code', {
            'class': 'source',
        })
        code.text = data['code']
        input = etree.SubElement(pre, 'code', {
            'class': 'input',
        })
        input.text = data['input']


class CodeSampleExtension(Extension):
    """
    Add code sample block support to Markdown
    """

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'codesample',
            CodeSampleProcessor(md.parser),
            '_begin'
        )


def makeExtension(*args, **kwargs):
    return CodeSampleExtension(*args, **kwargs)
