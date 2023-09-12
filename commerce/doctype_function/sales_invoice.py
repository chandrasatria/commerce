import frappe
from frappe import _
from frappe.model.document import Document

from commerce.helper import randomString
# from commerce.notification import send_notification_shipping,send_notification_cancelled,send_notification_packaged,send_notification_completed
# sinv_status = ""


def validate(self, method):
	
	if self.customer:
		val = frappe.get_value("Customer",self.customer, "email_id")
		if frappe.db.exists("User", val):
			self.user = val

	add_status_tracking(self)
	create_qr_code(self)
	# alert_customer(self)

def after_insert(self,method):
	from frappe.utils.background_jobs import enqueue
	for item in self.items:
		enqueue("commerce.schedule.enqueue_add_sold", item_code=item.get("item_code"))
	
	
#     global sinv_status
#     sinv_sql = frappe.db.sql("SELECT status FROM `tabSales Invoice` WHERE name = '{}' ".format(self.name),as_dict=True)
#     if len(sinv_sql)>0:
#         sinv_status = sinv_sql[0]["status"]
#     # frappe.msgprint(str(sinv_sql[0]["status"]))

def on_update(self, method):
	self.reload()
	pass
#     frappe.msgprint(self.status)
#     frappe.msgprint(sinv_status)
#     if self.status == "Unpaid" and sinv_status == "Draft":
#         frappe.msgprint("creating inv")
#         email_id = frappe.get_value("Customer",self.customer,"email_id")
#         if email_id:
#             frappe.session.user = email_id
#         create_xendit_invoice(self)
#         xendit_invoice_url=frappe.get_value("Xendit Invoice",{"external_id":self.name,"external_doctype" : "Sales Invoice"},"invoice_url")
#         if xendit_invoice_url:
#             frappe.db.sql("UPDATE `tabSales Invoice` SET xendit_invoice_url = '{}' WHERE name = '{}' ".format(xendit_invoice_url, self.name))
#             frappe.db.commit()
#             self.xendit_invoice_url = xendit_invoice_url
#             self.reload()



def before_update_after_submit(self,method):
	validation_status(self)
	if self.shipping_status == "Cancelled":
		# send_notification_cancelled(self.user)
		pass
	if self.shipping_status == "Packaged":
		packaged_validation(self)
		add_status_tracking(self)
		# NOTE ini auto shipped >> pake API JNE
		# if self.courier == "JNE":
		# 	make_auto_shipped(self)
		# send_notification_packaged(self.user)
	if self.shipping_status == "Shipped":
		packaged_validation(self)
		shipped_validation(self)
		add_status_tracking(self)
		# send_notification_cancelled(self.user)
	if self.shipping_status == "Completed":
		self.confirmed_at = frappe.utils.now()
		# send_notification_completed(self.user)
		add_status_tracking(self)
		
	create_qr_code(self)
	add_status_tracking(self)
		
	# frappe.msgprint(self.shipping_status)
	# get_xendit_url_from_shopping_cart_invoice(self)


def before_cancel(self,method):
	# frappe.msgprint("cancelled")
	if self.name:
		fga_sci = frappe.get_all("Shopping Cart Invoice",filters=[["sales_invoice","=",self.name]],fields="*")
		for item in fga_sci:
			cancel_xendit_invoice(item["name"])
			force_cancel_shopping_cart_invoice(item["name"])

def on_trash(self,method):
	if self.name:
		fga_sci = frappe.get_all("Shopping Cart Invoice",filters=[["sales_invoice","=",self.name]],fields="*")
		for item in fga_sci:
			try:
				cancel_xendit_invoice(item["name"])
				force_delete_cancel_shopping_cart_invoice(item["name"])
				
			
			except:
				frappe.msgprint("Sorry can't delete Shopping Cart Invoice:{} <br> Please contact administrator.".format(item["name"]))
		


# def create_xendit_invoice(self):
#     from xendit.invoice import create_invoice
#     if self.payment_method:
#         payment_method = [self.payment_method]
#     else:
#         payment_method =[]
#     try:
#         create_invoice(self.grand_total,"Sales Invoice",self.name,"test",payment_methods=payment_method)
#     except:
#         frappe.throw("Xendit Payment failed.")

