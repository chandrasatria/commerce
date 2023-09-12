import frappe
from api_integration.validation import success_format, error_format
from frappe import _

# @frappe.whitelist(allow_guest= False)
# def get_item():
# 	import json
# 	try:
# 		post = json.loads(frappe.request.data.decode('utf-8'))
# 	except:
# 		post = {}
# 	item_code = post.get("item_code") or ""
# 	search = post.get("search") or "%%"
# 	page = post.get("page") or 0
# 	limit = post.get("limit") or 20
# 	item_group = post.get("item_group") or ""
# 	popular = post.get("popular") or "%%"
# 	new_arrival = post.get("new_arrival") or "%%"
# 	flash_sale= post.get("flash_sale") or ""
# 	rating = post.get("rating") or 0
# 	min_price=post.get("min_price") or  0
# 	max_price= post.get("max_price") or 999999999999999
# 	order_by= post.get("order_by") or "creation DESC"
# 	price_list = post.get("price_list") or ""
# 	uom = post.get("uom") or "",
# 	customer = post.get("customer") or ""
# 	""" kenapa tidak pakai api request karena mau get_item dari erpnext"""

# 	# Pengecualian jika order_by nya pake harga
# 	# TODO
# 	if (order_by == "minimal_item_price ASC"):
# 		# TODO ini harus e pake get_order_by_price
# 		order_by = "creation ASC"
# 	if (order_by == "minimal_item_price DESC"):
# 		# TODO ini harus e pake get_order_by_price
# 		order_by = "creation DESC"
		
# 	# Item group nya ngga dibuat condition karena dia array takutnya ada yang ' jadi error
# 	if not item_group:
# 		item_group = get_all_to_list(fields= "name", filters=[],doctype="Item Group",field_to_append="name")
# 		print(item_group)

# 	# Supaya tepat sasaran item code
# 	item_code_sql_condition = ""
# 	if item_code:
# 		item_code_sql_condition = """ AND name = '{item_code}' """.format(item_code = item_code)

# 	# Untuk flash sale
# 	# flash_sale_select = ""
# 	flash_sale_sql_condition = ""
# 	if flash_sale == "" or flash_sale == "%" or flash_sale == "%%":
# 		flash_sale_sql_condition = ""
# 	elif flash_sale:
# 		# flash_sale_select = """, '{flash_sale}' as f_sale_template """.format(flash_sale = flash_sale)
# 		flash_sale_sql_condition = """ AND flash_sale = '{flash_sale}' """.format(flash_sale = flash_sale)
	
# 	sql_item = frappe.db.sql(""" 
# 	SELECT *
# 	FROM `tabItem`
# 	WHERE name IN (SELECT DISTINCT(variant_of) FROM `tabItem`)
# 	AND item_name LIKE %(search)s 
	
# 	AND popular LIKE %(popular)s
# 	AND new_arrival LIKE %(new_arrival)s
# 	AND disabled_item = 0
# 	AND rating >= %(rating)s
# 	AND item_group IN %(item_group)s 
# 	{flash_sale_sql_condition}
# 	{item_code_sql_condition}

# 	ORDER BY {order_by}
# 	LIMIT %(limit)s OFFSET %(page)s
# 	""".format(
# 		order_by = order_by,
# 		flash_sale_sql_condition = flash_sale_sql_condition,
# 		item_code_sql_condition = item_code_sql_condition

# 	),{
# 		"flash_sale" : flash_sale,
# 		"search" : "%"+search+"%",
# 		"item_group" : item_group,
# 		"popular" : popular,
# 		"new_arrival" : new_arrival,
# 		"min_price" : min_price,
# 		"max_price" : max_price,
# 		"limit" : limit,
# 		"page" : page,
# 		"rating" : rating
# 	},as_dict = True)

# 	print(sql_item)
# 	if min_price != 0 or max_price != 999999999999999:
# 		args = {
# 			"qty":1}

# 		args["price_list"] = price_list if price_list else get_default_price_list()
# 		args["customer"] = customer if customer else ""
		
# 		# Check price dan masukkan ke list to delete
# 		item_to_delete = []
# 		for index,item in enumerate(sql_item):
# 			if item["stock_uom"]:
# 				args["uom"] = item["stock_uom"]
# 			else:
# 				args["uom"] = uom
# 			item_price = get_item_price_erpnext(args,item["item_code"]) or 0
# 			item["item_price"] = item_price
# 			if (float(item_price) < float(min_price)) or (float(item_price) > float(max_price)):
# 				item_to_delete.append(index)

