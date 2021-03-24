#!/usr/bin/python

# todo: Modify to run under Windows as curl doesn't seem to work the same. Test on MacOS.

import os, subprocess, json, sys, getopt

usage = "usage:\n\tupdate_godaddy_dns.py -k <godaddy_api_key> -s <godaddy_api_secret> -d <domain> -t <dns_record_type> -n <dns_host_record_name> -T <ttl_in_seconds> -P <priority_num> -p <protocol> -S <service> -w <weight_num>\nexample:\n\tupdate_godaddy_dns.py -k MyApiKey -s MyApiSecret -d mydomain.com -t A -n www -T 3600 -P 0 -p none -S none -w 1\n"
key = ""
secret = ""
domain = ""
type = 'A'
name = 'www'
ttl = 3600
priority = 0
protocol = 'none'
service = 'none'
weight = 0

# process opts
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "k:s:d:t:n:T:P:p:S:w:", ["key=", "secret=", "domain=", "type=", "name=", "ttl=", "priority=", "protocol=", "service=", "weight="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-s", "--secret"):
            secret = arg
        elif opt in ("-d", "--domain"):
            domain = arg
        elif opt in ("-t", "--type"):
            type = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-T", "--ttl"):
            ttl = arg
        elif opt in ("-P", "--priority"):
            priority = arg
        elif opt in ("-p", "--protocol"):
            protocol = arg
        elif opt in ("-S", "--service"):
            service = arg
        elif opt in ("-w", "--weight"):
            weight = arg
    return opts

if __name__ == "__main__":
    opts = main(sys.argv[1:])

# put opts into a json object
optsjsonstr = "{ "
i = 0
for opt, arg in opts:
    optsjsonstr += '"' + opt.replace("--", "") + '": ' + '"' + arg + '"'
    if (i != len(opts) - 1): optsjsonstr += ','
    i += 1
optsjsonstr += " }"
optsjson = json.loads(optsjsonstr)

# query go daddy API for the record
query_record = "curl -s -X GET -H 'Authorization: sso-key " + optsjson['key'] + ":" + optsjson['secret'] + "' 'https://api.godaddy.com/v1/domains/" + optsjson['domain'] + "/records/" + optsjson['type'] + "/" + optsjson['name'] + "'"
request = subprocess.run([query_record],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
record = json.loads(request.stdout)[0]  # this is the record returned in json

# query for public ip
ipreqproc = subprocess.run(["curl -s GET 'http://ipinfo.io/json'"],
        stdout=subprocess.PIPE,
        shell=True)
ipinfo = json.loads(ipreqproc.stdout) # this is the record for your public IP in json

# if the record ip is different than your public ip, make a web request to change the record
if (record['data'] != ipinfo['ip']):
    change_record = "curl -X PUT -H 'accept: application/json' -H 'Content-Type: application/json' -H 'Authorization: sso-key " + optsjson['key'] + ":" + optsjson['secret'] + "' 'https://api.godaddy.com/v1/domains/" + optsjson['domain'] + "/records/" + optsjson['type'] + "/" + optsjson['name'] + "' -d '[{ \"data\": \"" + ipinfo['ip'] + "\", \"port\": 80, \"priority\": " + optsjson['priority'] + ", \"protocol\": \"" + optsjson['protocol'] + "\", \"service\": \"" + optsjson['service'] + "\", \"ttl\": " + optsjson['ttl'] + ", \"weight\": " + optsjson['weight'] + " }]'"
    change_request = subprocess.run([change_record], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

