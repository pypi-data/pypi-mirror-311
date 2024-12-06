from dataclasses import dataclass, asdict
import requests
from typing import Any, List, Dict, Optional

@dataclass
class Bank:
    status: int
    message: str
    form: str
    data: List[Dict[str, str]]

@dataclass
class FlickBankListResponse:
    status: int
    message: str
    data: List[Bank]

    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nData: {self.data}."

@dataclass
class checkOutRequest:
    amount: str
    Phoneno: str
    currency_collected: str
    currency_settled: str
    email: str
    redirectUrl: Optional[str] = None
    webhookUrl: Optional[str] = None
    transactionId: Optional[str] = None

@dataclass
class FlickpaySDKResponse:
    statusCode: int
    status: str
    message: str
    data: List[Dict[str, str]]
    def __str__(self):
        return f"StatusCode: {self.statusCode}\nStatus: {self.status}\nMessage: {self.message}\nData: {self.data}"

@dataclass
class BankNameRequest:
    account_number: str
    bank_code: str

@dataclass
class FlickBankNameResponse:
    status: int
    message: str
    account_number: str
    account_name: str
    def __str__(self):
        return f"Status: {self.status}\nMessage: {self.message}\nAccount Number: {self.account_number}\nAccount Name: {self.account_name}"


@dataclass
class PayoutRequest:
    bank_name: str
    bank_code: str
    account_number: str
    amount: str
    narration: str
    currency: str
    beneficiary_name: str
    reference: str
    debit_currency: str
    email: str
    mobile_number: str

@dataclass
class FlickPayoutResponse:
    status: int
    Id: str
    message: str
    description: str
    def __str__(self):
        return f"Status: {self.status}\nID: {self.Id}\nMessage: {self.message}\nDescription: {self.description}"

@dataclass
class FlickVerifyPayoutResponse:
    status: int
    Id: str
    account_number: str
    account_name: str
    bank_name: str
    amount: str
    currency: str
    transaction_status: str

    def __str__(self):
        return f"Status={self.status}\nID={self.Id}\nAccount_number={self.account_number}\nAccount_name={self.account_name}\nBank_name={self.bank_name}\nAmount={self.amount}\nCurrency={self.currency}\nTransaction_status={self.transaction_status}"

@dataclass
class BvnRequest:
    data_type: str
    data: str

@dataclass
class FlickBvnResponse:
    status: int
    message: str
    data: Any

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"

@dataclass
class NinRequest:
    nin: str
    dob: str

@dataclass
class FlickNinResponse:
    status: int
    message: str
    data: Any  # will be adjusted later

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"

@dataclass
class CacRequest:
    rcNumber: str


@dataclass
class FlickCacResponse:
    status: int
    message: str
    data: Any
    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"

@dataclass
class TinRequest:
    tin: str


@dataclass
class FlickTinResponse:
    status: int
    message: str
    data: Any

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"


