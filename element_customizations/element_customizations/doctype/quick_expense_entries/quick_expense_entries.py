# -*- coding: utf-8 -*-
# Copyright (c) 2020, Element Labs and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class QuickExpenseEntries(Document):
	def validate(self):
		pass

	def on_submit(self):
		if (self.description):
			item_name = self.description
		else: 
			item_name = self.expense_head

		doc = frappe.get_doc({
			"doctype" 	: "Purchase Invoice",
			"supplier"	: self.supplier,
			"is_paid"	: 1,
			"cash_bank_account"	: self.paid_from,
			"items": [{
				"item_name" : self.description,
				"uom"		: "Nos",
				"qty"		: 1,
				"rate"		: self.amount,
				"expense_account": self.expense_head,
				"project"	: self.project
			}]
		})

		doc.save()
		doc.submit()

		self.purchase_invoice = doc.name

	def on_cancel(self):
		pinv = frappe.get_doc('Purchase Invoice',self.purchase_invoice)
		pinv.docstatus = 2
		pinv.save()

		
	def on_trash(self):
		pi = self.purchase_invoice
		self.purchase_invoice = ""	
		frappe.get_doc('Purchase Invoice',pi).delete()



