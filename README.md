# Website Integration

This source code of this tutorial is hosted at https://github.com/ksher-solutions/payment_demo_python. 

You can try it here https://ksherpay-demo-store.herokuapp.com/

This is a poor man's ecommerce website with only two SKUs but with rich payment options.

### Adding SKU to shopping cart

Click ```add cart``` for adding the related SKU to shopping card. You can add serveral.

### Checkout 

Click ```Checkout``` to call payment gateway API and collect from customer.

### Get the payment result via Webhook

As soon as the transaction is authorized by the payer, the order status change will be sent by webhook.

---

## Outline

- [Requirement](#requirement)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run The Demo](#run-the-demo)
- [system overview](#system-overview)
- [How The App Make a payment using Ksher Payment Gateway](#how-the-app-make-a-payment-using-ksher-payment-gateway)
- [How The App Know that the payment has been done](#how-the-app-know-that-the-payment-has-been-done)


---

## Requirement
- Python 3.7
    - other python3 version should also work, but python package version might cause some conflice and minor change might need to be done.

- Ksher Payment API Account
    - Requesting sandbox account please contact support@ksher.com
    
- API_URL
    - Along with a sandbox accout, you will be receiving a API_URL in this format: s[UNIQUE_NAME].vip.ksher.net

- API_TOKEN
    - Log in into API_URL using given sandbox account and get the token. see (How to get API Token)[https://doc.vip.ksher.net/docs/howto/api_token]


## Installation
In this section we will install all the requirement and prepare our environment

### step 1: clone this respository
```shell
git clone https://github.com/ksher-solutions/payment_demo_python
```

### step 2: change directroy into cloned repository
```shell
cd ./payment_demo_python
```

### step 3: create virtual enviroment and activate it
``` shell
python -m venv ./venv
source ./venv/bin/activate
```
 ***NOTE: You migh have to specified if you have multiple python install***
    ```eg:
    python3 -m venv ./venv
    ```
### step 4: install all the requirements
```shell
pip install -r requirements.txt
```

---

## Configuration
before we can run there are parameters that need to be config. In this demo we use Environment variables. Which is a good way to prevent expose your secret keys to the source code and observe by other. especially in an opensoure softwar storing in github.

we already provide you with the template file
```shell
cp env.example .env
```
Your .env should now look like this:
```shell
export FLASK_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export FLASK_ENV=development
export STORE_LOCALE=th_TH
export STORE_CURRENCY=THB
export PREFERRED_URL_SCHEME=http
export SERVER_NAME=localhost:5000
export KSHER_API_BASE=https://s[UNIQUE_NAME].vip.ksher.net
export KSHER_API_TOKEN=token1234
export STORE_BASE_URL=https://315c0f6fc742.ngrok.io
```

Explanation on some configuation parameter

- FLASK_SECRET_KEY
    - random string to be use as a secret key of your flask app
- KSHER_API_BASE
    - ksher API_URL specified in requirement
- KSHER_API_TOKEN
    - ksher API_TOKEN specified in requirement
- SERVER_NAME
    - the url name of this flask app service. use for storing cookies
    - in heroku or production deployment this will be matched with STROE_BASE_URL 
- STORE_BASE_URL
    - the url name of this flask app service
    - in heroku or production deployment this will be matched with STROE_BASE_URL  how ever in localhost run we will set it to ngrok for webhook testing

### Config Object

the configuration parameters sepecified here is that loard into config object [here](/config.py)
which will later be load into flask app's config
```python
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.logger.setLevel('INFO')
    app.config.from_object(config_class)
```
---

## Run The Demo

In this section, we going to show you how to run this demo on you local machine. We also provide you on how to run this demo on Heroku on Deployment section

After you finnish all the previous sections(Installation, configuration), now it's time to run the demo

to run simply run below command
```shell
export FLASK_APP=app.py
python -m flask run
```

the service will be app and running and listen to port 5000

---

## System Overview
the system overview can be observed in the [application factories](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories)
inside [app.py](app.py) file locate in root directory of this demo.

The system is splited in to 3 modules (or 3 microservices);
- Store
    - Dealing with Store and how to get product into Cart
- Checkout
    - Creating order from the Cart being check out and redirect user to make a payment on Khser Payment Gateway and redirect after the payment has been finnish
- Webhook
    - Dealing with the webhook notification send back from Ksher Payment gateay after the payment has been done

```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.logger.setLevel('INFO')
    app.config.from_object(config_class)
    app.register_blueprint(store)
    app.register_blueprint(checkout)
    app.register_blueprint(webhook)

    # Adding Content Security Policy to load all content either locally or from heroku
    Talisman(
        app,
        content_security_policy={
            "default-src": "'unsafe-inline' 'self' *.amazonaws.com *.herokuapp.com *googleapis.com *.ksher.com"
        },
    )

    return app

```

---

## How The App Make a payment using Ksher Payment Gateway
After the user click 'check out' in Checkout page the method below will be executed making payment request to Ksher Payment Gateway.


```python
from ksherpay import Payment

@checkout.route("/charge", methods=["POST"])
def charge():
    """
    Create an Order based on Checkout page and 
    make a payment request to Ksher Payment Gateway
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

    resp = myPayment.order.create(order_data)
    if resp.status_code != 200:
        return json.dumps({
            "status_code":resp.status_code,
            "error":resp.text
        })
    resp_data = resp.json()
    redirect_url = resp_data['reference']
    return redirect(redirect_url)


```

here are some explanation;

### import the payment object

First need to import payment object from [Ksher payment python sdk](https://github.com/ksher-solutions/payment_sdk_python)

which in this demo we already clone the sdk and put it in root directory [here](/payment).

***In future version this sdk will be installable with pip install, but for not will still need to clone it.***
```python
from ksherpay import Payment
```


### Init the Payment Object
we then you paremters we've configured to init Payment Object
```python
api_url = current_app.config.get('KSHER_API_BASE')
api_token = current_app.config.get('KSHER_API_TOKEN')
myPayment = Payment(api_url,token=api_token)
```

### Create an Order
We get all the requried data to make the order from Checkout page and Cart and create the Order

***The order_id is not necessary need to make this way. you can use your own method, but make sure it will be a unique string.***
```python
# Generate a unique order id by using the current time "YYYYMMDDTHHMMSS"
order_id = myPayment.order.generate_order_id("Demo") 

order_data = {
    'amount': cart.total(), # ksher need cent unit
    'merchant_order_id':order_id,
    "channel": "linepay,airpay,wechat,bbl_promptpay,truemoney,ktbcard",
    'note': f'customer email:{email}',
    "redirect_url": f"{store_base_url}/orders/{order_id}/success",
    "redirect_url_fail": f"{store_base_url}/orders/{order_id}/fail",
}

resp = myPayment.order.create(order_data)
```

### Redirect user to make a payment
if the Order has been created successfully.(ksher will response with status code 200)
then we can use the redirect_url send back along with the response body to redirect the user into Khser Payment Gateway Page
```python
if resp.status_code != 200:
    return json.dumps({
        "status_code":resp.status_code,
        "error":resp.text
    })
resp_data = resp.json()
redirect_url = resp_data['reference']
return redirect(redirect_url)

```

## How The App Know that the payment has been done

After the payment is done khser will redirect the user back using redirect_url speicified in the Order Creation

```python
"redirect_url": f"{store_base_url}/orders/{order_id}/success",
"redirect_url_fail": f"{store_base_url}/orders/{order_id}/fail"
```

which is this endpoint implente in checkout module
```python
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

```

along with this redirect, Khser will send the notification to our webhook [here](/webhook/webhook.py)