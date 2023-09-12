# -*- coding: utf-8 -*-
# Copyright (c) 2021, DAS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class VerificationEmail(Document):
	def before_save(self):
		if not self.token:
			self.token = randomString(12)


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    import random, string
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
