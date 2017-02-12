from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import sys

SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/presentations',
)
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
HTTP = creds.authorize(Http())
SHEETS = discovery.build('sheets', 'v4', http=HTTP)
SLIDES = discovery.build('slides', 'v1', http=HTTP)

print('** Fetch Sheets data')
sheetID = '10FsJHEfMaxOuZZTI1DU2Q17gr57yRSUQxJ88C7ZXMSY'   # use your own!

doc = SHEETS.spreadsheets().get(spreadsheetId=sheetID).execute()
print(doc)

for data in doc["sheets"]:
    print(data)

sheets = doc.get('sheets', '')
for sheet in sheets:
    title = sheet["properties"]["title"]
    if not title.startswith("_"):
        orders = SHEETS.spreadsheets().values().get(range=title, spreadsheetId=sheetID).execute().get('values')
        print(orders)
