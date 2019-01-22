from telegram import utils
from telegram import httptransport


props = utils.SystemProperties()
http_endpoint = httptransport.Endpoint(props.id)


def get_updates(offset: int):
    print('Telegram API: getUpdates is calling')
    data = {}
    if offset is not None:
        data = {'offset': offset}
    http_response = http_endpoint.http_get('getUpdates', data)
    print('Response:\n' + http_response.text)
    # extract updates
    return http_response


def send_message(message):
    http_endpoint.http_post('sendMessage', message)


def send_message(chatid: int, text: str):
    http_endpoint.http_post('sendMessage', {'chat_id': chatid, 'text': text})
