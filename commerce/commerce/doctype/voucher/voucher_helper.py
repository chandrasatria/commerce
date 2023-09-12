import string
import random
import frappe

import datetime

def strToTimedelta(time):
	time = str(time)
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	delta = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta

def strToDatetime(dateTime):
	dateTime = str(dateTime)
	if "." in dateTime:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S")
	return t

def strToDate(date):
	date = str(date)
	if len(date)>=10:
		date = date[:10]
	t = datetime.datetime.strptime(date,"%Y-%m-%d")
	return t

def timeDeltaToStr(timedelta):
	seconds = timedelta.total_seconds()
	hours = seconds / 3600
	minutes = (seconds % 3600) / 60
	seconds = seconds % 3600 % 60
	return "{}:{}:{}".format(int(hours),int(minutes),int(seconds))

def getTimeStamp():
	#timestamp
	import time
	ts = float(time.time())
	return ts

def convertTimeStamp(ts):
	st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
	return st


def randomString(length=10):
	"""Generate a random string of fixed length """
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(length))

def randomStringInt (length=10, chars=string.ascii_uppercase + string.digits):
    """Generate a random int and string of fixed length by char"""
    return ''.join(random.choice(chars) for _ in range(length))

def generate_code(string):
	import qrcode
	from io import BytesIO
	import base64

	qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
	qr.add_data(string)
	qr.make(fit=True)
	img = qr.make_image()
	bio = BytesIO()
	img.save(bio)
	pngqr = bio.getvalue()
	base64qr = base64.b64encode(pngqr)
	return base64qr

def generate_code_bc(string):
	from barcode import generate,writer
	from barcode.writer import ImageWriter
	from io import BytesIO
	import base64
	name = generate('code128', string, writer=ImageWriter(), output="x",pil = True)
	buffer = BytesIO()
	name.save(buffer,format="PNG")
	pngbc = buffer.getvalue()                     
	base64bc = base64.b64encode(pngbc)
	return base64bc


def upload_base64_without_sql(fname, content, dt, dn, docf):
	#upload to frappe v12
	# namafile |content = base64 | dt = doctype | dn = docname | docf = docfield
	try:
		sf = save_file(fname, content, dt, dn,folder=None , decode=True, is_private=0, df=docf)
		frappe.db.commit()
		return sf.file_url, True
	except:
		return "Something went wrong", False

def upload_base64(fname, content, dt, dn, docf):
	#upload to frappe v12
	# namafile |content = base64 | dt = doctype | dn = docname | docf = docfield
	try:
		sf = save_file(fname, content, dt, dn,folder=None , decode=True, is_private=0, df=docf)
		frappe.db.commit()
		tabdt = "`tab{}`".format(dt)
		x=frappe.db.sql("""UPDATE {} SET {} = "{}" WHERE name = "{}" """.format(tabdt,docf,sf.file_url,dn))
		frappe.db.commit()
		return sf
	except:
		return "Something went wrong"