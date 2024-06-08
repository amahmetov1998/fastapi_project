from dotenv import dotenv_values
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail


from pydantic import EmailStr


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


async def send_email(email: EmailStr, token: int):
    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p>{token}</p> 

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
