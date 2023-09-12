import frappe
from frappe import _
import sys
import json

def success_format(doc, code=200):
	try:
		from api_integration.validation import success_format
		return success_format(doc)
	except:
		data = dict()

		data['code'] = code
		data['data'] = doc
		return data

# def error_format(exceptions, code = 500, err_text="", indicator = 'red'):
# 	data = dict()

# 	if err_text != "":
# 		data['error'] = err_text
# 		data['error_type'] = 'ValidationError'
# 	elif len(exceptions) > 1:
# 		data['error'] = str(exceptions[1])
# 		data['error_type'] = type(exceptions[1]).__name__

# 	if len(exceptions) > 0:
# 		data['code'] = exceptions[0].http_status_code
# 	else:
# 		data['code'] = code
# 	data['indicator'] = indicator


# 	return data

def error_format(exceptions, code = 500, err_text="", indicator = 'red'):
	try:
		from api_integration.validation import error_format
		return error_format(exceptions, code = code, err_text=err_text, indicator = indicator)
	except:
		data = dict()

		if err_text != "":
			data['error'] = err_text
			data['error_type'] = 'ValidationError'
		elif exceptions[0] != None and exceptions[1] != None and exceptions[2] != None:
			if type(exceptions) == str:
				data['error'] = exceptions
				data['error_type'] = 'ValidationError'
			else:
				data['error'] = str(exceptions[1])
				data['error_type'] = type(exceptions[1]).__name__
		else:
			# ((( NGASAL DULU )))
			data['error'] = 'ValidationError'
			data['error_type'] = 'ValidationError'

		if exceptions[0] != None and exceptions[1] != None and exceptions[2] != None:
			if type(exceptions) == str:
				data['code'] = code
			else:
				data['code'] = exceptions[0].http_status_code
		else:
			data['code'] = code
		data['indicator'] = indicator
		return data

@frappe.whitelist(allow_guest=False)
def test_error_not_permitted():
	try:
		frappe.set_user('chael147@gmail.com')
		frappe.get_list('Doctype')
		frappe.response = {}
	except:
		return error_format(sys.exc_info())

@frappe.whitelist(allow_guest=False)
def test_error_not_found():
	try:
		frappe.set_user('chael147@gmail.com')
		frappe.get_doc('Customer','c')
		frappe.response = {}
	except:
		return error_format(sys.exc_info())

@frappe.whitelist(allow_guest=False)
def test_error_validation():
	try:
		frappe.throw(_('This is error'))
		frappe.response = {}
	except:
		return error_format(sys.exc_info())


# def error_format(err, code = 500):
# 	data = dict()
# 	err = str(err).replace("ValidationError(u'","").replace("',)","").replace('ValidationError(u"','",)')
	
# 	data['error'] = err
# 	if type(err) == frappe.exceptions.AuthenticationError:
# 		data['code'] = 440
# 	elif type(err) == frappe.exceptions.ValidationError:
# 		data['code'] = 417
# 	elif type(err) == frappe.exceptions.DoesNotExistError:
# 		data['code'] = 404
# 	elif type(err) == frappe.exceptions.PermissionError:
# 		data['code'] = 403
# 	elif type(err) == frappe.exceptions.MandatoryError:
# 		data['code'] = 400
# 	else:
# 		data['code'] = code
# 	return data

def translate_error(some_error_string):
	list_translate = ["Could not find Row"]
	for item in list_translate:
		if str(some_error_string) in item:
			some_error_string = some_error_string.replace(item,(_(item)))
	return some_error_string