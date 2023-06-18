import os
import smtplib
import requests
import classes
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

def get_latest_event(org_id, pg_num=1):
    load_dotenv(find_dotenv())
    url = 'https://www.eventbriteapi.com/v3/organizers/%i/events' % (org_id)
    headers = {
        'Authorization': 'Bearer %s' % (os.getenv('EVENT_AUTH'))
    }
    r = requests.get(url, headers=headers)
    r_json = r.json()
    current_pg = r_json['pagination']['page_number']
    last_pg = r_json['pagination']['page_count']
    events = r_json['events']
    is_last_pg = True if current_pg == last_pg else False
    latest_event = events[len(events)-1] if is_last_pg else get_latest_event(org_id, last_pg)
    return latest_event

def test_latest_event(orgs):
    outputs = []
    for org in orgs:
        event = get_latest_event(org.id)
        outputs.append(classes.Event(event['id'], event['name']['text'], event['start']['local'], event['start']['utc'], event['url']))
    for output in outputs:
        output.test()