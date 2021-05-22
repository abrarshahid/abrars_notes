from django import template

register = template.Library()
@register.filter(name="extract_dict")
def extract_dict(dict,key):
	return dict.get(key)
