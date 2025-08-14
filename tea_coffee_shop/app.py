import os
from decimal import Decimal
from datetime import datetime
from typing import Dict, Tuple, List

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'tea_coffee_shop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security hardening defaults
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf = CSRFProtect(app)
db = SQLAlchemy(app)


# Database models
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	category = db.Column(db.String(50), nullable=False)  # Tea or Coffee
	product_type = db.Column(db.String(50), nullable=False)  # Instant, Fresh Brew, Beans, Leaves
	price = db.Column(db.Numeric(10, 2), nullable=False)
	description = db.Column(db.Text, nullable=False)
	image = db.Column(db.String(200), nullable=True)
	is_featured = db.Column(db.Boolean, default=False)


class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	customer_name = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.String(30), nullable=False)
	address = db.Column(db.Text, nullable=False)
	delivery_option = db.Column(db.String(50), nullable=False)  # Instant Delivery, Fresh Brew, Contactless Delivery
	status = db.Column(db.String(20), nullable=False, default='processing')  # processing, brewing, out_for_delivery, delivered
	created_at = db.Column(db.DateTime, server_default=func.now())

	items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

	@property
	def total(self):
		return sum(item.subtotal for item in self.items)


class OrderItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	quantity = db.Column(db.Integer, nullable=False, default=1)
	unit_price = db.Column(db.Numeric(10, 2), nullable=False)
	product = db.relationship('Product')

	@property
	def subtotal(self):
		return self.unit_price * self.quantity


# Utility and setup
ALL_CATEGORIES = ['Tea', 'Coffee']
ALL_TYPES = ['Instant', 'Fresh Brew', 'Beans', 'Leaves']


def currency(value):
	try:
		return f"${Decimal(value):.2f}"
	except Exception:
		return f"${value}"


app.jinja_env.filters['currency'] = currency


@app.context_processor
def inject_globals():
	cart: Dict[str, int] = session.get('cart', {})
	cart_count = sum(cart.values())
	return dict(
		cart_count=cart_count,
		all_categories=ALL_CATEGORIES,
		all_types=ALL_TYPES,
		csrf_token=generate_csrf()
	)


def initialize_products():
	if Product.query.count() > 0:
		return

	products = [
		# Teas
		{"name": "Normal Tea", "category": "Tea", "product_type": "Fresh Brew", "price": 2.99, "image": "tea_normal.jpg", "is_featured": True,
		 "description": "Classic comforting tea brewed to perfection with a rich aroma."},
		{"name": "Green Tea", "category": "Tea", "product_type": "Leaves", "price": 3.49, "image": "tea_green.jpg", "is_featured": True,
		 "description": "Delicate and fresh, loaded with antioxidants and subtle grassy notes."},
		{"name": "Chai", "category": "Tea", "product_type": "Fresh Brew", "price": 3.99, "image": "tea_chai.jpg", "is_featured": True,
		 "description": "Spiced Indian chai with cardamom, cinnamon, and ginger."},
		{"name": "Allam Tea", "category": "Tea", "product_type": "Fresh Brew", "price": 3.79, "image": "tea_allam.jpg",
		 "description": "Zesty ginger-forward brew with soothing warmth."},
		{"name": "Bellam Tea", "category": "Tea", "product_type": "Fresh Brew", "price": 3.59, "image": "tea_bellam.jpg",
		 "description": "Traditional jaggery-sweetened tea with deep caramel notes."},
		{"name": "Chamomile", "category": "Tea", "product_type": "Leaves", "price": 4.29, "image": "tea_chamomile.jpg",
		 "description": "Calming floral infusion perfect for unwinding."},
		{"name": "English Breakfast", "category": "Tea", "product_type": "Leaves", "price": 4.19, "image": "tea_english_breakfast.jpg",
		 "description": "Bold, malty black tea to kickstart your day."},
		{"name": "Jasmine Pearl", "category": "Tea", "product_type": "Leaves", "price": 4.99, "image": "tea_jasmine_pearl.jpg",
		 "description": "Hand-rolled pearls scented with jasmine blossoms."},

		# Coffees
		{"name": "Ethiopian", "category": "Coffee", "product_type": "Beans", "price": 5.99, "image": "coffee_ethiopian.jpg", "is_featured": True,
		 "description": "Bright acidity with floral and berry notes, single-origin."},
		{"name": "Colombian", "category": "Coffee", "product_type": "Beans", "price": 5.49, "image": "coffee_colombian.jpg",
		 "description": "Balanced and smooth with caramel sweetness."},
		{"name": "Espresso", "category": "Coffee", "product_type": "Fresh Brew", "price": 2.99, "image": "coffee_espresso.jpg",
		 "description": "Rich, concentrated shot with velvety crema."},
		{"name": "Cold Brew", "category": "Coffee", "product_type": "Fresh Brew", "price": 4.49, "image": "coffee_cold_brew.jpg", "is_featured": True,
		 "description": "Smooth, low-acidity brew steeped for 18 hours."},
		{"name": "French Press", "category": "Coffee", "product_type": "Fresh Brew", "price": 3.99, "image": "coffee_french_press.jpg",
		 "description": "Full-bodied cup with aromatic oils preserved."},
		{"name": "Instant Coffee", "category": "Coffee", "product_type": "Instant", "price": 2.49, "image": "coffee_instant.jpg",
		 "description": "Quick and convenient without compromising flavor."},
	]

	for p in products:
		product = Product(
			name=p['name'],
			category=p['category'],
			product_type=p['product_type'],
			price=Decimal(str(p['price'])),
			description=p['description'],
			image=p.get('image'),
			is_featured=p.get('is_featured', False)
		)
		db.session.add(product)

	db.session.commit()


