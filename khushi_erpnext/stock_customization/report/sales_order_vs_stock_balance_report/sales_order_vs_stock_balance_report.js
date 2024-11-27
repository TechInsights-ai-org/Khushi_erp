// Copyright (c) 2024, TechInsights and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order VS Stock Balance Report"] = {
	"filters": [
		{label: "Company", fieldname: "company", fieldtype: "Link", options: "Company"},
		{label: "From Date", fieldname: "f_date", fieldtype: "Date"},
		{label: "To Date", fieldname: "t_date", fieldtype: "Date"},
		{label: "Sales Order", fieldname: "sales_order", fieldtype: "Link", options: "Sales Order"},
		{label: "Warehouse", fieldname: "warehouse", fieldtype: "Link", options: 'Warehouse'},
		{label: "Status", fieldname: "status", fieldtype: "MultiSelectList","options": "Entity",
			"get_data": function(txt) {
				return ["Draft", "On Hold", "To Deliver and Bill", "To Bill", "To Deliver", "Completed", "Cancelled", "Closed"];
			}
		}
	]
};
