import os
import smtplib
import requests
import classes
from jinja2 import Environment, FileSystemLoader, select_autoescape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

LOCKFILE = '.lockfile'

def gen_lockfile():
    with open(LOCKFILE, 'w+') as f:
        pass

def is_lockfile():
    if os.path.isfile(LOCKFILE):
        return True
    else:
        return False

def get_template(filename):
    with open(filename) as f:
        template_code = f.read()
    return template_code

def personalize(template, pers_dict):
    environment = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape()
    )
    template = environment.get_template(template)
    return template.render(**pers_dict)

def deploy(host_name, port_num, emailuser, password, from_addr, to_addr, subj_txt, msg_txt):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subj_txt
    message = msg_txt
    msg.attach(MIMEText(message, 'html'))
    server = smtplib.SMTP(host_name, port_num)
    server.login(emailuser, password)
    server.sendmail(
        from_addr,
        to_addr,
        msg.as_string()
    )
    server.quit()

def get_latest_event(org_id, event_auth, pg_num=1):
    url = 'https://www.eventbriteapi.com/v3/organizers/%s/events' % (org_id)
    headers = {
        'Authorization': 'Bearer %s' % (event_auth)
    }
    r = requests.get(url, headers=headers)
    r_json = r.json()
    current_pg = r_json['pagination']['page_number']
    last_pg = r_json['pagination']['page_count']
    events = r_json['events']
    is_last_pg = True if current_pg == last_pg else False
    latest_event = events[len(events)-1] if is_last_pg else get_latest_event(org_id, event_auth, last_pg)
    return latest_event

def get_all_latest_events(orgs, event_auth):
    outputs = []
    for org in orgs:
        event = get_latest_event(org.id, event_auth)
        outputs.append(classes.Event(event['id'], event['organizer_id'], event['name']['text'], event['start']['local'], event['start']['utc'], event['url']))
    return outputs