# 			item["flash_sale_detail"] = fetch_flash_sale(item["flash_sale"])
		
# 		# Delete item
# 		print(item_to_delete)
# 		for idx,item in enumerate(item_to_delete):
# 			sql_item.pop(item-idx)
# 		print("----------------------")
# 		print(sql_item)
		
# 	return success_format(sql_item)


@frappe.whitelist(allow_guest= False)
def get_min_max_item():
	try:
		import json
		try:
			post = json.loads(frappe.request.data.decode('utf-8'))
		except:
			post = {}
		search = post.get("search") or ""
		item_group = post.get("item_group") or ""
		brand = post.get("brand") or  ""
		rating = post.get("rating") or "0"
		popular = post.get("popular") or "%%"
		new_arrival = post.get("new_arrival") or "%%"
		flash_sale= post.get("flash_sale") or ""
		price_list = post.get("price_list") or ""
		uom = post.get("uom") or "",
		customer = post.get("customer") or ""
		order_by = post.get("order_by") or "creation DESC"
		""" Ini kenapa tidak jadi satu dengan get item
		1. Karena ini ga pake limit
		2. Karena masterListDelegate ikut success format
		"""

		# Untuk get item_group
		if not item_group:
			item_group = get_all_to_list(fields= "name", filters=[],doctype="Item Group",field_to_append="name")
			print(item_group)

		# Brand dia array takutnya ada yang ' jadi error
		if not brand:
			brand = get_all_to_list(fields= "name", filters=[],doctype="Brand",field_to_append="name")
			print(brand)
		
		# NOTE ini masih bug, soale mau e ambil harga item yang paling baru
		price_list_name =  get_sql_to_list(sql_query=""" SELECT name,valid_from,item_code FROM `tabItem Price` GROUP BY item_code ORDER BY valid_from   """ ,field_to_append="name")
		print(price_list_name)

		uom_sql_condition = ""
		if not uom:
			uom_sql_condition = """ AND uom = '{uom}' """.format(uom = uom)

		price_list= price_list if price_list else get_default_price_list()

		sql_item_price = frappe.db.sql("""SELECT 
		tip.name as name,
		tip.item_code as item_code,
		tip.price_list_rate as price_list_rate,
		tip.price_list as price_list,
		tip.uom as uom,
		tip.customer as customer
		FROM `tabItem Price` tip INNER JOIN `tabItem` ti ON tip.item_code = ti.item_code
		WHERE tip.valid_from <= %(now)s
		AND ti.item_name LIKE %(search)s 
		AND ti.item_group IN %(item_group)s 
		AND ti.brand IN %(brand)s
		AND ti.rating >= %(rating)s
		AND tip.price_list = %(price_list)s
		{uom_sql_condition}
		GROUP BY item_code
		""".format(
			uom_sql_condition = uom_sql_condition
		),
		{
			
			"search" : "%"+search+"%",
			"price_list_name" : price_list_name,
			"item_group" : item_group,
			"brand" : brand,
			"now" : frappe.utils.now(),
			"price_list" : price_list,
			"rating" : rating,
			"order_by" : order_by
		},
		as_dict=True)

		print(sql_item_price)

		max_price = float(0)
		min_price = float(999999999999999)
		for item in sql_item_price:
			min_price = float(item["price_list_rate"]) if float(min_price) > float(item["price_list_rate"]) else float(min_price)
			max_price = float(item["price_list_rate"]) if float(max_price) < float(item["price_list_rate"]) else float(max_price)

		return success_format({"min_price": min_price, "max_price" : max_price})
	except:
		frappe.log_error(frappe.get_traceback(),"Error: item get_min_max")
		return error_format(_("Maaf ada kesalahan pada server"))


# NOTE ini untuk get doc item
@frappe.whitelist(allow_guest = False)
def get_doc_item(item_code, price_list= "", uom ="", customer = ""):
	from api_integration.api_integration.doctype.api_request.api_request import get_list_doctype
	if not frappe.db.exists("Item",item_code):
		return error_format(_("Item not found."))
	else:
		doc = frappe.get_doc("Item", item_code)
		
		output_list = get_list_doctype(doctype = "Item", name = item_code)
		args = {
			"qty":1
		}
		args["price_list"] = price_list if price_list else get_default_price_list()
		args["uom"] = uom if uom else doc.get("stock_uom")
		args["customer"] = customer if customer else ""

		output_list["item_price"] = get_item_price_erpnext(args,item_code) or 0
		
		return success_format([output_list])


