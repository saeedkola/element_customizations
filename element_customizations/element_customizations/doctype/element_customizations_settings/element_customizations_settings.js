// Copyright (c) 2020, Element Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Element Customizations Settings', {
	// refresh: function(frm) {

	// }
	setup: function(frm){		
		frm.set_query("qe_cash_bank_account",function(){
			return {
				filters :[
					["Account", "account_type", "in",["Bank", "Cash"]],
					["Account", "is_group", "=", 0]	
				]
			}
		});

		frm.set_query("ce_cash_bank_account",function(){
			return {
				filters :[
					["Account", "root_type", "in",["Expense"]],
					["Account", "is_group", "=", 0]	
				]
			}
		});


	}
});
