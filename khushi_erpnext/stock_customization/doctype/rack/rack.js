// Copyright (c) 2024, TechInsights and contributors
// For license information, please see license.txt

frappe.ui.form.on("Rack", {
	refresh(frm) {
        if (!frm.is_new()) {
            if (frm.has_perm("write")) {
                let enable_toggle = frm.doc.disabled ? "Enable" : "Disable";
                frm.add_custom_button(__(enable_toggle), () => {
                    frm.set_value("disabled", 1 - frm.doc.disabled);
                    frm.save();
                });
            }
        }
	},
});