class FlickpaySDK:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.base_url = "https://flickopenapi.co"

    def flickBankListSdk(self) -> FlickBankListResponse:

        try:

            url = f"{self.base_url}/merchant/banks"
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.secret_key}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return FlickBankListResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickBankListResponse(
                status= 400,
                message=str(http_err),
                data=[error_details]

            )
        except requests.exceptions.RequestException as e:
            return FlickBankListResponse(
                status=500,
                message=str(e),
                data=[]
            )

    def flickCheckOut(self, request: checkOutRequest) -> FlickpaySDKResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/collection/create-charge",
                json=payload,
                headers=headers,
            )

            response.raise_for_status()
            data = response.json()
            return FlickpaySDKResponse(
                statusCode=data["statusCode"], status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickpaySDKResponse(
                statusCode=response.status_code, status="error",
                message=str(http_err), data=[error_details]
            )
        except requests.exceptions.RequestException as e:
            return FlickpaySDKResponse(
                statusCode=500, status="error",
                message=str(e), data=[]
            )

    def flickBankNameInquiry(self, request: BankNameRequest) -> FlickBankNameResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"
                }
            response = requests.post(
                url=f"{self.base_url}/merchant/name-enquiry",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return FlickBankNameResponse(
                status=data["status"],
                message=data["message"],
                account_number=data["data"]["account_number"],
                account_name=data["data"]["account_name"])
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickBankNameResponse(
                status="error",
                message=str(error_details)
            )
        except requests.exceptions.RequestException as e:
            return FlickBankNameResponse(
            status=500,
            message=str(e),
            account_number="",
            account_name=""
        )

    def flickInitiatePayoutSdk(self, request: PayoutRequest) -> FlickPayoutResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}"}
            response = requests.post(
                url=f"{self.base_url}/transfer/payout",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickPayoutResponse(
                status=data["status"],
                Id=data["Id"],
                message=data["message"],
                description=data["description"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickPayoutResponse(
                status=response.status_code,
                message=str(error_details)
            )
        except requests.exceptions.RequestException as e:
            return FlickPayoutResponse(
                status=500,
                Id="",
                message="Request failed",
                description=str(e),
            )

    def flickVerifyPayoutSdk(self, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.get(
                url=f"{self.base_url}/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"],
                Id=data["Id"],
                account_number=data["account_number"],
                account_name=data["account_name"],
                bank_name=data["bank_name"],
                amount=data["amount"],
                currency=data["currency"],
                transaction_status=data["transaction_status"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickVerifyPayoutResponse(
                status=response.status_code,
                Id=str(error_details)
            )
        except requests.exceptions.RequestException as e:
            return FlickVerifyPayoutResponse(
                status=500,
                Id=str(e),
                account_number="",
                account_name="",
                bank_name="",
                amount="",
                currency="",
                transaction_status="failed"
            )

    def flickIdentityBvnSdk(self, request: BvnRequest) -> FlickBvnResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/kyc/identity-bvn",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickBvnResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickBvnResponse(
                status=response.status_code,
                data=[str(error_details)]
            )
        except requests.exceptions.RequestException as e:

            return FlickBvnResponse(
                status=500,
                message=f"Request failed: {str(e)}",
                data=None
            )
    def flickIdentityNinSdk(self, request: NinRequest) -> FlickNinResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/kyc/identity-nin",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickNinResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickNinResponse(
                status=response.status_code,
                data=[str(error_details)]
            )
        except requests.exceptions.RequestException as e:

            return FlickNinResponse(
                status=500,
                message=f"Request failed: {str(e)}",
                data=None
            )

    def flickIdentityCacBasicSdk(self, request: CacRequest) -> FlickCacResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/kyb/biz-basic",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickCacResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickCacResponse(
                status=response.status_code,
                data=[str(error_details)]
            )
        except requests.exceptions.RequestException as e:

            return FlickCacResponse(
                status=500,
                message=f"Request failed: {str(e)}",
                data=None
            )

    def flickIdentityCacAdvanceSdk(self, request: CacRequest) -> FlickCacResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/kyb/biz-advance",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickCacResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickCacResponse(
                status=response.status_code,
                data=[str(error_details)]
            )
        except requests.exceptions.RequestException as e:

            return FlickCacResponse(
                status=500,
                message=f"Request failed: {str(e)}",
                data=None
            )

    def flickPayKybInVerification(self, request: TinRequest) -> FlickTinResponse:
        try:
            payload = asdict(request)
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {self.secret_key}"
            }
            response = requests.post(
                url=f"{self.base_url}/kyb/tin-verification",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickTinResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()
            return FlickTinResponse(
                status=response.status_code,
                data=[str(error_details)]
            )
        except requests.exceptions.RequestException as e:

            return FlickTinResponse(
                status=500,
                message=f"Request failed: {str(e)}",
                data=None
            )

    @staticmethod
    def prompt_user_for_details() -> Dict[str, str]:
        print("Enter payment details:")

        amount = input("Amount: ").strip()
        phone_number = input("Phone Number: ").strip()
        currency_collected = input("Currency (e.g., NGN): ").strip()
        email = input("Email: ").strip()
        return {"amount": amount, "Phoneno": phone_number, "currency_collected": currency_collected,
            "currency_settled": "NGN", "email": email, }

    def crm_checkout(self, request_data: Dict[str, str]) -> Dict[str, Any]:
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": f"Bearer {self.secret_key}",
            }
            url = f"{self.base_url}/collection/create-charge"
            response = requests.post(
                url,
                json=request_data,
                headers=headers,
            )
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                redirect_url = data.get("data", {}).get("url")
                if redirect_url:
                    print(f"Redirecting to: {redirect_url}")
                    return {"success": True, "redirect_url": redirect_url}
                return {"success": False, "error": "Unexpected response format", "data": data}
            return {"success": False, "error": f"Failed with status code {response.status_code}",
            "data": response.json(),
            }
        except requests.exceptions.HTTPError as http_err:
            return {"success": False, "error": f"HTTP error occurred: {http_err}",
            "details": response.text, }
        except requests.exceptions.RequestException as req_err:
            return {"success": False, "error": f"Request failed: {str(req_err)}"}