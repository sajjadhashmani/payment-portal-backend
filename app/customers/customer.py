from app.db import get_db_connection

class Customer:
    """Customer model class to interact with the customers table."""

    @staticmethod
    def get_all():
        """Retrieve all customers from the database."""
        query = "SELECT * FROM customers;"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    # Use fetchall() to get all rows and process them into a list of dicts
                    columns = [col[0] for col in cursor.description]  # Get column names
                    rows = [
                        dict(zip(columns, row))  # Combine column names with their values
                        for row in cursor.fetchall()
                    ]
                    return rows
        except Exception as e:
            print("Error in get_all:", e)
            return []

    @staticmethod
    def get_customer_names():
        """Retrieve all customer names from the database"""
        query = "SELECT customer_id, first_name, last_name, email FROM customers;"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    # Use fetchall() to get all rows and process them into a list of dicts
                    columns = [col[0] for col in cursor.description]  # Get column names
                    rows = [
                        dict(zip(columns, row))  # Combine column names with their values
                        for row in cursor.fetchall()
                    ]
                    return rows
        except Exception as e:
            print("Error in get_all:", e)
            return []

    @staticmethod
    def get_by_id(customer_id):
        """Retrieve a specific customer by their ID."""
        query = "SELECT * FROM customers WHERE customer_id = %s;"
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (customer_id,))
                return cursor.fetchone()

    @staticmethod
    def add(data):
        """
        Add a new customer to the database.

        :param data: Dictionary containing customer details.
        :return: The ID of the newly added customer.
        """
        query = """
        INSERT INTO customers (first_name, last_name, email, phone, street, city, state, zip)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING customer_id;
        """
        # Extract address fields
        address = data.get("address", {})

        try:
            # Connect to the database and execute the query
            db = get_db_connection()
            with db.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        data.get("firstName"),
                        data.get("lastName"),
                        data.get("email"),
                        data.get("phone"),
                        address.get("street", ""),
                        address.get("city", ""),
                        address.get("state", ""),
                        address.get("zip", None),
                    )
                )
                customer_id = cursor.fetchone()[0]
            db.commit()
            return {"ok": True, "customer_id": customer_id}
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Database error: {e}")
            return {"ok": False, "error": str(e), "errorCode": e.pgcode}