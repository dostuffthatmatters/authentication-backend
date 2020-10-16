
from app import httpx_client, ENVIRONMENT, ADMIN_FRONTEND_URL


EMAIL_APPENDIX = (
    '<p>Best, the FastSurvey team</p>' +
    '<p><br/>If you have not signed up for this ' +
    'service, you can just ignore this email.</p>'
)


async def send_verification_mail(db_account):
    data = {
        'from': 'FastSurvey <noreply@fastsurvey.io>',
        'to': db_account["email"],
        'subject': 'Verify your FastSurvey account',
        'html': verification_email_html(db_account),
        'o:testmode': ENVIRONMENT == 'testing'
    }
    response = await httpx_client.post('/messages', data=data)
    assert(response.status_code == 200), f"{response}"


def verification_email_html(db_account):
    assert("email_token" in db_account)
    verification_url = (
        ADMIN_FRONTEND_URL + "/verify-email?token=" + db_account["email_token"]
    )
    return (
        '<h1>Welcome to FastSurvey!</h1>' +
        '<p>Please verify this email via the following link:</p>' +
        f'<a href="{verification_url}" target="_blank">{verification_url}</a>' +
        EMAIL_APPENDIX
    )


async def send_forgot_password_mail(email: str, token: str):
    data = {
        'from': 'FastSurvey <noreply@fastsurvey.io>',
        'to': email,
        'subject': 'Restore your FastSurvey password',
        'html': forgot_password_email_html(token),
        'o:testmode': ENVIRONMENT == 'testing'
    }
    response = await httpx_client.post('/messages', data=data)
    assert(response.status_code == 200), f"{response}"


def forgot_password_email_html(token: str):
    verification_url = (
        ADMIN_FRONTEND_URL + "/forgot-password?token=" + token
    )
    return (
        '<h1>Restore your FastSurvey account</h1>' +
        '<p>Please set a new password via the following link:</p>' +
        f'<a href="{verification_url}" target="_blank">{verification_url}</a>' +
        EMAIL_APPENDIX
    )
