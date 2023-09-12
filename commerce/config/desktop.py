# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Commerce",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Commerce")
		},
		{
			"module_name": "User Integration",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("User Integration")
		}
	]
