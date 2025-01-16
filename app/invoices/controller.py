from app.invoices.invoice import Invoice

class InvoiceController:


    @staticmethod
    def create_invoice(data):
        """Controller to create a new invoice."""
        return Invoice.add(data)

    @staticmethod
    def next_invoice_number():
        """Controller to get next invoice number."""
        next_invoice_number = Invoice.next_invoice_number()
        return next_invoice_number

    @staticmethod
    def add_invoice_items(invoiceItemData, invoice_id):
        response = Invoice.addInvoiceItemData(invoiceItemData, invoice_id)
        """Controller to add invoice_items"""

    @staticmethod
    def list_invoices():
        """Controller to list all customers."""
        invoices = Invoice.get_all()
        transformed_invoices = [
            {
                "invoice_id": invoice["invoice_id"],
                "invoice_number": invoice["invoice_number"],
                "customer_name": invoice["customer_name"],
                "email": invoice["email"],
                "issue_date": invoice["issue_date"],
                "due_date": invoice["due_date"],
                "amount_due": invoice["amount_due"],
                "status": invoice["status"].capitalize(),  # Capitalize the first letter
                "products_summary": ", ".join(
                    [f"{product['product_name']}({product['quantity']})" for product in invoice.get("products", [])])

            }
            for invoice in invoices
        ]

        # Return the variable
        return transformed_invoices