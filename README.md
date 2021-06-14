# KSHER_PAYMENT_DEMO_PYTHON

Here is the demo on how you can intergrate our payment service into your system.

## Outline

- requirement
- installation
- configuration
- run the demo
- system overview
- each module detail

## requirement
- ksher account
- python 3.7

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

### Configuration
before we can run there are parameters that need to be config. In this demo we use Environment variables. Which is a good way to prevent expose your secret keys to the source code and observe by other. especially in an opensoure softwar storing in github.

we already provide you with the template file
```shell
cp env.example .env
```
Your .env should now look like this:
```text
export OMISE_SECRET_KEY=skey_test_xxxxxxxxxxxxxxxxxxx
export OMISE_PUBLIC_KEY=pkey_test_xxxxxxxxxxxxxxxxxxx
export OMISE_API_VERSION=2017-11-02
export FLASK_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export FLASK_ENV=development
export STORE_LOCALE=th_TH
export STORE_CURRENCY=THB
export PREFERRED_URL_SCHEME=http
export SERVER_NAME=localhost:5000
```




