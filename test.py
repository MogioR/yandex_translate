from tqdm import  tqdm
from Modules.GoogleApi.google_sheets_api import GoogleSheetsApi
GOOGLE_DOC = '1QZD2roc1Q95weisCUDDx0hm4C3EbyBI9cw-ibnWfDdA'
GOOGLE_LIST = 'translate'
GOOGLE_TOKEN = 'Environment/red_sale_google_token.json'
PACKET_SIZE = 100000

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
raw_data = sheets.get_data_from_sheets(GOOGLE_DOC, GOOGLE_LIST, 'A2', 'B' +
                                       str(sheets.get_list_size(GOOGLE_DOC, GOOGLE_LIST)[1]), 'ROWS')

raw_data_new = sheets.get_data_from_sheets_packet(GOOGLE_DOC, GOOGLE_LIST, 'A', 2, 'B',
                                    sheets.get_list_size(GOOGLE_DOC, GOOGLE_LIST)[1], 'ROWS', PACKET_SIZE)

print(len(raw_data))
print(len(raw_data_new))

print('Done')