// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Voucher Giveaway', {
	onload: function(frm){
        
cur_frm.set_query("voucher", function () {
	return {
		"filters": [
			['voucher_claim_type', '=', 'My Voucher']
			
		]
	}
});

}
});
