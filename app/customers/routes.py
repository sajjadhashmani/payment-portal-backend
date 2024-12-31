from flask import Blueprint, jsonify, request

from app.customers.controller import CustomerController

customers = Blueprint("customers", __name__)

@customers.route("/customers/getCustomerList", methods=["GET"])
def get_customers():
    """API route to get all customers."""
    try:
        customers_list = CustomerController.list_customers()
        return jsonify(customers_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers.route("/customers/getCustomerNames", methods=["GET"])
def get_customer_names():
    """API route to get all customers names."""
    try:
        customer_names_list = CustomerController.get_customer_names()
        return jsonify(customer_names_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """API route to get a customer by ID."""
    try:
        customer = CustomerController.get_customer_by_id(customer_id)
        return jsonify(customer), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customers.route("/customers/addCustomer", methods=["POST"])
def add_customer():
    """API route to add a new customer."""
    try:
        data = request.json
        response = CustomerController.create_customer(data)
        if response["ok"]:
            return jsonify({
                "message": "Customer added successfully",
                "customer_id": response["customer_id"]
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
