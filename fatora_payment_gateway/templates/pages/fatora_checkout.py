# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE
import json, requests

import frappe
from frappe import _
from urllib.parse import urlencode
from frappe.utils import (
	# call_hook_method,
	# cint,
	# cstr,
	# flt,
	# get_request_site_address,
	get_url,
)

# from payments.payment_gateways.doctype.paytm_settings.paytm_settings import (
# 	get_paytm_config,
# 	get_paytm_params,
# )
from payments.utils.utils import validate_integration_request


def get_context(context):
	context.no_cache = 1
	# paytm_config = get_paytm_config()


	redirect_url = ""

	fatora_settings = frappe.get_single("Fatora Settings")

	api_key = fatora_settings.get("live_api_key", "")
	if fatora_settings.get("use_sandbox", 1):
		api_key = fatora_settings.get("test_api_key", "")
	if fatora_settings.get("enable_live", 1):
		api_key = fatora_settings.get("live_api_key", "")

	url = "https://api.fatora.io/v1/payments/checkout"

	payload = json.dumps({
		"amount": frappe.form_dict.get("amount", 0),
		"currency": frappe.form_dict.get("currency", ""),
		"order_id": frappe.form_dict.get("order_id", ""),
		"client": {
			"name": frappe.form_dict.get("payer_name", ""),
			"phone": "",
			"email": frappe.form_dict.get("payer_email", ""),
			"address": "",
			"note": ""
		},
		"language": "ar",
		# "success_url": get_url(f"./fatora_checkout_response?status=success&order_id={frappe.form_dict.get("order_id", "")}"),
		# "failure_url": get_url(f"./fatora_checkout_response?status=error&order_id={frappe.form_dict.get("order_id", "")}"),
		"success_url": get_url(f"./fatora_checkout_response?status=success"),
		"failure_url": get_url(f"./fatora_checkout_response?status=error"),
		"fcm_token": "",
		"save_token": True,
		"note": frappe.form_dict.get("description", "")
	})

	headers = {
		'api_key': api_key,
		'Content-Type': 'application/json',
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	response_text = response.text
	response_text_json = json.loads(response_text)
	response_text_json_result= response_text_json.get("result")
	redirect_url = response_text_json_result.get("checkout_url")
	context.url = redirect_url
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
