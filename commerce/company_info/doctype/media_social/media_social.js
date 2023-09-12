// Copyright (c) 2020, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Media Social', {
	refresh: function(frm) {
		document.querySelectorAll("[data-fieldname='facebook']")[1].style.height = "50px";
		document.querySelectorAll("[data-fieldname='instagram']")[1].style.height = "50px";
		document.querySelectorAll("[data-fieldname='twitter']")[1].style.height = "50px";
		document.querySelectorAll("[data-fieldname='youtube']")[1].style.height = "50px";
	}
});

