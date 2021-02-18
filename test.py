from flask import Flask
import matplotlib
from func import *
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import vk
import py2neo
from py2neo import Node

# print(friends_list)
# print(edgelist)
# G = nx.from_pandas_edgelist(edgelist, 'from', 'to')
# print("G len:", len(G))
# colors = create_colors(G, friends_list)
# print(colors[:10])
# plt.figure(figsize=(60, 40))
# # Plot it
# nx.draw_kamada_kawai(
#     G, with_labels=False, node_size=550,
#     alpha=0.7, node_color=colors,
#     edge_color="blue"
# )
# plt.savefig("fig.png")

friends_list = load_friends_list()
edge_list = create_edgelist(friends_list)
from_list = edge_list["from"].to_list()
to_list = edge_list["to"].to_list()
# print(friends_list)
# print(edge_list)
graph = py2neo.Graph(password="1")


def loadToNeo(friend_list):
    # print(len(friend_list))

    # print(edge_list)
    # for i in range(len(friend_list)):  # тут было принято решение что не надо отправлять по запросу на каждого друга
    #     # а можно сделать за одну функцию, сделав  подграф из 253х нод  и всего один запрос
    #     # str_node = request["items"][i]["first_name"] + " " + request["items"][i]["last_name"]
    #
    #     # print(str_node)
    #     if i == 0:
    #         nodes = py2neo.Node("Person", name=first_name, surname=last_name)
    #     else:
    #         node = py2neo.Node("Person", name=first_name, surname=last_name)
    #         nodes = nodes | node
    # graph.create(nodes)
    print(friends_list[0]["first_name"])
    k = 0
    nodes= Node("Person", name='Kirill', surname='Lukunin', vk_id=109175847)
    for person in friends_list:
        node = Node("Person", name=person["first_name"], surname=person["last_name"], vk_id=person["id"])
        nodes = nodes | node

    graph.create(nodes)

    return 0


def createFriends(from_list, to_list):
    for i in range(len(edge_list)):
        query = "MATCH (a:Person), (b:Person) WHERE a.vk_id = {fr} AND b.vk_id = {to}" \
                " CREATE (a)-[r:FRIENDSHIP]->(b) RETURN type(r)"
        new_query=query.format(fr=str(from_list[i]),to=str(to_list[i]))
        print(new_query)
        graph.run(new_query)
    return 0


#loadToNeo(friends_list)

# for i in range(len(edge_list)):
#     print(str(from_list[i])+"-   -"+str(to_list[i]))
#createFriends(from_list, to_list)
