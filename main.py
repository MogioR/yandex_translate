import json

from tqdm import  tqdm

from Modules.yandex_translate_service import YandexTranslateService
from Modules.GoogleApi.google_sheets_api import GoogleSheetsApi

YANDEX_FOLDER_ID = ''
YANDEX_API_KEY = ""
GOOGLE_TOKEN = 'Environment/red_sale_google_token.json'
GOOGLE_DOC = ''
GOOGLE_LIST = 'translate'
LANG = 'en'
TRANSLATE_LEN_LIMIT = 10000
PACKET_SIZE = 250

LOAD_FROM_BACKUP = False

if not LOAD_FROM_BACKUP:
    sheets = GoogleSheetsApi(GOOGLE_TOKEN)
    raw_data = sheets.get_data_from_sheets(GOOGLE_DOC, GOOGLE_LIST, 'A2', 'B' +
                                           str(sheets.get_list_size(GOOGLE_DOC, GOOGLE_LIST)[1]), 'ROWS')

    api = YandexTranslateService(YANDEX_API_KEY, YANDEX_FOLDER_ID)

    translated = ['']*len(raw_data)
    to_translate = []
    to_translate_indexes = []
    translate_len = 0
    for i, data in tqdm(enumerate(raw_data), total=len(raw_data)):
        try:
            if len(data) == 1:
                if translate_len + len(data[0]) < TRANSLATE_LEN_LIMIT:
                    translate_len += len(data[0])
                    to_translate.append(data[0])
                    to_translate_indexes.append(i)
                else:
                    if len(to_translate) > 0:
                        try:
                            buf = api.translate_strings(LANG, to_translate)
                            for j, index in enumerate(to_translate_indexes):
                                translated[index] = buf[j]
                        except Exception as e:
                            print(e)
                            break

                        to_translate.clear()
                        to_translate_indexes.clear()
                        translate_len = 0

                        if len(data[0]) < TRANSLATE_LEN_LIMIT:
                            to_translate.append(data[0])
                            translate_len += len(data[0])
                            to_translate_indexes.append(i)
                        else:
                            print('To long str:', data[0])
                            continue
            else:
                print('This string already translated:', data[0], 'translate:', data[1])
                translated[i] = data[1]
                continue
        except Exception as e:
            with open("bad_backup.json", "w", encoding='utf-8') as write_file:
                json.dump(translated, write_file, ensure_ascii=False, indent=4)
            print('Что-то пошло не так, переводы сохранены в bad_backup')
            print('Error:', str(e))

    if len(to_translate) > 0:
        try:
            buf = api.translate_strings(LANG, to_translate)
            for j, index in enumerate(to_translate_indexes):
                translated[index] = buf[j]
        except Exception as e:
            print(e)

    translated_pairs = []
    counter = 0
    try:
        for i in range(len(translated)):
            if len(raw_data[i]) > 0:
                translated_pairs.append([raw_data[i][0], LANG, translated[i]])
            else:
                counter += 1
        print('Пустых строк: ', counter)

        with open("backup.json", "w", encoding='utf-8') as write_file:
            json.dump(translated_pairs, write_file, ensure_ascii=False, indent=4)
    except Exception as e:
        with open("bad_backup.json", "w", encoding='utf-8') as write_file:
            json.dump(translated, write_file, ensure_ascii=False, indent=4)
        print('Что-то пошло не так, переводы сохранены в bad_backup')
        print('Error:', str(e))

else:
    with open("backup.json", "r", encoding='utf-8') as read_file:
        raw_data = json.load(read_file)

    translated = []
    for data in raw_data:
        translated.append(data[2])

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
sheets.put_column_to_sheets_packets(GOOGLE_DOC, GOOGLE_LIST, 'B', 2, translated, PACKET_SIZE)
