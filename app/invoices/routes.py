from flask import Blueprint, jsonify, request

from app.invoices.controller import InvoiceController
from app.invoices.invoice import Invoice

invoices = Blueprint("invoices", __name__)

@invoices.route("/invoices/addInvoice", methods=["POST"])
def add_invoice():
    """API route to add a new customer."""
    try:
        data = request.json
        invoiceItemData = data["rows"]
        response = InvoiceController.create_invoice(data)
        if response["ok"]:
            InvoiceController.add_invoice_items(invoiceItemData, response['invoice_id'])
            return jsonify({
                "message": "Invoice added successfully",
                "invoice_id": response["invoice_id"]
            }), 201
        else:
            return jsonify({
                "errorCode": response["errorCode"],
                "error": response["error"]
            }), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoices.route("/invoices/nextInvoiceNumber", methods=["GET"])
def next_invoice_number():
    try:
        next_invoice_number = InvoiceController.next_invoice_number()
        return jsonify(next_invoice_number), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoices.route("/invoices/getInvoiceList", methods=["GET"])
def get_invoices():
    try:
        invoice_list = InvoiceController.list_invoices()
        return jsonify(invoice_list), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
