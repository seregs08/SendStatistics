import smtplib as smtp
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(mail_from, mail_to, mail_subject):
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = mail_subject

    filepath = r'C:\Путь до файла'
    filename = r'Название файла.xlsx'
    texthtml = 'HTML текст письма'

    msg.attach(MIMEText(texthtml, 'html'))
    with open(filepath + '\\' + filename, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment',
            filename=filename
        )
        msg.attach(part)

    with smtp.SMTP('SMTP почты') as serv:
        serv.sendmail(mail_from, mail_to, msg.as_string())