# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{			
			"label": _("Element Customizations"),
			"items": [
				{
					"type": "doctype",
					"name": "Quick Expense Entries"
				},
				{
					"type": "doctype",
					"name": "Customer Expenses"
				}
			]
		},
		{
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Element Customizations Settings"
				}
			]
		}
	]
