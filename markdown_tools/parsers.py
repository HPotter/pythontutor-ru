import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension

from .code_sample import CodeSampleExtension


lesson_parser = markdown.Markdown(
    extensions=[
        FencedCodeExtension(),
        TocExtension(marker='[never-put-this-marker-in-lesson]', anchorlink=1),
        CodeSampleExtension(),
    ]
)
