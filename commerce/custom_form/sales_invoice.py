import frappe
# Sales Invoice
# mapped doc
@frappe.whitelist()
def create_form_delivery_tracking(source_name, target_doc=None):
	
	from frappe.model.mapper import get_mapped_doc
	doclist = get_mapped_doc("Sales Invoice", source_name, 	{
		"Sales Invoice": {
			"doctype": "Delivery Tracking"
		},
		
	}, target_doc)
	doclist.external_doctype = "Sales Invoice"
	fga_sinv = frappe.get_all("Sales Invoice",fields="*", filters=[["name","=",source_name]])
	if len(fga_sinv)>0:
		doclist.external_id =  fga_sinv[0]["name"]
	
	return doclist