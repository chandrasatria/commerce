import frappe
import sys
from frappe import _

from api_integration.validation import success_format, error_format

def get_customer(user):
	cust = frappe.get_value("Customer",{"email_id" : ("=",user)}, "name")
	return cust

@frappe.whitelist(allow_guest = False)
def claim_promo(voucher):
	""" ini untuk claim promo mandiri, jadi doctype Voucher -> My Voucher """
	try:
		from commerce.voucher.doctype.voucher.voucher import claim_voucher,check_quantity,check_voucher_claim_type
		
		user = frappe.session.user
		customer = get_customer(user)
		response_check_voucher_claim_type = check_voucher_claim_type(voucher, "My Voucher")
		print(response_check_voucher_claim_type)
		if response_check_voucher_claim_type.get("status") == 0 :
			return error_format(_("Sorry, you can't claim this voucher."))
		response_check_quantity = check_quantity(voucher, customer, for_claim_voucher = 1)
		if response_check_quantity.get("status") == 0 :
			return error_format(_(response_check_quantity.get("keterangan")))
		claim_voucher_response = claim_voucher(voucher = voucher, customer = customer)
		return success_format(claim_voucher_response)
	except:
		return error_format(sys.exc_info()[0])

# NOTE get_promo ini punya commerce(wss), karena ada ketambahan customer_group
@frappe.whitelist(allow_guest=False)
def get_promo(search='', customer_group = "", page=0, limit_page=20):
	try:
		today = frappe.utils.now()
		voucher_list = frappe.db.sql("""SELECT 
		tv.name,tv.voucher_type,tv.voucher_id, tv.voucher_title, tv.voucher_order, tv.voucher_image, tv.voucher_code, tv.voucher_type, tv.description_term_and_condition, tv.how_to_use, tv.max_amt, tv.min_amt, tv.start_date, tv.start_time, tv.publish_start_date,tv.end_date,tv.end_time,tv.publish_end_date,qr_code, tv.barcode,tv.publish_end_date
		FROM `tabVoucher` tv LEFT JOIN `tabVoucher Customer Group` tvcg ON tvcg.parent  = tv.name
		WHERE tv.voucher_claim_type = 'Promo Voucher' AND
		tv.publish_start_date <= '{today}' AND
		tv.publish_end_date >= '{today}' AND
		(tv.voucher_title LIKE %(search)s OR tv.voucher_code LIKE %(search)s) AND
		((tv.voucher_type = "All") OR (tv.voucher_type = "Customer Groups" AND tvcg.customer_group = %(customer_group)s))
		GROUP BY tv.name
		ORDER BY tv.voucher_order ASC
		LIMIT %(limit_page)s
		OFFSET %(page)s	
		 """.format(today=today)
		 ,{"search" : "%"+search+"%", "customer_group" : customer_group
		 ,"limit_page" : limit_page, "page":page}
		 ,as_dict=True)
		
		return success_format(voucher_list)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: api voucher get_promo")
		return error_format(sys.exc_info()[0])

@frappe.whitelist(allow_guest=False)
def get_promo_with_my_voucher(search='%', page=0, limit_page=20):
	try:
		today = frappe.utils.now()
		user = frappe.session.user
		customer = get_customer(user)
		voucher_list = frappe.db.sql("""SELECT 
		name,voucher_id, voucher_title, voucher_order, voucher_image, voucher_code, voucher_type, 
		description_term_and_condition, how_to_use, max_amt, min_amt, start_date, start_time, 
		publish_start_date,end_date,end_time,publish_end_date, publish_end_date, 
		voucher_left, voucher_claimed
		FROM `tabVoucher` 
		WHERE
		publish_end_date >= CAST('{today}' AS DATE) AND
		publish_start_date <= CAST('{today}' AS DATE) AND
		voucher_title LIKE %(search)s AND
		voucher_claim_type = "My Voucher"
		 """.format(today=today),{
			 "search" : search
		 },as_dict=True)
		for item in voucher_list:
			item["my_voucher"] = []
			fgl_my_voucher = frappe.get_list("My Voucher", fields = "*" , filters = [["voucher","=",item["name"]],["customer","=",customer]] , order_by="creation ASC")
			if len(fgl_my_voucher) > 0:
				item["my_voucher"] = fgl_my_voucher

		return success_format(voucher_list)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: api voucher get_promo_with_my_voucher")
		return error_format(sys.exc_info()[0])

def check_validation(start_date,end_date,voucher_left):
	today = frappe.utils.now()
	valid = 1
	if start_date > today:
		valid = 0
	if end_date < today:
		valid =0
	if voucher_left <1:
		valid = 0