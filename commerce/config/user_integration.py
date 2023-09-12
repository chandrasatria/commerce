# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("User Integration"),
			"items": [
				{
					"type": "doctype",
					"name": "Reset Password"
				},
				{
					"type": "doctype",
					"name": "Application Info"
				},
				{
					"type": "doctype",
					"name": "Reset Password Settings"
				},
				{
					"type": "doctype",
					"name": "Media Social"
				},
			
			]
		},
	
	]