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

def flickCheckOut(secret_key: str, request: FlickpaySDKRequest) -> FlickpaySDKResponse:
    try:
        payload = asdict(request)
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
        return FlickpaySDKResponse(
            statusCode=response.status_code, status="error",
            message=str(http_err), data=[error_details]
        )
    except requests.exceptions.RequestException as e:
        return FlickpaySDKResponse(
            statusCode=500, status="error",
            message=str(e), data=[]
        )
