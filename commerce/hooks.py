# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "commerce"
app_title = "Commerce"
app_publisher = "DAS"
app_description = "Commerce"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "digitalasiasolusindo@gmail.com"
app_license = "DAS"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/commerce/css/commerce.css"
# app_include_js = "/assets/commerce/js/commerce.js"

# include js, css files in header of web template
# web_include_css = "/assets/commerce/css/commerce.css"
# web_include_js = "/assets/commerce/js/commerce.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

fixtures = [
	# {
	# 	"dt"	: "API Request"
	# },
	# {
	# 	"dt"	: "API Creation"
	# },
	# {
	# 	"dt"	: "Translation"
	# },
	{
		"dt"	: "Notification"
	},
	# {
	# 	"dt"	: "UOM"
	# },
	# {
	# 	"dt" : "Brand"
	# },
	# {
	# 	"dt" : "Role"
	# },
	# {
	# 	"dt" : "Role Profile"
	# },
	# {
	# 	"dt" : "Custom DocPerm"
	# },
]


# include js in doctype views
doctype_js = {
	"Item" : "public/js/item.js",
	"Sales Invoice" : "public/js/sales_invoice.js",
	"Address" : "public/js/address.js"
	
}


website_context = { 
	# "favicon": "/assets/nungkymusicschool/favicon.png",
	"splash_image": "/files/logoonly.png"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "commerce.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "commerce.install.before_install"
# after_install = "commerce.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "commerce.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item Price": {
		"before_save" : "commerce.doctype_function.item_price.before_save", 
		"on_update" : "commerce.doctype_function.item_price.on_update",
    },
	"Item":{
		"before_save" : "commerce.doctype_function.item.before_save",
		"validate" 	: "commerce.doctype_function.item.validate",
		"on_update" : "commerce.doctype_function.item.on_update"
	},
	"User" : {
		"on_update":"commerce.doctype_function.user.on_update"
	},
	"Customer" : {
		"on_update" : "commerce.doctype_function.customer.on_update",
		"before_insert":"commerce.doctype_function.customer.before_insert",
		"after_insert":"commerce.doctype_function.customer.after_insert",
	},
	"Shopping Cart Item" : {
		"after_insert":"commerce.doctype_function.shopping_cart_item.after_insert",
	},
	"Sales Invoice" : {
		"validate" : "commerce.doctype_function.sales_invoice.validate",
		"on_update" : "commerce.doctype_function.sales_invoice.on_update",
		"before_update_after_submit" : "commerce.doctype_function.sales_invoice.before_update_after_submit",
		"before_cancel" : "commerce.doctype_function.sales_invoice.before_cancel",
		"on_trash" : "commerce.doctype_function.sales_invoice.on_trash",
	},
	"Payment Entry":{
		"on_submit" : "commerce.doctype_function.payment_entry.on_submit",
	},
	"Address" : {
		"before_insert" : "commerce.doctype_function.address.before_insert" ,
		"before_save" : "commerce.doctype_function.address.before_save",
		"validate" : "commerce.doctype_function.address.validate"
	},
	"Xendit Invoice" : {
		"on_update_after_submit" : "commerce.doctype_function.xendit_invoice.on_update_after_submit"
	},
	"Blog Post" : {
		"validate" 	  : "commerce.doctype_function.blog_post.validate",
		"before_save" : "commerce.doctype_function.blog_post.before_save"
	},
	"View Log" : {
		"after_insert" : "commerce.doctype_function.view_log.after_insert",
	},
	"Delivery Tracking":{
		"after_insert" : "commerce.doctype_function.delivery_tracking.after_insert"
	},
	"Blogger" : {
		"autoname" : "commerce.doctype_function.blogger.autoname"
	},
	"Verification Email" : {
		"before_save" :  "commerce.doctype_function.verification_email.before_save",
	},
	"Email Queue" : {
		"after_insert" : "commerce.doctype_function.email_queue.after_insert",
	}

}


# Scheduled Tasks
# ---------------


scheduler_events = {
    "cron": {
		# "* * * * *": [
		# 		"frappe.email.queue.flush"
        # ],
		"0 * * * *":[
			# NOTE untuk send user notification
			"commerce.user_notification.schedule.user_notification_send_message_scheduler"
		],
		"30 * * * *":[
			# NOTE untuk send user notification
			"commerce.user_notification.schedule.user_notification_send_message_scheduler"
		]
    },
}

# Testing
# -------

# before_tests = "commerce.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "commerce.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "commerce.task.get_dashboard_data"
# }

