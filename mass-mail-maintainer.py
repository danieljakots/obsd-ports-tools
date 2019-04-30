#!/usr/bin/env python3

# Copyright (c) 2019 Daniel Jakots
# Licensed under the MIT license. See the LICENSE file.

import json

import smtplib
import email.mime.text

import requests

PORTROACH = "https://portroach.openbsd.org/json/totals.json"


def send_email(maintainer, ports):
    name = maintainer.split("<")[0].strip().title()
    # hack - https://stackoverflow.com/a/44780467
    ports = "\n".join(ports)
    body = (f"Hi {name},\n\n"
            "This email is a check to verify OpenBSD ports maintainers can\n"
            "be reached and wish to remain active.\n\n"
            "You currently maintain the following port(s):\n"
            f"{ports}\n\n"
            "If you wish to continue, please respond. If we don't hear from\n"
            "you before the beginning of June, or if you wish to release a\n"
            "particular port, we will drop the maintainer line.\n"
            "Thanks for your understanding!\n"
            f"\nCheers,\n-- \n"
            "Daniel")
    msg = email.mime.text.MIMEText(str(body))
    msg['Subject'] = "About OpenBSD ports you maintain"
    msg['From'] = "Daniel Jakots <dont@spam.me>"
    msg['To'] = maintainer
    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()


def portroach(maintainer):
    g = requests.get(f"https://portroach.openbsd.org/json/{maintainer}.json")
    maintained_ports = g.json()
    result = []
    for port in maintained_ports:
        results = port["basepkgpath"]
        if port["newver"]:
            results = results + f" (newer version {port['newver']} is available)"
        else:
            results = results + " (up to date)"
        result.append(results)
    return result


def main():
    r = requests.get(PORTROACH)
    data = json.loads(r.text)
    for result in data["results"]:
        maintainer = result["maintainer"]
        # ignore multi maintainership
        if maintainer.count("@") > 1:
            continue
        data = portroach(maintainer)
        send_email(maintainer, data)


if __name__ == "__main__":
    main()
