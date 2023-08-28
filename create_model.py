import json
from config import *
import markovify


def cleaned_up_model():
    raw_messages = json.load(open('result.json', 'r', encoding='utf-8'))
    cleaned_up_messages = []

    for message in raw_messages['messages']:
        cur_message_str = ""
        for message_text in (message.get('text') or []):
            if 'from_id' in message and message['from_id'] == f'user{str(USER_ID)}' and "forward_date" not in message:
                if isinstance(message_text, str):
                    cur_message_str += message_text
                if isinstance(message_text, dict):
                    cur_message_str += message_text['text']
            
            cur_message_str.replace('\n', '')
        cleaned_up_messages.append(cur_message_str)

    return markovify.NewlineText('\n'.join(cleaned_up_messages), state_size=1)


def dirty_model():
    raw_messages = json.load(open('result.json', 'r', encoding='utf-8'))
    messages = ''
    # print('user502639073' in raw_messages['messages'])
    for msg in raw_messages['messages'] :
        if msg.get('from_id') == f'user{str(USER_ID)}' and "forward_date" not in msg:
            plain_text = msg['text']
            messages += f'{plain_text}\n'

    return markovify.NewlineText(messages, state_size=1)


def main():
    model = markovify.combine([dirty_model(),cleaned_up_model()], [1,1.5])

    compiled_model = model.compile()
    file = open('model.json', 'w')
    file.write(compiled_model.to_json())
    # model = markovify.NewlineText.from_json(open('marko59.json', 'r', encoding='utf-8').read())

    for i in range(10):
        print(compiled_model.make_sentence())


if __name__ == '__main__':
    main()