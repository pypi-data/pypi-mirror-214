# FacekiAPIClientV2

The `FacekiAPIClientV2` is a Python client for interacting with the Faceki API. It provides methods to generate an access token, perform various KYC (Know Your Customer) operations, and retrieve KYC records.

## Installation

You can install `FacekiAPIClientV2` using pip:

```
pip install facekiapiclientv2
```

## Usage

```python
import requests
from facekiapiclientv2 import FacekiAPIClientV2

client_id = 'your_client_id'
client_secret = 'your_client_secret'
api_client = FacekiAPIClientV2(client_id, client_secret)

# Generate an access token
api_client.generate_token()

# Get KYC rules
kyc_rules = api_client.getKYCRules()

# Perform a KYC verification
selfie_image = 'path_to_selfie_image.jpg'
id_front_image = 'path_to_id_front_image.jpg'
id_back_image = 'path_to_id_back_image.jpg'
dl_front_image = 'path_to_dl_front_image.jpg'
dl_back_image = 'path_to_dl_back_image.jpg'
pp_front_image = 'path_to_pp_front_image.jpg'
pp_back_image = 'path_to_pp_back_image.jpg'

result = api_client.requestKYC(selfie_image, id_front_image, id_back_image,
                               dl_front_image, dl_back_image, pp_front_image,
                               pp_back_image)

# Get KYC verification summary
kyc_summary = api_client.getKycSummary()

# Generate a KYC verification link
expire_time = 0
application_id = 'your_application_id'

link = api_client.generateKYCLink(expire_time, application_id)

# Get KYC records
link_id = 'your_link_id'
kyc_records = api_client.getKYCrecords(link_id)

# Perform a face check
selfie_image = 'path_to_selfie_image.jpg'

result = api_client.faceCheck(selfie_image)
```

## Exception Handling

The `FacekiAPIClientV2` class may raise exceptions in case of errors. Ensure that you handle these exceptions appropriately in your code. Examples of possible exceptions include:

- `requests.exceptions.RequestException`: Raised when there is an issue with making a request to the Faceki API.
- `Exception`: Raised for various errors such as failed token generation or failed requests.

## Disclaimer

Please note that this client code is provided as a starting point and may require modifications or updates depending on the Faceki API's specific requirements or changes. Refer to the Faceki API documentation for detailed information about the API's endpoints, request/response structures, and authentication requirements.