from app.clients.email_client import EmailClient


class EmailService:
    def __init__(self, email_client: EmailClient):
        self.email_client = email_client

    async def send_account_created_email(
        self,
        recipient: str,
        username: str,
    ):
        subject = "Your Account Has Been Created!"

        body = f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>Welcome, {username}!</h2>

                <p>Your account has been successfully created.</p>

                <p>You can now log in and start using our Product Management
                application.</p>

                <p>Thank you for joining us!</p>

                <br>
                <p>Regards,<br>Product Management Team</p>
            </body>
        </html>
        """

        await self.email_client.send_email(
            recipient=recipient,
            subject=subject,
            body=body,
        )
