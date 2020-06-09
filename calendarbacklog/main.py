import sys
import os
import csv
from datetime import datetime
import operator
import re
from csv import Dialect, register_dialect

def main():
    if len(sys.argv) != 4:
        print("USAGE: %s input monthnumber year" % os.path.basename(sys.argv[0]))
        print("       input        filename of a temporal data file (TSV)")
        print("       monthnumber  the number of the month (ex., May => 5)")
        print("       year         the year (2019 or 19)")
        print()
        sys.exit(1)

    csvFilename = sys.argv[1]
    csvFilenameOut = csvFilename + '.out'
    month = int(sys.argv[2])
    year = int(sys.argv[3])

    if year < 100:
        year += 2000

    parser = re.compile("([^:]*): (.*$)")

    with open(csvFilename, 'r') as csvfile, open(csvFilenameOut, 'w+') as csvfileout:
        reader = csv.reader(csvfile, dialect='thunderbird')
        writer = csv.writer(csvfileout, dialect='thunderbird')

        if csv.Sniffer().has_header(csvfile.read(1024)):
            csvfile.seek(0)
            next(reader)

        sortedlist = sorted(reader, key=sort_order, reverse=False)

        for row in sortedlist:
            parsed = parser.split(row[0])
            if len(parsed) == 1:
                subj = parsed[0]
                proj = ""
            else:
                proj = parsed[1]
                subj = parsed[2]
            start_date = datetime.strptime(row[1], '%m/%d/%y').date()

            if start_date.year != year or start_date.month != month:
                continue

            if row[5] == 'True':
                full_day_event = True
            else: 
                full_day_event = False

            start_time = datetime.strptime(row[2], '%I:%M:%S %p')
            start_time_str = datetime.strftime(start_time, '%H:%M')
            end_date = datetime.strptime(row[3], '%m/%d/%y').date()
            end_time = datetime.strptime(row[4], '%I:%M:%S %p')
            end_time_str = datetime.strftime(end_time, '%H:%M')

            diff_hours = (end_time - start_time).total_seconds() / 3600

            if full_day_event:
                start_time_str = ''
                end_time_str = ''
                diff_hours = ''
                if len(proj) == 0:
                    proj = 'Abwesend'
                    warning = f'CHANGED PROJECT NAME to "{proj}"'
                    print(f"FULL DAY EVENT: {start_date} - {proj} - {subj} / !!! {warning} !!!")
            #print(start_date.strftime("%V"), start_date, proj, subj, start_time_str, end_time_str, diff_hours)

            if len(proj) == 0:
                print(f"MISSING PROJECT NAME: {start_date} - {subj} - {start_time_str} - {end_time_str}")

            writer.writerow([start_date.strftime("%V"), start_date, proj, subj, start_time_str, end_time_str, diff_hours])


def sort_order(row):
    return (
        datetime.strptime(row[1], '%m/%d/%y'),
        datetime.strptime(row[2], '%I:%M:%S %p'),
        datetime.strptime(row[3], '%m/%d/%y'),
        datetime.strptime(row[4], '%I:%M:%S %p'),
        row[0]
    )


class thunderbird(Dialect):
    """Describe the usual properties of Thunderbird-calendar-generated CSV files."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = 1

register_dialect("thunderbird", thunderbird)

if __name__ == "__main__":
    main()
