import frappe
# from commerce.notification import send_notification_paid_payment,send_notification_expired_payment
from commerce.doctype_function.sales_invoice import return_stock_item

from api_integration.validation import error_format,success_format
from frappe import _

def on_update_after_submit(doc, method):
	try:
		sales_invoice = frappe.get_value(doc.external_doctype,doc.external_id,"sales_invoice")
		print(sales_invoice)
		# f = open("xinv.txt", "a")
		# f.write("docstatus="+doc.status+"\n"+"docname"+doc.name)
		# f.write("sinv="+sales_invoice)
		doc2 = frappe.get_doc("Xendit Invoice", {"name":doc.name})
		# f.write("docstatus2="+doc2.status+"\n")
		# f.close()
		# shopping_cart_invoice_name = frappe.get_value("Shopping Cart Invoice",{"sales_invoice":doc.external_id},"name")
		# doc_shopping_cart_invoice_name = frappe.get_doc("Shopping Cart Invoice", shopping_cart_invoice_name)
		if doc.status=="PAID":
			fg_payment_entry = frappe.get_all("Payment Entry",fields="*",filters=[["reference_no","=",doc.name]])
			if len(fg_payment_entry)==0:
				create_payment_entry(doc,sales_invoice)
				frappe.db.sql("UPDATE `tabSales Invoice` SET paid = 1 WHERE name = '{}'".format(sales_invoice))
				frappe.db.commit()
			# send_notification_paid_payment(doc.user)
		elif doc.status == "EXPIRED":
			frappe.db.sql("UPDATE `tabSales Invoice` SET status = 'Overdue', shipping_status = 'Payment Expired' WHERE name = '{}'".format(sales_invoice))
			frappe.db.commit()
			doc_sinv = frappe.get_doc("Sales Invoice",sales_invoice)
			return_stock_item(doc_sinv)
			# send_notification_expired_payment(doc.user)
	except:
		pass
	# except Exception as e:
	# 	import traceback
	# 	from commerce.tools.error import error
	# 	err_title = "Error Callback Xendit"
	# 	err_message = traceback.format_exc()
	# 	error(log_message=err_title, log_title=err_message, err_message=err_title, err_title=None, raise_exception=False)
	# 	return error_format(_("Maaf terjadi kesalahan"))

	
def create_payment_entry(doc,sales_invoice):
	from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
	doc_payment_entry = get_payment_entry(dt="Sales Invoice",dn=sales_invoice)
	doc_payment_entry.reference_no = doc.name
	doc_payment_entry.reference_date = frappe.utils.now()
	doc = frappe.get_doc(doc_payment_entry)
	doc.docstatus=1
	doc.save(ignore_permissions=True)
	frappe.db.commit()



def make_paid_invoice(cinv_name):
	# make it a paid and change workflow
	doc_ciputra_invoice = frappe.get_doc("Ciputra Invoice", cinv_name)
	doc_ciputra_invoice.paid_on = frappe.utils.now()
	doc_ciputra_invoice.save(ignore_permissions =True)
	frappe.db.commit()
	frappe.db.sql("UPDATE `tabCiputra Invoice` SET workflow_state = 'Paid',docstatus = 1 WHERE name = '{}'".format(cinv_name))
	frappe.db.commit()
	
	f = open("xinv.txt", "a")
	f.write("makepaidinv="+cinv_name+"\n")
	f.close()

