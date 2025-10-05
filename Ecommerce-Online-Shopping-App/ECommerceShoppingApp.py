# ------------------- E-Commerce Backend -------------------
class ECommerceBackend:
    def __init__(self):
        # Demo users
        self.users = {
            "user1": {"password": "pass1", "name": "Alice"},
            "user2": {"password": "pass2", "name": "Bob"}
        }

        # Demo admin
        self.admins = {
            "admin": {"password": "admin123", "name": "Super Admin"}
        }

        # Categories
        self.categories = {
            1: "Footwear",
            2: "Clothing",
            3: "Electronics",
            4: "Accessories"
        }

        # Products
        self.products = {
            101: {"name": "Sports Shoes", "category_id": 1, "price": 1500},
            102: {"name": "Leather Boots", "category_id": 1, "price": 2000},
            103: {"name": "T-Shirt", "category_id": 2, "price": 500},
            104: {"name": "Jeans", "category_id": 2, "price": 1200},
            105: {"name": "Smartphone", "category_id": 3, "price": 15000},
            106: {"name": "Laptop", "category_id": 3, "price": 45000},
            107: {"name": "Cap", "category_id": 4, "price": 300},
            108: {"name": "Watch", "category_id": 4, "price": 2500}
        }

        self.active_sessions = {}  # {session_id: {"username": username, "type": "user/admin"}}
        self.user_carts = {}  # {session_id: {product_id: quantity}}
        self.next_session_id = 1
        self.next_product_id = 109
        self.next_category_id = 5

    # ------------------- Static Welcome Message -------------------
    @staticmethod
    def display_welcome_message():
        print("=" * 50)
        print("Welcome to the Demo Marketplace")
        print("=" * 50)

    # ------------------- Login / Logout -------------------
    def login(self, username, password, user_type="user"):
        database = self.users if user_type == "user" else self.admins
        if username in database and database[username]["password"] == password:
            session_id = str(self.next_session_id)
            self.next_session_id += 1
            self.active_sessions[session_id] = {"username": username, "type": user_type}
            if user_type == "user":
                self.user_carts[session_id] = {}
            print(f"Login successful. Welcome {database[username]['name']}!")
            return session_id
        else:
            print("Invalid credentials. Please try again.")
            return None

    def logout(self, session_id):
        if session_id in self.active_sessions:
            user_type = self.active_sessions[session_id]["type"]
            del self.active_sessions[session_id]
            if user_type == "user" and session_id in self.user_carts:
                del self.user_carts[session_id]
            print("Logout successful. Goodbye!")
            return True
        print("Invalid session. Please login again.")
        return False

    def is_valid_session(self, session_id, required_type=None):
        if session_id not in self.active_sessions:
            print("Invalid session. Please login again.")
            return False
        if required_type and self.active_sessions[session_id]["type"] != required_type:
            print(f"Access denied. Requires {required_type} privileges.")
            return False
        return True

    # ------------------- Display Catalog / Categories -------------------
    def display_catalog(self, session_id):
        if not self.is_valid_session(session_id):
            return False
        print("\nProduct Catalog")
        print("=" * 50)
        print("{:<10} {:<20} {:<15} {:<10}".format("ID", "Name", "Category", "Price"))
        print("-" * 55)
        for pid, product in self.products.items():
            category = self.categories.get(product["category_id"], "Unknown")
            print("{:<10} {:<20} {:<15} ₹{:<10}".format(pid, product["name"], category, product["price"]))
        return True

    def display_categories(self, session_id):
        if not self.is_valid_session(session_id):
            return False
        print("\nProduct Categories")
        print("=" * 50)
        print("{:<10} {:<20}".format("ID", "Category Name"))
        print("-" * 30)
        for cid, cname in self.categories.items():
            print("{:<10} {:<20}".format(cid, cname))
        return True

    # ------------------- User Cart Operations -------------------
    def display_cart(self, session_id):
        if not self.is_valid_session(session_id, "user"):
            return False
        cart = self.user_carts.get(session_id, {})
        if not cart:
            print("\nYour cart is empty.")
            return True
        total_amount = 0
        print("\nYour Shopping Cart")
        print("=" * 50)
        print("{:<10} {:<20} {:<10} {:<10} {:<10}".format("ID", "Product", "Price", "Quantity", "Total"))
        print("-" * 60)
        for pid, qty in cart.items():
            if pid in self.products:
                price = self.products[pid]["price"]
                total = price * qty
                total_amount += total
                print("{:<10} {:<20} ₹{:<10} {:<10} ₹{:<10}".format(pid, self.products[pid]["name"], price, qty, total))
        print("-" * 60)
        print(f"Total Amount: ₹{total_amount}")
        return True

    def add_to_cart(self, session_id, product_id, quantity=1):
        if not self.is_valid_session(session_id, "user"):
            return False
        product_id = int(product_id)
        quantity = int(quantity)
        if product_id not in self.products:
            print("Product not found.")
            return False
        if quantity <= 0:
            print("Quantity must be > 0.")
            return False
        cart = self.user_carts.get(session_id, {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        self.user_carts[session_id] = cart
        print(f"Added {quantity} {self.products[product_id]['name']}(s) to cart.")
        return True

    def remove_from_cart(self, session_id, product_id, quantity=None):
        if not self.is_valid_session(session_id, "user"):
            return False
        product_id = int(product_id)
        cart = self.user_carts.get(session_id, {})
        if product_id not in cart:
            print("Product not in cart.")
            return False
        if quantity is None or quantity >= cart[product_id]:
            del cart[product_id]
            print(f"Removed product {product_id} from cart.")
        else:
            quantity = int(quantity)
            cart[product_id] -= quantity
            print(f"Reduced quantity of product {product_id} by {quantity}.")
        self.user_carts[session_id] = cart
        return True

    # ------------------- Checkout -------------------
    def checkout(self, session_id, payment_method):
        if not self.is_valid_session(session_id, "user"):
            return False
        cart = self.user_carts.get(session_id, {})
        if not cart:
            print("Cart empty. Nothing to checkout.")
            return False
        total = sum(self.products[pid]["price"] * qty for pid, qty in cart.items() if pid in self.products)
        methods = {"1": "Net Banking", "2": "PayPal", "3": "UPI", "4": "Debit Card", "5": "Credit Card"}
        method_name = methods.get(payment_method, payment_method)
        print("\nProcessing Payment...")
        if method_name.lower() == "upi":
            print(f"Redirecting to UPI for payment of ₹{total}")
        else:
            print(f"Redirecting to {method_name} for payment of ₹{total}")
        print("Order successfully placed!")
        self.user_carts[session_id] = {}  # clear cart
        return True

    # ------------------- Admin Operations -------------------
    def add_product(self, session_id, name, category_id, price):
        if not self.is_valid_session(session_id, "admin"):
            return False
        category_id = int(category_id)
        price = float(price)
        if category_id not in self.categories:
            print("Invalid category.")
            return False
        if price <= 0:
            print("Price must be > 0.")
            return False
        pid = self.next_product_id
        self.next_product_id += 1
        self.products[pid] = {"name": name, "category_id": category_id, "price": price}
        print(f"Product '{name}' added with ID {pid}.")
        return True

    def update_product(self, session_id, product_id, name=None, category_id=None, price=None):
        if not self.is_valid_session(session_id, "admin"):
            return False
        product_id = int(product_id)
        if product_id not in self.products:
            print("Product not found.")
            return False
        if name:
            self.products[product_id]["name"] = name
        if category_id:
            category_id = int(category_id)
            if category_id not in self.categories:
                print("Category invalid.")
                return False
            self.products[product_id]["category_id"] = category_id
        if price:
            price = float(price)
            if price <= 0:
                print("Price must be > 0.")
                return False
            self.products[product_id]["price"] = float(price)  # type: ignore
        print(f"Product {product_id} updated.")
        return True

    def delete_product(self, session_id, product_id):
        if not self.is_valid_session(session_id, "admin"):
            return False
        product_id = int(product_id)
        if product_id not in self.products:
            print("Product not found.")
            return False
        del self.products[product_id]
        for cart in self.user_carts.values():
            cart.pop(product_id, None)
        print(f"Product {product_id} deleted.")
        return True

    def add_category(self, session_id, name):
        if not self.is_valid_session(session_id, "admin"):
            return False
        cid = self.next_category_id
        self.next_category_id += 1
        self.categories[cid] = name
        print(f"Category '{name}' added with ID {cid}.")
        return True

    def delete_category(self, session_id, category_id):
        if not self.is_valid_session(session_id, "admin"):
            return False
        category_id = int(category_id)
        if category_id not in self.categories:
            print("Category not found.")
            return False
        if any(p["category_id"] == category_id for p in self.products.values()):
            print("Cannot delete category with products.")
            return False
        del self.categories[category_id]
        print(f"Category {category_id} deleted.")
        return True

# ------------------- Helper Functions -------------------
def display_menu(session_type=None):
    print("\n" + "="*50)
    print("Demo Marketplace Menu")
    print("="*50)
    if session_type is None:
        print("1. User Login\n2. Admin Login\n3. Exit")
    elif session_type == "user":
        print("1. View Catalog\n2. View Categories\n3. View Cart\n4. Add to Cart\n5. Remove from Cart\n6. Checkout\n7. Logout")
    elif session_type == "admin":
        print("1. View Catalog\n2. View Categories\n3. Add Product\n4. Update Product\n5. Delete Product\n6. Add Category\n7. Delete Category\n8. Logout")
    return input("Enter your choice: ")

def display_payment_methods():
    print("\nPayment Methods:")
    print("1. Net Banking\n2. PayPal\n3. UPI\n4. Debit Card\n5. Credit Card")
    return input("Choose payment method: ")

# ------------------- Main Application Loop -------------------
def main():
    app = ECommerceBackend()
    app.display_welcome_message()
    session_id = None
    session_type = None

    while True:
        choice = display_menu(session_type)

        if session_type is None:
            # Login / Exit
            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                session_id = app.login(username, password, "user")
                if session_id: session_type = "user"
            elif choice == "2":
                username = input("Admin Username: ")
                password = input("Password: ")
                session_id = app.login(username, password, "admin")
                if session_id: session_type = "admin"
            elif choice == "3":
                print("Thank you for visiting Demo Marketplace!")
                break
            else:
                print("Invalid choice.")

        elif session_type == "user":
            if choice == "1": app.display_catalog(session_id)
            elif choice == "2": app.display_categories(session_id)
            elif choice == "3": app.display_cart(session_id)
            elif choice == "4":
                app.display_catalog(session_id)
                pid = int(input("Product ID to add: "))
                qty = int(input("Quantity: "))
                app.add_to_cart(session_id, pid, qty)
            elif choice == "5":
                app.display_cart(session_id)
                pid = int(input("Product ID to remove: "))
                qty_input = input("Quantity to remove (leave blank for all): ")
                qty = int(qty_input) if qty_input.strip() else None
                app.remove_from_cart(session_id, pid, qty)
            elif choice == "6":
                app.display_cart(session_id)
                method = display_payment_methods()
                app.checkout(session_id, method)
            elif choice == "7":
                if app.logout(session_id):
                    session_id = None
                    session_type = None
            else:
                print("Invalid choice.")

        elif session_type == "admin":
            if choice == "1": app.display_catalog(session_id)
            elif choice == "2": app.display_categories(session_id)
            elif choice == "3":
                name = input("Product name: ")
                app.display_categories(session_id)
                cid = int(input("Category ID: "))
                price = float(input("Price: "))
                app.add_product(session_id, name, cid, price)
            elif choice == "4":
                app.display_catalog(session_id)
                pid = int(input("Product ID to update: "))
                name = input("New name (leave blank to keep): ")
                app.display_categories(session_id)
                cid = input("New Category ID (leave blank to keep): ")
                price = input("New price (leave blank to keep): ")
                app.update_product(session_id, pid, name if name.strip() else None,
                                   int(cid) if cid.strip() else None,
                                   float(price) if price.strip() else None)
            elif choice == "5":
                app.display_catalog(session_id)
                pid = int(input("Product ID to delete: "))
                app.delete_product(session_id, pid)
            elif choice == "6":
                name = input("Category name: ")
                app.add_category(session_id, name)
            elif choice == "7":
                app.display_categories(session_id)
                cid = int(input("Category ID to delete: "))
                app.delete_category(session_id, cid)
            elif choice == "8":
                if app.logout(session_id):
                    session_id = None
                    session_type = None
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
