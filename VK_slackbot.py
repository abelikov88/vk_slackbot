import time

import vk_api
from slacker import Slacker

slack = Slacker(TOKEN)
kingdom_group_id = GROUPID
alexGT_id = ALEXGTID
topic_id = TOPICID


def get_last_comment_id():
    with open('comment_id.txt', 'r') as comment_id:
        return comment_id.read()


def find_user_name(id, profiles):
    for profile in profiles:
        if id == profile['id']:
            return profile['first_name'] + ' ' + profile['last_name']
    return ''


def main():
    login, password = VKLOGIN, VKPASSWORD
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    while True:
        try:
            comments = vk.board.getComments(group_id=kingdom_group_id, topic_id=topic_id,
                                            start_comment_id=get_last_comment_id(),
                                            extended=1)
        except Exception as e:
            print(e)
            time.sleep(300)
            continue

        items = comments['items'][1:]
        profiles = comments['profiles']

        if len(items) > 0:
            last_comment_id = items[len(items) - 1]['id']
            with open('comment_id.txt', 'w') as comment_id:
                comment_id.write(str(last_comment_id))

        items = [i for i in items if i['from_id'] != -kingdom_group_id and i['from_id'] != alexGT_id]

        for item in items:
            user_name = find_user_name(item['from_id'], profiles)
            message = user_name + ': ' + item['text']
            slack.chat.post_message(SLACKCHANEL, '@abelikov Новое сообщение от ' + message,
                                    link_names='@abelikov', as_user=True)

        time.sleep(300)


if __name__ == '__main__':
    main()
