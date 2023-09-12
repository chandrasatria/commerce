
// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Address', {
	onload: function(frm) {

        cur_frm.set_query("province_delivery", function () {
            return {
                    "filters": [
                    ['Territory', 'type', '=', 'Province']
                    ]
            }
        });

        cur_frm.set_query("city_delivery", function () {
            return {
                    "filters": [
                    ['Territory', 'type', '=', 'City']
                    ]
            }
        });

        cur_frm.set_query("district_delivery", function () {
            return {
                    "filters": [
                    ['Territory', 'type', '=', 'District']
                    ]
            }
        });

        cur_frm.set_query("subdistrict_delivery", function () {
            return {
                    "filters": [
                    ['Territory', 'type', '=', 'Subdistrict']
                    ]
            }
        });
	},
});
