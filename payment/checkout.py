import json
from flask import (
    Blueprint,
    Markup,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from store.cart import Cart, Price
from ksherpay import Payment

checkout = Blueprint("checkout", __name__, template_folder="templates")



@checkout.route("/orders/<order_id>/<complete>")
def order(order_id,complete):
    """
    Charge completion return URL.  Once the customer is redirected
    back to this site from the authorization page, we search for the
    charge based on the provided `order_id`.
    """

    return render_template(
        "complete.html",
        order_id=order_id,
        complete=complete
    )



@checkout.route("/checkout")
def check_out():
    """
    Simple checkout page.
    """

    cart = Cart()
    return render_template(
        "checkout.html",
        cart=cart,
        Price=Price,
        currency=current_app.config.get("STORE_CURRENCY"),
        customer=session.get("customer"),
        location=current_app.config.get("LOCATION")
    )


@checkout.route("/charge", methods=["POST"])
def charge():
    """
    Create an Order based on Checkout page and 
    redirect using to make a payment on Ksher Payment Gateway
    """
    email = request.form.get("email")
    api_url = current_app.config.get('KSHER_API_BASE')
    api_token = current_app.config.get('KSHER_API_TOKEN')
    myPayment = Payment(api_url,token=api_token)
    store_base_url = current_app.config.get('STORE_BASE_URL')
    cart = Cart()
    order_id = myPayment.order.generate_order_id("Demo")
    order_data = {
        'amount': cart.total(), # ksher need cent unit
        'merchant_order_id':order_id,
        "channel": "linepay,airpay,wechat,bbl_promptpay,truemoney,ktbcard",
        'note': f'customer email:{email}',
        "redirect_url": f"{store_base_url}/orders/{order_id}/success",
        "redirect_url_fail": f"{store_base_url}/orders/{order_id}/fail",
    }
    print(f'order data:{order_data}')
    resp = myPayment.order.create(order_data)
    if resp.status_code != 200:
        return json.dumps({
            "status_code":resp.status_code,
            "error":resp.text
        })
    resp_data = resp.json()
    print(f"resp_data:{resp_data}")
    redirect_url = resp_data['reference']
    return redirect(redirect_url)
