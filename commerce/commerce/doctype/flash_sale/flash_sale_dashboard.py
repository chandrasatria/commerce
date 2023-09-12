from frappe import _

def get_data():
	return {
		'fieldname': 'flash_sale',
		'transactions': [
			{
				'label': _('Item'),
				'items': ['Item']
			},
		]
	}