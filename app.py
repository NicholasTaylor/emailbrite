import functions
import classes
import os
import json
from dotenv import load_dotenv, find_dotenv

ORGS = []
CONTACTS = []

def gen_metadata():
    for org in json.loads(os.getenv('ORGS')):
        ORGS.append(classes.Org(**org))
    for contact in json.loads(os.getenv('CONTACTS')):
        CONTACTS.append(classes.Contact(**contact))

def main():
    load_dotenv(find_dotenv())
    gen_metadata()
    events = functions.get_all_latest_events(ORGS, os.getenv('EVENT_AUTH'))
    for event in events:
        if event.is_future():
            for contact in CONTACTS:
                if contact.is_optin(event.org_id):
                    msg = functions.personalize(os.getenv('TEMPLATE'), {'first_name': contact.first_name, 'event_name': event.name, 'event_url': event.url})
                    functions.deploy(os.getenv('HOST_NAME'), os.getenv('PORT_NUM'), os.getenv('EMAILUSER'), os.getenv('PASSWORD'), os.getenv('FROM_ADDR'), contact.email, os.getenv('SUBL_TEXT'), msg)
main()