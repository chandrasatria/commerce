import frappe
def strToDatetime(dateTime):
	import datetime
	dateTime = str(dateTime)
	if "." in dateTime:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S")
	return t


def randomString(stringLength=10):
	import string
	import random
	"""Generate a random string of fixed length """
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(stringLength))


def upload(doctype,docname,private):
	# get record details
	dt = doctype
	dn = docname
	folder = ""
	file_url = frappe.form_dict.file_url
	filename = frappe.form_dict.filename
	is_private = private

	if not filename and not file_url:
		frappe.msgprint(_("Please select a file or url"),
			raise_exception=True)

	# save
	if frappe.form_dict.filedata:
		filedata = save_uploaded(dt, dn, folder, is_private)
	elif file_url:
		filedata = save_url(file_url, filename, dt, dn, folder, is_private)

	comment = {}
	if dt and dn:
		comment = frappe.get_doc(dt, dn).add_comment("Attachment",
			_("added {0}").format("<a href='{file_url}' target='_blank'>{file_name}</a>{icon}".format(**{
				"icon": ' <i class="fa fa-lock text-warning"></i>' if filedata.is_private else "",
				"file_url": filedata.file_url.replace("#", "%23") if filedata.file_name else filedata.file_url,
				"file_name": filedata.file_name or filedata.file_url
			})))

	return {
		"name": filedata.name,
		"file_name": filedata.file_name,
		"file_url": filedata.file_url,
		"is_private": filedata.is_private,
		"comment": comment.as_dict() if comment else {}
	}


def save_url(file_url, filename, dt, dn, folder, is_private):
	from six.moves.urllib.parse import unquote
	# if not (file_url.startswith("http://") or file_url.startswith("https://")):
	# 	frappe.msgprint("URL must start with 'http://' or 'https://'")
	# 	return None, None

	file_url = unquote(file_url)

	f = frappe.get_doc({
		"doctype": "File",
		"file_url": file_url,
		"file_name": filename,
		"attached_to_doctype": dt,
		"attached_to_name": dn,
		"folder": folder,
		"is_private": is_private
	})
	f.flags.ignore_permissions = True
	try:
		f.insert()
	except frappe.DuplicateEntryError:
		return frappe.get_doc("File", f.duplicate_entry)
	return f

def upload_base64_set_profile_picture(fname, content, dt, dn, docf, is_private =0):
	# upload to frappe v12
	# namafile |content = base64 | dt = doctype | dn = docname | docf = docfield
	from frappe.utils.file_manager import save_file
	try:
		sf = save_file(fname, content, dt, dn,folder=None , decode=True, is_private=is_private, df=docf)
		frappe.db.commit()
		tabdt = "`tab{}`".format(dt)
		x=frappe.db.sql("UPDATE {} SET {} = '{}' WHERE name = '{}'".format(tabdt,docf,sf.file_url,dn))
		frappe.db.commit()
		return sf
	except:
		frappe.log_error(frappe.get_traceback(), "Error: Upload base64")
		return "Something went wrong"


	