# -- Helper

def get_item_price_erpnext(args, item_code):
	""" 
	args is like this 
		args = {
			"price_list" : "Jawa Standard Selling",
			"customer" : "ant",
			"uom" : "Unit",
			"qty":1,
			"transaction_date" : "2021-01-27"}
 
	item code is like this >>
		item_code = "ST-00001-M"
	"""
	from erpnext.stock.get_item_details import get_price_list_rate_for
	final_item_price = get_price_list_rate_for(args,item_code)
	return final_item_price

def get_all_to_list(fields, filters,doctype, field_to_append, order_by = "modified DESC"):
	sql = frappe.get_all(doctype,fields=fields,filters=filters,order_by=order_by)
	some_list = []
	for item in sql:
		if item not in some_list:
			some_list.append(item[field_to_append])
	return some_list

def get_sql_to_list(sql_query, field_to_append):
	sql = frappe.db.sql(sql_query,as_dict=True)
	print(sql)
	some_list = []
	for item in sql:
		some_list.append(item[field_to_append])
	return some_list

def fetch_flash_sale(flash_sale):
	if flash_sale:
		if frappe.db.exists("Flash Sale",flash_sale):
			doc = frappe.get_doc("Flash Sale",flash_sale)
			return [doc]
	return []
	
def get_default_price_list():
	single_selling_setting = frappe.get_single("Selling Settings")
	return single_selling_setting.get("selling_price_list","Standard Selling")

# TODO sort item
def get_order_by_price(item_group,search,rating,price_list, order_by):
	search = search or ""
	item_group = item_group or ""
	rating = rating or "0"
	price_list = price_list or ""
	# uom = uom or "",
	# customer = customer or ""

	sql_item_price = frappe.db.sql("""SELECT 
	tip.name as name,
	tip.item_code as item_code,
	tip.price_list_rate as price_list_rate,
	tip.price_list as price_list,
	tip.uom as uom,
	tip.customer as customer
	FROM `tabItem Price` tip INNER JOIN `tabItem` ti ON tip.item_code = ti.item_code
	WHERE tip.valid_from <= %(now)s
	AND ti.item_name LIKE %(search)s 
	AND ti.item_group IN %(item_group)s 
	AND ti.rating >= %(rating)s
	AND tip.price_list = %(price_list)s
	ORDER BY %(order_by)s  
	GROUP BY item_code
	""",
	{
		"search" : "%"+search+"%",
		"price_list_name" : price_list,
		"item_group" : item_group,
		"now" : frappe.utils.now(),
		"price_list" : price_list,
		"order_by" : order_by,
		"rating" : rating
	},
	as_dict=True)
	return sql_item_price


