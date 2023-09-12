
import frappe
from frappe import _
from frappe.model.document import Document

def before_save(self, method):
	make_disabled_item_stronger(self)
	fill_info_uom_to_default(self)
	fill_info_weight_uom_default(self)

	if not self.brand:
		if frappe.db.exists("Brand", "others"):
			self.brand = "Others"
		else:
			create_brand_others()
			self.brand = "Others"
	
	if self.flash_sale:
		update_flash_sale(self)
	
	# Untuk check item price apakah ada item yang tidak memiliki harga
	check_item_price(self)
	
def validate(self,method):
	print("validate")
	print(self.description)
	print("--------")
	# Supaya di Mobile bisa embed video
	print("++++")
	make_embbed_video(self)
	print("????")
	print(self.description_content)
	print("--------")

def on_update(self, method):
	from commerce.commerce.doctype.flash_sale.flash_sale import update_empty_flash_sale
	if self.flash_sale:
		doc_flash_sale = frappe.get_doc("Flash Sale",self.flash_sale)
		# doc_flash_sale.update_all_item_flash_sale()
	else:
		if self.has_variants == 1:
			template_item = self.name
		else:
			template_item = self.variant_of
		update_empty_flash_sale(template_item)

		
	self.reload()
		# DEPRECETEDDDDDDDDDDDDD
		# from commerce.commerce.doctype.flash_sale.flash_sale import create_or_update_pricing_rule
		# create_or_update_pricing_rule(self.item_code,flash_sale= self.flash_sale)

# ------------ End of hooks -----------------

def make_embbed_video(self):
	if self.description:
		self.description_content = convert_custom_content(self.description)

#DEWE: Function
# - to convert content Rich Text Type into iframe when there's link youtube
def convert_custom_content(content):
	import re
	iframes = re.findall("&lt;&lt;.*&gt;&gt;", content)
	print("-====")
	print(iframes)
	for iframe in iframes:
		youtube_links = re.findall('\\"https://www.youtube.com/watch\?v=[^\\"]*', iframe)
		if not youtube_links:
			youtube_links = re.findall('&lt;&lt;(.+?(?=&gt;))', iframe)
			# youtube_links = re.findall('\\"https://www.youtube.com/watch\?v=(.+?(?=&gt;))', iframe)
		print (youtube_links)
		for youtube_link in youtube_links:
			print(youtube_link)
			youtube_link = youtube_link.replace('\"','').replace('watch?v=','embed/')
			content = content.replace(iframe, '<iframe src="{youtube_link}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(youtube_link=youtube_link))
	print(content)
	return content

def check_item_price(self):
	pass
	# if self.name:
	# 	fga_item_price = frappe.get_all("Item Price", fields="*", filters=[["item_code","=",self.name]])
	# 	if not fga_item_price:
			# frappe.msgprint(_("Item Price not found. Please insert the price."))


# Ini dibuat karna issue template update disable ke child nya, which is kita ngga mau kayak gitu
def make_disabled_item_stronger(self):
	if self.disabled_item != self.disabled:
		self.disabled = self.disabled_item

def create_brand_others():
	doc = frappe.get_doc({
		"doctype" : "Brand",
		"brand" : "Others"
	})
	doc.save(ignore_permissions=True)
	frappe.db.commit()

# Ini udah ngga kepake karna get price nya udah dari applikasi
def get_all_item_price(self):
	# Ini untuk mengubah harga template
	# Jadi ketika ada lowest price di salah satu item, maka akan tampil di home sebagai harga utama
	if self.has_variants == 1:
		template_item = self.name
	else:
		template_item = self.variant_of

	fga = frappe.get_all("Item",fields="*",filters=[["variant_of","=",template_item]])
	min_price_item = 9999999999999
	max_price_item = 0
	
	lowest_price_flash_sale = 99999999999
	discount_flash_sale = 0
	lowest_item_price = 0
	item_price = 0
	flash_sale = ""
	if len(fga) > 0:
		for item in fga:
			if item["item_price"] < min_price_item:
				min_price_item = item["item_price"]
			if item["item_price"] > max_price_item:
				max_price_item = item["item_price"]
			if item["flash_sale"] and item["flash_sale_price"] and item["flash_sale_price"] < lowest_price_flash_sale:
				lowest_price_flash_sale = item["flash_sale_price"]
				flash_sale = item["flash_sale"]
				item_price = item["item_price"]
				discount_flash_sale = item["discount_flash_sale"]
		if not flash_sale:
			item_price = lowest_item_price
		min_price_item = 0 if min_price_item == 99999999999 else min_price_item
		lowest_price_flash_sale = 0 if lowest_price_flash_sale == 99999999999 else lowest_item_price


		frappe.db.sql("UPDATE `tabItem` SET item_price = '{item_price}', minimal_item_price = '{min_price_item}', maximal_item_price = '{max_price_item}', flash_sale = '{flash_sale}', flash_sale_price = '{flash_sale_price}', discount_flash_sale = '{discount_flash_sale}' WHERE name = '{template_item}' ".format(
			item_price = item_price,
			min_price_item = min_price_item,
			max_price_item= max_price_item,
			flash_sale_price = lowest_price_flash_sale,
			discount_flash_sale = discount_flash_sale,
			flash_sale = flash_sale,
			template_item = template_item,
			))
		frappe.db.commit()

def update_flash_sale(self):
	doc_flash_sale = frappe.get_doc("Flash Sale",self.flash_sale)
	self.flash_sale_valid_from = doc_flash_sale.get("valid_from")
	self.flash_sale_valid_till = doc_flash_sale.get("valid_till")

def fill_info_uom_to_default(self):
	for item in self.uoms:
		if item.get("minimal_qty") == 0:
			item.minimal_qty = 1
		if item.get("multiplication_qty") == 0:
			item.multiplication_qty = 1

def fill_info_weight_uom_default(self):
	if not self.weight_uom:
		self.weight_uom = "Kilogram"
		self.weight_per_unit = 1
	