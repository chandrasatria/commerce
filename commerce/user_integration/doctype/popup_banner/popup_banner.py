# -*- coding: utf-8 -*-
# Copyright (c) 2020, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PopupBanner(Document):
	def validate(self):
		self.alert_user_when_overlap_with_other_banner()
		


	# -- end of hooks
	def alert_user_when_overlap_with_other_banner(self):
		now = frappe.utils.nowdate()
		
		self_name = ""
		if self_name:
			self_name = self.name
		fga_popup_banner = frappe.get_all("Popup Banner",fields="*", filters=[["publish_from","<=",now],["publish_until",">=", now],["published","=",1],["name","!=",self_name]])
		if len(fga_popup_banner) > 0:
			string_overlapped_with = ""
			for item in fga_popup_banner:
				string_overlapped_with += "<br> <a href='/desk#Form/Popup%20Banner/{name}'> {title} </a>".format(name = item["name"], title = item["title"])

			frappe.msgprint("Oops, your popup banner is overlapped with: {}".format(string_overlapped_with), title="Overlapped Banner Schedule", indicator="orange")