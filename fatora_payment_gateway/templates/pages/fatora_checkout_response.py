# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import json, requests

import frappe
from frappe import _
from urllib.parse import urlencode

# from payments.payment_gateways.doctype.paytm_settings.paytm_settings import (
# 	get_paytm_config,
# 	get_paytm_params,
# )
from payments.utils.utils import validate_integration_request


def get_context(context):
	context.no_cache = 1
	# paytm_config = get_paytm_config()
	order_id = frappe.form_dict.get("order_id", 0)

	request = frappe.get_doc("Integration Request", order_id)
	context.data = request.data
	status = frappe.form_dict.get("status", "error")
	context.status = status
	# transaction_data = frappe._dict(json.loads(request.data))
	# redirect_to = transaction_data.get("redirect_to") or None
	# redirect_message = transaction_data.get("redirect_message") or None

	# if transaction_data.reference_doctype and transaction_data.reference_docname:
	# 		custom_redirect_to = None
	# 		try:
	# 			custom_redirect_to = frappe.get_doc(
	# 				transaction_data.reference_doctype, transaction_data.reference_docname
	# 			).run_method("on_payment_authorized", "Completed")
	# 			request.db_set("status", "Completed")
	# 		except Exception:
	# 			request.db_set("status", "Failed")
	# 			frappe.log_error(frappe.get_traceback())

	# 		if custom_redirect_to:
	# 			redirect_to = custom_redirect_to

	# 		redirect_url = "payment-success"

	# if frappe.form_dict.get("status", "error") == "success":
		
	# 	context.reference_docname = transaction_data.reference_docname
	# 	# test1 = frappe.get_doc(
	# 	# 			transaction_data.reference_doctype, transaction_data.reference_docname
	# 	# 		).run_method("on_payment_authorized", "Completed")
	# 	test1 = frappe.get_doc(
	# 				transaction_data.reference_doctype, transaction_data.reference_docname
	# 			).run_method("create_payment_entry", )
	# 	context.test1 = test1
	# 	if transaction_data.reference_doctype and transaction_data.reference_docname:
	# 		custom_redirect_to = None
	# 		try:
	# 			# custom_redirect_to = frappe.get_doc(
	# 			# 	transaction_data.reference_doctype, transaction_data.reference_docname
	# 			# ).run_method("on_payment_authorized", "Completed")
	# 			request.db_set("status", "Completed")
	# 		except Exception:
	# 			request.db_set("status", "Failed")
	# 			frappe.log_error(frappe.get_traceback())

	# 		if custom_redirect_to:
	# 			redirect_to = custom_redirect_to

	# 		redirect_url = "payment-success"
	# else:
	# 	request.db_set("status", "Failed")
	# 	redirect_url = "payment-failed"

	# if redirect_to:
	# 	redirect_url += "?" + urlencode({"redirect_to": redirect_to})
	# if redirect_message:
	# 	redirect_url += "&" + urlencode({"redirect_message": redirect_message})

	# frappe.local.response["type"] = "redirect"
	# frappe.local.response["location"] = redirect_url

	# context.url = redirect_url

	context.csrf_token = frappe.sessions.get_csrf_token()
	context.order_id = order_id

	html_str = ""

	if status=="success":
		html_str = '''<div style="max-width:420px;margin:40px auto;padding:25px;
						background:#f0fff4;border:1px solid #b7ebc6;
						border-radius:8px;font-family:Arial,Helvetica,sans-serif;
						text-align:center;">

						<div style="font-size:48px;color:#28a745;line-height:1;">
							✓
						</div>

						<h2 style="margin:15px 0 10px;color:#155724;">
							Payment Successful
						</h2>

						<p style="margin:0;font-size:14px;color:#155724;">
							Thank you! Your payment has been processed successfully.
						</p>

						</div>'''
	else :
		html_str = '''<div style="max-width:420px;margin:40px auto;padding:25px;
						background:#fff5f5;border:1px solid #f5c2c7;
						border-radius:8px;font-family:Arial,Helvetica,sans-serif;
						text-align:center;">

						<div style="font-size:48px;color:#dc3545;line-height:1;">
							✕
						</div>

						<h2 style="margin:15px 0 10px;color:#842029;">
							Payment Failed
						</h2>

						<p style="margin:0;font-size:14px;color:#842029;">
							Sorry! Your payment could not be processed.
						</p>

						</div>
						'''
						
	context.html_str = html_str




	# redirect_url = ""

	# fatora_settings = frappe.get_single("Fatora Settings")

	# api_key = fatora_settings.get("live_api_key", "")
	# if fatora_settings.get("use_sandbox", 1):
	# 	api_key = fatora_settings.get("test_api_key", "")

	# url = "https://api.fatora.io/v1/payments/checkout"

	# payload = json.dumps({
	# 	"amount": frappe.form_dict.get("amount", 0),
	# 	"currency": frappe.form_dict.get("currency", ""),
	# 	"order_id": frappe.form_dict.get("order_id", ""),
	# 	"client": {
	# 		"name": frappe.form_dict.get("payer_name", ""),
	# 		"phone": "",
	# 		"email": frappe.form_dict.get("payer_email1", "shyamsundersahani01@gmail.com"),
	# 		"address": "",
	# 		"note": ""
	# 	},
	# 	"language": "ar",
	# 	"success_url": "http://176.57.150.65/app",
	# 	"failure_url": "http://176.57.150.65/app",
	# 	"fcm_token": "",
	# 	"save_token": True,
	# 	"note": frappe.form_dict.get("description", "")
	# })

	# headers = {
	# 	'api_key': api_key,
	# 	'Content-Type': 'application/json',
	# }

	# response = requests.request("POST", url, headers=headers, data=payload)

	# response_text = response.text
	# response_text_json = json.loads(response_text)
	# response_text_json_result= response_text_json.get("result")
	# redirect_url = response_text_json_result.get("checkout_url")
	# context.url = redirect_url
	# context.url = response.text

	# try:
	# 	# validate_integration_request(frappe.form_dict["order_id"])

	# 	# doc = frappe.get_doc("Integration Request", frappe.form_dict["order_id"])

	# 	# context.payment_details = get_paytm_params(json.loads(doc.data), doc.name, paytm_config)

	# 	# context.url = paytm_config.url
	# 	redirect_url = ""

	# 	fatora_settings = frappe.get_single("Fatora Settings")

	# 	api_key = fatora_settings.get("live_api_key", "")
	# 	if fatora_settings.get("use_sandbox", 1):
	# 		api_key = fatora_settings.get("test_api_key", "")

	# 	url = "https://api.fatora.io/v1/payments/checkout"

	# 	payload = json.dumps({
	# 		"amount": frappe.form_dict.get("amount", 0),
	# 		"currency": frappe.form_dict.get("currency", ""),
	# 		"order_id": frappe.form_dict.get("order_id", ""),
	# 		"client": {
	# 			"name": frappe.form_dict.get("payer_name", ""),
	# 			"phone": "",
	# 			"email": frappe.form_dict.get("payer_email", ""),
	# 			"address": "",
	# 			"note": ""
	# 		},
	# 		"language": "ar",
	# 		"success_url": "http://176.57.150.65/app",
	# 		"failure_url": "http://176.57.150.65/app",
	# 		"fcm_token": "",
	# 		"save_token": True,
	# 		"note": frappe.form_dict.get("description", "")
	# 	})

	# 	headers = {
	# 		'api_key': api_key,
	# 		'Content-Type': 'application/json',
	# 	}

	# 	response = requests.request("POST", url, headers=headers, data=payload)

	# 	response_text = response.text
	# 	response_text_json = json.dumps(response_text)
	# 	response_text_json_result= response_text_json.get("result")
	# 	redirect_url = response_text_json_result.get("checkout_url")
	# 	context.url = redirect_url

	# except Exception:
	# 	frappe.log_error()
	# 	frappe.redirect_to_message(
	# 		_("Invalid Token"),
	# 		_("Seems token you are using is invalid!"),
	# 		http_status_code=400,
	# 		indicator_color="red",
	# 	)

	# 	frappe.local.flags.redirect_location = frappe.local.response.location
	# 	raise frappe.Redirect
