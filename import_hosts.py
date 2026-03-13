import requests
import csv

ZABBIX_URL = ""
ZABBIX_TOKEN = ""

headers = {
    "Content-Type": "application/json-rpc",
    "Authorization": f"Bearer {ZABBIX_TOKEN}"
}

# -------------------------
# API REQUEST
# -------------------------

def zabbix_api(method, params):

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    response = requests.post(ZABBIX_URL, json=payload, headers=headers)
    data = response.json()

    if "error" in data:
        print("ERRO API:", data["error"])
        return None

    return data.get("result")


# -------------------------
# GET HOSTGROUP
# -------------------------

def get_hostgroup(group_name):

    result = zabbix_api(
        "hostgroup.get",
        {
            "output": ["groupid", "name"],
            "filter": {
                "name": [group_name]
            }
        }
    )

    if result:
        return result[0]["groupid"]

    print("Grupo nÃ£o encontrado:", group_name)
    return None


# -------------------------
# GET TEMPLATE
# -------------------------

def get_template(template_name):

    result = zabbix_api(
        "template.get",
        {
            "output": ["templateid", "name"],
            "filter": {
                "name": [template_name]
            }
        }
    )

    if result:
        return result[0]["templateid"]

    print("Template nÃ£o encontrado:", template_name)
    return None


# -------------------------
# CREATE HOST (SNMP)
# -------------------------

def create_host(hostname, ip, groupid, templateid, community):

    result = zabbix_api(
        "host.create",
        {
            "host": hostname,
            "interfaces": [
                {
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": 2,
                        "community": community
                    }
                }
            ],
            "groups": [
                {"groupid": groupid}
            ],
            "templates": [
                {"templateid": templateid}
            ],
            "macros": [
                {
                    "macro": "{$SNMP_COMMUNITY}",
                    "value": community
                }
            ]
        }
    )

    if result:
        print("Host criado:", hostname)
    else:
        print("Erro ao criar host:", hostname)


# -------------------------
# IMPORT CSV
# -------------------------

def import_hosts():

    with open("hosts.csv") as file:

        reader = csv.DictReader(file)

        for row in reader:

            hostname = row["hostname"].strip()
            ip = row["ip"].strip()
            group = row["group"].strip()
            template = row["template"].strip()
            community = row["community"].strip()

            print("\nImportando:", hostname)

            groupid = get_hostgroup(group)
            templateid = get_template(template)

            if not groupid:
                continue

            if not templateid:
                continue

            create_host(hostname, ip, groupid, templateid, community)


# -------------------------
# RUN
# -------------------------

import_hosts()
