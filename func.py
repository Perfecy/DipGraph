import sys
import vk
import setup

import json
import time
import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd


def debug(*args):
    print("DEBUG:", *args)


token = setup.token
session = vk.Session(access_token=token)
api = vk.API(session)

my_id = 109175847


def load_mutual_friends(source_id, target_id):
    # time.sleep(0.3)
    responce = str(api.friends.get(user_id=int(target_id), v='5.95'))
    responce = responce.replace("'", '"')
    return json.loads(responce)['items']


def load_friends_list():
    responce = str(api.friends.get(count=209, user_id=my_id, fields="bdate, city, sex", v='5.95'))
    responce = responce.replace("'", '"')
    responce = responce.replace("False", '"False"')
    responce = responce.replace("True", '"True"')
    debug("received responce length:", len(responce))
    debug("responce:", responce[90:105])
    return json.loads(responce)['items']


def load_degrees(friends_list):
    degrees = []
    for friend in (friends_list):
        time.sleep(0.3)
        try:
            responce = str(api.friends.get(user_id=friend['id'], fields="sex", v='5.95'))
            responce = responce.replace("'", '"')
            array = json.loads(responce)
            degrees.append(len(array))
        except Exception:
            continue
    return degrees


def create_edgelist(friends_list):
    from_vert = []
    to_vert = []
    debug("request mutual friends list:")
    failed_friends = []
    print(friends_list[0])
    friends_list = [friend['id'] for friend in friends_list]
    vtou = {}
    for friend in (friends_list):
        # debug("friend:", friend['id'])
        from_vert.append(my_id)
        to_vert.append(friend)
        # debug("friend:", friend)
        try:
            mutual_friends = load_mutual_friends(my_id, friend)
            for value in mutual_friends:
                if value not in vtou:
                    vtou[value] = set()
            if friend not in vtou:
                vtou[friend] = set()
            for value in mutual_friends:
                vtou[friend].add(value)
                vtou[value].add(friend)
        except Exception as message:
            failed_friends.append(friend)
            continue

    used_ids = set()
    for v, us in vtou.items():
        for u in us:
            if v > u:
                if (v in friends_list and u in friends_list) or (len(vtou[v]) > 7 and len(vtou[u]) > 7):
                    from_vert.append(v)
                    to_vert.append(u)
                    used_ids.add(v)
                    used_ids.add(u)

    print("used_ids size:", len(used_ids))
    return pd.DataFrame({'from': from_vert, 'to': to_vert})


def create_edgelist_without_me(friends_list):
    from_vert = []
    to_vert = []
    debug("request mutual friends list:")
    failed_friends = []
    friends_list = [friend['id'] for friend in friends_list]
    vtou = {}
    for friend in (friends_list):
        # debug("friend:", friend['id'])
        from_vert.append(my_id)
        to_vert.append(friend)
        # debug("friend:", friend)
        try:
            mutual_friends = load_mutual_friends(my_id, friend)
            for value in mutual_friends:
                if value not in vtou:
                    vtou[value] = set()
            if friend not in vtou:
                vtou[friend] = set()
            for value in mutual_friends:
                vtou[friend].add(value)
                vtou[value].add(friend)
        except Exception as message:
            failed_friends.append(friend)
            continue

    used_ids = set()
    for v, us in vtou.items():
        for u in us:
            if v > u:
                if u != my_id and v != my_id:
                    if (v in friends_list and u in friends_list) or (len(vtou[v]) > 7 and len(vtou[u]) > 7):
                        from_vert.append(v)
                        to_vert.append(u)
                        used_ids.add(v)
                        used_ids.add(u)

    print("used_ids size:", len(used_ids))
    return pd.DataFrame({'from': from_vert, 'to': to_vert})


def create_colors(G, friends_list):
    ids = []
    colors = []
    for id in G.nodes():
        ids.append(id)
        color = 'red'
        if id == my_id:
            color = 'green'
        elif id % 2 == 0:
            color = 'blue'
        colors.append(color)

    carac = pd.DataFrame({'ID': ids, 'colors': colors})
    carac = carac.set_index('ID')
    carac = carac.reindex(G.nodes())
    # carac['colors'] = pd.Categorical(carac['colors'])
    return carac['colors']

def graphdraw(G, colors):
    plt.figure(figsize=(60, 40))
    # Plot it
    nx.draw_kamada_kawai(
        G, with_labels=False, node_size=550,
        alpha=0.7, node_color=colors,
        edge_color="gray"
    )
    return ''

