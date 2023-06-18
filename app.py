import functions
import config
import classes

ORGS = []

def gen_orgs():
    for org in config.ORGS:
        ORGS.append(classes.Org(org['org_id'], org['name']))

host_name, port_num, user, password = config.get_cred()
#config.deploy(config.FROM_ADDR, config.TO_ADDR, config.SUBL_TEXT, config.MSG_TEXT)
gen_orgs()
functions.test_latest_event(ORGS)