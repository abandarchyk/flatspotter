class From:
    def __init__(self, id, is_bot, first_name, last_name, username, language_code):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code


class Chat:
    def __init__(self, id, first_name, last_name, username, type):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.type = type


class Message:
    def __init__(self, message_id, from_obj, chat_obj, date, text):
        self.message_id = message_id
        self.From = from_obj
        self.Chat = chat_obj
        self.date = date
        self.text = text


class Update:
    def __init__(self, update_id, message):
        self.update_id = update_id
        self.Message = message








