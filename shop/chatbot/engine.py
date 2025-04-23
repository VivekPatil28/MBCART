import spacy
from .chatbot_views import *
from difflib import SequenceMatcher

nlp = spacy.load("en_core_web_md")

# Expanded FAQ data with synonyms and alternative phrases
faq_data = {
    "How do I reset my password?": "You can reset your password by clicking on 'Forgot Password' at login.",
    "Can I cancel my order?": "Yes, orders can be canceled before they are shipped.",
    "where is my recent order": get_recent_order,
    "last order": get_recent_order,
    "what is the status of my last order": get_recent_order,
    "why was my order cancelled": get_cancel_reason,
    "reason for order cancellation": get_cancel_reason,
    "how can i return my product": get_return_policy,
    "what is the return policy": get_return_policy,
    "when will my order arrive": get_estimated_delivery,
    "estimated delivery date of my order": get_estimated_delivery,
    "show my cart items": get_cart_items,
    "list items in my cart": get_cart_items,
    "what is the total price of my cart": get_total_cart_price,
    "total cost of items in my cart": get_total_cart_price,
    "show reviews for a product": get_product_reviews,
    "what are the shipping charges for a product": get_shipping_charges,
    "shipping cost for a product": get_shipping_charges,
    "what is the price of a product": get_product_price,
    "cost of a product": get_product_price,
    "show my default address": get_default_address,
    "what is my default address": get_default_address,
    "all addresses": get_addresses,
    "show my order history": get_order_history,
    "list all my past orders": get_order_history,
    "show my last or get my last review": get_last_review,
    "what was my last review": get_last_review,
    "show my notifications": get_notifications,
    "list my unread notifications": get_notifications,
    "show details of a product": get_product_details,
    "product details": get_product_details,
    "what is the rating of a product": get_product_rating,
    "product rating": get_product_rating,
    "show my last purchased item": get_last_purchased_item,
    "what was the last item I bought": get_last_purchased_item,

}


def preprocess_text(text):
    """Normalize text by converting to lowercase and stripping extra spaces."""
    return text.lower().strip()


def get_bot_response(user_input,request,product): # to be developed according the product data
    user_input = preprocess_text(user_input)
    user_doc = nlp(user_input)
    max_score = 0
    best_match = None

    for question in faq_data.keys():
        question_normalized = preprocess_text(question)
        question_doc = nlp(question_normalized)
        
        similarity_score = user_doc.similarity(question_doc)
        
        sequence_score = SequenceMatcher(None, user_input, question_normalized).ratio()
        
        combined_score = (similarity_score + sequence_score) / 2

        if combined_score > max_score:
            max_score = combined_score
            best_match = question

    if max_score > 0.7:  # Adjust threshold as needed
        response = faq_data[best_match]
        return response(request=request,product=product) if callable(response) else response
    return "Sorry, I couldn't find a suitable answer."
