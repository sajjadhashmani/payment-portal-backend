from app.db import get_db_connection

class Product:
    """Product model class to interact with the products table."""

    @staticmethod
    def get_all():
        """Retrieve all customers from the database."""
        query = "SELECT * FROM products;"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    # Use fetchall() to get all rows and process them into a list of dicts
                    columns = [col[0] for col in cursor.description]  # Get column names
                    return [
                        dict(zip(columns, row))  # Combine column names with their values
                        for row in cursor.fetchall()
                    ]
        except Exception as e:
            print("Error in get_all:", e)
            return []

    @staticmethod
    def add(data):
        """
        Add a new product to the database.

        :param data: Dictionary containing product details.
        :return: The ID of the newly added product.
        """
        query = """
           INSERT INTO products (name, description, price)
           VALUES (%s, %s, %s)
           RETURNING product_id;
           """
        # Extract address fields
        try:
            # Connect to the database and execute the query
            db = get_db_connection()
            with db.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        data.get("name"),
                        data.get("description"),
                        data.get("price"),
                    )
                )
                product_id = cursor.fetchone()[0]
            db.commit()
            return {"ok": True, "product_id": product_id}
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Database error: {e}")
            return {"ok": False, "error": str(e), "errorCode": e.pgcode}