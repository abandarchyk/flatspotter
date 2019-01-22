import sys
import telegram.model


class SystemProperties:
    def __init__(self):
        for param in sys.argv:
            if 'id=' in param:
                bid = param[len('id='): len(param)]
                self.id = bid


def decode_updates(get_updates_rs: dict):
    updates_list = []
    results = get_updates_rs['result']
    for result in results:
        # From
        from_dict = result['message']['from']
        from_obj = telegram.model.From(from_dict['id'], from_dict['is_bot'], from_dict['first_name'],
                                       from_dict['last_name'], from_dict['username'], from_dict['language_code'])
        # Chat
        chat_dict = result['message']['chat']
        chat_obj = telegram.model.Chat(chat_dict['id'], chat_dict['first_name'], chat_dict['last_name'],
                                       chat_dict['username'], chat_dict['type'])
        # Message
        message_id = result['message']['message_id']
        message_date = result['message']['date']
        message_text = result['message']['text']
        update_id = result['update_id']

        message = telegram.model.Message(message_id, from_obj, chat_obj, message_date, message_text)
        update = telegram.model.Update(update_id, message)
        updates_list.append(update)
    return updates_list




