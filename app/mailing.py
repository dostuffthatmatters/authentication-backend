import os
import httpx


# development / production / testing environment
ENV = os.getenv('ENV')
# frontend url
FURL = os.getenv('FURL')
# mailgun api key
MGKEY = os.getenv('MGKEY')


class Letterbox:
    """Well ... you post it, and sometimes it arrives where it should."""

    def __init__(self):
        """Create a general email client to be used by all surveys."""
        self.domain = 'fastsurvey.io'
        self.sender = f'FastSurvey <noreply@{self.domain}>'
        self.client = httpx.AsyncClient(
            auth=('api', MGKEY),
            base_url=f'https://api.eu.mailgun.net/v3/email.{self.domain}',
        )

    async def send(self, receiver: str, subject: str, html: str):
        """Send an email to the given receiver."""
        data = {
            'from': self.sender,
            'to': f'test@{self.domain}' if ENV != 'production' else receiver,
            'subject': subject,
            'html': html,
            'o:testmode': ENV == 'testing',
            'o:tag': [f'{ENV} transactional'],
        }
        response = await self.client.post('/messages', data=data)
        return response.status_code

    async def send_verification_email(self, receiver: str, token: str):
        """Send confirmation email in order to verify an email address."""
        subject = 'Welcome to FastSurvey!'
        vurl = f'{FURL}/verify?token={token}'  # verification url
        html = (
            '<p>Welcome to FastSurvey!</p>'
            + f'<p>Please verify your email address by <a href="{vurl}" target="_blank">clicking here</a>.</p>'
            + '<p>The verification link is valid for 10 minutes.</p>'
            + '<p>Best, the FastSurvey team</p>'
        )
        return await self.send(receiver, subject, html)

    async def send_reset_password_email(self, receiver: str, token: str):
        """Send email in order to reset the password of an existing account."""
        subject = 'Reset Your FastSurvey Password'
        rurl = f'{FURL}/set-password?token={token}'  # reset url
        html = (
            '<p>Hi there,</p>'
            + f'<p>You can set your new password by <a href="{rurl}" target="_blank">clicking here</a>.</p>'
            + '<p>Best, the FastSurvey team</p>'
        )
        return await self.send(receiver, subject, html)
