# Copyright (c) 2024, iota technologies and contributors
# For license information, please see license.txt

# batch.py
import random
import string
import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days

class VoucherBatch(Document):
    def before_submit(self):
        # Call the voucher generation function
        self.generate_vouchers()

    def generate_vouchers(self):
        # Fetch batch details
        generation_date = self.generation_date or today()
        quantity = self.quantity
        name_length = int(self.name_length) 
        prefix = self.prefix or ''  
        character_set = self.characters
        voucher_plan = self.voucher_plan
        router = self.router

        # Map the character set to actual characters
        character_map = {
            "abcd": string.ascii_lowercase,
            "ABCD": string.ascii_uppercase,
            "AbCd": string.ascii_letters,
            "5ab2c34cd": string.ascii_letters + string.digits,
            "5AB2C3CD4": string.ascii_uppercase + string.digits,
            "1234567": string.digits
        }

        characters = character_map.get(character_set, string.ascii_letters)

        # Generate vouchers and store in Voucher Code doctype
        for i in range(quantity):
            # Generate random voucher code excluding the prefix length
            random_code_length = name_length
            random_code = ''.join(random.choices(characters, k=random_code_length))

            # Concatenate prefix with the random code
            voucher_code = f"{prefix}{random_code}"

            # Create a new Voucher Code entry
            new_voucher = frappe.get_doc({
                "doctype": "Voucher Code",
                "voucher_code": voucher_code,
                "voucher_batch": self.name,
                "voucher_plan": voucher_plan,
                "router": router,
                "status": "Unused",  # Set default status
            })

            # Insert the voucher record into the database
            new_voucher.insert()

        # Commit the changes
        frappe.db.commit()

        frappe.msgprint(f"{quantity} vouchers generated for batch {self.name}.")
