#!/usr/bin/env python3

# Copyright (c) 2019 Daniel Jakots
# Licensed under the MIT license. See the LICENSE file.

import datetime
import json
import time

import smtplib
import email.mime.text

import requests

PORTROACH = "https://portroach.openbsd.org"


def in_two_weeks():
    today = datetime.date.today()
    today_in_two_weeks = today + datetime.timedelta(days=14)
    return today_in_two_weeks.strftime("%Y/%m/%d")


def send_email(maintainer, ports):
    time.sleep(30)
    name = maintainer.split("<")[0].strip().title()
    # hack - https://stackoverflow.com/a/44780467
    ports = "\n".join(ports)
    body = (f"Hi {name},\n\n"
            "This email is a check to verify OpenBSD ports maintainers can\n"
            "be reached and wish to remain active.\n\n"
            "You currently maintain the following port(s):\n"
            f"{ports}\n\n"
            "If you wish to continue, please reply to this email letting me know.\n"
            f"If we don't hear from you before {in_two_weeks()}, or if you wish\n"
            "to release a particular port, we will drop the maintainer line.\n"
            "Thanks for your understanding!\n"
            f"\nCheers,\n-- \n"
            "Daniel")
    msg = email.mime.text.MIMEText(str(body))
    msg['Subject'] = "OpenBSD ports - maintainer check"
    msg['From'] = "Daniel Jakots <dont@spam.me>"
    msg['To'] = maintainer
    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()


def portroach(maintainer):
    g = requests.get(f"{PORTROACH}/json/{maintainer}.json")
    maintained_ports = g.json()
    result = []
    for port in maintained_ports:
        result.append(port["basepkgpath"])
    return result


def ignore(maintainer):
    if maintainer == "the openbsd ports mailing-list <ports@openbsd.org>":
        return True
    # ignore multi maintainership
    if maintainer.count("@") > 1:
        return True
    return False


def main():
    today = datetime.date.today().strftime("%Y/%m/%d")
    r = requests.get(f"{PORTROACH}/json/totals.json")
    data = json.loads(r.text)
    for result in data["results"]:
        maintainer = result["maintainer"]
        if ignore(maintainer):
            continue
        print(today, maintainer)
        data = portroach(maintainer)
        send_email(maintainer, data)


if __name__ == "__main__":
    main()
