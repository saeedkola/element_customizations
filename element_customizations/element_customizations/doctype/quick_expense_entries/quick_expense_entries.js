// Copyright (c) 2020, Element Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Quick Expense Entries', {
	// refresh: function(frm) {

	// }
	setup: function(frm){
		frm.set_query("expense_head",function(){
			return {
				filters:[
					["Account", "root_type", "in",["Expense"]],
					["Account", "is_group", "=", 0]
				]
			}
		});
		frm.set_query("paid_from",function(){
			return {
				filters :[
					["Account", "account_type", "in",["Bank", "Cash"]],
					["Account", "is_group", "=", 0]	
				]
			}
		});

		frappe.model.get_value('Element Customizations Settings', {'name': 'Element Customizations Settings'}, null, function(d) {
		    if (d.qe_default_supplier) {
		    	frm.set_value("supplier", d.qe_default_supplier);
		    }
		    if(d.qe_cash_bank_account){
		    	frm.set_value("paid_from", d.qe_cash_bank_account);
		    }
		});	
	}
});
