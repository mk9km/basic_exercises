"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime
from typing import Dict, Tuple
import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids,
                                     random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


def get_user_ids_with_max_messages(messages: Dict) -> Tuple:
    message_num_to_user = {}
    max_user_ids, max_message_num = {}, 0

    for message in messages:
        user_id = message['sent_by']
        message_num_to_user[user_id] = message_num_to_user.get(user_id, 0) + 1

        if max_message_num < message_num_to_user[user_id]:
            max_user_ids, max_message_num = {user_id}, message_num_to_user[user_id]
        elif max_message_num == message_num_to_user[user_id]:
            max_user_ids.add(user_id)

    return max_user_ids, max_message_num


def get_user_ids_with_max_replies(messages: Dict) -> Tuple:
    message_id_to_user_id = {}
    user_id_to_reply_num = {}
    max_user_ids, max_reply_num = {}, 0
    for message in messages:
        message_id = message['id']
        user_id = message['sent_by']
        message_id_to_user_id[message_id] = user_id

        reply_for_id = message['reply_for']
        if reply_for_id is None:
            continue

        reply_for_user_id = message_id_to_user_id[reply_for_id]
        user_id_to_reply_num[reply_for_user_id] = user_id_to_reply_num.get(reply_for_user_id, 0) + 1

        if max_reply_num < user_id_to_reply_num[reply_for_user_id]:
            max_user_ids, max_reply_num = {reply_for_user_id}, user_id_to_reply_num[reply_for_user_id]
        elif max_reply_num == user_id_to_reply_num[reply_for_user_id]:
            max_user_ids.add(user_id)

    return max_user_ids, max_reply_num


def get_user_ids_with_max_views(messages: Dict) -> Tuple:
    user_id_to_views = {}
    max_user_ids, max_view_num = {}, 0

    for message in messages:
        user_id = message['sent_by']
        views = message['seen_by']
        user_id_to_views.setdefault(user_id, set()).update(views)
        view_num = len(user_id_to_views[user_id])

        if max_view_num < view_num:
            max_user_ids, max_view_num = {user_id}, view_num
        elif max_view_num == view_num:
            max_user_ids.add(user_id)

    return max_user_ids, max_view_num


def get_message_num_for_time_day(messages: Dict) -> Tuple:
    evening  = datetime.time(18, 0)
    noon = datetime.time(12, 0)
    morning = datetime.time(6, 0)
    midnight = datetime.time(0, 0)

    message_num_to_daytime = {
        'morning': 0,
        'day': 0,
        'evening': 0,
        'night': 0,
    }

    for message in messages:
        message_time = message['sent_at'].time()
        if message_time >= evening:
            message_num_to_daytime['evening'] += 1
        elif message_time >= noon:
            message_num_to_daytime['day'] += 1
        elif message_time >= morning:
            message_num_to_daytime['morning'] += 1
        elif message_time >= midnight:
            message_num_to_daytime['night'] += 1

    max_time_days, max_message_num = {}, 0
    for time_day, message_num in message_num_to_daytime.items():
        if max_message_num < message_num:
            max_time_days, max_message_num = {time_day}, message_num
        elif max_message_num == message_num:
            max_time_days.add(time_day)

    return max_time_days, message_num_to_daytime


def get_message_ids_with_max_replies(messages):
    message_id_to_thread_level = {}
    max_message_ids, max_thread_level = set(), 0

    for message in messages:
        message_id = message['id']
        reply_for_id = message['reply_for']

        if reply_for_id is None:
            root_id = message_id
            message_id_to_thread_level[message_id] = (0, root_id)
        else:
            prev_message_level, root_id = message_id_to_thread_level[reply_for_id]
            message_id_to_thread_level[message_id] = (prev_message_level + 1, root_id)

        if max_thread_level < message_id_to_thread_level[message_id][0]:
            max_message_ids, max_thread_level = {root_id}, message_id_to_thread_level[message_id][0]
        elif max_thread_level == message_id_to_thread_level[message_id][0]:
            max_message_ids.add(root_id)

    return max_message_ids, max_thread_level

OUTPUT_FORMAT = '{0}: {1} |||||||||||||| DEBUG: {2}'

if __name__ == "__main__":
    chat_history = generate_chat_history()  # Assumes that messages are already sorted by timestamp, but...
    # chat_history = sorted(chat_history, key=lambda x: x['sent_at'])  # ...we can sort them again if needed.
    #print(chat_history)

    rv = get_user_ids_with_max_messages(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max messages', *rv))

    rv = get_user_ids_with_max_replies(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max replies', *rv))

    rv = get_user_ids_with_max_views(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max views', *rv))

    rv = get_message_num_for_time_day(chat_history)
    print(OUTPUT_FORMAT.format('Max message number in(at)', *rv))

    rv = get_message_ids_with_max_replies(chat_history)
    print(OUTPUT_FORMAT.format('Message ids with max replies', *rv))
