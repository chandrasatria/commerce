import frappe

# reset Titan pertama kali
def delete_entry(confirm):
	""" to delete confirm = "y" """
	if confirm != "y":
		return "Cancelled"
	frappe.db.sql("DELETE FROM `tabSales Invoice`")
	frappe.db.sql("DELETE FROM `tabShopping Cart Invoice`")
	frappe.db.sql("DELETE FROM `tabXendit Invoice`")
	frappe.db.sql("DELETE FROM `tabGL Entry`")
	frappe.db.sql("DELETE FROM `tabPayment Entry`")


	frappe.db.sql("DELETE FROM `tabXendit Log`")
	frappe.db.sql("DELETE FROM `tabJNE Log`")
	frappe.db.sql("DELETE FROM `tabFirebase Log`")

	frappe.db.commit()
	print("Success delete")

# Untuk delet customer dan user
def delete_customer_and_user(customer):
	doc = frappe.get_doc("Customer", customer)
	user = doc.get("email_id")
	# Delete Use
	try:
		fga_up = frappe.get_all("User Permission",fields = "name" ,filter=[["user","=",user]])
		for item_up in fga_up:
			try:
				frappe.get_doc("User Permission", item_up)
			except:
				print("{} failed".format(str(item_up)))
	except:
		pass

	try:
		if user:
			frappe.delete_doc("User",user)
			frappe.db.commit()
	except:
		print("berhasil delete user")


	frappe.delete_doc("Customer" , customer )
	frappe.db.commit()

# Setelah export item maka item price untuk variant dibuatin
def create_item_price_variant():
	f = open("create Item Price Var.txt", "a")
	sql_select = frappe.db.sql("SELECT * FROM `tabItem` WHERE variant_of IS NOT NULL",as_dict=True)
	
	for item in sql_select:
		print(item["name"])
		fga = frappe.get_all("Item Price", fields="*", filters= [["item_code","=",item["name"]]])
		if len(fga) == 0:
			get_variant_price = frappe.get_all("Item Price", fields="*", filters= [["item_code","=",item["variant_of"]]],order_by= "creation DESC")
			if get_variant_price:
				print("insertingggggggggggggggg")
				print(item["name"])
				print(get_variant_price[0]["price_list_rate"])
				doc =frappe.get_doc({
					"item_code": item["name"],
					"packing_unit": 0,
					"item_name": item["item_name"],
					"price_list": "Standard Selling",
					"buying": 0,
					"selling": 1,
					"currency": "IDR",
					"price_list_rate": get_variant_price[0]["price_list_rate"],
					"lead_time_days": 0,
					"doctype": "Item Price"
				})
				f.write(item["name"] + "," +str(get_variant_price[0]["price_list_rate"]))
				f.write("\n")
				doc.save(ignore_permissions=True)
				frappe.db.commit()
		else:
			get_variant_price = frappe.get_all("Item Price", fields="*", filters= [["item_code","=",item["variant_of"]]],order_by= "creation DESC")
			if get_variant_price:
				print("fail sudah ada price: " + fga[0]["item_code"] + "with item" + str(get_variant_price[0]["price_list_rate"]))
			else:
				print("fail price template tidak ada: " + fga[0]["item_code"])

				# doc.save(ignore_permissions=True)
				# frappe.db.commit()
	f.close()

# Membuat item variant sama image nya dengan template
def patch_image_variant_same_as_template():
	f = open("making same image as template.txt", "a")
	sql_item_no_image = frappe.db.sql("SELECT name, variant_of FROM `tabItem` WHERE variant_of is not null AND image is null AND name = 'BIONDI ADJUSTABLE SEPARATE HANDLEBAR SET CLASS VORTEX ALUMINIUM-GOLD BLACK' ",as_dict=True)
	for item in sql_item_no_image:
		doc_item = frappe.get_doc("Item", item["name"])
		image_variant = frappe.get_value("Item",item["variant_of"],"image")
		if image_variant:
			doc_item.image = frappe
			doc_item.save(ignore_permissions = True)
			f.write(item["name"] + "," +str(image_variant))
			frappe.db.commit()
		else:
			f.write(item["name"] + "," +str(item["variant_of"])+ ","+ "fail")

	f.close()
			
def check_not_inserted_item_price():
	list_item_price = []
	fga_item_price= frappe.get_all("Item Price",fields="item_name")
	for item in fga_item_price:
		list_item_price.append(item["item_name"])
	all_item= frappe.get_all("Item",fields="item_name", filters=[["has_variants","=",1]])
	for item in all_item:
		if item["item_name"] in list_item_price:
			pass
		else:
			print(item["item_name"])

