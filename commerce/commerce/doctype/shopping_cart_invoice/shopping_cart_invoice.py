# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import json


class ShoppingCartInvoice(Document):
	def validate(self):
		self.validate_item()

	def before_save(self):
		if self.voucher:
			self.voucher_check_rule()
		if not self.voucher:
			self.total_discount = 0
		self.make_to_float()
		self.fill_default_value()
		self.posting_date = frappe.utils.now()
		self.calculate_price()
		self.calculate_weight()
		self.pay_later_check()
		
	def on_update(self):
		self.calculate_voucher_discount()
		self.calculate_shipment_fee()
		self.calculate_payment_fee()
		self.calculate_grand_total()
		self.reload()

	def before_submit(self):
		# Pastikan payment method, alamat, dan shipment choice
		self.payment_method_and_shipment()
		self.check_qty()
		self.last_check_flash_sale()
		self.validate_submit()

	def on_submit(self):
		# Pengecekan pada on update 
		if self.voucher:
			self.shopping_cart_invoice_claim_voucher()
		self.submit_function()
		self.clear_shopping_cart()

	def on_trash(self):
		self.sales_invoice = ""
		self.reload()
		

	def before_insert(self):
		self.check_qty(with_change_qty=1)
		self.get_first_sales_user()
		
# ------ end of hooks -----

# SECTION VALIDATE

	def validate_item(self):
		if not self.items:
			frappe.throw(_("Item must be filled."))
		if len(self.items) <= 0:
			frappe.throw(_("Item must be filled."))

	def payment_method_and_shipment(self):
		if not self.address:
			frappe.throw(_("Please select address first."))
		if not self.courier and not self.courier_service:
			frappe.throw(_("Please select shipment first."))
		if not self.payment_method:
			frappe.throw(_("Please select payment method first."))
		
# SECTION before_insert
	def check_qty(self, with_change_qty = 0):
		from commerce.commerce.doctype.flash_sale.flash_sale import check_flash_sale,calculate_discount_flash_sale_price,check_qty_flash_sale
		from api_integration.api_integration.doctype.api_request.api_request import master_get_item_details
		for item in self.items:
			item_detail = master_get_item_details(warehouse="", price_list="",customer=self.customer, company=self.company, transaction_date=frappe.utils.now(),item = item.get("item_code"))
		
			if item_detail["item_detail"]["actual_qty"] < float(item.get("qty")):
				item_name = frappe.get_value("Item",item.get("item_code"), "item_name")
				frappe.throw("Oops this item {} quantity is not sufficient.".format(item_name))

	# Untuk mengambil sales user dari Customer
	def get_first_sales_user(self):
		if self.user:
			fga_customer = frappe.get_all("Customer",fields="name",filters=[["email_id","=",self.user]])
			if len(fga_customer)>0:
				doc_customer = frappe.get_doc("Customer", fga_customer[0]["name"])
				sales_team = doc_customer.get("sales_team")
				if sales_team > 0:
					self.sales_person = doc_customer.get("sales_team")[0].get("sales_person")


# !SECTION before_insert