# Ini dipakai di mana-mana jangan dihapus
@frappe.whitelist(allow_guest= False)
def get_item(args={}):
	try:
		import json
		session_user = frappe.session.user
		default_price_list = frappe.get_single("Selling Settings").get("selling_price_list")
		if session_user:
			temp_default_price_list = get_default_price_list_from_customer(session_user)
			if temp_default_price_list:
				default_price_list = temp_default_price_list
		
		if not args:
			try:
				post = json.loads(frappe.request.data.decode('utf-8'))
			except:
				post = args
		else:
			post = args
		item_code = post.get("item_code") or ""
		search = post.get("search") or "%%"
		page = post.get("page") or 0
		limit = post.get("limit") or 20
		item_group = post.get("item_group") or ""
		brand = post.get("brand") or ""
		popular = post.get("popular") or "%%"
		new_arrival = post.get("new_arrival") or "%%"
		flash_sale= post.get("flash_sale") or ""
		rating = post.get("rating") or 0
		min_price=post.get("min_price") or  0
		max_price= post.get("max_price") or 999999999999999
		order_by= post.get("order_by") or "tip.creation DESC"
		price_list = post.get("price_list") or default_price_list
		uom = post.get("uom") or "",
		customer = post.get("customer") or ""
		favourite = post.get("favourite") or 0
		""" kenapa tidak pakai api request karena mau get_item dari erpnext"""
			
		# Ini ketika order_by e view
		# last_view_sql_join = ""
		# if order_by == "tvl.last_view ASC" or order_by == "tvl.last_view DESC":
		# 	last_view_sql_join = """ LEFT JOIN `tabView Log` tvl ON ti.name = tvl.reference_name """
		user = frappe.session.user
		if not user:
			return error_format(_("Please login first."))

		
		# Item group nya ngga dibuat condition karena dia array takutnya ada yang ' jadi error
		if not item_group:
			item_group = get_all_to_list(fields= "name", filters=[],doctype="Item Group",field_to_append="name")
			print(item_group)

		# Brand dia array takutnya ada yang ' jadi error
		if not brand:
			brand = get_all_to_list(fields= "name", filters=[],doctype="Brand",field_to_append="name")
			print(brand)

		# Supaya tepat sasaran item code
		item_code_sql_condition = ""
		if item_code:
			item_code_sql_condition = """ AND ti.name = '{item_code}' """.format(item_code = item_code)

		# Untuk flash sale
		# flash_sale_select = ""
		flash_sale_sql_condition = ""
		if flash_sale == "" or flash_sale == "%" or flash_sale == "%%":
			flash_sale_sql_condition = ""
		elif flash_sale:
			# flash_sale_select = """, '{flash_sale}' as f_sale_template """.format(flash_sale = flash_sale)
			flash_sale_sql_condition = """ AND ti.flash_sale = '{flash_sale}' """.format(flash_sale = flash_sale)
		
		favourite_condition = ""
		if favourite == 1:
			favourite_condition = """ AND is_liked = 1 """


		all_item = get_all_to_list(fields= "variant_of", filters=[],doctype="Item",field_to_append="variant_of")

		sql_item = frappe.db.sql(""" 
		SELECT ti.*,tip.* , 
		ti._liked_by as liked,
		CASE
			WHEN ti._liked_by LIKE %(user)s THEN 1
			ELSE 0
		END as is_liked
		FROM `tabItem Price` tip JOIN 
		(SELECT MAX(valid_from) as valid_from,item_code 
		FROM `tabItem Price`
		WHERE price_list = %(price_list)s
		GROUP BY item_code 
		ORDER BY price_list_rate ASC) stip
		ON tip.item_code = stip.item_code AND tip.valid_from = stip.valid_from
		JOIN `tabItem` ti ON tip.item_code = ti.item_code
		WHERE 
			ti.name IN %(all_item)s
			AND ti.item_name LIKE %(search)s 
			AND ti.popular LIKE %(popular)s
			AND ti.disabled = 0
			AND ti.new_arrival LIKE %(new_arrival)s
			AND ti.disabled_item = 0
			AND ti.rating >= %(rating)s
			AND ti.item_group IN %(item_group)s
			AND ti.brand IN %(brand)s
			AND tip.price_list = %(price_list)s
			{flash_sale_sql_condition}
			{item_code_sql_condition}
		GROUP BY ti.item_code
		HAVING tip.price_list_rate >= %(min_price)s AND
		tip.price_list_rate <= %(max_price)s
		{favourite_condition}
		ORDER BY {order_by}
		LIMIT %(limit)s OFFSET %(page)s


		""".format(
				order_by = order_by,
				flash_sale_sql_condition = flash_sale_sql_condition,
				item_code_sql_condition = item_code_sql_condition,
				favourite_condition = favourite_condition
			),{
				"user" : "%"+user+"%",
				"all_item" : all_item,
				"flash_sale" : flash_sale,
				"search" : "%"+search+"%",
				"item_group" : item_group,
				"brand" : brand,
				"popular" : popular,
				"new_arrival" : new_arrival,
				"min_price" : min_price,
				"max_price" : max_price,
				"limit" : limit,
				"page" : page,
				"rating" : rating,
				"price_list" : price_list
			},as_dict = True)
		

		# for index,item in enumerate(sql_item):
		# 	item["flash_sale_detail"] = fetch_flash_sale(item["flash_sale"])
			
		# print(sql_item)
		# if min_price != 0 or max_price != 999999999999999:
		# 	args = {
		# 		"qty":1}

		# 	args["price_list"] = price_list if price_list else get_default_price_list()
		# 	args["customer"] = customer if customer else ""
			
		# 	# Check price dan masukkan ke list to delete
		# 	item_to_delete = []
		# 	for index,item in enumerate(sql_item):
		# 		if item["stock_uom"]:
		# 			args["uom"] = item["stock_uom"]
		# 		else:
		# 			args["uom"] = uom
		# 		item_price = get_item_price_erpnext(args,item["item_code"]) or 0
		# 		item["item_price"] = item_price
		# 		if (float(item_price) < float(min_price)) or (float(item_price) > float(max_price)):
		# 			item_to_delete.append(index)

		# 		item["flash_sale_detail"] = fetch_flash_sale(item["flash_sale"])
			
		# 	# Delete item
		# 	print(item_to_delete)
		# 	for idx,item in enumerate(item_to_delete):
		# 		sql_item.pop(item-idx)
		# 	print("----------------------")
		# 	print(sql_item)
			
		return success_format(sql_item)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: item get_item")
		return error_format(_("Maaf ada kesalahan pada server"))

