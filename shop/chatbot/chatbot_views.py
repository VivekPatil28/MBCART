from UserProfile.models import Address, Order, Notification
from ..models import Product, Cart, Review, Category, SubCategory, ProductImages, ProductDescriptionImages


# Order-related functions
def get_recent_order(**kwargs):
    request = kwargs.get("request")
    order = Order.objects.filter(user=request.user).order_by('-order_date').first()
    if order is None:
        return "You don't have any recent orders."
    status = (
        "shipped" if order.shipped else
        "out for delivery" if order.outfordelivery else
        "delivered" if order.delivered else
        "ordered"
    )
    return f"Your last order '{order.product.product_name}' is currently {status}."


def get_cancel_reason(**kwargs):
    request = kwargs.get("request")
    order = Order.objects.filter(user=request.user, canceled=True).order_by('-order_date').first()
    if order:
        return f"Your order '{order.product.product_name}' was cancelled due to: {order.product.cancel_reason or 'unknown reason'}."
    return "No cancelled orders found."


def get_return_policy(**kwargs):
    # Placeholder for the return policy
    policy = "You can return your product within 7 days of delivery. The product must be unused and in its original packaging."
    return f"Our return policy is as follows: {policy}"


def get_estimated_delivery(**kwargs):
    request = kwargs.get("request")
    order = Order.objects.filter(user=request.user, delivered=False).order_by('-order_date').first()
    if order:
        return f"Your order '{order.product.product_name}' will be delivered by {order.delivered_date.strftime('%B %d, %Y')}."
    return "You don't have an active order."


def get_order_history(**kwargs):
    request = kwargs.get("request")
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    if not orders:
        return "You don't have any order history."
    order_details = [f"{order.product.product_name} (Ordered on: {order.order_date.strftime('%B %d, %Y')})" for order in orders]
    return "Your order history:\n" + "\n".join(order_details)


def get_last_purchased_item(**kwargs):
    request = kwargs.get("request")
    order = Order.objects.filter(user=request.user).order_by('-order_date').first()
    if not order:
        return "You haven't purchased anything yet."
    return f"Your last purchased item is '{order.product.product_name}'."


# Cart-related functions
def get_cart_items(**kwargs):
    request = kwargs.get("request")
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return "Your cart is empty."
    items = [f"{item.product.product_name} (Quantity: {item.quantity})" for item in cart_items]
    return "Your cart contains: " + ", ".join(items)


def get_total_cart_price(**kwargs):
    request = kwargs.get("request")
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.totalprice for item in cart_items)
    return f"The total price of items in your cart is ₹{total_price}."


# Product-related functions
def get_product_reviews(**kwargs):
    product = kwargs.get("product")
    if not product:
        return "No product found."
    reviews = product.comments.all()
    if not reviews:
        return f"No reviews found for '{product.product_name}'."
    review_texts = [f"{review.name}: {review.body}" for review in reviews]
    return "Reviews for the product:\n" + "\n".join(review_texts)


def get_shipping_charges(**kwargs):
    product = kwargs.get("product")
    if not product:
        return "Product is undefined."
    return f"The shipping charges for '{product.product_name}' are ₹{product.product_shipping_charges}."


def get_product_price(**kwargs):
    product = kwargs.get("product")
    if not product:
        return "Product is undefined."
    return f"The price of '{product.product_name}' is ₹{product.product_price}."


def get_product_details(**kwargs):
    product = kwargs.get("product")
    if not product:
        return "Product is undefined."
    return f"Details of '{product.product_name}': {product.product_desc}"


def get_product_rating(**kwargs):
    product = kwargs.get("product")
    if not product:
        return "Product is undefined."
    return f"The rating of '{product.product_name}' is {product.product_rating}."


# Address-related functions
def get_default_address(**kwargs):
    request = kwargs.get("request")
    address = Address.objects.filter(user=request.user, default_address=True).first()
    if not address:
        return "No default address found."
    return f"Your default address is: {address.full_name}, {address.house_no}, {address.area}, {address.city}, {address.state}, {address.pincode}."


def get_addresses(**kwargs):
    request = kwargs.get("request")
    addresses = Address.objects.filter(user=request.user)
    if not addresses:
        return "No addresses found."
    return "Your addresses:\n" + "\n".join([f"{address.full_name}, {address.house_no}, {address.area}, {address.city}, {address.state}, {address.pincode}" for address in addresses])


# Notification-related functions
def get_notifications(**kwargs):
    request = kwargs.get("request")
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    if not notifications:
        return "You have no new notifications."
    return "Your notifications:\n" + "\n".join([n.notification for n in notifications])


# Review-related functions
def get_last_review(**kwargs):
    request = kwargs.get("request")
    review = Review.objects.filter(user=request.user).order_by('-created').first()
    if not review:
        return "No reviews found."
    return f"Your last review was for '{review.product.product_name}': {review.body}"