# SECTION before_save
	def make_to_float(self):
		if self.total:
			self.total = float(self.total)
		if self.total_discount :
			self.total_discount = float(self.total_discount)
		if self.shipping_fee :
			self.shipping_fee = float(self.shipping_fee)
		if self.payment_fee :
			self.payment_fee = float(self.payment_fee)
		if self.grand_total :
			self.grand_total = float(self.grand_total)


	def fill_default_value(self):
		if not self.get("user"):
			self.user = frappe.session.user
		if not self.get("customer"):
			customer_name = frappe.get_value("Customer",{"email_id" : frappe.session.user},"name")
			self.customer = customer_name
		if not self.get("address"):
			address_default = frappe.get_value("Address",{"is_default":1,"user" : self.user,"enabled":1},"name")
			if address_default:
				fga_address = frappe.get_all("Address",fields="*", filters=[["name","=",address_default]])
				if len(fga_address) >0:
					self.address_title = fga_address[0]["address_title"]
					self.address_line1 = fga_address[0]["address_line1"]
					self.city = fga_address[0]["city"]
					self.pincode = fga_address[0]["pincode"]
					self.is_default = fga_address[0]["is_default"]
					self.recipient_name = fga_address[0]["recipient_name"]
					self.phone = fga_address[0]["phone"]
					self.address = address_default
				

	def calculate_weight(self):
		import math
		
		total_weight = 0.0
		for item in self.items:
			if not item.get("conversion_uom"):
				item.conversion_factor = 1
			if not item.get("qty"):
				item.qty = 1

			weight_item,weight_item_uom = frappe.get_value("Item",item.item_code,["weight_per_unit","weight_uom"])
			if weight_item and weight_item_uom:
				if weight_item_uom == "Gram":
					total_weight += ((float(weight_item))*float(item.qty)*float(item.get("conversion_uom")))
				elif weight_item_uom == "Kilogram":
					total_weight += (float(weight_item)*1000.0*int(item.qty)*float(item.get("conversion_uom")))
		if total_weight:
			total_weight = total_weight/1000
			self.total_weight = total_weight
			self.weight_uom = "Kilogram"
			self.rounded_weight = math.ceil(float(total_weight))
		elif not total_weight:
			self.total_weight = 1
			self.rounded_weight = 1
			self.weight_uom = "Kilogram"




	def calculate_price(self):
		from commerce.commerce.doctype.flash_sale.flash_sale import check_flash_sale,calculate_discount_flash_sale_price,check_qty_flash_sale,check_rule_flash_sale_maximum,check_rule_flash_sale
		from api_integration.api_integration.doctype.api_request.api_request import master_get_item_details
		total_price = 0.0
		total_qty = float(0)
		# NOTE ini yang pake pricing rule
		
		# for item in self.items:
			
		# 	item.price = item_detail["item_detail"]["price_list_rate"]
		# 	if not item.get("margin"):
		# 		item.margin = 0.0
		# 	item.total = (item.price*float(item.qty))
		# 	if item_detail["item_detail"].get("margin_type") == "Amount" : 
		# 		item.margin = item_detail["item_detail"]["margin_rate_or_amount"]
		# 	if item_detail["item_detail"].get("margin_type") == "Percentage":
		# 		item.margin = item_detail["item_detail"]["margin_rate_or_amount"] * item.total
		# 	item.total = item.total+(item.margin *float(item.qty))
		# 	total_price += item.total
		# 	total_qty += float(item.qty)
		
		# Pake flash sale
		list_item = []
		for item in self.items:
			if item.get("item_code"):
				list_item.append(item.get("item_code"))

		item_sql_list = frappe.db.sql(""" SELECT * FROM `tabItem` WHERE name IN %(list_item)s """,{"list_item":list_item})
		

		all_flash_sale = []
		qty_x_flash_sale = {}
		for item in self.items:
			item_detail = master_get_item_details(warehouse="", price_list=self.get("price_list"),customer=self.customer, company=self.company, transaction_date=frappe.utils.now(),item = item.get("item_code"),uom=item.get("uom"))
			item.margin = 0.0
			item_flash_sale = frappe.get_value("Item",item.get("item_code"),"flash_sale")
			item.price = item_detail["item_detail"]["price_list_rate"] or 0.0
			if item_flash_sale:
				print(item.get("item_code"))
				print(item_flash_sale)
				print(item.get("qty"))
				# Check Flash Sale
				if check_flash_sale(item.get("item_code"),item_flash_sale):
					if check_qty_flash_sale(item.get("item_code"),float(item.get("qty"))):
						# Assign Rule Flash Sale Maximum
						if item_flash_sale:
							if item_flash_sale not in all_flash_sale:
								all_flash_sale.append(item_flash_sale)
								qty_x_flash_sale[item_flash_sale] = 0
							
							qty_x_flash_sale[item_flash_sale] += int(item.get("qty"))

						item.margin = calculate_discount_flash_sale_price(item.price,item_flash_sale)
						item.flash_sale = item_flash_sale

					else:
						frappe.throw(_("Quantity exceed the Flash Sale quantity."))
				
			item.total = (item.price *float(item.qty)) - (item.margin*float(item.qty))
			total_price += item.total
			total_qty += float(item.qty)
		
		self.total = total_price
		self.total_qty = total_qty

		print("qtyxflashsale--------------")
		print(qty_x_flash_sale)
		# Check Rule Flash Sale
		for item in all_flash_sale:
			if item:
				checking_rule_flash_sale = check_rule_flash_sale_maximum(item,self.get("customer"),qty_x_flash_sale[item])
				if checking_rule_flash_sale.get("status") == 0:
					frappe.throw(_("{}".format(checking_rule_flash_sale.get("keterangan"))))

		# Check platform Flash Sale
		for item in self.items:
			if item.get("flash_sale"):
				check_rfs = check_rule_flash_sale(item.get("flash_sale"), self.platform)
				if check_rfs.get("status") == 0:
					frappe.throw(_("{}".format(check_rfs.get("keterangan"))))

	def pay_later_check(self):
		if self.payment_method == "COD":
			self.pay_later = 1
		else:
			self.pay_later = 0
