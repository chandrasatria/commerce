
import frappe
from frappe import _
from frappe.model.document import Document

def before_save(self, method):
    make_customer_verified(self)
	

# ------------ End of hooks -----------------


def make_customer_verified(self):
    if self.user:
        fga = frappe.get_all("Customer",fields="*",filters=[["email_id","=",self.user]])
        if len(fga) > 0:
            if self.is_used == 1:
                doc = frappe.get_doc("Customer", fga[0]["name"])
                doc.verification_email = 1
                doc.save(ignore_permissions = True)
        else:
            frappe.log_error(frappe.get_traceback(),"Data Error : Customer cannot find User")
            pass
    pass

	