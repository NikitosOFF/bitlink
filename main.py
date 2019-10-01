import os
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()


def shorten_link(token_bitly, input_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": "Bearer " + token_bitly}
    payload = {"long_url": input_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(token_bitly, input_url):
    clicks_url_template = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"
    url = clicks_url_template.format(input_url)
    headers = {"Authorization": "Bearer " + token_bitly}
    parametres = {'unit': 'day', 'units': '-1'}
    response = requests.get(url, headers=headers, params=parametres)
    response.raise_for_status()
    return response.json()['total_clicks']


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Ссылка')
    return parser

if __name__ == "__main__":
    token_bitly = os.getenv('TOKEN_BITLY')
    parser = create_parser()
    args = parser.parse_args()
    input_url = args.link
    if input_url.startswith('bit'):
        try:
            count_clicks(token_bitly, input_url)
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку')
        else:
            print('number of clicks :', count_clicks(token_bitly, input_url))
    else:
        try:
            shorten_link(token_bitly, input_url)
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку')
        else:
            print('Bitlink :', shorten_link(token_bitly, input_url))
