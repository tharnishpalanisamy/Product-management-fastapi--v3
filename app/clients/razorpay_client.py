import razorpay

from app.config import setting

razorpay_client = razorpay.Client(auth=(setting.TEST_API_KEY, setting.TEST_SECRET_KEY))
