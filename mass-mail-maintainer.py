#!/usr/bin/env python3

# Copyright (c) 2019 Daniel Jakots
# Licensed under the MIT license. See the LICENSE file.

import json

import requests

PORTROACH = "https://portroach.openbsd.org/json/totals.json"


def send_email(maintainer, ports):
    first_name = maintainer.split(" ")[0].capitalize()
    # hack - https://stackoverflow.com/a/44780467
    print(f"to: {maintainer}")
    ports = "\n".join(ports)
    body = (f"Hi {first_name},\n\n"
            f"You're marked as maintainer for some ports on OpenBSD.\n"
            "This email is to check if you still wants to maintain them.\n\n"
            "Here's the ports you're the maintainer of:\n"
            f"{ports}"
            f"\n\nCheers,\n-- \n"
            "Daniel")
    print(body)


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
    for n, result in enumerate(data["results"]):
        if n > 4:
            break
        maintainer = result["maintainer"]
        # ignore multi maintainership
        if maintainer.count("@") > 1:
            continue
        print(maintainer)
        data = portroach(maintainer)
        # for line in data:
        #     print("   ", line)
        send_email(maintainer, data)


if __name__ == "__main__":
    main()