# !SECTION before_save

# SECTION on_update
	def calculate_shipment_fee(self):
		from delivery_integration.api.delivery import get_delivery

		if self.address and self.delivery_area:
			doc_delivery_area = frappe.get_doc("Delivery Area",self.address)
		
		
		# # TODO
		# from logistics_integration.api import get_all_tariff
		# if self.address and self.courier and self.service:
		# 	fga_address = frappe.get_all("Address",fields="*", filters=[["name","=",self.address]])
		# 	if len(fga_address) > 0:
		# 		if self.courier == "JNE":
		# 			try:
		# 				weight_tariff = 1 if self.rounded_weight == 0 else self.rounded_weight
		# 				item_tarif = get_all_tariff(address = fga_address[0]["name"],weight =weight_tariff)
		# 				for item in item_tarif["data"]["JNE"]:
		# 					if item["service_code"] == self.service:
													
		# 						self.shipping_fee = float(item["price"])
		# 						frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET shipping_fee = {} WHERE name = '{}' ".format(self.shipping_fee,self.name))
		# 						# frappe.msgprint(str(self.shipping_fee))
		# 						# frappe.msgprint(str(item["price"]))
		# 			except:
		# 				pass
		# 		else:
		# 			pass
		# 	else:
		# 		frappe.throw(_("Address not found."))
		# else:
		# 	self.shipping_fee = 0
		# 	frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET shipping_fee = {} WHERE name = '{}' ".format(self.shipping_fee,self.name))
			
	def calculate_payment_method(self):
		# TODO
		from xendit.payment_methods import get_all_payment_method
		if self.payment_method and self.total:
			result = get_all_payment_method(self.total)
			for item in result["data"]:
				if item["payment_method_value"] == self.payment_method:
					self.payment_fee = item["fee_amount"]
					frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET payment_fee = {} WHERE name = '{}' ".format(self.payment_fee,self.name))
					break
