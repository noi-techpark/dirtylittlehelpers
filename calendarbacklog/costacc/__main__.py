import json
import sys
import os
from datetime import datetime
from dateutil.tz import tzutc, tzlocal

CAT_ALLOWED = [
    "Know-How Transfer Events",
    "Networking & Cooperation",
    "R&D Consultancy",
    "Communication",
    "Training",
    "Administration",
    "Special Project",
    "Special Project: NOI Community App",
    "Special Project: St. Virtual",
    "Opportunity",
    "Management",
    "Open Data Hub",
    "Free Software Lab",
]

SKIP_PREFIXES = [
    "*",
    "Abwesend",
    "Urlaub",
    "Feiertag"
]

def main():
    if len(sys.argv) != 4:
        print("USAGE: %s input monthnumber year" % os.path.basename(sys.argv[0]))
        print("       input        json file exported from https://developer.microsoft.com/en-us/graph/graph-explorer")
        print("       monthnumber  the number of the month (ex., May => 5)")
        print("       year         the year (2019 or 19)")
        print("For more information see calendar-output.md")
        print()
        sys.exit(1)

    month = int(sys.argv[2])
    year = int(sys.argv[3])

    if year < 100:
        year += 2000

    fn_json = sys.argv[1]

    with open(fn_json, 'r') as file_in:
        j = json.load(file_in)

        sorted_events = sorted(j['value'], key=lambda x: x['start']['dateTime'])

        print("subject,start_date,start_time,end_date,end_time,category")

        for r in sorted_events:
            start_date, start_time = make_local_date_time(r['start']['dateTime'])
            end_date, end_time = make_local_date_time(r['end']['dateTime'])
            category = ", ".join(r['categories']).strip()
            subj = r['subject'].replace('"', "'").strip()

            if start_date.month != month or start_date.year != year:
                continue

            if r['isAllDay']:
                print_inf(f"Skipping (allday) -> {r['subject']}")
                continue

            if r['isCancelled']:
                print_inf(f"Skipping (cancelled) -> {r['subject']}")
                continue

            prefix = skip_prefix(subj)
            if prefix:
                print_inf(f"Skipping (prefix '{prefix}') -> {r['subject']}")
                continue

            # if not category:
            #     print_err(f"NO category -> {r['subject']}")

            # if category not in CAT_ALLOWED:
            #     print_err(f"Wrong category '{category}' -> {r['subject']}")

            print(f'"{subj}",{start_date},{start_time},{end_date},{end_time},{category}')

def skip_prefix(subj):
    for prefix in SKIP_PREFIXES:
        if subj.startswith(prefix):
            return prefix
    return ""

def make_local_date_time(datetime_str):
    utc_date = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.0000000")
    utc_date = utc_date.replace(tzinfo=tzutc())
    local_date = utc_date.astimezone(tzlocal())

    return (
        local_date.date(),
        local_date.strftime("%H:%M")
    )

def print_inf(info):
    print(f"\033[92mINF: {info}\033[00m", file=sys.stderr)

def print_err(warn):
    print(f"\033[91mERR: {warn}\033[00m", file=sys.stderr)

if __name__ == '__main__':
    main()