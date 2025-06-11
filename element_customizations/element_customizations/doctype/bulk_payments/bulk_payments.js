// Copyright (c) 2025, Element Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Payments', {
	refresh: function (frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Queue Submit'), function () {
				frappe.call({
					method: 'element_customizations.element_customizations.doctype.bulk_payments.bulk_payments.queue_submit',
					args: {
						docname: frm.doc.name
					},
					callback: function (r) {
						return false;
					}
				});
			})
		}
	},
	get_bank_transactions: function (frm) {
		if (frm.doc.bank_account) {
			frappe.call({
				method: 'element_customizations.element_customizations.doctype.bulk_payments.bulk_payments.get_bank_transactions',
				args: {
					bank_account: frm.doc.bank_account,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date,
					search_queries: frm.doc.search_queries
				},
				callback: function (r) {
					if (r.message && Array.isArray(r.message)) {
						frm.clear_table('bank_transactions');
						r.message.forEach(function (row) {
							frm.add_child('bank_transactions', {
								bank_transaction: row.name,
								date: row.date,
								withdrawal: row.withdrawal,
								description: row.description
							});
						});
						frm.refresh_field('bank_transactions');
					}
				}
			});
		} else {
			frappe.msgprint(__('Please select a bank account.'));
		}

	}
});
