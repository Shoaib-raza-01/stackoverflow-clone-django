from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

# @register.filter()
# def extract_code_blocks(value):
#     code_blocks = []
#     lines = value.split('\n')
#     for line in lines:
#         if line.startswith('```'):
#             code_blocks.append('</div>' if code_blocks else '<div class="code-block">')
#         else:
#             code_blocks.append(f'{line}\n')

#     code_blocks.append('</div>' if code_blocks and code_blocks[-1].startswith('<div') else '')

#     return ''.join(code_blocks)
