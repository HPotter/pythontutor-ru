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
    RE = re.compile(r'^@@@@(?P<executable>executable)?\n(?P<code>.*?)@@@@\n(?P<input>.*?)@@@@$', re.DOTALL)  # TODO [at] looks weird

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)

        data = self.RE.match(block).groupdict()

        # TODO fix copypaste from templates/includes/code.html
        lesson_code = etree.SubElement(parent, 'div', {
            'class': 'lesson_code',
            'data-executable': 'true' if 'executable' in data else 'false',
            'data-dataviz': 'true',
        })

        if 'executable' in data:
            input = etree.SubElement(lesson_code, 'pre', {
                'class': 'stdin',
                'style': 'display: none;',
            })
            input.text = data['input']

        code = etree.SubElement(lesson_code, 'pre', {
            'class': 'code',
        })
        code.text = data['code']


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
