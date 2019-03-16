#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import requests
import argparse
import logging
import json
import os
import sentry_sdk
sentry_sdk.init("https://a35a6ccc460a4e7fab874ccb67e2f064@sentry.io/1326307")

#API Handling
API = 'https://api.digitalocean.com/v2'
DOMAIN_NOT_FOUND = 1
RECORD_NOT_FOUND = 2
REQUEST_ERROR = 4
IP_FETCH_FAILED = 8

def getIp():
    r = requests.get('https://api.ipify.org')
    if r.status_code != 200:
        sys.exit(IP_FETCH_FAILED)
    return r.text

def request(uri, params={}, method='GET'):
    url = API + '/' + uri.strip('/')

    headers = {
        'Authorization': 'Bearer {0}'.format(TOKEN)
    }

    logging.debug('Requesting: %s (%s)' % (url, method))
    try:
        if method == 'POST':
            r = requests.post(url, headers=headers, data=params)
        elif method == 'PUT':
            r = requests.put(url, headers=headers, data=params)
        else:
            r = requests.get(url, params=params, headers=headers)

        if r.status_code < 200 or r.status_code >= 300:
            logging.error('Host replied with a non-OK status.')
            logging.error(r.status_code)
            sys.exit(REQUEST_ERROR)
    except(ConnectionError):
        logging.error('Connection error!')
        exit()

    return r.json()

# Define arguments.
parser = argparse.ArgumentParser(description='Dynamic DNS updater for Digital Ocean')
parser.add_argument('--domain', '-d', help='Domain name', required=True)
parser.add_argument('--record', '-r', help='Record for domain', required=True)
parser.add_argument('--key', '-k', help='DigitalOcean API key', required=True)
parser.add_argument('--allownew', '-c', help='Allow creation of a new record', action='store_true')
parser.add_argument('--verbose', '-v', help='Increase verbosity', action='count', default=0)
args = parser.parse_args()

# Set TOKEN.
TOKEN = str(format(args.key))

# Verbosity level config.
if args.verbose >= 2:
    debug = logging.DEBUG
elif args.verbose == 1:
    debug = logging.INFO
else:
    debug = logging.WARNING

logging.basicConfig(filename='dnsUpdater.log', format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y-%I:%M:%S-%p', level=debug)

# Looking up the records.
recordId = None
records = request('/domains/{0}/records'.format(args.domain))
for record in records.get('domain_records'):
    if record.get('type') == 'A' and record.get('name') == args.record:
        recordId = record.get('id')
        logging.info('Found record %s, ID: %s.' % (args.record, recordId))
        break

# Create the record if it does not exist.
if not recordId:
    if not args.allownew:
        logging.warning('Could not find the A record %s for domain %s.' % (args.record, args.domain))
        sys.exit(RECORD_NOT_FOUND)

    ip = getIp()
    params = {
        'type': 'A',
        'name': args.record,
        'data': ip
    }
    result = request('/domains/{0}/records'.format(args.domain), params=params, method='POST')
    logging.info('Record created with ID %s using IP %s.' % (result.get('domain_record', {}).get('id', '<?>'), ip))

# Update the existing record.
else:
    ip = getIp()
    if record.get('data') == ip:
        logging.info('No update required.')

    else:
        params = {
            'type': 'A',
            'name': args.record,
            'data': ip
        }
        result = request('/domains/{0}/records/{1}'.format(args.domain, recordId), params=params, method="PUT")
        logging.info('Updated record with IP %s.' % (ip))