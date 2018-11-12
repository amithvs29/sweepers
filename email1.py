import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging


class email1(object):
    def __init__(self, server, username, password, tls=True):
        self.server = smtplib.SMTP(server)
        if tls:
            self.server.starttls()
        self.server.login(username, password)
        logging.info('Logged into email server')
        self.fromaddr = username

    def set_recipients(self, recipients_list):
        self.recipients = recipients_list

    def set_email_content(self, email_subject, email_body, email_body_type='plain'):
        self.email_subject = email_subject
        self.email_body = email_body
        self.email_body_type = email_body_type

    def new_email(self):
        self.msg = MIMEMultipart()

    def attach_file(self, filename):
        with open(filename, "rb") as f:
            part = MIMEApplication(f.read(), Name=basename(filename))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        if not hasattr(self, 'msg'):
            self.msg = MIMEMultipart()
        self.msg.attach(part)

    def send(self):
        if not hasattr(self, 'msg'):
            self.msg = MIMEMultipart()
        self.msg['From'] = self.fromaddr
        self.msg['To'] = ', '.join(self.recipients)
        self.msg['Subject'] = self.email_subject
        self.msg.attach(MIMEText(self.email_body, self.email_body_type))
        self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        logging.info('Sent email to ' + self.msg['To'])
