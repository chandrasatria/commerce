// Copyright (c) 2019, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Voucher', {
	onload:function(frm){
		console.log("asd");
		cur_frm.set_query("item","voucher_item_group_based_child", function () {
			return {
					"filters": [
					['item', '=', "asd"]
					]
			}
	});
	},

	refresh: function(frm){
		if (cur_frm.is_new()) {
			cur_frm.set_df_property("prefix","hidden",0)	
			cur_frm.set_df_property("add_random_voucher","hidden",0)
		}else{
			cur_frm.set_df_property("prefix","hidden",0)	
			cur_frm.set_df_property("add_random_voucher","hidden",0)
		}
	},
	before_save: function(frm) {
		if (frm.doc.start_date && !frm.doc.publish_start_date){
			frm.set_value("publish_start_date",frm.doc.start_date)
		}
		if (frm.doc.end_date && !frm.doc.publish_end_date){
			frm.set_value("publish_end_date",frm.doc.end_date)
		}
	},
	start_date:function(frm){
		if (frm.doc.end_date && frm.doc.start_date) {
			// alert(frm.doc.valid_till < frm.doc.valid_from)
			if (frm.doc.end_date < frm.doc.start_date ) {
				frappe.show_alert("Sorry, <b>Valid From</b> must be bigger than <b>Valid Till</b>")
				frm.set_value("start_date" , "")
		}
	}
	},
	end_date:function(frm){
		if (frm.doc.end_date && frm.doc.start_date) {
			if (frm.doc.end_date < frm.doc.start_date ) {
				frappe.show_alert("Sorry, <b>Valid Til</b>l must be smaller than <b>Valid From</b>")
				frm.set_value("end_date" , "")
		}
	}
	},
	prefix_validation:function(prefix){
		// check duplicate prefix is in add_random voucher code
		var stat = 0
		if(!prefix){
			frappe.show_alert("Prefix must be filled")	
			return 0
		}
		else if(prefix.length < 4){
			frappe.show_alert("Prefix at least must be a 4 character.")	
			return 0
		}
		else{
			return 1
		}
	},
	add_random_voucher:function(frm){
		console.log("a")
		if (frm.doc.batch_code) {
			var batch_code = frm.doc.batch_code
		}else{
			var batch_code = ""
		}
			frappe.prompt([
				{'fieldname': 'prefix', 'fieldtype': 'Data', 'label': 'Prefix', 'description' : 'Example: TOUR-', 'reqd': 1},
				{'fieldname': 'amount', 'fieldtype': 'Int', 'label': 'Code Amount', 'reqd': 1},
				{'fieldname': 'html', 'fieldtype': 'HTML', 'options' : "<b>Warning!⚠</b> This will add prefix on your previous code.", 'label': ''}
			],
			function(values){
				console.log(values)
				if (frm.events.prefix_validation(values.prefix) == 1){
					cur_frm.set_value("prefix",values.prefix)
				frappe.call({
					method: "commerce.commerce.doctype.voucher.voucher.add_random_voucher",
					callback: function (r) {
						console.log("called")
						if (r.message) {
							console.log(r.message)
							if (r.message.status == 1){
								var string = ""
								$.each(r.message.data, function (i, f) {
									string += String(f)+String("\n")
								})
								frm.set_value("batch_code",string)
							} else{
								msgprint(r.message.data)
							}
						}
					},
					args: {
						"amount" : values.amount,
						"prefix" : values.prefix,
						"batch_code" : batch_code
	
					}
				});
			}

			},
			'Add Random Voucher',
			'Generate'
			)

			
		
	}

});
