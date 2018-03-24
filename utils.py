import pickle
import json

from config import left_members_db


def get_new_chat_member(message_json):
    try:
        new_chat_member = message_json['message']['new_chat_member']
        print('new_chat_member: {}'.format(new_chat_member))
        return new_chat_member
    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return None


def get_left_chat_member(message_json):
    try:
        left_chat_member = message_json['message']['left_chat_member']
        print('left_chat_member: {}'.format(left_chat_member))
        return left_chat_member
    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return None


def get_message(message_json):
    try:
        return message_json['message']['text']
    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return None


def get_chat_id(message_json):
    try:
        return str(message_json['message']['chat']['id'])
    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return None


def get_photo(message_json):
    try:
        return str(message_json['message']['photo'])
    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return None


def load_left_members():
    print('load_left_members')
    try:
        with open(left_members_db, 'rb') as pickle_file:
            left_members = pickle.load(pickle_file)
            if left_members:
                return left_members
            else:
                return dict()
    except Exception:
        print('load_left_members.LOADING ERROR !!!')
        # TODO create Exception object (◕‿‿◕｡)
        return dict()


def save_left_members(left_members):
    print('save_left_members:\n{}'.format(left_members))

    try:
        with open(left_members_db, 'wb') as pickle_file:
            pickle.dump(left_members, pickle_file)
        return True

    except (OSError, IOError):
        print('save_left_members.SAVING ERROR !!!')
        # TODO create Exception object (◕‿‿◕｡)
        return False


def is_new_user(uid):
    try:
        left_members = load_left_members()

        left_member = left_members[uid]

        if left_member:
            return False
        else:
            return True

    except Exception:
        # TODO create Exception object (◕‿‿◕｡)
        return True


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
