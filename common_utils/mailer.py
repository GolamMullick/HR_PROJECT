import logging
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from graphql import GraphQLError

logger = logging.getLogger('openaccess')


class Mailer():

    def send_email(self, recipient, subject, html_message, text_message=None, sender='no-reply@myfarm.com'):
        try:
            mail_host = settings.EMAIL_HOST
            mail_port = settings.EMAIL_PORT
            host_user = settings.EMAIL_HOST_USER
            host_password = settings.EMAIL_HOST_PASSWORD
            server = smtplib.SMTP_SSL(mail_host, mail_port)
            server.login(host_user, host_password)
            # message = html_message

            message = MIMEMultipart("alternative")

            # Turn these into plain/html MIMEText objects

            if text_message:
                part1 = MIMEText(text_message, "plain")
                message.attach(part1)

            part2 = MIMEText(html_message, "html")
            message.attach(part2)

            message['Subject'] = subject
            message['From'] = sender
            message['To'] = recipient
            server.sendmail(sender, [recipient], message.as_string())
            server.quit()
            return True
        except Exception as exp:
            logger.warning('Send mail Failed. Exception: %s' % str(exp))
            raise GraphQLError('Send mail Failed. Exception: %s' % str(exp))
            return False