def get_default_price_list_from_customer(email_customer):
	""" untuk mendapatkan price list dari customer """
	price_list = ""
	fga_customer = frappe.get_all("Customer",fields="*",filters=[["email_id","=",email_customer]])
	if len(fga_customer) > 0:
		if fga_customer[0]["customer_group"]:
			price_list = frappe.get_value("Customer Group",fga_customer[0]["customer_group"],"default_price_list")
		if fga_customer[0]["default_price_list"] and not price_list:
			price_list = fga_customer[0]["default_price_list"]
	return price_list


@frappe.whitelist(allow_guest= False)
def get_flash_sale():
	try:
		now = frappe.utils.now()

		fgl_flash_sale = frappe.get_list("Flash Sale",fields="*",filters=[["valid_from","<=",now],["valid_till",">=",now]])
		if len(fgl_flash_sale)>0:
			for item in fgl_flash_sale:
				item["now"] = now
				detail_item = get_item({
					"flash_sale" : item["name"]
				})
				if detail_item.get("data"):
					item["item"] = detail_item["data"]


			return success_format(fgl_flash_sale)
		else:
			return success_format([])
	except:
		frappe.log_error(frappe.get_traceback(),"Error: item get_flash_sale")
		return error_format(_("Maaf ada kesalahan pada server"))


# Concat dari Get Item Details, Get Doc dan Get Flash Sale
@frappe.whitelist(allow_guest=False)
def get_item_detail_and_doc():
	from api_integration.api_integration.doctype.api_request.api_request import master_get_item_details
	import json
	try:
		post = json.loads(frappe.request.data.decode("UTF-8"))
		tr_date = frappe.utils.now()
		response_item = {}
		response_item["item_details"] =  master_get_item_details(
		warehouse = post.get("warehouse"),
		price_list = post.get("price_list"),
		customer = post.get("customer"),
		company = post.get("company"),
		transaction_date = tr_date,
		item = post.get("item"),
		uom = post.get("uom"))

		response_item["item_doc"] = frappe.get_doc("Item",post.get("item"))

		# Ini ngga pake % karena tanggal
		response_item["flash_sale"] = frappe.db.sql(""" SELECT *, NOW() as now FROM `tabFlash Sale` WHERE name = (SELECT flash_sale FROM `tabItem` WHERE name = %(item)s AND valid_from <= '{date}' AND valid_till >= '{date}' ) """.format(date = frappe.utils.now()),{
			"item" : post.get("item")
		},as_dict=True)

		return success_format(response_item)
	except:
		frappe.log_error(frappe.get_traceback(),"Error: API Get Item Details Error")
		return error_format(_("Something went wrong. Please try again in a few minutes"))

