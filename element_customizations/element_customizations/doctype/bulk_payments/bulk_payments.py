# Copyright (c) 2025, Element Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe import _

class BulkPayments(Document):
	def before_submit(self):
		#create payment entry against each bank transaction against doc.supplier
		if self.payment_type == "Payment Entry":
			for bank_transaction in self.bank_transactions:
				if bank_transaction.withdrawal > 0:
					payment_entry = frappe.new_doc("Payment Entry")
					payment_entry.posting_date = bank_transaction.date
					payment_entry.payment_type = "Pay"
					payment_entry.party_type = "Supplier"
					payment_entry.party = self.supplier
					payment_entry.paid_from = self.paid_from
					# payment_entry.paid_to = self.supplier
					payment_entry.paid_amount = bank_transaction.withdrawal
					payment_entry.received_amount = bank_transaction.withdrawal
					payment_entry.reference_no = bank_transaction.description
					payment_entry.reference_date = bank_transaction.date
					
					payment_entry.insert()
					bank_transaction.payment_entry = payment_entry.name
					payment_entry.submit()
					#reconsile bank transaction
					bt = frappe.get_doc("Bank Transaction", bank_transaction.bank_transaction)
					# bt.status = "Reconciled"
					bt.append("payment_entries", {
						"payment_document": "Payment Entry",
						"payment_entry": payment_entry.name,
						"allocated_amount": bank_transaction.withdrawal
					})
					bt.save()
		elif self.payment_type == "Journal Entry":
			for bank_transaction in self.bank_transactions:
				if bank_transaction.withdrawal > 0:
					journal_entry = frappe.new_doc("Journal Entry")
					journal_entry.posting_date = bank_transaction.date
					journal_entry.voucher_type = "Journal Entry"

					journal_entry.user_remark = bank_transaction.description
					
					# Debit the supplier account
					journal_entry.append("accounts", {
						"account": self.debit_to,

						"debit_in_account_currency": bank_transaction.withdrawal,
					})
					
					# Credit the bank account
					journal_entry.append("accounts", {
						"account": self.paid_from,
						"credit_in_account_currency": bank_transaction.withdrawal,
						
					})
					
					journal_entry.insert()
					journal_entry.submit()
					
					bank_transaction.journal_entry = journal_entry.name
					
					bt = frappe.get_doc("Bank Transaction", bank_transaction.bank_transaction)
					# bt.status = "Reconciled"
					bt.append("payment_entries", {
						"payment_document": "Journal Entry",
						"payment_entry": journal_entry.name,
						"allocated_amount": bank_transaction.withdrawal
					})
					bt.save()
	def on_cancel(self):
		#cancel payment entry against each bank transaction against doc.supplier
		if self.payment_type == "Payment Entry":
			for bank_transaction in self.bank_transactions:
				if bank_transaction.withdrawal > 0 and bank_transaction.payment_entry:
					payment_entry = frappe.get_doc("Payment Entry", bank_transaction.payment_entry)
					payment_entry.cancel()
					# bt = frappe.get_doc("Bank Transaction", bank_transaction.bank_transaction)
					# bt.remove_payment_entry(bank_transaction.payment_entry)
					# bt.save()
		elif self.payment_type == "Journal Entry":
			for bank_transaction in self.bank_transactions:
				if bank_transaction.withdrawal > 0 and bank_transaction.journal_entry:
					journal_entry = frappe.get_doc("Journal Entry", bank_transaction.journal_entry)
					journal_entry.cancel()
					# bt = frappe.get_doc("Bank Transaction", bank_transaction.bank_transaction)
					# bt.remove_payment_entry(bank_transaction.journal_entry)
					# bt.save()
	
@frappe.whitelist()
def queue_submit(docname):
	"""
	Queue the submission of a Bulk Payments document.
	"""
	doc = frappe.get_doc("Bulk Payments", docname)
	if doc.docstatus == 0:
		doc.queue_action(
			action="submit",
			queue="long",
			timeout=600
		)
		frappe.msgprint(_("Document {0} has been queued for submission.").format(docname))
	else:
		frappe.throw(_("Document {0} is already submitted.").format(docname))
@frappe.whitelist()
def get_bank_transactions(bank_account, from_date, to_date,search_queries):
	"""
	Fetch bank transactions for a given bank account within a date range.
	"""
	or_filters = []
	search_queries = json.loads(search_queries) 
	for query in search_queries:
		or_filters.append(
			["description", "like", f"%{query['search_query']}%"]
		)
			
		
	return frappe.get_all(
		"Bank Transaction",
		filters=[
			["bank_account", "=", bank_account],
			['withdrawal', ">", 0],
			["date", ">=", from_date],
			["date", "<=", to_date],
			["docstatus", "=", 1],
			['status',"!=", "Reconciled"]
		],
		or_filters=or_filters,
		fields=["name", "date", "withdrawal", "description"]
	)