# Cart helpers
CartData = Dict[str, int]


def get_cart() -> CartData:
	return session.get('cart', {})


def save_cart(cart: CartData) -> None:
	session['cart'] = cart
	session.modified = True


def add_to_cart(product_id: int, quantity: int = 1) -> None:
	cart = get_cart()
	key = str(product_id)
	cart[key] = cart.get(key, 0) + max(1, quantity)
	save_cart(cart)


def update_cart_item(product_id: int, quantity: int) -> None:
	cart = get_cart()
	key = str(product_id)
	if quantity <= 0:
		cart.pop(key, None)
	else:
		cart[key] = quantity
	save_cart(cart)


def clear_cart() -> None:
	save_cart({})


def compute_cart_details() -> Tuple[List[dict], Decimal]:
	cart = get_cart()
	items: List[dict] = []
	total = Decimal('0.00')
	if not cart:
		return items, total

	product_ids = [int(pid) for pid in cart.keys()]
	products = {p.id: p for p in Product.query.filter(Product.id.in_(product_ids)).all()}
	for pid_str, qty in cart.items():
		pid = int(pid_str)
		product = products.get(pid)
		if not product:
			continue
		subtotal = Decimal(product.price) * int(qty)
		total += subtotal
		items.append({
			'product': product,
			'quantity': int(qty),
			'subtotal': subtotal
		})
	return items, total


# Routes
@app.route('/')
def index():
	featured = Product.query.filter_by(is_featured=True).limit(8).all()
	return render_template('index.html', featured=featured)


@app.route('/menu')
def menu():
	category = request.args.get('category')
	ptype = request.args.get('type')
	query = Product.query
	if category in ALL_CATEGORIES:
		query = query.filter_by(category=category)
	if ptype in ALL_TYPES:
		query = query.filter_by(product_type=ptype)
	products = query.order_by(Product.category.asc(), Product.name.asc()).all()
	return render_template('menu.html', products=products, selected_category=category, selected_type=ptype)


@app.route('/product/<int:product_id>')
def product_detail(product_id: int):
	product = Product.query.get_or_404(product_id)
	related = Product.query.filter(Product.category == product.category, Product.id != product.id).limit(4).all()
	return render_template('product_detail.html', product=product, related=related)


@app.route('/cart')
def cart_view():
	items, total = compute_cart_details()
	return render_template('cart.html', items=items, total=total)


