from pydoc_data.topics import topics
from Profiles.topics import topics as t
from typing import List

from random import randint

users = {
    "u0": [t[randint(i,10)] for i in range(randint(1,6))],
    "u1": [t[randint(i,10)] for i in range(randint(1,6))],
    "u2": [t[randint(i,10)] for i in range(randint(1,6))],
    "u3": [t[randint(i,10)] for i in range(randint(1,6))],
    "u4": [t[randint(i,10)] for i in range(randint(1,6))],
    "u5": [t[randint(i,10)] for i in range(randint(1,6))],
    "u6": [t[randint(i,10)] for i in range(randint(1,6))],
    "u7": [t[i] for i in range(11)]
}

def get_users_from_topics(topcis_found: List[str]) -> List[str]:
    resulting_users = []
    for user, l_topics in users.items():
        if all(x in l_topics for x in topcis_found):
            resulting_users.append(user)

    return resulting_users
