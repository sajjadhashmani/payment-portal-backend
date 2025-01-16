from app.db import get_db_connection
from psycopg2.extras import RealDictCursor

class Invoice:
    @staticmethod
    def add(data):
        """
        Add a new invoice to the database.

        :param data: Dictionary containing product details.
        :return: The ID of the newly added product.
        """
        query = """
               INSERT INTO invoices (customer_id, invoice_number, issue_date, due_date, total_amount,
    tax_amount, discount_amount, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, 'draft')
    RETURNING invoice_id;
               """
        # Extract address fields
        try:
            # Connect to the database and execute the query
            db = get_db_connection()
            with db.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        data.get("selectedCustomer"),
                        data.get("invoiceNumber"),
                        data.get("dateOfIssue"),
                        data.get("dueDate"),
                        data.get("subtotal"),
                        data.get("tax"),
                        data.get("discount"),

                    )
                )
                invoice_id = cursor.fetchone()[0]
            db.commit()
            return {"ok": True, "invoice_id": invoice_id}
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Database error: {e}")
            return {"ok": False, "error": str(e), "errorCode": e.pgcode}

    @staticmethod
    def next_invoice_number():
        """
        Get the next invoice number by finding the maximum current invoice number and incrementing it.

        :return: The next invoice number as a string.
        """
        query = "SELECT MAX(invoice_number) FROM invoices"
        try:
            # Connect to the database and execute the query
            db = get_db_connection()
            with db.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()

                # Determine the next invoice number
                if result[0] is not None:
                    next_invoice_number = str(int(result[0]) + 1).zfill(7)  # Increment and zero-fill
                else:
                    next_invoice_number = "0000001"  # Start from 000001 if no invoices exist

            return {"ok": True, "next_invoice_number": next_invoice_number}
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Database error: {e}")
            return {"ok": False, "error": str(e), "errorCode": e.pgcode}

    @staticmethod
    def addInvoiceItemData(invoiceItemData, invoice_id):
        try:
            # Get database connection
            db = get_db_connection()
            cursor = db.cursor()

            # SQL query for inserting into invoice_items
            query = """
               INSERT INTO invoice_items (
                   invoice_id,
                   product_id,
                   quantity,
                   unit_price
               )
               VALUES (%s, %s, %s, %s);
               """

            # Loop through the array of objects and insert each item
            for item in invoiceItemData:
                cursor.execute(query, (
                    invoice_id,  # Invoice ID (FK from invoices table)
                    item.get('description'),  # Product ID (or description ID, adapt as needed)
                    item.get('qty', 1),  # Quantity
                    item.get('rate', 0.00)  # Unit Price (rate)
                ))

            # Commit the transaction
            db.commit()
            print("Invoice items successfully added!")

        except Exception as e:
            # Rollback in case of error
            print(f"Error: {e}")
            db.rollback()
        finally:
            # Close the connection
            if cursor:
                cursor.close()
            if db:
                db.close()

    @staticmethod
    def get_all():
        """Retrieve all invoices from the database."""
        query = """
                    SELECT
                    i.invoice_id,
                    i.invoice_number,
                    TO_CHAR(i.issue_date, 'MM/DD/YYYY') AS issue_date,
                    TO_CHAR(i.due_date, 'MM/DD/YYYY') AS due_date,
                    i.amount_due,
                    i.status,
                    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
                    c.email,
                    JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'product_name', p.name,
                            'quantity', ii.quantity,
                            'unit_price', ii.unit_price,
                            'total_price', ii.total_price
                        )
                    ) AS products
                FROM
                    invoices i
                JOIN
                    customers c ON i.customer_id = c.customer_id
                JOIN
                    invoice_items ii ON i.invoice_id = ii.invoice_id
                LEFT JOIN
                    products p ON ii.product_id = p.product_id
                GROUP BY
                    i.invoice_id, i.invoice_number, i.issue_date, i.due_date, i.amount_due, i.status, c.first_name, c.last_name, c.email
                ORDER BY
                    i.invoice_id;

                    """
        try:
            db = get_db_connection()
            # Create a cursor with dictionary-like behavior for rows
            with db.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)  # Execute the SQL query
                results = cursor.fetchall()  # Fetch all results

            return results  # Return the list of dictionaries
        except Exception as e:
            print(f"Error: {e}")
            return None

        finally:
            # Ensure the database connection is closed
            if db:
                db.close()