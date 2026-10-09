from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail

from django.conf import settings


class EmailService:
    
    @staticmethod   
    def send_notification(to_email, subject, message):
        

        message_obj = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=message,
        )

        try:
            
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            
            response = sg.send(message_obj)

            if response.status_code == 202:
                
                return True
            
            return False

        except Exception as e:
            
            print(f"SendGrid Error: {str(e)}")
            
            return False