import sys
import os
import csv
from datetime import datetime
import operator
import re

def main():
    print(sys.argv)
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
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        writer = csv.writer(csvfileout, dialect)

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
                #print("SKIP")
                continue

            start_time = datetime.strptime(row[2], '%I:%M:%S %p')
            start_time_str = datetime.strftime(start_time, '%H:%M')
            end_date = datetime.strptime(row[3], '%m/%d/%y').date()
            end_time = datetime.strptime(row[4], '%I:%M:%S %p')
            end_time_str = datetime.strftime(end_time, '%H:%M')

            diff_hours = (end_time - start_time).total_seconds() / 3600

            #print(start_date.strftime("%V"), start_date, proj, subj, start_time_str, end_time_str, diff_hours)
            writer.writerow([start_date.strftime("%V"), start_date, proj, subj, start_time_str, end_time_str, diff_hours])


def sort_order(row):
    return (
        datetime.strptime(row[1], '%m/%d/%y'),
        datetime.strptime(row[2], '%I:%M:%S %p'),
        datetime.strptime(row[3], '%m/%d/%y'),
        datetime.strptime(row[4], '%I:%M:%S %p'),
        row[0]
    )


if __name__ == "__main__":
    main()