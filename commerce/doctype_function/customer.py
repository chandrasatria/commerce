
import frappe
from frappe import _
from frappe.model.document import Document

from commerce.helper import randomString,randomInt

from commerce.user_integration.controllers.verification_controller import create_verification_email


user_new_global = ""

def on_update(doc, method):
	if doc.get("sales_team"):
		update_shopping_cart_sales(doc)
	# User yang update customer
	# gender_update(doc)
	# if doc.mobile_no:
	# 	try:
	# 		if doc.name:
	# 			contact_doc = frappe.get_doc("Contact",doc.get("customer_primary_contact")) 
	# 			contact_doc.mobile_no = doc.mobile_no
	# 			contact_doc.phone_nos = []
	# 			contact_doc.append("phone_nos",{"phone" : doc.mobile_no , "is_primary_mobile_no" : 1})
	# 			contact_doc.save(ignore_permissions=True)
				
	# 			frappe.db.commit()
	# 			frappe.msgprint(contact_doc.name)
	# 	except:
	# 		pass

def before_insert(doc, method):
	# untuk generate random customer name kalo customer tidak isi
	generate_customer_name(doc)
	check_unique(doc)
	make_verified(doc)
	if doc.get("register_via") in ["Frappe","Google","Facebook","Apple"]:
		try:
			global user_new_global
			user_new_global = create_user(doc)
		except:
			# pass
			frappe.throw(_("Cannot create user, please pick another email/mobile no"))
	
	
	

def after_insert(doc,method):
	if doc.get("register_via") in ["Frappe","Google","Facebook","Apple"]:
		create_user_permission(doc, user_new_global)
		create_shopping_cart(doc,user_new_global)
	generate_customer_verification_email(doc)

# ====================== ENDLINE FRAPPE HOOKS ======================

def make_verified(doc):
	if doc.register_via and doc.register_via != "Frappe":
		doc.verification_email = 1

def generate_customer_verification_email(doc):
	if doc.email_id:
		d = create_verification_email(doc.email_id)
		if not d:
			frappe.log_error(frappe.get_traceback(),"Error: Customer cannot create verification email")
			frappe.throw(_("Something went wrong. Please try again in a few minutes"))


def gender_update(doc):
	if doc.gender and doc.email_id:
		doc_user = frappe.get_doc("User",doc.email_id)
		doc_user.gender = doc.gender
		doc_user.save(ignore_permissions=True)
		print(doc_user)
		frappe.db.commit()

def check_unique(doc):
	# ((( EMAIL )))
	if doc.email_id:
		exist_email = frappe.db.sql("""
			SELECT name
			FROM `tabCustomer`
			WHERE email_id LIKE '{email}'
			""".format(email = doc.email_id))
		if len(exist_email) > 0:
			frappe.throw("Email has been used\nTry to login or reset your password")
	if doc.mobile_no:
		exist_mobile_no = frappe.db.sql("""
			SELECT name
			FROM `tabCustomer`
			WHERE mobile_no LIKE '{mobile_no}'
			""".format(mobile_no = doc.mobile_no))
		if len(exist_mobile_no) > 0:
			frappe.throw("Mobile no has been used\nTry to login or reset your password")



def create_user(doc):
	# customer_password = get_password("Customer", doc.name, "password")
	customer_password = doc.get("password")
	customer_image = doc.get("image") if doc.get("image") != None else ""
	
	# ((( CREATE NEW USER )))

	payload = {
		"doctype" : "User",
		"enabled" : 1,
		"send_welcome_email" : 0,
		"email" : doc.email_id,
		"new_password" : customer_password,
		"first_name" : doc.customer_name,
		"role_profile_name" : "Customer",
		"user_image" : customer_image
		}
	if doc.get("mobile_no"):
		payload["mobile_no"]=doc.mobile_no
	if doc.get("username"):
		payload["username"] = doc.username
	
	user_new = frappe.get_doc(payload)
	user_new.save(ignore_permissions=True)
	frappe.db.commit()
	return user_new

def create_user_permission(doc,user):
	doc_user_permission = frappe.get_doc({
		"is_default": 0,
		"allow": "Customer",
		"for_value": doc.name,
		"apply_to_all_doctypes": 1,
		"doctype": "User Permission",
		"user": str(user.name)
	})
	doc_user_permission.save(ignore_permissions=True)
	frappe.db.commit()

def create_shopping_cart(doc, user):
	doc_shopping_cart = frappe.get_doc({
		"user" : user.name,
		"customer" : doc.name,
		"doctype" : "Shopping Cart"
	})
	doc_shopping_cart.save(ignore_permissions=True)
	frappe.db.commit()

def delete_user(doc):
	try:
		fga = frappe.get_all("User",fields="*",filters=[["email","=",doc.email_id]])
		if len(fga)>0:
			frappe.delete_doc("User", fga[0]["name"])
	except:
		pass


def delete_customer(doc):
	try:
		frappe.get_all("Customer",fields="*",filters=[["email","=",doc.email_id],["customer_name","=",doc.customer_name]])
		if len(fga)>0:
			frappe.delete_doc("Customer", fga[0]["name"])
	except:
		pass

def generate_customer_name(doc):
	# Ini ketika dia ada email, maka akan create customer name berdasarkan email + random
	if not doc.get("customer_name") and doc.get("email_id"):
		email_split = doc.email_id.split("@")
		if email_split[0]:
			doc.customer_name = "{}_{}".format(email_split[0],str(randomInt(3)))
	# Ini ketika dia gaad email which is impossible but just in case
	if not doc.get("customer_name"):
		while True:
			some_random_string = randomString(10)
			fga_cek = frappe.get_all("Customer", fields= "customer_name", filters=[["customer_name","=",some_random_string]])
			if len(fga_cek) == 0:
				break
		doc.customer_name = some_random_string

def update_shopping_cart_sales(doc):
	# print(doc.get("sales_team"))
	# print(doc.get("sales_team")[0])
	if doc.get("email_id"):
		if len(doc.get("sales_team")) > 0 :
			if not frappe.db.exists("Shopping Cart", {"user" : doc.get("email_id")}):
				create_shopping_cart(doc, doc.get("email_id"))
			
			doc_sc = frappe.get_doc("Shopping Cart",{"user" : doc.get("email_id")})
			doc_sc.sales_person = doc.get("sales_team")[0].get("sales_person")
			doc_sc.save(ignore_permissions=True)
	else:
		if len(doc.get("sales_team")) > 0 :
			frappe.msgprint("Warning. This Customer doesn't have email ID. Shopping Cart for sales team will not created.")