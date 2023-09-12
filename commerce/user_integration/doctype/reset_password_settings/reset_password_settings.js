// Copyright (c) 2021, DAS and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reset Password Settings', {
	onload:function(frm){
		cur_frm.events.set_instruction(frm)
		
	},
	set_instruction:function(frm){
		cur_frm.set_df_property("instruction","options",`<b> Here step-step to create Reset Password Integration </b><br>
		1. Setup your email account on doctype Email Account. <br>
		2. Fill data on this doctype <br>
		3. To setup style please see doctype Application Info <br>
		3. Generate reset_password.html by clicking button bellow<br>
		4. Generate notification by clicking button below<br>
		5. Upload <code> reset_password.html </code> to your web destination <br>
		6. Done.
		`)

		var base_url = "{{base_url}}";
		var module = "{{module}}";
		if (cur_frm.doc.url_frappe){
			base_url = cur_frm.doc.url_frappe
		}
		if (cur_frm.doc.module_name){
			module = cur_frm.doc.module_name
		}

		cur_frm.set_df_property("api_instruction","options",`
		<b> Functional Request Reset Password</b> <br>
		 - (Step 1) Customer melakukan klik tombol lalu memasukkan email <br>
		System akan melakukan <b>Request Reset Password</b> : `+base_url+module+`.user_integration.api.api_reset_password.request_reset_password
		Dengan Body : {"email_id":"example@mail.com"}
		<br>
		 - (Step 2) Customer mendapatkan email lalu redirect ke web <br>
		System akan melakukan <b>Reset Password</b> : `+base_url+module+`.user_integration.api.api_reset_password.reset_password
		Dengan Body : {
			"user":"example@mail.com",
			"key":"ILDNFVMGVQDA",
			"password" : "asd1234"
		}
		<br> <br>
		<b>Reset Password</b> <br>
		<b> Style </b> : `+base_url+module+`.user_integration.api.api_reset_password.get_style_reset_password
		
		`)

	},
	generate_resetpassword(){
		window.open('/api/method/commerce.user_integration.api.api_reset_password.download_html', '_blank')
	}
	// refresh: function(frm) {

	// }
});
