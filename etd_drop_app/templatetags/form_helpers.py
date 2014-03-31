from django import template

register = template.Library()

@register.inclusion_tag('partials/form_field.html')
def bootstrap_field(field, param1=''):
	"""Take a FormField and produce nice HTML for its label, input, etc."""
	value = ''
	if hasattr(field.form, 'cleaned_data'):
		value = field.form.cleaned_data.get(field.name, '')

	return {
		'field': field,
		'type': field.__class__.__name__,
		'value': value,
		'param1': param1,
		'widget': field.field.widget.__class__.__name__,
	}
