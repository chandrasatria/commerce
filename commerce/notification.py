import frappe
# from firebase.firebase.notification import flutter_send_notification_data
from firebase.user_notification.api import get_unread_inbox_with_user

def get_badge_from_user(customer = ""):
	user_customer = frappe.get_value("Customer",{"name":customer},"name")
	if not user_customer:
		user_customer = frappe.get_value("Customer",{"email_id":customer},"name")
	return get_unread_inbox_with_user(user_customer)

# ---- Start Notification here ----

# Ketika customer klik lanjutkan ke Pembayaran (Create Sales Invoice)
def send_notification_pending_payment(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Please proceed the payment"
	# body = "Please proceed the payment"
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)


# Ketika customer selesai bayar (Sales Invoice -> paid)
def send_notification_paid_payment(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Thank you for your purchase"
	# body = "Thank you for your purchase"
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)

# Ketika customer tidak melakukan pembayaran dan Xendit Expired (Sales Invoice -> expired)
def send_notification_expired_payment(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Sorry your payment has expired."
	# body = "Sorry your payment has expired."
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)

# Ketika admin melakukan prosess pengepakan pada barang customer (Sales Invoice -> Packaged)
def send_notification_packaged(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Your item is being prepared"
	# body = "Your item is being prepared"
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)

# Ketika admin melakukan pengiriman pada barang customer (Sales Invoice -> Shipping)
def send_notification_shipping(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Your item is being delivered"
	# body = "Your item is being delivered"
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)

# Ketika admin melakukan cancell pada order customer (Sales Invoice -> Cancel order)
def send_notification_cancelled(user='',reason= ''):
	pass
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Oops, your order has been cancelled"
	# body = "{}Contact us for detail".format(reason+". " if reason else "")
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)

# Ketika customer melakukan confirmation pada order customer (Sales Invoice -> Confirmed)
def send_notification_completed(user=''):
	pass
	# NOTE Sementara for demo purpose 6 Feb
	# if not user:
	# 	user = frappe.session.user
	# badge = get_badge_from_user(user).get("data") or 0
	# title = "Thank you for your purchase"
	# body = "We hope you enjoy our product"
	# flutter_send_notification_data(user, title, body, data={}, badge=badge)




