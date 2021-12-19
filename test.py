from tqdm import  tqdm
from Modules.GoogleApi.google_sheets_api import GoogleSheetsApi
GOOGLE_DOC = '1QZD2roc1Q95weisCUDDx0hm4C3EbyBI9cw-ibnWfDdA'
GOOGLE_LIST = 'translate'
GOOGLE_TOKEN = 'Environment/red_sale_google_token.json'


sheets = GoogleSheetsApi(GOOGLE_TOKEN)
raw_data = sheets.get_data_from_sheets(GOOGLE_DOC, GOOGLE_LIST, 'A2', 'B' +
                                       str(sheets.get_list_size(GOOGLE_DOC, GOOGLE_LIST)[1]), 'ROWS')

print(len(raw_data))
translated = ['']*len(raw_data)
print(len(translated))
count = 0
for i in tqdm(range(len(translated)), total=len(translated)):
    if len(raw_data[i]) > 0:
        translated[i] = raw_data[i][0]
    else:
        if count == 0:
            print(i)
        count += 1
print(count)
print('Done')