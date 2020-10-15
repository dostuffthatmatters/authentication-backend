
from app import httpx_client, ENVIRONMENT, ADMIN_FRONTEND_URL


async def send_verification_mail(db_account):
    data = {
        'from': 'FastSurvey <noreply@admin.fastsurvey.io>',
        'to': db_account["email"],
        'subject': 'Please verify your FastSurvey account',
        'html': generate_verification_email_html(db_account),
        'o:testmode': ENVIRONMENT == 'testing'
    }
    response = await httpx_client.post('/messages', data=data)
    assert(response.status_code == 200), f"{response}"


def generate_verification_email_html(db_account):
    assert("email_token" in db_account)
    verification_url = (
        ADMIN_FRONTEND_URL + "/verification?token=" + db_account["email_token"]
    )
    return (
        '<h1>Welcome to FastSurvey!</h1>' +
        '<p>Please verify this email vie the following link:</p>' +
        f'<a href="{verification_url}" target="_blank">{verification_url}</a>' +
        '<p>Best,<br/>The FastSurvey Team</p>' +
        '<p><br/>If you have not signed up for this ' +
        'service, you can just ignore this email.</p>'
    )


async def send_forgot_password_mail(email: str, token: str):
    "to be implemented"
    pass
