import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def deploy(fromAddr, toAddr, subjTxt, msgTxt):
    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = subjTxt
    message = msgTxt
    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP(config.HOST_NAME, config.PORT_NUM)
    server.login(config.USER, config.PASS)
    server.sendmail(
        fromAddr,
        toAddr,
        msg.as_string()
    )
    server.quit()

deploy(config.FROM_ADDR, config.TO_ADDR, config.SUBL_TEXT, config.MSG_TEXT)