from app.customers.customer import Customer

class CustomerController:
    """Controller for managing customer-related business logic."""

    @staticmethod
    def list_customers():
        """Controller to list all customers."""
        customers = Customer.get_all()
        return [
            {
                "id": customer["customer_id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "street": customer["street"],
                "city": customer["city"],
                "state": customer["state"],
                "zip": customer["zip"]
            }
            for customer in customers
        ]


    @staticmethod
    def get_customer_names():
        """Controller to list all customers."""
        customers = Customer.get_customer_names()
        return [
            {
                "id": customer["customer_id"],
                "full_name_email": f"{customer['first_name']} {customer['last_name']} - {customer['email']}",
            }
            for customer in customers
        ]

    @staticmethod
    def get_customer_by_id(customer_id):
        """Controller to retrieve a customer by ID."""
        customer = Customer.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist.")
        return {
            "id": customer["customer_id"],
            "name": f"{customer['first_name']} {customer['last_name']}",
            "email": customer["email"],
            "phone": customer["phone"],
            "address": customer["address"]
        }

    @staticmethod
    def create_customer(data):
        """Controller to create a new customer."""
        if not data.get("firstName") or not data.get("lastName"):
            raise ValueError("First and last name are required.")
        if not data.get("email"):
            raise ValueError("Email is required.")
        return Customer.add(data)
