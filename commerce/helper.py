import string
import random
import frappe
from frappe import _
from frappe.utils.file_manager import save_file

import datetime

def randomString(stringLength=10):
	"""Generate a random string of fixed length """
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(stringLength))

def randomInt(Length=10):
    """Generate a random int of fixed length """
    import random
    return "".join(str(random.randrange(10)) for i in range(Length))

def timeFormat(timedelta):
	seconds = timedelta.total_seconds()
	hours = seconds / 3600
	minutes = (seconds % 3600) / 60
	seconds = seconds % 3600 % 60
	return "{}:{}:{}".format(int(hours), int(minutes), int(seconds))

def strToDate2(date):
	import datetime
	date = str(date)
	if len(date)>=10:
		date = date[:10]
	t = datetime.date.strptime(date,"%Y-%m-%d")
	return t

def timediff(a, b):
	return strToDatetime(str(a)) - strToDatetime(str(b))


def timediffInStr(a, b):
	return timeDeltaToStr(min(strToDatetime(str(a)) - strToDatetime(str(b)), datetime.timedelta(hours=30)))


def timediffInSeconds(a, b):
	return min((strToDatetime(str(a)) - strToDatetime(str(b))).total_seconds(), 30 * 3600)


def datediff(a, b):
	return strToDate(str(a)) - strToDate(str(b))


def datediffInSeconds(a, b):
	return min((strToDate(str(a)) - strToDate(str(b))).total_seconds(), 30 * 3600)


def strToTime(time):
	time = str(time)
	if "." in time:
		t = datetime.datetime.strptime(time,"%H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(time,"%H:%M:%S")
	return t.time()

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


# -------------------QrCode / Barcode
from io import BytesIO
from PIL import Image
import base64

def generate_code(string):
	#string to base64 (qrcode)
	import qrcode
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
	import barcode
	from barcode import writer
	from barcode.writer import ImageWriter

	name = barcode.get('code128', string, writer=ImageWriter())
	buffer = BytesIO()
	# name = generate('code128', string, writer=ImageWriter(), output="x",pil = True)
	buffer = BytesIO()
	name.write(buffer)
	pngbc = buffer.getvalue()                     
	base64bc = base64.b64encode(pngbc)
	return base64bc

def upload_base64(fname, content, dt, dn, docf=''):
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

def generate_barcode(doctype,name,string_to_encode,qr =1,field_qr="" ,bar=1, field_bar = ""):
	# STUB QRcode
	qrname = "qr"+string_to_encode+".jpg"
	brname = "br"+string_to_encode+".jpg"
	# barqrcode = isi dari qrcode/barcodenya nya
	barqrcode = string_to_encode
	# qrcodebase64 itu qrcode yang sudah jadi base64
	if qr and field_qr:
		qrcodebase64 = generate_code(barqrcode)
		sfqr = upload_base64(qrname, qrcodebase64,doctype, name, docf=field_qr)
	elif qr:
		print(_("Please enter field_qr"))
	
	# barcode garis
	if bar and field_bar:
		barcodebase64 = generate_code_bc(barqrcode)
		sfbc = upload_base64(brname, barcodebase64,doctype, name, docf=field_bar)
		print(sfbc)
	elif bar:
		print(_("Please enter field_bar"))

