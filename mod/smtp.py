import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage


class smtpSendMsg:
    def __init__(self, addr_from, addr_to, password):
        self.addr_from = addr_from
        self.addr_to = addr_to
        self.password = password

        self.msg = MIMEMultipart()
        self.msg['From'] = addr_from
        self.msg['To'] = addr_to
        self.msg['Subject'] = 'Уведомление о наличии товара'

    def __call__(self, str):
        body = str
        self.msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.addr_from, self.password)
        server.send_message(self.msg)
        server.quit()
