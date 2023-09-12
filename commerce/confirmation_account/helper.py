import frappe

def randomString(stringLength=10):
	import string
	import random
	"""Generate a random string of fixed length """
	letters = string.ascii_uppercase
	return ''.join(random.choice(letters) for i in range(stringLength))


def strToDatetime(dateTime):
	import datetime
	dateTime = str(dateTime)
	if "." in dateTime:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S.%f")
	else:
		t = datetime.datetime.strptime(dateTime,"%Y-%m-%d %H:%M:%S")
	return t

def timeStrToTimeDelta(time):
	from datetime import datetime, timedelta
	t = datetime.strptime(time,"%H:%M:%S")
	delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
	return delta