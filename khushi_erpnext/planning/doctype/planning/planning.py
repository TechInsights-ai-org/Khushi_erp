# Copyright (c) 2024, TechInsights and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Planning(Document):
	def update_total_output(self):
		_output = ((float(self.total_sheets) * float(self.ups)) - (float(self.total_sheets) * float(self.ups) * float(self.wastage))) / float(self.packing)
		self.output = _output
		frappe.msgprint(_output)

	def before_save(self):
		self.update_total_output()

	def before_validate(self):
		self.update_total_output()
