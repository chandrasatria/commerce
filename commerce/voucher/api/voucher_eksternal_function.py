import frappe
from frappe import _
# This is an EXAMPLE documentation how to use voucher function
# Ini adalah dokumentasi CONTOH function yang memakai Voucher


# Ini untuk cek apakah voucher valid atau tidak
def voucher_check_rule(self):
    from commerce.voucher.doctype.voucher.voucher import check_quantity, check_rule_time, check_rule_total_amount,check_rule_type
    print(self.get("voucher"))
    print(self.get("voucher_code"))
    check = check_rule_type(self.voucher,self.get("voucher_code"))
    
    if check.get("status") == 0:
        frappe.throw(_(check.get("keterangan")))
    check = check_rule_time(self.voucher)
    if check.get("status") == 0:
        frappe.throw(_(check.get("keterangan")))
    check = check_quantity(self.voucher,self.customer)
    if check.get("status") == 0:
        frappe.throw(_(check.get("keterangan")))
    check = check_rule_total_amount(self.voucher, self.total)
    if check.get("status") == 0:
        frappe.throw(_(check.get("keterangan")))

# Ini untuk cek apakah item termasuk di voucher apa ngga, ga dimasukin fungsi krn FROM nya belum parameter.
def voucher_check_item(self):
    irisan_item = []
    error_item = "Item not in sale."
    doc_voucher = frappe.get_doc("Voucher", self.voucher)
    if doc_voucher.based_on == "All Item":
        irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item WHERE sc_item.parent = '{sc_name}' ".format(sc_name = self.name),as_dict=True)
        print(irisan_item)
    if doc_voucher.based_on == "Item":
        irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Based Child` v_item ON v_item.item = sc_item.item_code WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
        error_item = "Your purchase item not include in sale item"
        print(irisan_item)
    if doc_voucher.based_on == "Item Group":
        irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Group Based Child` v_item ON v_item.item_group = sc_item.item_group WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
        error_item = "Your purchase item group not include in sale item"
    if doc_voucher.based_on == "Brand":
        irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Brand Based Child` v_item ON v_item.brand = sc_item.brand WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
        error_item = "Your purchase item brand not include in sale item"
    if not irisan_item:
        frappe.throw(_("{}".format(error_item)))
    return irisan_item


# ini untuk ketika claim promo voucher maka create => Applied My Voucher
# Ketika claim my voucher maka update Claimed My Voucher => Applied My Voucher 
def shopping_cart_invoice_claim_voucher(self):
    from commerce.voucher.doctype.voucher.voucher import claim_voucher
    if self.my_voucher:
        my_voucher_name = self.my_voucher
    else:
        my_voucher_status = claim_voucher(self.voucher, self.customer ,using_system=1)
        my_voucher_name = my_voucher_status.get("my_voucher_id")
    
    doc_mv =frappe.get_doc("My Voucher",my_voucher_name)
    doc_mv.status = "Applied"
    doc_mv.save(ignore_permissions=True)


def calculate_voucher_discount(self,no_update = 0):
    total_discount = 0.0
    if self.voucher:
        doc_voucher = frappe.get_doc("Voucher", self.voucher)
        if doc_voucher.based_on == "All Item":
            irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item WHERE sc_item.parent = '{sc_name}' ".format(sc_name = self.name),as_dict=True)
            print(irisan_item)
        if doc_voucher.based_on == "Item":
            irisan_item = frappe.db.sql("SELECT sc_item.name, sc_item.total FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Based Child` v_item ON v_item.item = sc_item.item_code WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
            print(irisan_item)
        if doc_voucher.based_on == "Item Group":
            irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Item Group Based Child` v_item ON v_item.item_group = sc_item.item_group WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
        if doc_voucher.based_on == "Brand":
            irisan_item = frappe.db.sql("SELECT * FROM `tabShopping Cart Invoice Item` sc_item INNER JOIN `tabVoucher Brand Based Child` v_item ON v_item.brand = sc_item.brand WHERE v_item.parent = '{v_name}' AND sc_item.parent = '{sc_name}' ".format(v_name = self.voucher, sc_name = self.name),as_dict=True)
        if irisan_item:
            # Kalo mo tambah coret harga disini
            #  tambah field -> masukkan ke field itu setiap iterasi
            for item in irisan_item:
                print(item)
                diskon = 0
                
                if (doc_voucher.get("discount_type")=="Discount Percentage"):
                    diskon = (item["total"] * doc_voucher.get("discount_percentage")/100)
                    total_discount += diskon

            if (doc_voucher.get("discount_type")=="Discount Amount"):
                    total_discount = (doc_voucher.get("discount_amount"))
            
        if doc_voucher.get("maximal_discount"):
            if doc_voucher.maximal_discount != 0:
                if total_discount > doc_voucher.maximal_discount:
                    total_discount = doc_voucher.maximal_discount

        if no_update == 0:
            self.total_discount = total_discount
        
            frappe.db.sql("UPDATE `tabShopping Cart Invoice` SET total_discount = {} WHERE name = '{}' ".format(self.total_discount,self.name))
            frappe.db.commit()
            print(total_discount)
        else:
            return total_discount