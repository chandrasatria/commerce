
import frappe
from frappe import _
from frappe.model.document import Document

def validate(self, method):
	if not self.links and self.user:
		fga = frappe.get_all("Customer", fields ="name" ,filters =[["email_id","=",self.user]])
		if len(fga) >0:
			customer_name = fga[0]["name"]
		customer_name = ""
			# customer_name = frappe.get_value("Customer",{"email_id":self.user},"name")
		if customer_name:
			self.append("links",{
			"link_doctype": "Customer",
			"link_name": customer_name,
			"link_title": customer_name
			})
			print(str(self.links))

def before_save(self, method):
	change_value_recipient(self)
	make_other_default_zero(self)

def before_insert(self, method):
	if not self.user:
		self.user = frappe.session.user
	default_address_first_time(self)

# --------------------------------------------

# def get_parent_delivery(delivery_territory):
# 	parrent_territory = frappe.get_value("Territory",delivery_territory,"parent_territory")
# 	return parrent_territory

# def get_parent_delivery_address(self):
# 	if not self.district_delivery and self.subdistrict_delivery:
# 		self.district_delivery = get_parent_delivery(self.subdistrict_delivery)
# 	if not self.city_delivery and self.district_delivery:
# 		self.city_delivery = get_parent_delivery(self.district_delivery)
# 	if not self.province_delivery and self.city_delivery:
# 		self.province_delivery = get_parent_delivery(self.city_delivery)


def change_value_recipient(self):
	if not self.recipient_name and self.user:
		user_full_name = frappe.get_value("User", self.user, "full_name")
		self.recipient_name = user_full_name
	elif not self.recipient_name:
		self.recipient_name = "-"

def make_other_default_zero(self):
	if self.is_default == 1:
		frappe.db.sql("UPDATE `tabAddress` SET is_default = 0 WHERE name != '{}' AND user = '{}' ".format(self.name,self.user))
		frappe.db.commit()

def default_address_first_time(self):
	if self.is_default == 0:
		select_sql = frappe.db.sql("SELECT * FROM `tabAddress` WHERE user = '{}' ".format(self.user))
		if len(select_sql) == 0:
			self.is_default = 1


# --------- for js fetch ------------


@frappe.whitelist(allow_guest=True)
def fetch_detail_jne(jne_destination):
	fga = frappe.get_all("JNE Destination", fields="*" , filters = [["name","=",jne_destination]])
	if len(fga) > 0:
		return {"data" : fga[0]}
	else:
		return {"data" : ""}


@frappe.whitelist(allow_guest=True)
def fetch_customer(customer):
	fga = frappe.get_all("Customer", fields="*" , filters = [["name","=",customer]])
	if len(fga) > 0:
		return {"data" : fga[0]}
	else:
		return {"data" : ""}


