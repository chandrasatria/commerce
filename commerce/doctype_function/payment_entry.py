import frappe

def on_submit(doc, method):
   make_paid_invoice(doc)
   enqueue_calculate_add_sold(doc)

def make_paid_invoice(doc):
	if doc.references:
		if len(doc.references) > 0 :
			if doc.references[0].get("reference_doctype") == "Sales Invoice":
				sinv_doc = frappe.get_doc("Sales Invoice",doc.references[0].get("reference_name"))
				if sinv_doc.grand_total == doc.total_allocated_amount:
					print("ok")
					frappe.db.sql("UPDATE `tabSales Invoice` SET paid = 1 WHERE name = '{}'".format(doc.references[0].get("reference_name")))
					frappe.db.commit()

def enqueue_calculate_add_sold(doc):
	try:
		from frappe.utils.background_jobs import enqueue
		if doc.references:
			if len(doc.references) > 0 :
				if doc.references[0].get("reference_doctype") == "Sales Invoice":
					sinv_doc = frappe.get_doc("Sales Invoice",doc.references[0].get("reference_name"))
					for item in sinv_doc.items:
						enqueue("commerce.schedule.enqueue_add_sold", item_code=item.get("item_code"))
	except:
		pass

