from flask import jsonify, request, abort, url_for
from service.models import Product, Category
from service.common import status
from . import app


######################################################################
# HEALTH CHECK
######################################################################
@app.route("/health")
def healthcheck():
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# HOME PAGE
######################################################################
@app.route("/")
def index():
    return app.send_static_file("index.html")

######################################################################
# UTILITY FUNCTION
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    if request.headers["Content-Type"] != content_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

######################################################################
# CREATE PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    app.logger.info("Request to Create a Product...")
    check_content_type("application/json")

    data = request.get_json()
    product = Product()
    product.deserialize(data)
    product.create()

    location_url = url_for("get_products", product_id=product.id, _external=True)

    return jsonify(product.serialize()), status.HTTP_201_CREATED, {
        "Location": location_url
    }


######################################################################
# READ PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper())
        products = Product.find_by_category(category_value)
    elif available:
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK