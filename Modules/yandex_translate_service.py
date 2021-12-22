import requests
import time

SERVICE_URL = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
TRANSLATE_LEN_LIMIT = 10000
TRANSLATE_COUNT_LIMIT = 20
SLEEP_TIME = 1.1


class YandexTranslateService:
    def __init__(self, api_key: str, folder: str):
        self.api_key = api_key
        self.folder = folder
        self.api_requests = 0

    def translate_strings(self, target_language: str, data: list, source_language=None) -> list:
        if self.api_requests == TRANSLATE_COUNT_LIMIT:
            time.sleep(SLEEP_TIME)
            self.api_requests = 0
        self.api_requests += 1

        translate_len = 0
        for text in data:
            translate_len += len(text)

        if translate_len > TRANSLATE_LEN_LIMIT:
            raise Exception('To many characters to translate. Max count of characters is ' + str(TRANSLATE_LEN_LIMIT))

        headers = {
            "Content-Type": "application/json",
            "Authorization": 'Api-Key ' + self.api_key
        }

        body = {
            "targetLanguageCode": target_language,
            "format": "PLAIN_TEXT",
            "texts": data
        }

        if source_language is not None:
            body['sourceLanguageCode'] = source_language

        try:
            response = requests.post(url=SERVICE_URL, json=body, headers=headers)
        except Exception as e:
            raise e

        if response.status_code != 200:
            raise Exception('Error reason: ' + response.reason)

        result = []
        for translation in response.json()['translations']:
            result.append(translation['text'])

        return result
