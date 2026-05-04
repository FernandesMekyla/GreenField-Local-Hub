from flask import Blueprint, render_template, redirect, url_for, request, flash, session


main_bp = Blueprint("main", __name__)


# -------------------------
# DEMO USERS
# -------------------------
DEMO_USERS = {
    "admin@demo.com": {"password": "admin123", "role": "admin"},
    "producer@demo.com": {"password": "producer123", "role": "producer"},
}


# -------------------------
# ROLE CHECK HELPERS
# -------------------------
def require_admin():
    if session.get("user_role") != "admin":
        flash("Admin access only (demo mode).", "error")
        return False
    return True


def require_producer():
    if session.get("user_role") != "producer":
        flash("Producer access only (demo mode).", "error")
        return False
    return True




# -------------------------
# ROUTES
# -------------------------


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])
    total = sum(item["quantity"] * item["price"] for item in cart_items)
    return render_template("checkout.html", cart_items=cart_items, total=total)


@main_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Load product list (same list you use in catalogue)
    products = [
        {"id": 1, "name": "Sourdough Bread", "price": 4.20},
        {"id": 2, "name": "Banana Bread", "price": 3.50},
        {"id": 3, "name": "Croissants", "price": 2.20},
        # ... add all products here
    ]


    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("main.catalogue"))


    cart = session.get("cart", [])


    # If product already in cart, increase quantity
    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({
            "id": product_id,
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })


    session["cart"] = cart
    flash(f"{product['name']} added to cart.", "success")
    return redirect(url_for("main.catalogue"))




# -------------------------
# PROTECTED DASHBOARDS
# -------------------------


@main_bp.route("/admin-dashboard")
def admin_dashboard():
    if not require_admin():
        return redirect(url_for("main.login"))
    return render_template("admin-dashboard.html")


@main_bp.route("/producer-dashboard")
def producer_dashboard():
    if not require_producer():
        return redirect(url_for("main.login"))
    return render_template("producer-dashboard.html")




# -------------------------
# LOGIN
# -------------------------
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")


        user = DEMO_USERS.get(email)


        if user and user["password"] == password:
            session["user_role"] = user["role"]
            session["user_email"] = email
            flash(f"Logged in as {user['role'].title()} (demo mode).", "success")


            if user["role"] == "admin":
                return redirect(url_for("main.admin_dashboard"))
            if user["role"] == "producer":
                return redirect(url_for("main.producer_dashboard"))


        flash("Invalid email or password.", "error")


    return render_template("login.html")




# -------------------------
# LOGOUT
# -------------------------
@main_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))




