from os import getenv, path
import smtplib
from email.message import EmailMessage
import mimetypes
import envconfiguration as config

class SMTPClient:
    def __init__(self):
        self.SMTP_SERVER = config.SMTP_EXT_SERVER
        self.SMTP_PORT = config.SMTP_EXT_PORT
        self.MAIL_ACCOUNT = config.MAIL_EXT_ACCOUNT
        self.MAIL_PASSWORD = config.MAIL_EXT_PASSWORD
        self.MAIL_FROM = config.MAIL_EXT_FROM
        # self.SMTP_SERVER = config.GOOGLE_SMTP_SERVER
        # self.SMTP_PORT = config.GOOGLE_SMTP_PORT
        # self.MAIL_ACCOUNT = config.GOOGLE_SMTP_USER
        # self.MAIL_PASSWORD = config.GOOGLE_SMTP_PASSWORD
        # self.MAIL_FROM = config.GOOGLE_SMTP_USER
        self.toAddresses = []
        self.bccAddresses = []
        self.ccAddresses = []
        self.subject = 'Messagem enviada automáticamente pelo sistema'
        self.senderEmail = self.MAIL_FROM
        self.htmlMessage = ''
        self.textMessage = ''
        self.attachments = []
        print( "Dados sendo trazidos do env",
            "self.SMTP_SERVER" + self.SMTP_SERVER,
            "self.SMTP_PORT" +self.SMTP_PORT,
            "self.MAIL_ACCOUNT", self.MAIL_ACCOUNT,
            "self.MAIL_PASSWORD", self.MAIL_PASSWORD,
            "self.MAIL_FROM", self.MAIL_FROM,
        )

    def send(self):
        
        if len(self.toAddresses) == 0:
            print('Enter an email address for toAddresses')
            return False

        message = EmailMessage()
        message['Subject'] = self.subject
        message['From'] = self.senderEmail
        message['To'] = self.toAddresses
        message['Bcc'] = ', '.join(self.bccAddresses)
        message['Cc'] = ', '.join(self.ccAddresses)
        message.set_content(self.textMessage, subtype='plain')
        message.add_alternative(self.htmlMessage, subtype='html')
        
        for file_path in self.attachments:
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            file_name = path.basename(file_path)
            mime_type, encoding = mimetypes.guess_type(file_path)
            maintype = 'application'
            subtype = 'octet-stream'
            if mime_type:
                maintype, subtype = mime_type.split('/', 1)

            message.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

        smtp = smtplib.SMTP(host=self.SMTP_SERVER, port=self.SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.MAIL_ACCOUNT, self.MAIL_PASSWORD)
        
        try:
            print('Sending email...')
            smtp.send_message(message)
            print('Email sent!')
            smtp.quit()
            return True
        except Exception as error:
            print("dentro de erro", error)
            return False
       