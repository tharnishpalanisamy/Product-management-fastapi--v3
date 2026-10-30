from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import setting

email_config = ConnectionConfig(
    MAIL_USERNAME=setting.MAIL_USERNAME,
    MAIL_PASSWORD=setting.MAIL_PASSWORD,
    MAIL_FROM=setting.MAIL_FROM,
    MAIL_PORT=setting.MAIL_PORT,
    MAIL_SERVER=setting.MAIL_SERVER,
    MAIL_STARTTLS=setting.MAIL_STARTTLS,
    MAIL_SSL_TLS=setting.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailClient:
    def __init__(self):
        self.mailer = FastMail(email_config)

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        subtype: MessageType = MessageType.html,
    ):
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype=subtype,
        )

        await self.mailer.send_message(message)
