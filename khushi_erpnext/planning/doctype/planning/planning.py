# Copyright (c) 2024, TechInsights and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Planning(Document):

	def update_total_output(self) -> None:
		""" Calculates the total quantity (output) """
		if not self.packing:
			self.output = 0
			return
		total_output_without_wastage = (float(self.total_sheets) * float(self.ups)) / float(self.packing)
		total_wastage = total_output_without_wastage * (float(self.wastage) / 100)
		self.output = total_output_without_wastage - total_wastage


	def get_costing_value(self,field: str, fc:bool = False , vc:bool = False) -> float | int:
		"""
		Retrieves the total cost value for a specified field in the costing child table.
		It aggregates values based on the field name and cost type (Fixed or Variable cost).
		Args:
		    field (str): The field name for which the costing value is calculated.
		    fc (bool): If True, Return only SUM OF Fixed Costs (FC) .
		    vc (bool): If True,Return only SUM OF Variable Costs (VC).
		Returns:
		    float | int: The calculated cost value (sum of the relevant field values).
		"""
		fc_total, vc_total, total = 0, 0, 0
		costing_details : list = self.costing_sub_detail
		for costing_detail in costing_details:
			if hasattr(costing_detail, field) and costing_detail.count == 1:
				value: int = getattr(costing_detail, field) or 0
				if costing_detail.cost_type == "FC":
					fc_total += value
				elif costing_detail.cost_type == "VC":
					vc_total += value
				total += value
		if fc:
			return fc_total
		elif vc:
			return vc_total
		return total

	def update_investment(self):
		""" Updates the value for the fields that are in Investment Tab """
		self.total_investment_bef_gst: float  = self.get_costing_value("amt_bef_tax")
		self.total_investment_with_gst: float  = self.get_costing_value("total_amt")
		self.fix_cost_bef_tax: float  = self.total_investment_bef_gst - self.get_costing_value("amt_bef_tax",vc=True ,fc=False)
		self.fix_cost_with_tax: float  = self.total_investment_with_gst - self.get_costing_value("total_amt",vc=True ,fc=False)
		self.variable_cost_bef_tax: float  = self.total_investment_bef_gst -  self.get_costing_value("amt_bef_tax",fc=True , vc = False)
		self.variable_cost_with_tax: float  = self.total_investment_with_gst - self.get_costing_value("total_amt",fc=True , vc = False)
		self.input_gst: float = self.get_costing_value("gst_amount")

	def update_cost_details(self):
		""" Updates the value for the fields that are in cost details Tab """
		if self.output == 0 or self.output is None:
			return
		self.cost_with_gst: float = self.total_investment_with_gst / self.output
		self.cost_without_gst: float = self.total_investment_bef_gst / self.output
		self.fix_cost_with_gst: float = self.fix_cost_with_tax / self.output
		self.fix_cost_without_gst:  float = self.fix_cost_bef_tax / self.output

	def update_cost_table(self):
		"""Updates the costing sub-details child table"""
		cost_table : list = self.costing_sub_detail
		if cost_table:
			for cost_data in cost_table:
				qnty: int | float = cost_data.qnty or 0
				s1: int | float = cost_data.s1 or 0
				s2: int | float = cost_data.s2 or 0
				weight: int | float = cost_data.weight or 0
				rate: int | float = cost_data.rate or 0
				rate_unit: int | float = cost_data.rate_unit or 0
				cost_data.amt_bef_tax: float = 0.00
				if cost_data.rate_unit and cost_data.rate_unit !=0 :
					cost_data.amt_bef_tax: float = (qnty * s1 * s2 * weight * rate) / rate_unit
				if cost_data.gst:
					gst_percentage: int | float = eval(cost_data.gst.replace("%",""))
					gst_percentage = gst_percentage /100
					cost_data.gst_amount: float = cost_data.amt_bef_tax * gst_percentage
				if not cost_data.gst_amount:
					cost_data.gst_amount = 0
				cost_data.total_amt: float = cost_data.amt_bef_tax + cost_data.gst_amount

	def update_roi(self):
		if self.cost_without_gst != 0:
			self.roi_without_tax: float = ((self.net_sales_rate_without_tax/self.cost_without_gst) - 1) * 100
		if self.cost_with_gst != 0:
			self.roi_with_tax: float = ((self.net_sales_rate_with_tax/self.cost_with_gst) -1) * 100
		if self.net_sales_rate_with_tax:
			self.ros_with_tax: float = (1 - (self.cost_with_gst/self.net_sales_rate_with_tax)) * 100
		if self.net_sales_rate_without_tax:
			self.ros_without_tax: float = (1 - (self.cost_without_gst/self.net_sales_rate_without_tax)) * 100

	def update_investment_and_cost_details(self):
		self.update_investment()
		self.update_cost_details()

	def before_save(self):
		self.update_cost_table()
		self.update_total_output()
		self.update_investment_and_cost_details()
		self.update_roi()


	@frappe.whitelist()
	def on_costing_change(self):
		self.update_cost_table()
		self.update_investment_and_cost_details()
		self.update_roi()