# !SECTION on_update
		
	# SUBSECTION Module Voucher
	def calculate_voucher_discount(self,no_update = 0):
		total_discount = 0.0
		if self.voucher:
			doc_voucher = frappe.get_doc("Voucher", self.voucher)
			if doc_voucher.based_on == "All Item":
				irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item WHERE sc_item.parent = '{sc_name}' ".format(sc_name = self.name),as_dict=True)
				print(irisan_item)
			if doc_voucher.based_on == "Item":
				irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Based Child` v_item ON v_item.item = sc_item.item_code WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
				print(irisan_item)
			if doc_voucher.based_on == "Item Group":
				irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Group Based Child` v_item ON v_item.item_group = sc_item.item_group WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
			if doc_voucher.based_on == "Brand":
				irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Brand Based Child` v_item ON v_item.brand = sc_item.brand WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
			if irisan_item:
				# Kalo mo tambah coret harga disini
				#  tambah field -> masukkan ke field itu setiap iterasi
				for item in irisan_item:
					print(item)
					diskon = 0
					
					if (doc_voucher.get("discount_type")=="Discount Percentage"):
						diskon = (item["total"] * doc_voucher.get("discount_percentage")/100)
						total_discount += diskon

				if (doc_voucher.get("discount_type")=="Discount Amount"):
						total_discount = (doc_voucher.get("discount_amount"))
				
			if doc_voucher.get("maximal_discount"):
				if doc_voucher.maximal_discount != 0:
					if total_discount > doc_voucher.maximal_discount:
						total_discount = doc_voucher.maximal_discount

			if no_update == 0:
				self.total_discount = total_discount
			
				frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET total_discount = {} WHERE name = '{}' ".format(self.total_discount,self.name))
				frappe.db.commit()
				print(total_discount)
			else:
				return total_discount
	
	def calculate_payment_fee(self):
		total_payment_fee = 0.0
		from xendit.xendit.doctype.xendit_payment_methods.xendit_payment_methods import calculate
		
		if self.payment_method:
			if not self.get("total_discount"):
				self.total_discount= 0.0
			if not self.get("shipping_fee"):
				self.shipping_fee = 0.0
			total_before_payment_fee = self.total - self.total_discount + self.shipping_fee
			
			payment_method_check = frappe.get_value("Xendit Payment Methods",self.payment_method,"name")
			if payment_method_check:
				calculated_total = calculate(total_before_payment_fee, payment_method_check)
				self.payment_fee = calculated_total
				frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET payment_fee = {} WHERE name = '{}' ".format(calculated_total,self.name))
				print(calculated_total)

	

	# SUBSECTION Module Voucher
	def voucher_check_rule(self):
		from commerce.voucher.doctype.voucher.voucher import check_quantity, check_rule_time, check_rule_total_amount,check_rule_type
		print(self.get("voucher"))
		print(self.get("voucher_code"))
		check = check_rule_type(self.voucher,self.get("voucher_code"))
		
		if check.get("status") == 0:
			frappe.throw(_(check.get("keterangan")))
		check = check_rule_time(self.voucher)
		if check.get("status") == 0:
			frappe.throw(_(check.get("keterangan")))
		check = check_quantity(self.voucher,self.customer)
		if check.get("status") == 0:
			frappe.throw(_(check.get("keterangan")))
		check = check_rule_total_amount(self.voucher, self.total)
		if check.get("status") == 0:
			frappe.throw(_(check.get("keterangan")))

	# SUBSECTION Module Voucher
	def voucher_check_item(self):
		irisan_item = []
		error_item = "Item not in sale."
		doc_voucher = frappe.get_doc("Voucher", self.voucher)
		if doc_voucher.based_on == "All Item":
			irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item WHERE sc_item.parent = '{sc_name}' ".format(sc_name = self.name),as_dict=True)
			print(irisan_item)
		if doc_voucher.based_on == "Item":
			irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Based Child` v_item ON v_item.item = sc_item.item_code WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
			error_item = "Your purchase item not include in sale item"
			print(irisan_item)
		if doc_voucher.based_on == "Item Group":
			irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Group Based Child` v_item ON v_item.item_group = sc_item.item_group WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
			error_item = "Your purchase item group not include in sale item"
		if doc_voucher.based_on == "Brand":
			irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Brand Based Child` v_item ON v_item.brand = sc_item.brand WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
			error_item = "Your purchase item brand not include in sale item"
		if not irisan_item:
			frappe.throw(_("{}".format(error_item)))

			

	def calculate_grand_total(self):
		if not self.get("total_discount"):
			self.total_discount= 0.0
		if not self.get("shipping_fee"):
			self.shipping_fee = 0.0
		if not self.get("payment_fee"):
			self.payment_fee = 0.0
		if not self.get("total_discount"):
			self.total_discount = 0.0
		self.grand_total = float(self.total) - self.total_discount + self.payment_fee + self.shipping_fee
		frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET grand_total = {} WHERE name = '{}'".format(self.grand_total,self.name))


	def validate_submit(self):
		if self.get("sales_invoice"):
		# doc_shopping_cart_invoice = frappe.get_doc("Shopping Cart Invoice",self.name)
		# if doc_shopping_cart_invoice.get("sales_invoice"):
		# 	doc_voucher = frappe.get_doc("Sales Invoice", doc_shopping_cart_invoice.get("sales_invoice") )
			return frappe.throw(_("Sales Invoice has been created already."))

	def last_check_flash_sale(self):
		from commerce.commerce.doctype.flash_sale.flash_sale import check_flash_sale,calculate_discount_flash_sale_price,check_qty_flash_sale,check_rule_flash_sale_maximum
		all_flash_sale = []
		qty_x_flash_sale = {}
		for item in self.items:
			# item_flash_sale = frappe.get_value("Item",item.get("item_code"),"flash_sale")
			item_flash_sale = item.get("flash_sale")
			if item_flash_sale:
				if check_flash_sale(item.get("item_code"),item_flash_sale):
					if check_qty_flash_sale(item.get("item_code"), 0):
						if item.flash_sale:
							if item.flash_sale not in all_flash_sale:
								all_flash_sale.append(item.flash_sale)
								qty_x_flash_sale[item.flash_sale] = 0
							qty_x_flash_sale[item.flash_sale] += int(item.get("qty",0))
					else:
						frappe.throw("Quantity exceed the Flash Sale quantity.")	
				else:
					frappe.throw("Flash sale is over.")

		
		for item in all_flash_sale:
			checking_rule_flash_sale = check_rule_flash_sale_maximum(item,self.get("customer"),qty_x_flash_sale[item])
			if checking_rule_flash_sale.get("status") == 0:
				frappe.throw(_("{}".format(checking_rule_flash_sale.get("keterangan"))))

