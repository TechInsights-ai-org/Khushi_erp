// Copyright (c) 2024, TechInsights and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order VS Stock Balance Report"] = {
	"filters": [
		{label: "Company", fieldname: "company", fieldtype: "Link", options: "Company"},
		{label: "From Date", fieldname: "f_date", fieldtype: "Date"},
		{label: "To Date", fieldname: "t_date", fieldtype: "Date"},
		{label: "Sales Order", fieldname: "sales_order", fieldtype: "Link", options: "Sales Order"},
		{label: "Warehouse", fieldname: "warehouse", fieldtype: "Link", options: 'Warehouse'},
		{label: "Status", fieldname: "status", fieldtype: "MultiSelectList", options: [{value: "Draft", description:""},
				{value: "On Hold", description:""}, {value: "To Deliver and Bill", description:""},
				{value: "To Bill", description:""}, {value: "To Deliver", description:""},
				{value: "Completed", description:""}, {value: "Cancelled", description:""},
				{value: "Closed", description:""}]
		},
		{label: "Group By Item", fieldname: "group_by_item", fieldtype: "Check"},
	],
	 "formatter":function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id === "qty_to_deliver" &&
				data["qty_to_deliver"] > data["stock_balance"] + data["subcontract_qty_to_receive"] ||
				(data["subcontract_qty_to_receive"] === 0 && column.id === "qty_to_deliver" &&
				data["qty_to_deliver"] > data["stock_balance"] + data["purchase_qty"])) {
			value = "<span style='color:red!important;font-weight:bold'>" + value + "</span>";
		}
		if (column.id === "qty_to_deliver" &&
				data["qty_to_deliver"] > data["stock_balance"] &&
				data["qty_to_deliver"] < data["stock_balance"] + data["subcontract_qty_to_receive"] ||
				(data["subcontract_qty_to_receive"] === 0 && column.id === "qty_to_deliver" &&
				data["qty_to_deliver"] > data["stock_balance"] &&
				data["qty_to_deliver"] < data["stock_balance"] + data["purchase_qty"])) {
			value = "<span style='color:darkorange!important;font-weight:bold'>" + value + "</span>";
		}
		return value;
    }
};
