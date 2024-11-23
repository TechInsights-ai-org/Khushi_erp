# Copyright (c) 2024, TechInsights and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Planning(Document):
	def update_total_output(self) -> None:
		if float(self.packing) == 0:
			frappe.msgprint("Packing value cannot be zero.")
			return
		_output: float = ((float(self.total_sheets) * float(self.ups)) - (float(self.total_sheets) * float(self.ups) * float(self.wastage))) / float(self.packing)
		self.total_qnty = _output

	def get_sum(self, table: list, field: str) -> float | int:
		return sum([getattr(table_row, field) if getattr(table_row, field) else 0 for table_row in table])

	def update_investment_details(self):
		costing_details : list = self.costing_sub_detail
		fix_cost_bef_tax: float = self.fix_cost_bef_tax or 0
		fix_cost_with_gst: float = self.fix_cost_with_tax or 0
		if costing_details:
			self.total_investment_bef_gst: float | int = self.get_sum(costing_details,"amt_bef_tax")
			self.total_investment_with_gst: float | int = self.get_sum(costing_details,"total_amt")
			self.input_gst: float | int = self.get_sum(costing_details,"gst_amount")
			self.fix_cost_bef_tax: float | int = self.total_investment_bef_gst - (fix_cost_with_gst + fix_cost_bef_tax)

	def update_cost_details(self):
		self.total_investment_with_gst = 0
		# TODO


	def before_save(self):
		self.update_total_output()
		self.update_investment_details()
		self.update_cost_details()


