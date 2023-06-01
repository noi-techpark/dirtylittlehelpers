<!--
SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>

SPDX-License-Identifier: CC0-1.0
-->

Go to https://developer.microsoft.com/en-us/graph/graph-explorer
Login
Click "Modify permissions (preview)"
Consent to "Calendars.Read"

Query to use:
https://graph.microsoft.com/v1.0/me/events?$top=500&$select=categories,subject,isAllDay,isCancelled,start,end

Copy/paste the JSON output here as "calendar-output.json"

run 

```
python3 -m costacc calendar-output.json MONTH YEAR > YEAR-MONTH-pm.csv
```

to import into the [backlog google drive spreadsheet](https://docs.google.com/spreadsheets/d/1C4ZPeuZUIj5Uj48nHYlw3Q7ZsTESiYPBdkOCfKcKE7k), do:

```
cat YEAR-MONTH-pm.csv YEAR-MONTH2-pm.csv ...... | ./costacc2backlog.py | p-cc
```

Open LibreOffice Calc and import it

Copy/paste it into the spreadsheet.


Alternatively, just do `./costacc2backlog.py > yourfile`
```
alias p-cc='xclip -selection clipboard'
```