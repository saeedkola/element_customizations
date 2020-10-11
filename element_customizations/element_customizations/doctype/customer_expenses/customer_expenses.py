# -*- coding: utf-8 -*-
# Copyright (c) 2020, Element Labs and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomerExpenses(Document):

	def before_submit(self):
		if (self.description):
			remarks = item_name = self.description
		else: 
			item_name = self.expense_head
			remarks = "No remarks"

		pinv = frappe.get_doc({
			"doctype" 	: "Purchase Invoice",
			"supplier"	: self.supplier,
			"is_paid"	: 1,
			"cash_bank_account"	: self.paid_from,
			"items": [{
				"item_name" : item_name,
				"uom"		: "Nos",
				"qty"		: 1,
				"rate"		: self.amount,
				"expense_account": self.expense_head,
				"project"	: self.project
			}],
			"remarks" : remarks
		})

		pinv.save()
		pinv.submit()

		sinv = frappe.get_doc({
			"doctype"	: "Sales Invoice",
			"customer"	: self.customer,
			"items"		: [{
				"item_name"	: item_name,
				"description"	: item_name,
				"uom"		: "Nos",
				"qty"		: 1,
				"conversion_factor"	: 1,
				"rate"		: self.amount,
				"income_account": self.expense_head,
				"project"	: self.project
			}],
			remarks: "remarks"
		})

		sinv.save()
		sinv.submit()

		self.purchase_invoice = pinv.name
		self.sales_invoice = sinv.name

	def on_cancel(self):
		if self.purchase_invoice:
			pinv = frappe.get_doc('Purchase Invoice',self.purchase_invoice)
			pinv.docstatus = 2
			pinv.save()

		if self.sales_invoice:
			sinv = frappe.get_doc('Sales Invoice',self.sales_invoice)
			sinv.docstatus = 2
			sinv.save()
		
	def on_trash(self):
		if self.purchase_invoice:
			pi = self.purchase_invoice
			self.purchase_invoice = ""
			frappe.get_doc('Purchase Invoice',pi).delete()
		
		if self.sales_invoice: 
			si = self.sales_invoice	
			self.sales_invoice = ""
			frappe.get_doc('Sales Invoice',si).delete()