@app.route('/cart/add', methods=['POST'])
@csrf.exempt  # We'll validate with token from header manually for fetch; regular forms still protected
def cart_add():
	# Basic CSRF validation for JSON fetch requests
	if request.is_json:
		header_token = request.headers.get('X-CSRFToken')
		try:
			validate_csrf(header_token)
		except Exception:
			return jsonify({'ok': False, 'error': 'Invalid CSRF token'}), 400
	data = request.get_json(silent=True) or {}
	product_id = int((request.form.get('product_id') or data.get('product_id') or 0))
	quantity = int((request.form.get('quantity') or data.get('quantity') or 1))
	if product_id <= 0:
		return jsonify({'ok': False, 'error': 'Invalid product'}), 400
	add_to_cart(product_id, quantity)
	items, total = compute_cart_details()
	if request.accept_mimetypes.best == 'application/json' or request.is_json:
		return jsonify({
			'ok': True,
			'cart_count': sum(get_cart().values()),
			'total': str(total)
		})
	flash('Added to cart!', 'success')
	return redirect(request.referrer or url_for('menu'))


@app.route('/cart/update', methods=['POST'])
def cart_update():
	for key, value in request.form.items():
		if key.startswith('qty_'):
			try:
				pid = int(key.split('_', 1)[1])
				qty = int(value)
			except Exception:
				continue
			update_cart_item(pid, qty)
	flash('Cart updated', 'info')
	return redirect(url_for('cart_view'))


@app.route('/cart/remove', methods=['POST'])
def cart_remove():
	pid = int(request.form['product_id'])
	update_cart_item(pid, 0)
	flash('Item removed from cart', 'info')
	return redirect(url_for('cart_view'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	items, total = compute_cart_details()
	if request.method == 'GET':
		if total == Decimal('0.00'):
			flash('Your cart is empty. Add items to proceed to checkout.', 'warning')
			return redirect(url_for('menu'))
		return render_template('checkout.html', items=items, total=total)

	# POST - minimal server-side validation
	name = request.form.get('name', '').strip()
	email = request.form.get('email', '').strip()
	phone = request.form.get('phone', '').strip()
	address = request.form.get('address', '').strip()
	delivery_option = request.form.get('delivery_option', 'Instant Delivery')

	if not name or not email or not phone or not address:
		flash('Please fill out all required fields.', 'danger')
		return render_template('checkout.html', items=items, total=total), 400

	order = Order(
		customer_name=name,
		email=email,
		phone=phone,
		address=address,
		delivery_option=delivery_option,
		status='processing'
	)
	db.session.add(order)
	db.session.flush()  # to get order.id

	for item in items:
		order_item = OrderItem(
			order_id=order.id,
			product_id=item['product'].id,
			quantity=item['quantity'],
			unit_price=item['product'].price
		)
		db.session.add(order_item)

	db.session.commit()
	clear_cart()
	flash('Order placed! Your fresh brew is on the way.', 'success')
	return redirect(url_for('order_confirmation', order_id=order.id))


@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id: int):
	order = Order.query.get_or_404(order_id)
	return render_template('order_confirmation.html', order=order)


@app.route('/api/order/<int:order_id>/status')
def order_status(order_id: int):
	order = Order.query.get_or_404(order_id)
	# Simulate status progression over time for demo
	if order.status != 'delivered' and order.created_at:
		elapsed = (datetime.utcnow() - order.created_at).total_seconds()
		if elapsed > 900:
			order.status = 'delivered'
		elif elapsed > 600:
			order.status = 'out_for_delivery'
		elif elapsed > 300:
			order.status = 'brewing'
		db.session.commit()
	return jsonify({
		'id': order.id,
		'status': order.status,
		'created_at': order.created_at.isoformat() if order.created_at else None
	})


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		name = request.form.get('name', '').strip()
		email = request.form.get('email', '').strip()
		message = request.form.get('message', '').strip()
		if not name or not email or not message:
			flash('Please complete all fields.', 'danger')
		else:
			flash('Thanks for reaching out! We will get back to you shortly.', 'success')
			return redirect(url_for('contact'))
	return render_template('contact.html')


@app.route('/healthz')
def healthz():
	return {'status': 'ok'}


def setup_db():
	with app.app_context():
		db.create_all()
		initialize_products()


setup_db()


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)