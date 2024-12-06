# pylint: disable=missing-function-docstring,invalid-name,too-many-return-statements
# type: ignore
from dataclasses import dataclass, asdict  
import requests 
from typing import Any, List, Dict, Optional



@dataclass
class FlickpaySDKRequest:
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
class FlickBankNameSdkRequest:
    account_number: str
    bank_code: str



@dataclass
class FlickBankNameData:
    account_number: str
    account_name: str


@dataclass
class FlickBankNameResponse:
    status: int
    message: str
    account_number: str
    account_name: str

    # def __str__(self):
    #     return f"Status: {self.status}\nMessage: {self.message}\nAccount Number: {self.account_number}\nAccount Name: {self.account_name}"



@dataclass
class FlickPayoutSdkRequest:
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
class FlickBvnRequest:
    secret_key: str
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
class FlickNinRequest:
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
class FlickCacRequest:
    rcNumber: str


@dataclass
class FlickCacResponse:
    status: int
    message: str
    data: Any

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"


@dataclass
class FlickTinRequest:
    tin: str


@dataclass
class FlickTinResponse:
    status: int
    message: str
    data: Any  

    def __str__(self):
        return f"Status={self.status}\nMessage={self.message}\nData={self.data}"


def flickBankListSdk(secret_key: str) -> FlickBankListResponse:

    try:

   
        url = "https://flickopenapi.co/merchant/banks" 
        headers = { "Content-Type": "application/json", "Authorization": f"Bearer {secret_key}" } 
        response = requests.get(url, headers=headers) 
        response.raise_for_status() # Will raise an HTTPError for bad responses 
        data = response.json() 
        return FlickBankListResponse(
                status=data["status"], message=data["message"], data=data["data"]
            )
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") 
        error_details = response.json()
        # return {"error": "HTTP error occurred", "details": str(http_err)} 
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}") 
        return {"error": "Connection error occurred", "details": str(conn_err)} 
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}") 
        return {"error": "Timeout error occurred", "details": str(timeout_err)} 
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}") 
        return {"error": "An unspecified error occurred", "details":str(req_err)}
    

def flickCheckOut(secret_key: str, request: FlickpaySDKRequest) -> FlickpaySDKResponse:
    try:
        payload = {
            "amount": request.get("amount"),
            "Phoneno": request.get("Phoneno"),
            "currency_collected": request.get("currency_collected"),
            "currency_settled": request.get("currency_settled"),
            "email": request.get("email"),
            "redirectUrl": request.get("redirectUrl"),
            "webhookUrl": request.get("webhookUrl"),
            "transactionId":request.get("transactionId")
            }    
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/collection/create-charge",
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
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}


    except requests.exceptions.RequestException as e:
          
        return {"error": f"Request failed: {str(e)}"}

def flickBankNameInquirySdk(secret_key: str, request:FlickBankNameSdkRequest ) -> FlickBankNameResponse:
    try:
        payload = {
            "account_number": request.get("account_number"),
            "bank_code": request.get("bank_code")
            }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/merchant/name-enquiry",
            json=payload,
            headers=headers
            )
            
        response.raise_for_status()
        data = response.json()
        return FlickBankNameResponse(
            status=data["status"], message=data["message"],
            account_number=data["data"]["account_number"], account_name=data["data"]["account_name"]
            )
    except requests.exceptions.HTTPError as http_err:
        error_details = response.json()  
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

    except requests.exceptions.RequestException as e:
        return FlickBankNameResponse(
        status=500,
        message=f"Request failed: {str(e)}",
        account_number="",  
        account_name=""  
        )

def flickInitiatePayoutSdk(secret_key: str, request:FlickPayoutSdkRequest) -> FlickPayoutResponse:
    try:
        payload = {
            "bank_name": request.get("bank_name"),
            "bank_code": request.get("bank_code"),
            "account_number": request.get("account_number"),
            "amount": request.get("amount"),
            "currency": request.get("currency"),
            "narration": request.get("narration"),
            "beneficiary_name": request.get("beneficiary_name"),
            "reference": request.get("reference"),
            "debit_currency": request.get("debit_currency"),
            "email": request.get("email"),
            "mobile_number": request.get("mobile_number"),
            }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/transfer/payout",
            json=payload,
            headers=headers
            )
        response.raise_for_status()
        data = response.json()
        return FlickPayoutResponse(
            status=data["status"], Id=data["Id"], message=data["message"], description=data["description"]
            )
    except requests.exceptions.HTTPError as http_err:
        error_details = response.json()  
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

    except requests.exceptions.RequestException as e:
        return FlickPayoutResponse(
        status=500,
        Id="",
        message="Request failed",
        description=str(e),
        )
  
