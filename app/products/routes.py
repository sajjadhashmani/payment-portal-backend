from flask import Blueprint, jsonify, request

from app.products.controller import ProductController

products = Blueprint("products", __name__)

@products.route("/products/getProductList", methods=["GET"])
def get_customers():
    """API route to get all customers."""
    try:
        products_list = ProductController.list_products()
        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @products.route("/products/<int:product_id>", methods=["GET"])
# def get_customer(product_id):
#     """API route to get a customer by ID."""
#     try:
#         customer = ProductController.get_product_by_id(product_id)
#         return jsonify(customer), 200
#     except ValueError as e:
#         return jsonify({"error": str(e)}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@products.route("/products/addProduct", methods=["POST"])
def add_product():
    """API route to add a new customer."""
    try:
        data = request.json
        response = ProductController.create_product(data)
        if response["ok"]:
            return jsonify({
                "message": "Product added successfully",
                "product_id": response["product_id"]
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
