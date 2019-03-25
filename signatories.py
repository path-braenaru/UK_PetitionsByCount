#!/usr/bin/env python


import argparse
import json
import operator
import requests


class co:
    PU = '\033[95m'
    CY = '\033[96m'
    DC = '\033[36m'
    BL = '\033[94m'
    GR = '\033[92m'
    RE = '\033[91m'
    BO = '\033[1m'
    E = '\033[0m'


class factory():
    def grab_link(self, link):
        r = requests.get(link)
        JSONdata = json.loads(r.text)
        return JSONdata


    def meta(self, JSONdata):
        title = 'Title:\n%s' % \
                JSONdata['data']['attributes']['action']

        sig_Count = 'Current count:\n%s' % \
                    str(JSONdata['data']['attributes']['signature_count'])
        title_Count = title + '\n' + sig_Count
        return title_Count


def crunch(JSONdata, cm, cl, outCount):
    all = {}
    for x in JSONdata['data']['attributes']['signatures_by_constituency']:
        place = x['name'].encode('ascii', 'ignore')
        count = int(x['signature_count'])
        if not place in all:
            all[place] = count

    most = dict(sorted(all.items(), key=operator.itemgetter(1), reverse=True)[:outCount])
    least = dict(sorted(all.items(), key=operator.itemgetter(1))[:outCount])

    print('%sMost Signatures%s' % (co.DC, co.E))
    for key,val in sorted(most.iteritems(),key=lambda (k,v):(v,k),reverse=True):
        print('%s%s: %s%s' % (cm, key, str(val), co.E))

    print('%sLeast Signatures%s' % (co.DC, co.E))
    for key,val in sorted(least.iteritems(),key=lambda (k,v):(v,k),reverse=True):
        print('%s%s: %s%s' % (cl, key, str(val), co.E))


def __init__():
    a = argparse.ArgumentParser()
    a.add_argument(
        '-l', '--link')
    a.add_argument(
        '-c', '--count', default=5)
    a.add_argument(
        '--agree', action='store_true', default=False)
    args = a.parse_args()
    link = args.link
    outCount = int(args.count)
    if not args.agree:
        cm = co.RE
        cl = co.GR
    else:
        cm = co.GR
        cl = co.RE
    if not link:
        print("\nNo link given! Try again...\n")
        exit(0)
    if not link.startswith('http'):
        link = 'https://' + link
    f = factory()
    JSONdata = f.grab_link(link)
    title_Count = f.meta(JSONdata)
    print('%s%s%s\n' % (co.BO, title_Count, co.E))
    crunch(JSONdata, cm, cl, outCount)


if __name__ == '__main__':
    __init__()