def patch_city_in_address():
	sql = frappe.db.sql("SELECT * FROM `tabAddress` WHERE jne_tariff_code is not null", as_dict=True)
	for item in sql:
		if item["jne_tariff_code"]:
			jne_dest = frappe.get_all("JNE Destination" , fields = "*" , filters = [["tariff_code","=",item["jne_tariff_code"]]])
			if len(jne_dest) > 0:
				doc = frappe.get_doc("Address",item["name"])
				doc.jne_id = jne_dest[0]["name"]
				doc.city = jne_dest[0]["origin_name"]
				print(jne_dest[0]["tariff_code"] + "--" + item["jne_tariff_code"])
				doc.save(ignore_permissions=True)
				frappe.db.commit()

def patch_image_thumbnail():
	import json
	limiter = 5
	index = 0
	with open('make thumbnail.json') as json_file:
		data = json.load(json_file)
		for item in data:
			print(item["attached_to_name"])
			doc = frappe.get_doc("Item",item["attached_to_name"])
			doc.image = item["file_url"]
			doc.save(ignore_permissions=True)
			# index += 1 
			# if index > limiter:
			#     break
			# print(item["zip_code"])
		   
			frappe.db.commit()

def territory_search_list():
	territories = frappe.get_all("Territory", fields=["name", "lft", "rgt"])
	for t in territories:
		search_list = ""
		country, province, city, district, subdistrict = None, None, None, None, None

		parent_territory = frappe.get_all("Territory", fields=["name", "type"], filters=[['lft', '<=', t['lft']], ['rgt', '>=', t['rgt']], ['name', '!=', 'All Territories']], order_by="lft DESC")
		if len(parent_territory) > 0:
			for pt in parent_territory:
				print('{} = "{}"'.format(pt['type'].lower(), pt['name']))
				if pt['type'].lower() == "country":
					country = pt['name']
				if pt['type'].lower() == "province":
					province = pt['name']
				if pt['type'].lower() == "city":
					city = pt['name']
				if pt['type'].lower() == "district":
					district = pt['name']
				if pt['type'].lower() == "subdistrict":
					subdistrict = pt['name']
				search_list += "{}\n".format(pt['name'])
		else:
			# tidak ada parentnya
			pass

		print("{} | {} | {} | {} | {}".format(country, province, city, district, subdistrict))

		frappe.db.sql("""
			UPDATE `tabTerritory`
			SET 
				search_list = %(search_list)s,
				country = %(country)s,
				province = %(province)s,
				city = %(city)s,
				district = %(district)s,
				subdistrict = %(subdistrict)s
			WHERE name = %(name)s
			""", {
			"search_list"	: search_list,
			"name"			: t['name'],
			"country"		: country,
			"province"		: province,
			"city"			: city,
			"district"		: district,
			"subdistrict"	: subdistrict
			})
		print("Updating {}: {}".format("Territory", t['name']))
	frappe.db.commit()


def create_contact(customer):
	doc_customer = frappe.get_doc("Customer",customer)
	if doc_customer.mobile_no and doc_customer.email_id:
		data = {
			"first_name": doc_customer.customer_name,
			"email_id": doc_customer.email_id,
			"user": doc_customer.email_id,
			"sync_with_google_contacts": 0,
			"status": "Passive",
			"mobile_no": doc_customer.mobile_no,
			"image": "",
			"pulled_from_google_contacts": 0,
			"is_primary_contact": 1,
			"unsubscribed": 0,
			"doctype": "Contact",
			"email_ids": [
			{
			
			"email_id": doc_customer.email_id,
			"is_primary": 1,
			"doctype": "Contact Email"
			}
			],
			"phone_nos": [
			{
		
			"phone": doc_customer.mobile_no,
			"is_primary_phone": 0,
			"is_primary_mobile_no": 1,
			"doctype": "Contact Phone"
			}
			],
			"links": [
			{
			
			"link_doctype": "Customer",
			"link_name": doc_customer.name,
			"doctype": "Dynamic Link"
			}
			]
		}
		doc_contact = frappe.get_doc(data)
		doc_contact.save(ignore_permissions=True)
		frappe.db.commit()
		doc_customer.customer_primary_contact = doc_contact.name
		doc_customer.save(ignore_permissions = True)
		frappe.db.commit() 


""" Membuat blogger memiliki name yang besar""" 
def patch_blogger():
	from frappe.model.rename_doc import rename_doc
	fga_blogger = frappe.get_all("Blogger",fields="name,short_name")
	if len(fga_blogger) > 0:
		for item in fga_blogger:
			rename_doc("Blogger",item["name"],item["short_name"].title(),False,0,False,False)
	frappe.db.commit()
