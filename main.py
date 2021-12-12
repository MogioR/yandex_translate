import json

from Modules.yandex_translate_service import YandexTranslateService
from Modules.GoogleApi.google_sheets_api import GoogleSheetsApi

YANDEX_FOLDER_ID = ''
YANDEX_API_KEY = ''
GOOGLE_TOKEN = ''
GOOGLE_DOC = ''
GOOGLE_LIST = 'translate'
LANG = 'en'
PACKET_SIZE = 250


TRANSLATE_LEN_LIMIT = 10000
sheets = GoogleSheetsApi(GOOGLE_TOKEN)
raw_data = sheets.get_data_from_sheets(GOOGLE_DOC, GOOGLE_LIST, 'A2', 'A' +
                                       str(sheets.get_list_size(GOOGLE_DOC, GOOGLE_LIST)[1]), 'COLUMNS')

api = YandexTranslateService(YANDEX_API_KEY, YANDEX_FOLDER_ID)

translated = []
to_translate = []
translate_len = 0
for text in raw_data[0]:
    if translate_len + len(text) < TRANSLATE_LEN_LIMIT:
        translate_len += len(text)
        to_translate.append(text)
    else:
        if len(to_translate) > 0:
            try:
                translated += api.translate_strings(LANG, to_translate)
            except Exception as e:
                print(e)
                break

            to_translate.clear()
            translate_len = 0

            if len(text) < TRANSLATE_LEN_LIMIT:
                to_translate.append(text)
                translate_len += len(text)
            else:
                translated.append('')
                print('To long str:', text)
                continue
        else:
            translated.append('')
            print('To long str:', text)
            continue

if len(to_translate) > 0:
    try:
        translated += api.translate_strings(LANG, to_translate)
    except Exception as e:
        print(e)

translated_pairs = []
for i in range(len(translated)):
    translated_pairs.append([raw_data[0][i], LANG, translated[i]])


with open("backup.json", "w", encoding='utf-8') as write_file:
    json.dump(translated_pairs, write_file, ensure_ascii=False)

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
sheets.put_column_to_sheets_packets(GOOGLE_DOC, GOOGLE_LIST, 'B', 2, translated, PACKET_SIZE)
