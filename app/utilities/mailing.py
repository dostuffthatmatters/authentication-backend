
from app import ENVIRONMENT, httpx_client


async def send_verification_mail(db_account):
    data = {
        'from': 'noreply@admin.fastsurvey.io',
        'to': db_account["email"],
        'subject': 'Please verify your FastSurvey account',
        'html': generate_verification_email(db_account),
        'o:testmode': ENVIRONMENT == 'testing'
    }
    response = await httpx_client.post('/messages', data=data)
    return response.status_code == 200


def generate_verification_email(db_account):
    return ''
