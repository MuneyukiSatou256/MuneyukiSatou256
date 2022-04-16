import html
from urllib import parse
from django import template
from django.shortcuts import resolve_url
from django.template.defaultfilters import stringfilter
from django.utils.html import *
from django.utils.safestring import mark_safe

register = template.Library()

#@register.simple_tagでタグとして認識する。
@register.simple_tag
def get_return_link(request):
    top_page = resolve_url('diary:list')
    referer = request.environ.get('HTTP_REFERER')
    
    if referer:
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc():
            return referer
        
    return top_page