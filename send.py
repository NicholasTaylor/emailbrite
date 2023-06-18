import os
import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, find_dotenv

def deploy(from_addr, to_addr, subj_txt, msg_txt):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subj_txt
    message = msg_txt
    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP(host_name, port_num)
    server.login(user, password)
    server.sendmail(
        from_addr,
        to_addr,
        msg.as_string()
    )
    server.quit()

def get_cred():
    load_dotenv(find_dotenv())
    return os.getenv('HOST_NAME'), os.getenv('PORT_NUM'), os.getenv('USER'), os.getenv('PASS')

host_name, port_num, user, password = get_cred()
deploy(config.FROM_ADDR, config.TO_ADDR, config.SUBL_TEXT, config.MSG_TEXT)