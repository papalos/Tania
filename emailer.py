import smtplib as smtp
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv


class Mailer:
    server = ''
    port = ''
    email = ''
    login = ''
    password = ''

    def read_setup(self):
        with open('setup.csv', newline='') as setup:
            setup = csv.reader(setup, delimiter=':')
            for row in setup:
                if row[0] == 'server': self.server = row[1]
                if row[0] == 'port': self.port = row[1]
                if row[0] == 'email': self.email = row[1]
                if row[0] == 'login': self.login = row[1]
                if row[0] == 'password': self.password = row[1]

    def setup(self, server, port, email, login, password):
        with open('setup.csv', 'w+', newline='') as setup:
            writer = csv.writer(setup)
            writer.writerows([[f'server:{server}'], [f'port:{port}'], [f'email:{email}'], [f'login:{login}'],
                              [f'password:{password}']])

    def send_email(self, destination, subject, body, attach=None):
        # text = MIMEText(body, 'plain', 'utf-8')
        text = MIMEText(body, 'html', 'utf-8')

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = destination
        msg.attach(text)

        if attach:
            with open(attach, "rb") as f:
                attachment = MIMEBase('application', 'pdf')
                attachment.set_payload(f.read())
                print(attach.split('/')[-1])
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', attach.split('/')[-1]))
                msg.attach(attachment)

        server = smtp.SMTP(self.server, self.port)
        server.starttls()
        server.set_debuglevel(0)
        server.ehlo()
        server.login(self.login, self.password)
        server.auth_plain()
        server.sendmail(self.email, destination, msg.as_string())
        server.quit()

    def spam(self, data_file):
        with open(data_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            for row in spamreader:
                if '@' in row[0]:
                    self.send_email(row[0], row[1], row[2], row[3])


if __name__ == '__main__':
    ml = Mailer()
    print('до чтения файла настрйоки', ml.login)
    print('до чтения файла настрйоки', ml.password)
    ml.read_setup()
    print('после чтения файла настрйоки', ml.login)
    print('после чтения файла настрйоки', ml.password)
    ml.send_email('hseolymp@yandex.ru', 'Олимпиада', 'Когда будут опубликованы результаты высшего пилотажа', 'i.jpg')
    # ml.spam('address.csv')
