# Flick SDK For PYTHON

flick_paymentSDK is a secure and quick way for customers to access accounts and interact with the Flick API for Identity, Financial Data, Payouts, Collections, and Miscellaneous operations. It provides a straightforward integration for python developers.

## Features

- **Checkout:** Collect payments easily with various options.
- **Banking:** Retrieve bank lists, perform name inquiries, and manage payouts.
- **Identity Verification:** Verify BVN, NIN, CAC, and more.
- **Secure SDK:** Handles multi_factor authentication, credential validation, and error handling.

---

## Getting Started

1. **Register on Flick:**
   Sign up at [Flick](https://merchant.getflick.co/) to obtain your API keys (`secret_key` and `public_key`).

2. **Installation:**
   Install the package via `pip`:

   ```bash
   pip install flick_paymentsdk
   ```

Initialization: Create an instance of the flick_payment class using your secret_key.

Usage
Initialize the SDK

```python
import requests
from flick_paymentsdk.sdk import flick_payment

# Replace with your actual secret key
secret_key = "your_secret_key"
```

For Checkout 
Initiate a checkout process:

```python

checkout_payload = {
    "amount": "1000",
    "Phoneno": "1234567890",
    "currency_collected": "NGN",
    "currency_settled": "USD",
    "email": "example@example.com",
    "redirectUrl": "https://example.com/redirect",
    "webhookUrl": "https://example.com/webhook",
}
response = flick_payment.flickCheckOut(checkout_payload)
print(response)
```

Bank List Retrieval
Retrieve a list of supported banks:

```python

response = flickBankListSdk()
print(response)
```

Bank Name Inquiry
Perform a bank name inquiry:


```python

bank_name_payload = {
    "account_number": "1234567890",
    "bank_code": "001"
}
response = flick_payment.flickBankNameInquirySdk(bank_name_payload)
print(response)
```

Payout Initialization
Initiate a payout:

```python

payout_payload = {
    "bank_name": "Example Bank",
    "bank_code": "012",
    "account_number": "1234567890",
    "amount": "1000",
    "narration": "Payment for services",
    "currency": "NGN",
    "beneficiary_name": "John Doe",
}
response = flick_payment.flickInitiatePayoutSdk(payout_payload)
print(response)
```

Payout Verification
Verify a payout:

```python

transaction_id = "1234567890"
response = flick_payment.flickVerifyPayoutSdk(transaction_id)
print(response)
```

Identity Verification
Perform various identity verifications:

```python

# BVN Verification
response = flick_payment.flickIdentityBvnSdk({"bvn": "12345678901"})
print(response)

# NIN Verification
response = flick_payment.flickIdentityNinSdk({"nin": "12345678901"})
print(response)

# CAC Verification (Basic)
response = flick_payment.flickIdentityCacBasicSdk({"rc_number": "123456"})
print(response)

# Best Practices
Always handle exceptions raised by API calls.
Store your secret_key securely to prevent unauthorized access.
# Support
If you need help with flick_paymentSDK or your Flick integration, reach out to support@getflick.app or join our Slack channel.

License
This project is licensed under the MIT License.
```