# Concat dari Get Item Details, Get Doc dan Get Flash Sale
""" item : "Test-I-0001" """
@frappe.whitelist(allow_guest=False)
def get_all_item_detail_and_doc():
	from api_integration.api_integration.doctype.api_request.api_request import master_get_item_details
	import json
	try:
		post = json.loads(frappe.request.data.decode("UTF-8"))
		

		if "item_parent" in post:
			item_parent = post["item_parent"]
		else:
			frappe.throw(_("Parameter Item parent needed"))

		if "customer" in post:
			customer = post["customer"]
		else:
			frappe.throw(_("Parameter Customer needed"))
		
		if "price_list" in post:
			price_list = post["price_list"]
		else:
			price_list = ""
		
		# warehouse = post.get("warehouse")
		# price_list = post.get("price_list")
		# customer = post.get("customer")
		# company = post.get("company")
		# item = post.get("item")
		# uom = post.get("uom")

		
		warehouse = ""
		if not price_list and customer:
			resp_cg = get_customer_group_by_customer(customer)
			if resp_cg:
				price_list = resp_cg[1]
		else:
			price_list = price_list or ""
		company = ""
		tr_date = frappe.utils.now()

		if not item_parent:
			return error_format(_("Parameter Item perlu diisi."))

		# Get semua item
		# Parameter untuk semua item
		# Loop per item nya
			# Di get item detail dan docnya
			# 
		# Get all possibility
		response_item = {}
		item_sql = frappe.db.sql("""SELECT i.name,ucd.uom 
		FROM `tabItem` i 
		LEFT JOIN `tabUOM Conversion Detail` ucd 
		ON i.name = ucd.parent 
			WHERE i.variant_of = %(item_parent)s AND
			i.disabled = 0
		ORDER BY i.name ASC, ucd.conversion_factor ASC """,{"item_parent" : item_parent}, as_dict=True)
		print(item_sql)

		# List to Delete
		
		list_to_delete = []

		# Get Doc
		item_doc = {}
		for item in item_sql:
			if item["name"] not in item_doc:
				item_doc[item["name"]] = frappe.get_doc("Item",item["name"]).as_dict()

		# Get Flash Sale
		item_flash_sale = {}
		for item in item_sql:
			if item["name"] not in item_flash_sale:
				# ini masih harus diubah
				sql_flash_sale = frappe.db.sql(""" SELECT *, NOW() as now FROM `tabFlash Sale` WHERE name = (SELECT flash_sale FROM `tabItem` WHERE name = %(item)s AND valid_from <= '{date}' AND valid_till >= '{date}' ) """.format(date = frappe.utils.now()),{
				"item" : item["name"]
				},as_dict=True)
				item_flash_sale[item["name"]] = sql_flash_sale

		# Concat dan get item detail
		for item in item_sql:
			print(item["uom"])
			if item["name"] not in response_item:
				response_item[item["name"]] = {}

			if item["uom"] not in response_item[item["name"]]:
				response_item[item["name"]][item["uom"]] = {}
			
			response_item[item["name"]][item["uom"]]["item_details"] = master_get_item_details(
			warehouse = warehouse,
			price_list = price_list,
			customer = customer,
			company = company,
			transaction_date = tr_date,
			item = item["name"],
			uom = item["uom"])


			print(item["name"])
			print( response_item[item["name"]][item["uom"]]["item_details"]["item_detail"]["price_list_rate"])
			if not response_item[item["name"]][item["uom"]]["item_details"]["item_detail"]["price_list_rate"]:
				list_to_delete.append({"variant" : item["name"] , "uom" : item["uom"]})
			elif response_item[item["name"]][item["uom"]]["item_details"]["item_detail"]["price_list_rate"] == 0.0:
				list_to_delete.append({"variant" : item["name"] , "uom" : item["uom"]})

			response_item[item["name"]]["item_doc"] = item_doc[item["name"]]
			# Get File
			list_file = frappe.get_all("File",fields = "file_url",filters=[["attached_to_name" 
			,"=", item["name"]]])
			response_item[item["name"]]["item_doc"]["list_image"] = []
			for some_file in list_file:
				response_item[item["name"]]["item_doc"]["list_image"].append(some_file["file_url"])

			# Assign Flash Sale
			response_item[item["name"]][item["uom"]]["flash_sale"] = item_flash_sale[item["name"]]
		
		for item_to_delete in list_to_delete:
			print(item_to_delete)
			del response_item[item_to_delete["variant"]][item_to_delete["uom"]]

		return success_format(response_item)
			
	except:
		frappe.log_error(frappe.get_traceback(),"Error: API Get All Item Details Error")
		return error_format(_("Something went wrong. Please try again in a few minutes"))



def get_customer_group_by_customer(customer):
	default_price_list = ""
	customer_group = ""
	customer_group = frappe.get_value("Customer",{"name": customer },"customer_group")
	
	if not customer_group:
		customer_group = frappe.get_value("Customer",{"email_id": frappe.session.user },"customer_group")
	if customer_group:
		fga_customer_group = frappe.get_all("Customer Group",fields="default_price_list",filters=[["name","=",customer_group]])
		if len(fga_customer_group)>0:
			default_price_list = fga_customer_group[0]["default_price_list"]
	return customer_group,default_price_list