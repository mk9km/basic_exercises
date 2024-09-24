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
    msg_num_to_usr = {}
    max_usr_ids, max_msg_num = None, 0

    for msg in messages:
        usr_id = msg['sent_by']
        msg_num_to_usr[usr_id] = msg_num_to_usr.get(usr_id, 0) + 1

        if max_msg_num < msg_num_to_usr[usr_id]:
            max_usr_ids, max_msg_num = {usr_id}, msg_num_to_usr[usr_id]
        elif max_msg_num == msg_num_to_usr[usr_id]:
            max_usr_ids.add(usr_id)

    return max_usr_ids, max_msg_num


def get_user_ids_with_max_replies(messages: Dict) -> Tuple:
    msg_id_to_usr_id = {}
    usr_id_to_rpl_num = {}
    max_usr_ids, max_rpl_num = None, 0
    for msg in messages:
        msg_id = msg['id']
        usr_id = msg['sent_by']
        msg_id_to_usr_id[msg_id] = usr_id

        rpl_for_id = msg['reply_for']
        if rpl_for_id is None:
            continue

        rpl_for_usr_id = msg_id_to_usr_id[rpl_for_id]
        usr_id_to_rpl_num[rpl_for_usr_id] = usr_id_to_rpl_num.get(rpl_for_usr_id, 0) + 1

        if max_rpl_num < usr_id_to_rpl_num[rpl_for_usr_id]:
            max_usr_ids, max_rpl_num = {rpl_for_usr_id}, usr_id_to_rpl_num[rpl_for_usr_id]
        elif max_rpl_num == usr_id_to_rpl_num[rpl_for_usr_id]:
            max_usr_ids.add(usr_id)

    return max_usr_ids, max_rpl_num


def get_user_ids_with_max_views(messages: Dict) -> Tuple:
    usr_id_to_views = {}
    max_usr_ids, max_view_num = None, 0

    for msg in messages:
        usr_id = msg['sent_by']
        views = msg['seen_by']
        usr_id_to_views.setdefault(usr_id, set()).update(views)
        view_num = len(usr_id_to_views[usr_id])

        if max_view_num < view_num:
            max_usr_ids, max_view_num = {usr_id}, view_num
        elif max_view_num == view_num:
            max_usr_ids.add(usr_id)

    return max_usr_ids, max_view_num


def get_msg_num_for_time_day(messages: Dict) -> Tuple:
    evening  = datetime.time(18, 0)
    noon = datetime.time(12, 0)
    morning = datetime.time(6, 0)
    midnight = datetime.time(0, 0)

    msg_num_to_daytime = {
        'morning': 0,
        'day': 0,
        'evening': 0,
        'night': 0,
    }

    for msg in messages:
        msg_time = msg['sent_at'].time()
        if msg_time >= evening:
            msg_num_to_daytime['evening'] += 1
        elif msg_time >= noon:
            msg_num_to_daytime['day'] += 1
        elif msg_time >= morning:
            msg_num_to_daytime['morning'] += 1
        elif msg_time >= midnight:
            msg_num_to_daytime['night'] += 1

    max_time_days, max_msg_num = None, 0
    for time_day, msg_num in msg_num_to_daytime.items():
        if max_msg_num < msg_num:
            max_time_days, max_msg_num = {time_day}, msg_num
        elif max_msg_num == msg_num:
            max_time_days.add(time_day)

    return max_time_days, msg_num_to_daytime


def get_msg_ids_with_max_replies(messages):
    msg_id_to_rpl_num = {}
    max_msg_ids, max_rpl_num = None, 0

    for msg in messages:
        msg_id = msg['reply_for']
        if msg_id is None:
            continue
        msg_id_to_rpl_num[msg_id] = msg_id_to_rpl_num.get(msg_id, 0) + 1

        if max_rpl_num < msg_id_to_rpl_num[msg_id]:
            max_msg_ids, max_rpl_num = {msg_id}, msg_id_to_rpl_num[msg_id]
        elif max_rpl_num == msg_id_to_rpl_num[msg_id]:
            max_msg_ids.add(msg_id)

    return max_msg_ids, max_rpl_num

OUTPUT_FORMAT = '{0}: {1} |||||||||||||| DEBUG: {2}'

if __name__ == "__main__":
    chat_history = generate_chat_history()
    print(chat_history)

    rv = get_user_ids_with_max_messages(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max messages', *rv))

    rv = get_user_ids_with_max_replies(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max replies', *rv))

    rv = get_user_ids_with_max_views(chat_history)
    print(OUTPUT_FORMAT.format('User ids with max views', *rv))

    rv = get_msg_num_for_time_day(chat_history)
    print(OUTPUT_FORMAT.format('Max message number in(at)', *rv))

    rv = get_msg_ids_with_max_replies(chat_history)
    print(OUTPUT_FORMAT.format('Message ids with max replies', *rv))
