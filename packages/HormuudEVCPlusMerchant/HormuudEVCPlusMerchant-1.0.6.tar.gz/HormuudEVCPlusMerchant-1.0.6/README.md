# HormuudEVCPlusMarchant

HormuudEVCPlusMarchant is a Python package that provides an interface for interacting with the HormuudEVPClusMarchant API. It allows you to perform various operations related to payment processing and transactions.

## Installation

You can install HormuudEVCPlusMarchant using pip:

```shell
pip install HormuudEVPlusMarchant



import HormuudEVCPlusMerchant

# Configure the client with your credentials
merchant_uid = [YOUR MERCHANT-UID]
api_user_id = [YOUR API USERID]
api_key = [YOR API KEY]

# Create an instance of the client
client = HormuudEVCPlusMerchant(merchant_uid, api_user_id, api_key)

# Create payerInfo and transactionInfo objects
payer_info = {
    "accountNo": "25261XXXXXXX"
}

transaction_info = {
    "referenceId": "12345",
    "invoiceId": "IVO001",
    "amount": "1",
    "currency": "USD",
    "description": "descirption "
}

# Make the request with the payerInfo and transactionInfo objects
response = client.make_request(payer_info, transaction_info)

# Process the response
print(response)

 
