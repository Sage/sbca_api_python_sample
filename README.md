# Sage Business Cloud Accounting API starter sample application (Python)

The Sage Business Cloud Accounting simple Python sample is an starter application written to demonstrate a method of consuming the Accounting API v3.1.

## Prerequisites

Prior to using this sample application there are a few things you need to ensure you have set up and ready:

* A Sage Accounting trial business, which can be created using the links available in the documentation [quick start guide](https://developer.sage.com/accounting/quick-start/set-up-the-basics/#set-up-a-developer-trial). There is an option to upgrade to a free of charge developer account [here](https://developer.sage.com/accounting/quick-start/upgrade-your-account/). We have a range of variants and regions to choose from.

* A Sage developer account used to register an application, set your callback url(s), and obtain your client credentials (client_id & client_secret). You can sign up [here](https://developerselfservice.sageone.com/), with a guide available [here](https://developer.sage.com/accounting/guides/getting-started/developer_signup/).

* A registered application using the app registry above. We have a guide on that process available [here](https://developer.sage.com/accounting/guides/getting-started/client_app_registration/).

### Optional

* For UK businesses we also offer a Postman collection that will create some sample data in your test account. More on this process is available on the [developer portal](https://developer.sage.com/accounting/quick-start/preparing-to-create-test-data/). We are looking to add testing datasets for other regions in the future.

## Configuration

* Install the latest version of [python3](https://www.python.org/downloads/).
* Create and activate a virtual environment - [offical Python docs](https://docs.python.org/3/library/venv.html).
* Ensure pip is installed and using the following command in your virtual environment install all required packages:

```terminal
pip install -r requirements.txt
```

* Update the config.py with your registered application credentials (Client ID, Client Secret and Redirect URL), and set or generate a new (16-24 character) Flask session key, updating the details in the configuration.

You can use the os package via os.urandom(24) (passing in the number of characters you require)
For example in a python terminal:

```terminal
>>> import os
>>> os.urandom(24)
>>> b'"\xf7\xb5\..........\xa5\x0e'
```

Once your session key and credentials are set in the config.py, setup is complete.

## Usage

Start the sample app using:

```terminal
python -m flask run
```

## Contributing

This sample is only one of many ways to work with our API, and so we welcome feedback. Please let us know on our [developer community](https://developer-community.sage.com/forum/4-sage-business-cloud-accounting/) your thoughts, and get involved in the discussion.

© 2022 The Sage Group plc or its licensors. All rights reserved.

## Licence

Licensed under the [Apache-2.0 licence](https://github.com/Sage/sbca_api_python_sample/blob/master/LICENCE).

