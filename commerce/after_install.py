import frappe
from frappe import _


def after_install():
	try:
		doc = frappe.get_doc({
			"brand": "Others",
			"doctype": "Brand",
			})
		doc.save(ignore_permissions=True)
		frappe.db.commit()
	except:
		pass


	# SUBSECTION Role Write Read User
	try:
		fga = frappe.get_all("Role",filters=[["name","=","Write Read User"]])
		if len(fga)==0:
			doc = frappe.get_doc({
				"doctype" : "Role",
				"role_name" : "Write Read User"
			})
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	except:
		pass

	try:
		fga = frappe.get_all("Custom DocPerm",filters=[["role","=","Write Read User"],["parent","=","User"]])
		if len(fga) == 0:
			doc = frappe.get_doc({
				"parent": "User",
				"parentfield": "permissions",
				"parenttype": "DocType",
				"idx": 0,
				"docstatus": 0,
				"role": "Write Read User",
				"if_owner": 0,
				"permlevel": 0,
				"read": 1,
				"write": 1,
				"create": 0,
				"delete": 0,
				"submit": 0,
				"cancel": 0,
				"amend": 0,
				"report": 0,
				"export": 1,
				"import": 0,
				"set_user_permissions": 0,
				"share": 0,
				"print": 0,
				"email": 0,
				"doctype": "Custom DocPerm"
			})
			doc.save(ignore_permissions=True)
			frappe.db.commit()
	except:
		pass


	# !SUBSECTION



# def checklist(with_ok = False):
# 	# Ini untuk subscribe email yang ada di web.
# 	checker_data("User Notification Group Recipient","info_general",with_ok=True)

# def checker_data(doctype, name, err_message = "",with_ok = False):
# 	import urllib.parse
# 	common_path = urllib.parse.quote('/desk#List/{}/List'.format(doctype))
	
# 	err_code = "(:#dnf:#{})".format(name)
# 	try:
# 		check_ungr =frappe.db.exists(doctype,name)
# 		if not check_ungr:
# 			if not err_message:
# 				print("Please add `{name}` in {doctype}. {err_code}".format(name = name, doctype = doctype, err_code = err_code))
# 				frappe.msgprint(_("Please add `{name}` in <a href = '{doctype}' > {err_code} </a> ".format(name = name, doctype = doctype, err_code = err_code)))
# 			if err_message:
# 				print("{}".format(err_message))
# 				frappe.msgprint(_("{}".format(err_message)))
# 		else:
# 			if with_ok:
# 				print("Ok {}".format(err_code))
# 	except:
# 		pass


# def reference(code = ""):
# 	print("under dev")