# SECTION on_submit
	def submit_function(self):
		# TODO stock uom
		data_item=[]
		for item in self.get("items"):
			data_item.append({
                "item_code": item.get("item_code"),
				"qty": item.get("qty"),
				"stock_uom": item.get("uom"),
				"uom": item.get("uom"),
				"conversion_factor": item.get("conversion_factor"),
				"stock_qty": item.get("qty"),
				"price_list_rate": item.get("price"),
				"base_price_list_rate": item.get("price"),
				"discount_percentage": 0.0,
				"discount_amount": item.get("margin"),
				"rate": (float(item.get("price"))-float(item.get("margin"))),
				"doctype": "Sales Invoice Item"
			})

		data_sales_team = []
		# STUB Sales Person
		# Diasumsikan 100% karena wss cuma pilih 1 orang
		if self.get("sales_person"):
			data_sales_team.append({
				"sales_person": self.get("sales_person"),
				"allocated_percentage" : "100",
				"doctype": "Sales Team"
				})

		data_taxes_and_charges = []
		# STUB Shipping fee
		if self.get("shipping_fee"):
			shipping_fee_account = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","shipping_fee_account")
			cost_center = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","cost_center")
			if not shipping_fee_account:
				frappe.throw(_("Please set up Sales Taxes and Charges Settings."))
			data_taxes_and_charges.append({       
				"charge_type": "Actual",
				"account_head": shipping_fee_account,
				"description": "Shipping Fee",
				"cost_center": cost_center,
				"tax_amount": self.get("shipping_fee"),
				"doctype": "Sales Taxes and Charges"
			})
		# STUB Payment Fee
		if self.get("payment_fee"):
			admin_fee_account = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","admin_fee_account")
			cost_center = frappe.get_value("Sales Taxes and Charges Settings","Sales Taxes and Charges Settings","cost_center")
			if not admin_fee_account:
				frappe.throw(_("Please set up Sales Taxes and Charges Settings."))
			data_taxes_and_charges.append({       
				"charge_type": "Actual",
				"account_head": admin_fee_account,
				"description": "Payment Fee",
				"cost_center": cost_center,
				"tax_amount": self.get("payment_fee"),
				"doctype": "Sales Taxes and Charges"
			})
		
		if self.payment_method:
			payment_method_temp = frappe.get_value("Xendit Payment Methods", self.payment_method, "payment_method_value")
			if payment_method_temp:
				payment_method = payment_method_temp
			else:
				payment_method = self.payment_method
		else:
			payment_method = "No payment method selected"

		# check apakah ini adalah cod atau tidak
		use_cod = 0
		if (self.pay_later == 1 and self.payment_method == "COD"):
			use_cod = 1
		data = {
			"order_via" : self.get("platform"),
			"naming_series": "ACC-SINV-.YYYY.-",
			"company": self.get("company"),
			"posting_date": frappe.utils.now(),
			"customer":  self.get("customer"),
			"customer_address" : self.get("address"),
			"recipient_name": self.get("recipient_name"),
			"recipient_phone" : self.get("phone"),
			"due_date":  self.get("posting_date"),
			"currency": "IDR",
			"conversion_rate": 1.0,
			"selling_price_list": "Standard Selling",
			"price_list_currency": "IDR",
			"plc_conversion_rate": 1.0,
			"courier" : self.get("courier"),
			"courier_service" : self.get("courier_service"),
			"from_territory" :self.get("from_territory"),
			"to_territory" : self.get("to_territory"),		
			"notes" :  self.get("note"),
			"items": data_item,
			"taxes" : data_taxes_and_charges,
			"sales_team" : data_sales_team,
			"ignore_pricing_rule" : 1,
			"update_stock" : 1,
			"payment_method" : "{}".format(payment_method),
			"use_cod" : use_cod,
			"doctype": "Sales Invoice"
		}

		if self.get("total_discount"):
			data.update({       
				"apply_discount_on": "Grand Total",
				"discount_amount": self.get("total_discount"),
			})
		data.update({
			"shopping_cart_invoice" : self.name
		})
		
		doc = frappe.get_doc(data)
		doc.save(ignore_permissions=True)
		print(doc)

		if doc.grand_total != self.grand_total:
			return frappe.throw(_("Kesalahan pada server. Silahkan coba lagi beberapa saat"))
		frappe.db.commit()

		if self.pay_later == 0:
			# Create invoice dan dapat xendit url
			xendit_url = shopping_cart_create_invoice(self)
			frappe.db.commit()
			frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET sales_invoice = '{sales_invoice}' WHERE name = '{shopping_cart_invoice}' "
			.format(sales_invoice = doc.name, shopping_cart_invoice = self.name))
			frappe.db.commit()
			if xendit_url:
				print("masuk xendit url")
				frappe.db.sql("UPDATE `tabSales Invoice` SET user = '{user}',xendit_invoice_url = '{xendit_url}' WHERE name = '{sales_invoice}' "
				.format(sales_invoice = doc.name, xendit_url = xendit_url, user = self.user))
			else:
				frappe.db.sql("UPDATE `tabSales Invoice` SET user = '{user}' WHERE name = '{sales_invoice}' "
				.format(sales_invoice = doc.name, user = self.user))
			frappe.db.commit()
		else:
			# Tidak create xendit sama sekali, tapi butuh link untuk ke sales invoice
			frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET sales_invoice = '{sales_invoice}' WHERE name = '{shopping_cart_invoice}' "
			.format(sales_invoice = doc.name, shopping_cart_invoice = self.name))
			frappe.db.commit()


		# Make Sales Invoice submitted
		print(doc.name)
		doc.reload()
		doc_unpaid = submit_sales_invoice(doc.name)

		
		print(doc_unpaid.name)
		print(doc_unpaid.docstatus)
		self.reload()
	
	
	def clear_shopping_cart(self):
		doc_fgs = frappe.get_doc("Shopping Cart",self.user)
		temp = []
		
		for idx,item in enumerate(doc_fgs.get("shopping_cart_item")):
			if item.get("is_selected") == 1:
				print(idx)
				temp.append(idx)

		for idx,int_temp in enumerate(temp):
			doc_fgs.shopping_cart_item.remove(doc_fgs.get("shopping_cart_item")[int_temp-idx])

		doc_fgs.save(ignore_permissions = True)
		frappe.db.commit()
		

	def shopping_cart_invoice_claim_voucher(self):
		# try:
		from commerce.voucher.doctype.voucher.voucher import claim_voucher
		if self.my_voucher:
			my_voucher_name = self.my_voucher
		else:
			my_voucher_status = claim_voucher(self.voucher, self.customer ,using_system=1)
			my_voucher_name = my_voucher_status.get("my_voucher_id")
		
		doc_mv =frappe.get_doc("My Voucher",my_voucher_name)
		doc_mv.status = "Applied"
		doc_mv.save(ignore_permissions=True)
		# except:
		# 	frappe.throw("There are error in Voucher")

