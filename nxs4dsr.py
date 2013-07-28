import sys
from bs4 import BeautifulSoup
import requests

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def get_content(url):
    return requests.get(url)

def is_available(html):
    print 'is_available', len(html)
    soup = BeautifulSoup(html)
    return len(soup.find_all('span', 'hardware-sold-out')) == 0

def process_url(url):
    print 'process', url
    res = get_content(url)
    if res.status_code != 200:
        print 'error getting content from ', url
        exit()

    return is_available(res.text)

def send_notify(url, email, is_avail):
    if is_avail:
        msg = MIMEText("%s is showing availability!" % (url))
        msg["From"] = email
        msg["To"] = email
        msg["Subject"] = "warm up your credit card, son"
        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        p.communicate(msg.as_string())

def main(url, notify_email):
    result = process_url(url)
    send_notify(url, notify_email, result) 


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'usage: python nxs4dsr.py {URL} {NOTIFY_EMAIL}'
    main(sys.argv[1], sys.argv(2))


