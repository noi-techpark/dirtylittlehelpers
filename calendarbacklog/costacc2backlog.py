#!/usr/bin/env python3

# SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import sys
import csv
import re
from datetime import datetime

def main():
    
    class Thunderbird(csv.Dialect):
        """Describe the usual properties of Thunderbird-calendar-generated CSV files."""
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = '\r\n'
        quoting = 1

    csv.register_dialect("thunderbird", Thunderbird)
    
    parser = re.compile("([^:]*): (.*$)")        
    reader = csv.reader(sys.stdin.readlines(), dialect='thunderbird')
    writer = csv.writer(sys.stdout, dialect='thunderbird')
    
    old_date = ""
    count_hours = 0.0
    for row in reader:
        
        if row[0] == "subject" and row[1] == "start_date":
            print_inf("Starting with new CSV, header found...")
            continue
        
        parsed = parser.split(row[0])
        if len(parsed) == 1:
            subj = parsed[0]
            proj = ""
        else:
            proj = parsed[1]
            subj = parsed[2]
            
        if len(proj) == 0:
            proj = fix_proj(subj)
            if len(proj) == 0:
                print_err(f"{start_date}: MISSING PROJECT NAME: '{subj}' - {start_time} - {end_time}")
            else:
                print_inf(f"{start_date}: MISSING PROJECT NAME: '{subj}' - {start_time} - {end_time} --> Autodetected: {proj}")

        proj = proj.lower()            
            
        start_date = row[1]
        start_time = row[2]
        end_date = row[3]
        end_time = row[4]
        
        if start_date != old_date:
            if count_hours > 0 and count_hours != 8:
                print_err(f"{old_date}: WORKED {count_hours} HOURS")
            count_hours = 0
            old_date = start_date
        
        if start_date != end_date:
            print_err(f"{start_date}: We have a multiday event from {start_date} to {end_date}.")
        
        diff_hours = (
            (
                datetime.strptime(end_time, '%H:%M') 
                - datetime.strptime(start_time, '%H:%M')
            )
            .total_seconds() / 3600
        )
        count_hours += diff_hours
        
        writer.writerow(
            [
                datetime.strptime(start_date, '%Y-%m-%d').strftime("%V"), 
                start_date, 
                proj, 
                subj, 
                start_time, 
                end_time, 
                diff_hours
            ]
        )
    
PROJECT_DETECTION = {
    "solda": [
        "solda",
        "ip compliance"
    ],
    "odh": [
       "A22 Events",
       "Open Data Hub",
       "Data Collector"
    ],
    "noiapp": [
        "NOI-Community App"
    ],
    "noi": [
        "NOI goes digital",
        "Tech Transfer Digital",
        "NOI-Team Klausur"
    ],
    "infrastructure": [
        "AWS ECS",
        "ECS Terraform",
        "Matrix/Element",
        "Jitsi - AWS"
    ]
}
        
def fix_proj(subj):
    
    result = None
    
    for proj, phrases in PROJECT_DETECTION.items():
        for phrase in phrases:
            if phrase.lower() in subj.lower():
                if result == None:
                    result = proj.lower()
                else:
                    print_err(f"Cannot fix project: Multiple matches --> {result} + {proj}")
                    return ""
    return result if result else ""
        
def print_inf(info):
    print(f"\033[92mINF: {info}\033[00m", file=sys.stderr)

def print_err(warn):
    print(f"\033[91mERR: {warn}\033[00m", file=sys.stderr)
    
if __name__ == '__main__':
    main()
    