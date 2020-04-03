import sys
import os
import csv
from datetime import datetime
import operator

def main():
    print(sys.argv)
    if len(sys.argv) != 4:
        print("USAGE: %s input monthnumber year" % os.path.basename(sys.argv[0]))
        print("       input        filename of a temporal data file (TSV)")
        print("       monthnumber  the number of the month (ex., May => 5)")
        print("       year         the last two digits of the year (ex., 2020 => 20)")
        print()
        sys.exit(1)

    csvFilename = sys.argv[1]
    month = sys.argv[2]
    year = sys.argv[3]

    with open(csvFilename, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        if csv.Sniffer().has_header(csvfile.read(1024)):
            csvfile.seek(0)
            next(reader)

        sortedlist = sorted(reader, key=sort_order, reverse=False)

        for row in sortedlist:
            subj = row[0]
            start_date = datetime.strptime(row[1], '%m/%d/%y').date()
            start_time = datetime.strftime(datetime.strptime(row[2], '%I:%M:%S %p'), '%H:%M')
            end_date = datetime.strptime(row[3], '%m/%d/%y').date()
            end_time = datetime.strftime(datetime.strptime(row[4], '%I:%M:%S %p'), '%H:%M')

            print(start_date, " --- ", subj, start_time, end_time)


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