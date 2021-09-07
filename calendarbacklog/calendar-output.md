Go to https://developer.microsoft.com/en-us/graph/graph-explorer
Login
Click "Modify permissions (preview)"
Consent to "Calendars.Read"

Query to use:
https://graph.microsoft.com/v1.0/me/events?$top=500&$select=categories,subject,isAllDay,isCancelled,start,end

Copy/paste the JSON output here as "calendar-output.json"