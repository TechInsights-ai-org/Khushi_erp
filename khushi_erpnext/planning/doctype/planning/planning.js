// Copyright (c) 2024, TechInsights and contributors
// For license information, please see license.txt

frappe.ui.form.on("Planning", {
	refresh(frm) {

	},

});
frappe.ui.form.on("Costing Child", {
    count: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        frm.call({
            doc: frm.doc,
            method: "on_costing_change",
            freeze: true,
            callback: function (r) {
            }
        })
    }
});


