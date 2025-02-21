# keys: channel_id, name, messages
import json
with open("C02U38XQY.json", 'r') as f:
    j = json.load(f)
msg = j['messages']


user_list = []

for m in msg:
    # dict_keys(['type', 'user', 'text', 'ts', 'bot_id', 'bot_profile', 'team', 'replace_original', 'delete_original', 'metadata', 'blocks'])
    # types: message

    if 'user' in m.keys():
        if m['user'] not in user_list:
            user_list.append(m['user'])
        if m['user'] ==  'U014ASD5456':
            print(f"*** {m['text']}")
    # else:
        # print(f"no user in {m}")

print(f"users:{user_list}")