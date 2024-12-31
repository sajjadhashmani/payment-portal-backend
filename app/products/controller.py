from app.products.product import Product

class ProductController:
    """Controller for managing customer-related business logic."""

    @staticmethod
    def list_products():
        """Controller to list all customers."""
        products = Product.get_all()
        return [
            {
                "id": product["product_id"],
                "name": product["name"],
                "description": product["description"],
                "price": product["price"]
            }
            for product in products
        ]

    # @staticmethod
    # def get_product_by_id(customer_id):
    #     """Controller to retrieve a customer by ID."""
    #     customer = Product.get_by_id(customer_id)
    #     if not customer:
    #         raise ValueError(f"Customer with ID {customer_id} does not exist.")
    #     return {
    #         "id": customer["customer_id"],
    #         "name": f"{customer['first_name']} {customer['last_name']}",
    #         "email": customer["email"],
    #         "phone": customer["phone"],
    #         "address": customer["address"]
    #     }

    @staticmethod
    def create_product(data):
        """Controller to create a new customer."""
        return Product.add(data)
