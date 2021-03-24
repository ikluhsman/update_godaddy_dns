# Update GoDaddy DNS

Python script to update a DNS record for your domain using the Go Daddy API.

Works in Linux OS's, not tested in MacOS or Windows.

# Usage

usage:
        update_godaddy_dns.py -k <godaddy_api_key> -s <godaddy_api_secret> -d <domain> -t <dns_record_type> -n <dns_host_record_name> -T <ttl_in_seconds> -P <priority_num> -p <protocol> -S <service> -w <weight_num>
example:
        update_godaddy_dns.py -k MyApiKey -s MyApiSecret -d mydomain.com -t A -n www -T 3600 -P 0 -p none -S none -w 1