# !SECTION on_submit 

# Xendit Invoice
''' Untuk create xendit invoice url lalu update tab shopping cart invoice'''
def shopping_cart_create_invoice(self):
	email_id = frappe.get_value("Customer",self.customer,"email_id")
	if email_id:
		frappe.session.user = email_id
	create_xendit_invoice(self)
	xendit_invoice_url=frappe.get_value("Xendit Invoice",{"external_id":self.name,"external_doctype" : "Shopping Cart Invoice"},"invoice_url")
	if xendit_invoice_url:
		frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET xendit_invoice_url = '{}' WHERE name = '{}' ".format(xendit_invoice_url, self.name))
		frappe.db.commit()
		self.xendit_invoice_url = xendit_invoice_url

	return xendit_invoice_url

def create_xendit_invoice(self):
	from xendit.invoice import create_invoice
	if self.payment_method:
		payment_method_value = frappe.get_value("Xendit Payment Methods",self.payment_method,"payment_method_value")
		if payment_method_value:
			payment_method = [payment_method_value]
		else:
			payment_method = [self.payment_method]
	else:
		payment_method =[]
	try:
		create_invoice(self.grand_total,"Shopping Cart Invoice",self.name,"Pembayaran barang dengan invoice {name}".format(name= self.name),payment_methods=payment_method)
	except:
		frappe.throw("Xendit Payment failed.")

def make_description_item(self):
    string_description = "Pembelian: "
    for item in self.ciputra_invoice_item:
        if item.get("item_name"):
            string_description+= item.get("item_name") + ","
    string_description[:-1]
    return string_description


def submit_sales_invoice(sales_invoice):
	doc_sinv = frappe.get_doc("Sales Invoice",sales_invoice)
	doc_sinv.docstatus = 1
	print(doc_sinv.docstatus)
	doc_sinv.save(ignore_permissions =True)
	frappe.db.commit()
	return doc_sinv