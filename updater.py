#!/usr/bin/python

from dnsimple import DNSimple
from urllib import urlopen
from sys import stderr, exit

domains = [{"domain": 'jshaver.net', "names": ["", "bc"]},
            {"domain": 'theamazingshavers.com', "names": [""]}]

token = "esnmgLubCqZkRKiNsbwVQ"

email = "bobjohnbob@gmail.com"

ttl = 600

dns = DNSimple(email=email, api_token = token)

response = urlopen("http://icanhazip.com/")

if response.getcode() != 200:
    stderr.write("Non 200 status when retrieving ip! Status: {}".format(response.getcode()))
    exit(-1)

ip = response.readline().rstrip()

def get_a_record(domain, name):
    records = dns.records(domain)
    for record in records:
        if record["name"] is name and ["record_type"] is 'A':
            return record
    return None

def update_record(domain, name, record, ip):
    new = {"record": {"name": name, "content": ip}}
    response = dns.update_record(domain, record["id"], new)
    return response["record"]

def create_record(domain, name, ip):
    new = {"record": {
            "name": name,
            "content",: ip,
            "record_type": "A",
            "ttl": ttl}}
    response = dns.add_record(domain, new)
    return response["record"]

def update_domain_ip(domain, name, ip):
    record = get_a_record(domain, name)

    if record is None:
        return create_record(domain, name, ip)

    if record["content"] is ip:
        return record

    return update_record(record, name, ip)

def main(domainList, ip):
    for domain in domainList:
        for name in domain["names"]:
            update_domain_ip(domain, name,  ip)

main(domains, ip)

