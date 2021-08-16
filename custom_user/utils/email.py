from decouple import config
from sendgrid.helpers.mail import Mail, To
from sendgrid import SendGridAPIClient

class Email:
    @staticmethod
    def send_new_registration_email(to_email,role,password):
        # create Mail object and populate
        message = Mail(
            from_email=config('EMAIL_HOST_USER'),
            to_emails=[ to_email ],
            )

        # pass custom values for HTML placeholders
        message.dynamic_template_data = {
            'role': role,
            'password': password,
            'frontend_url': config('FRONTEND_URL')
        }
        message.template_id = config('SENDGRID_USER_REGISTRATION_MAIL_TEMPLATE')

        # create our sendgrid client object, pass it our key, then send and return our response objects
        sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print("Registration >>>>>> Mail Sent")