def flickVerifyPayoutSdk(secret_key: str, transaction_id: str) -> FlickVerifyPayoutResponse:
        try:
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {secret_key}"
            }
            response = requests.get(
                url=f"https://flickopenapi.co/transfer/verify/{transaction_id}",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return FlickVerifyPayoutResponse(
                status=data["status"], Id=data["Id"], account_number=data["account_number"],
                account_name=data["account_name"], bank_name=data["bank_name"], amount=data["amount"],
                currency=data["currency"], transaction_status=data["transaction_status"]
            )
        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()  
            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

        except requests.exceptions.RequestException:
            return FlickVerifyPayoutResponse(
            status=500,
            Id="",
            account_number="",
            account_name="",
            bank_name="",
            amount="",
            currency="",
            transaction_status="failed"
        )
   
def flickIdentityBvnSdk(secret_key: str, request:FlickBvnRequest) -> FlickBvnResponse:
        try:
            payload = {
                "data_type": request.get("data_type"),
                "data": request.get("data"),
            }
            headers = {
                "accept": "application/json",
                "authorization": f"Bearer {secret_key}"
            }
            response = requests.post(
                url="https://flickopenapi.co/kyc/identity-bvn",
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
            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}


        except requests.exceptions.RequestException as e:
       
            return FlickBvnResponse(
            status=500,
            message=f"Request failed: {str(e)}",
            data=None
        )

    
def flickIdentityNinSdk(secret_key: str, request:FlickNinRequest) -> FlickNinResponse:
    try:
        payload = {
            "nin": request.get("nin"),
            "dob": request.get("dob")
            }
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/kyc/identity-nin",
            json=payload,
             headers=headers
            )
        response.raise_for_status()
        
        data = response.json()
        return FlickNinResponse(
        status=data["status"], message=data["message"], data=data["data"]
                )

    except requests.exceptions.Timeout:
        return FlickNinResponse(
        status=408,
        message="Request timed out. Please try again later.",
        data=None
        )

    except requests.exceptions.ConnectionError:
        return FlickNinResponse(
        status=503,
        message="Network problem. Could not connect to server.",
        data=None
        )

    except requests.exceptions.HTTPError as http_err:
        error_details = response.json()  
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

    except requests.exceptions.RequestException as req_err:
        return FlickNinResponse(
        status=500,
        message=f"Request error: {req_err}",
        data=None
        )
   
def flickIdentityCacBasicSdk(secret_key: str, request: FlickCacRequest) -> FlickCacResponse:
    try:
        payload = {
            "rcNumber": request.get("rcNumber")
            }
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/kyb/biz-basic",
            json=payload,
            headers=headers,
           
            )
        response.raise_for_status()
        data = response.json()
        return FlickCacResponse(
        status=data["status"],
        message=data["message"],
        data=data["data"],
                )

    except requests.exceptions.HTTPError as http_err:
        error_details = response.json()  
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}


    except requests.exceptions.RequestException as req_err:
        return FlickCacResponse(
        status=500,
        message=f"Request error: {req_err}",
        data=None,
        )
    

def flickIdentityCacAdvanceSdk(secret_key: str, request: FlickCacRequest) -> FlickCacResponse:
    try:
        payload = {
            "rcNumber": request.get("rcNumber")
            }
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
        response = requests.post(
            url="https://flickopenapi.co/kyb/biz-advance",
            json=payload,
            headers=headers,
            timeout=120
            )
        response.raise_for_status()

        
        data = response.json()
        return FlickCacResponse(
        status=data["status"],
        message=data["message"],
        data=data["data"],
                )


    except requests.exceptions.Timeout:
        return FlickCacResponse(
        status=408,
        message="Request timed out. Please try again later.",
        data=None,
        )

    except requests.exceptions.ConnectionError:
        return FlickCacResponse(
        status=503,
        message="Network problem. Could not connect to server.",
        data=None,
        )

    except requests.exceptions.HTTPError as http_err:
        error_details = response.json()  
        return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}


    except requests.exceptions.RequestException as req_err:
        return FlickCacResponse(
        status=500,
        message=f"Request error: {req_err}",
        data=None,
        )

def flickPayKybInVerification(secret_key: str, request: FlickTinRequest) -> FlickTinResponse:
        try:
            payload = {
            "tin": request.get("tin")
            }
            headers = {
            "accept": "application/json",
            "authorization": f"Bearer {secret_key}"
            }
            response = requests.post(
            url="https://flickopenapi.co/kyb/tin-verification",
            json=payload,
            headers=headers
            )
            response.raise_for_status()

            data = response.json()
            return FlickTinResponse(
            status=data["status"],
            message=data["message"],
            data=data["data"],
                )


        except requests.exceptions.Timeout:
            return FlickTinResponse(
            status=408,
            message="Request timed out. Please try again later.",
            data=None,
            )

        except requests.exceptions.ConnectionError:
            return FlickTinResponse(
            status=503,
            message="Network problem. Could not connect to server.",
            data=None,
            )

        except requests.exceptions.HTTPError as http_err:
            error_details = response.json()  
            return {"error": f"HTTP Error {response.status_code}: {http_err}", "details": error_details}

        except requests.exceptions.RequestException as req_err:
            return FlickTinResponse(
            status=500,
            message=f"Request error: {req_err}",
            data=None,
        )

 
def promptUserForDetails():
      
    print("Enter payment details:")
    amount = input("Amount: ").strip()
    phone_number = input("Phone Number: ").strip()
    currency_collected = input("Currency (e.g., NGN): ").strip()
    email = input("Email: ").strip()
    return {
        "amount": amount,
        "Phoneno": phone_number,
        "currency_collected": currency_collected,
        "currency_settled": "NGN", 
        "email": email,
        }

def flickCRMCheckout(secret_key, request_data):
        
    # request_data = secret_key.promptUserForDetails()

    try:
          
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {secret_key}",
            }
        url = "https://flickopenapi.co/collection/create-charge"
            
       
        response = requests.post(url, json=request_data, headers=headers, timeout=120)
        response.raise_for_status() 

        if response.status_code == 200:
            data = response.json()
            redirect_url = data.get("data", {}).get("url")
            if redirect_url:
                print(f"Redirecting to: {redirect_url}")
                return {"success": True, "redirect_url": redirect_url}

            return {"success": False, "error": "Unexpected response format", "data": data}

        return {
            "success": False,
            "error": f"Failed with status code {response.status_code}",
            "data": response.json(),
        }

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again later."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Network problem. Could not connect to the server."}
    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "error": f"HTTP error occurred: {http_err}",
            "details": response.text,
        }
    except requests.exceptions.RequestException as req_err:
        return {"success": False, "error": f"Request failed: {str(req_err)}"}
