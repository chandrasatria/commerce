// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Flash Sale', {
	refresh: function(frm) {

	},
	// STUB Function
	add_description_on_flash_sale_type:function(){
		if (cur_frm.doc.discount_type == "Discount Percentage")
		{
			cur_frm.set_df_property("discount_type","description","Discount Percentage")
		}
		else if (cur_frm.doc.discount_type == "Discount Amount")
		{
			cur_frm.set_df_property("discount_type","description","Discount Amount")
		}
		else if (cur_frm.doc.discount_type == "Discount Override")
		{
			cur_frm.set_df_property("discount_type","description","Discount Override")
		}
	}
});
