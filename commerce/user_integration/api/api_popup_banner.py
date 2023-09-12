import frappe
import json
import base64
import sys

from frappe import _

from commerce.user_integration.validation import success_format, error_format


# Define the field and parameter
from commerce.user_integration.setting import doctype_user,user_field,password_field,field_user_customer_profile_picture

@frappe.whitelist(allow_guest=True)
def get_single_popup_banner():
    now = frappe.utils.nowdate()
    fga = frappe.get_all("Popup Banner",fields="*", filters=[["publish_from","<=",now],["publish_until",">=", now],["published","=",1]], order_by="creation DESC")
    if len(fga) > 0:
        return success_format(fga[0])
    return success_format("no_banner")


# ---- end of api ------
# ---- below is helper ----
def strToDate(date):
    import datetime
    date = str(date)
    if len(date)>=10:
        date = date[:10]
    t = datetime.datetime.strptime(date,"%Y-%m-%d")
    return t