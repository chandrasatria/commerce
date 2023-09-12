import frappe
import io

def log_cronjob(method=""):
	try:
		f = open("log_cronjob.txt", "a")
		f.write(str(method)+":"+str(frappe.utils.now())+"\n")
		f.close()
		print("berhasil")
	except:
		print("error while logging")

# Calculate item, sold from sales invoice item
def enqueue_add_sold(item_code):
	log_cronjob("enqueue_add_sold")
	sum_qty = frappe.db.sql("""SELECT SUM(sii.qty) FROM `tabSales Invoice Item` sii
	LEFT JOIN `tabSales Invoice` si ON sii.parent = si.name 
	WHERE sii.item_code = '{}' AND si.paid = 1""".format(item_code))
	if sum_qty[0][0]:
		doc = frappe.get_doc("Item", item_code)
		doc.sold = sum_qty[0][0]
		doc.save(ignore_permissions=True)
		print(sum_qty[0][0])
		frappe.db.commit()


	flash_sale = frappe.get_value("Item",item_code,"flash_sale")
	if flash_sale:
		sum_qty_flash_sale = frappe.db.sql("""SELECT SUM(scii.qty) FROM `tabShopping Cart Invoice Item` scii
		LEFT JOIN `tabShopping Cart Invoice` sci ON scii.parent = sci.name
		LEFT JOIN `tabSales Invoice` si ON si.shopping_cart_invoice = sci.name
		WHERE scii.flash_sale = '{}' AND si.paid = 1 AND scii.item_code = '{}' """.format(flash_sale,item_code))
		if sum_qty_flash_sale[0][0]:
			doc = frappe.get_doc("Item", item_code)
			doc.flash_sale_qty = sum_qty_flash_sale[0][0]
			doc.save(ignore_permissions=True)
			print(sum_qty_flash_sale[0][0])
			frappe.db.commit()
	print("cronjob finished")
