from django import template
import HTMLParser
import urllib

register = template.Library()

@register.filter
def decode(value):
    """HTML decodes a string """
    h = HTMLParser.HTMLParser()
    return h.unescape(value)

@register.filter
def unquote(value):    
    return urllib.unquote(value)

@register.filter
def unquote_plus(value):    
    return urllib.unquote_plus(value)

@register.filter
def is_true(value):
	if value:
		return 'True'
	else:
		return 'False'