# def make_description_item(self):
#     string_description = "Pembelian: "
#     for item in self.ciputra_invoice_item:
#         if item.get("item_name"):
#             string_description+= item.get("item_name") + ","
#     string_description[:-1]
#     return string_description

# ------------- end of hooks
	
def cancel_xendit_invoice(shopping_cart_invoice):
	try:
		fga_xendit_invoice = frappe.get_all("Xendit Invoice",filters=[["external_id","=",shopping_cart_invoice]],fields="name")
		for item in fga_xendit_invoice:
			doc_xi = frappe.get_doc("Xendit Invoice",item["name"])
			doc_xi.cancel()
			frappe.db.commit()
	except:
		pass

def force_cancel_shopping_cart_invoice(shopping_cart_invoice):
	frappe.db.sql("""UPDATE `tabShopping Cart Invoice` SET docstatus = 2 WHERE name = %(shopping_cart_invoice)s """,{
		"shopping_cart_invoice" : shopping_cart_invoice
	})
	frappe.db.commit()

def force_delete_cancel_shopping_cart_invoice(shopping_cart_invoice):
	frappe.db.sql("""UPDATE `tabShopping Cart Invoice` SET sales_invoice = '',docstatus = 2 WHERE name = %(shopping_cart_invoice)s """,{
		"shopping_cart_invoice" : shopping_cart_invoice
	})
	frappe.db.commit()
	# ddoc = frappe.delete_doc("Shopping Cart Invoice", item["name"])
	# frappe.db.commit()
	# Ini karena kalo pake frappe.delete_doc ada error ga bisa lgsg delete
	frappe.db.sql("""DELETE FROM `tabShopping Cart Invoice` WHERE name = %(shopping_cart_invoice)s """,{
		"shopping_cart_invoice" : shopping_cart_invoice
	})
	frappe.db.commit()


def alert_customer(self):
	try:
		if self.shipping_status == "Cancelled" or self.shipping_status == "Request Return":
			doc = frappe.get_doc("Sales Invoice", self.name)
			if doc.shipping_status != "Cancelled" or self.shipping_status == "Request Return":
				frappe.msgprint("Don't forget to create Return/Credit Note", title="{} Notice".format(doc.shipping_status), indicator="orange")
	except:
		pass


def validation_status(self):
	if self.shipping_status and self.status_tracking:
		workflow_internal = [{"from": "Pending", "to" : "Packaged" },
		{"from": "Pending", "to" : "Cancelled" },
		{"from": "Pending", "to" : "Payment Expired"},
		{"from": "Packaged", "to" : "Payment Expired" },
		{"from": "Packaged", "to" : "Shipped"},
		{"from": "Shipped", "to" : "Completed" },
		{"from": "Shipped", "to" : "Request Return"}]
		array_split = self.status_tracking.split(":::")
		last_status = array_split[-1]
		if not last_status:
			last_status = array_split[-2]
		for item in workflow_internal:
			if self.shipping_status == item["to"] and (last_status != item["from"] and last_status != item["to"]):
				frappe.throw(_("Workflow Error"))
		

