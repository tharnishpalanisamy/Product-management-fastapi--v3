import razorpay

from app.config import setting

from razorpay.errors import BadRequestError , GatewayError , ServerError 
from app.exceptions import RazorPayIntegrationException 

razorpay_client = razorpay.Client(auth=(setting.TEST_API_KEY, setting.TEST_SECRET_KEY))


def create_order(amount: int, receipt: str):
    data = {"amount": amount, "currency": "INR", "receipt": receipt}

    try : 
        return razorpay_client.order.create(data)  

    except BadRequestError as error :
        raise RazorPayIntegrationException(
            'Razor pay rejected the order request'
        )from error 
    
    except (ServerError , GatewayError)  as error :
        raise RazorPayIntegrationException(
            "Unable to communicate with Razorpay"
        ) from error 
