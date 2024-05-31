from dotenv import dotenv_values
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
import random

from pydantic import EmailStr


VERIFICATION_CODE = random.randint(1000, 9999)

config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials["MAIL"],
    MAIL_PASSWORD=config_credentials["PASSWORD"],
    MAIL_FROM=config_credentials["MAIL"],
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)


async def send_email_with_code(email: EmailStr):
    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p>{VERIFICATION_CODE}</p> 

            </div>
        </body>
        </html>
    """

    message = MessageSchema(
        subject="Confirmation",
        recipients=[email],
        body=template,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_email_with_token(email: EmailStr):
    template = f"""
        <!DOCTYPE html>
<html>
<head>
</head>
<body>
    <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <h3> Account Verification </h3>
        <br>
        <a style=" padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;" href="http://localhost:8000/verification/?token=token">
            Verify your email
        <a>
    </div>
</body>
</html>
    """

    message = MessageSchema(
        subject="Confirmation",
        recipients=[email],
        body=template,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