# def make_auto_shipped(self):
# 	from logistics_integration.jne_integration.api.create_airwaybill import create_awb,get_info_awb_from_address,get_info_awb_from_sinv
# 	if not self.delivery_receipt:
# 		if self.customer_address and self.name:
# 			olshop_receiver = get_info_awb_from_address(self.customer_address)
# 			olshop_invoice = get_info_awb_from_sinv(self.name)
# 			awb_jne = create_awb(
# 				OLSHOP_ORDERID = olshop_invoice["olshop_orderid"],
# 				olshop_receiver_dict = olshop_receiver["olshop_receiver"],
# 				OLSHOP_QTY = olshop_invoice["olshop_qty"],
# 				OLSHOP_WEIGHT = olshop_invoice["olshop_weight"],
# 				OLSHOP_GOODSDESC = "aksesories motor",
# 				OLSHOP_GOODSVALUE = olshop_invoice["olshop_goodsvalue"],
# 				OLSHOP_GOODSTYPE = 2,
# 				OLSHOP_SERVICE = olshop_invoice["olshop_service"],
# 				OLSHOP_DEST = olshop_receiver["olshop_dest"],
# 				OLSHOP_INST = "Jangan Dibanting"
# 				)
# 			if awb_jne:
# 				print(awb_jne)
# 				# frappe.msgprint(str(awb_jne))
# 				try:
# 					frappe.msgprint("Sukses, cnote: "+awb_jne.get("data").get("detail")[0].get("cnote_no"))
# 				except:
# 					frappe.msgprint("Maaf terjadi kesalahan pada JNE.")
# 					frappe.msgprint(str(awb_jne))
# 				# {'status': 200, 'result': {'error': 'Cnote No. Not Found.', 'status': False}}
# 				self.delivery_receipt = awb_jne.get("data").get("detail")[0].get("cnote_no")
# 				self.shipping_status = "Shipped"

# 		frappe.db.commit()


	

def add_status_tracking(self):
	if not self.status_tracking:
		self.status_tracking = ""
	if self.shipping_status not in self.status_tracking:
		self.status_tracking += self.shipping_status +":::"

def packaged_validation(self):
	if self.paid == 0 and self.use_cod == 0:
		frappe.throw("Customer must pay first.")

def shipped_validation(self):
	if not self.delivery_receipt:
		frappe.throw("Oops, you must input delivery receipt.")
	self.shipped_at = frappe.utils.now()
	

def get_xendit_url_from_shopping_cart_invoice(self):
	if self.shopping_cart_invoice:
		sci_xiu = frappe.get_value("Shopping Cart Invoice", self.shopping_cart_invoice, "xendit_invoice_url")
		if sci_xiu:
			frappe.db.sql("UPDATE `tabSales Invoice` SET xendit_invoice_url = '{}' WHERE name = '{}' ".format(sci_xiu,self.name))
			frappe.db.commit()
			self.xendit_invoice_url = sci_xiu
			self.reload()

def return_stock_item(self):
	# Ambil default warehouse
	doc_stock_settings = frappe.get_single("Stock Settings")
	default_warehouse = ""
	if doc_stock_settings.get("default_warehouse"):
		default_warehouse = doc_stock_settings.get("default_warehouse")

	default_company = ""
	default_company = frappe.get_value("Global Defaults","Global Defaults","default_company")

	# Masukkan item ke items
	item_to_add = []
	for item in self.items:
		item_to_add.append({
			"t_warehouse" : default_warehouse,
			"item_code" : item.get("item_code"),
			"qty" : item.get("qty"),
			"doctype" : "Stock Entry Detail"
		})

	doc_stock_entry = frappe.get_doc({
    "title": "Material Receipt",
    "naming_series": "MAT-STE-.YYYY.-",
    "stock_entry_type": "Material Receipt",
    "purpose": "Material Receipt",
    "company": default_company,
    "set_posting_time": 0,
    "inspection_required": 0,
    "from_bom": 0,
    "fg_completed_qty": 0,
    "use_multi_level_bom": 1,
    "total_incoming_value": 0,
    "total_outgoing_value": 0,
    "value_difference": 0,
    "total_additional_costs": 0,
    "is_opening": "No",
    "per_transferred": 0,
    "total_amount": 0,
	"items" : item_to_add,
    "doctype": "Stock Entry",
	})
	
	doc_stock_entry.insert()
	doc_stock_entry.docstatus = 1
	doc_stock_entry.save(ignore_permissions=True)
	frappe.db.commit()

def create_qr_code(self):
	from commerce.helper import generate_barcode
	try:
		if self.name and not self.sales_invoice_barcode:
			generate_barcode("Sales Invoice", self.name, self.name, qr = 0, bar =1 , field_bar = "sales_invoice_barcode")
	except:
		pass
	try:
		if self.delivery_receipt and not self.delivery_receipt_barcode:
			generate_barcode("Sales Invoice", self.name, self.delivery_receipt, qr = 0, bar =1 , field_bar = "delivery_receipt_barcode")
	except:
		pass
		
	