# -------------------------
# REGISTER
# -------------------------
@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")


        if not all([name, email, password, confirm]):
            flash("Please complete all fields.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            flash("Registration successful (placeholder).", "success")
            return redirect(url_for("main.login"))


    return render_template("register.html")




# -------------------------
# CONTACT
# -------------------------
@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")


        if not all([name, email, message]):
            flash("Please complete all fields.", "error")
        else:
            flash("Your message has been sent (placeholder).", "success")


    return render_template("contact.html")




# -------------------------
# CATALOGUE (FULLY FIXED)
# -------------------------
@main_bp.route("/catalogue")
def catalogue():
    category = request.args.get("category", "all")


    products = [
        # Bakery
        {"id": 2, "name": "Banana Bread", "price": 3.50, "category": "bakery",
         "image": "images/banana bread.jpg", "description": "Moist banana loaf."},


        {"id": 3, "name": "Croissants", "price": 2.20, "category": "bakery",
         "image": "images/croissants.jpg", "description": "Flaky buttery croissants."},


        {"id": 4, "name": "Ciabatta Rolls", "price": 2.80, "category": "bakery",
         "image": "images/ciabatta-rolls.jpg", "description": "Crispy Italian rolls."},


        {"id": 5, "name": "Focaccia", "price": 3.00, "category": "bakery",
         "image": "images/focaccia.jpg", "description": "Rosemary focaccia bread."},


        {"id": 6, "name": "Panini", "price": 2.50, "category": "bakery",
         "image": "images/panini.jpg", "description": "Soft Italian panini bread."},


        {"id": 7, "name": "Muffins", "price": 2.00, "category": "bakery",
         "image": "images/muffins.jpg", "description": "Fresh baked muffins."},


        {"id": 33, "name": "Chocolate Brownies", "price": 2.50, "category": "bakery",
         "image": "images/chocolate brownies.jpg", "description": "Rich chocolate brownies."},




        # Dairy & Eggs
        {"id": 8, "name": "Eggs (12)", "price": 3.80, "category": "dairy",
         "image": "images/eggs.jpg", "description": "Free-range eggs."},


        {"id": 9, "name": "Whole Milk", "price": 1.20, "category": "dairy",
         "image": "images/whole milk.jpg", "description": "Fresh whole milk."},


        {"id": 10, "name": "Semi Skimmed Milk", "price": 1.10, "category": "dairy",
         "image": "images/semi skimmed milk.jpg", "description": "Semi-skimmed milk."},


        {"id": 11, "name": "Whipped Cream", "price": 1.80, "category": "dairy",
         "image": "images/whipped cream.jpg", "description": "Fresh whipped cream."},


        {"id": 12, "name": "Amul Fresh Cream", "price": 2.00, "category": "dairy",
         "image": "images/amul fresh cream.jpg", "description": "Rich fresh cream."},


        # Vegetables
        {"id": 13, "name": "Carrots", "price": 1.50, "category": "vegetables",
         "image": "images/carrots.jpg", "description": "Crisp local carrots."},


        {"id": 14, "name": "Cucumber", "price": 1.00, "category": "vegetables",
         "image": "images/cucumbers.jpg", "description": "Fresh cucumbers."},


        {"id": 15, "name": "Onions", "price": 1.20, "category": "vegetables",
         "image": "images/onions.jpg", "description": "Brown onions."},


        {"id": 16, "name": "Potatoes", "price": 1.80, "category": "vegetables",
         "image": "images/potatoes.jpg", "description": "White potatoes."},


        {"id": 17, "name": "Tomatoes", "price": 1.60, "category": "vegetables",
         "image": "images/tomatoes.jpg", "description": "Juicy tomatoes."},


        {"id": 18, "name": "Seasonal Vegetables Box", "price": 18.50, "category": "vegetables",
         "image": "images/season vegetables box.jpg", "description": "Mixed seasonal veg."},


        # Fruits
        {"id": 19, "name": "Apples", "price": 2.20, "category": "fruits",
         "image": "images/apples.jpg", "description": "Crisp apples."},


        {"id": 20, "name": "Bananas", "price": 1.50, "category": "fruits",
         "image": "images/banana.jpg", "description": "Fresh bananas."},


        {"id": 21, "name": "Blueberries", "price": 3.00, "category": "fruits",
         "image": "images/blueberries.jpg", "description": "Sweet blueberries."},


        {"id": 22, "name": "Grapes", "price": 2.80, "category": "fruits",
         "image": "images/grapes.jpg", "description": "Seedless grapes."},


        {"id": 24, "name": "Lemons", "price": 1.20, "category": "fruits",
         "image": "images/lemons.jpg", "description": "Zesty lemons."},


        {"id": 25, "name": "Oranges", "price": 2.00, "category": "fruits",
         "image": "images/oranges.jpg", "description": "Sweet oranges."},


        {"id": 26, "name": "Pears", "price": 2.30, "category": "fruits",
         "image": "images/pears.jpg", "description": "Juicy pears."},


        {"id": 27, "name": "Pineapples", "price": 3.50, "category": "fruits",
         "image": "images/pineapples.jpg", "description": "Fresh pineapples."},


        {"id": 28, "name": "Strawberries", "price": 3.00, "category": "fruits",
         "image": "images/strawberries.jpg", "description": "Sweet strawberries."},


        # Meat & Fish
        {"id": 29, "name": "Salmon Fillet", "price": 5.50, "category": "meat_fish",
         "image": "images/salmon fillet.jpg", "description": "Fresh salmon fillet."},


        {"id": 30, "name": "Pork Ribs", "price": 6.80, "category": "meat_fish",
         "image": "images/pork ribs.jpg", "description": "Tender pork ribs."},


        {"id": 31, "name": "Mince", "price": 4.50, "category": "meat_fish",
         "image": "images/mince.jpg", "description": "Lean beef mince."},


        {"id": 32, "name": "Meat Selection", "price": 10.00, "category": "meat_fish",
         "image": "images/meat.jpg", "description": "Mixed meat selection."},
    ]


    if category != "all":
        products = [p for p in products if p["category"] == category]


    return render_template("catalogue.html", products=products, selected_category=category)