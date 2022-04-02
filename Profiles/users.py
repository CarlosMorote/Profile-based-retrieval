from pydoc_data.topics import topics
from topics import Topic
from typing import List

from random import randint

def get_users_from_topics(topcis_found: List[str]) -> List[str]:
    resulting_users = []
    for user, l_topics in users.items():
        if all(x in l_topics for x in topcis_found):
            resulting_users.append(user)

    return resulting_users


class User():

    id: int
    interested_topics: List[Topic]

    def _assign_random_topics(self) -> None:
        self.interested_topics = []

    def __init__(self, id: int, interested_topics: List[str] = None) -> None:
        self.id = id
        if interested_topics != None:
            self.interested_topics = [Topic(topic) for topic in interested_topics]
        else:
            self._assign_random_topics()


users = [
    User(1, ["Movies", "Races"]),
    User(2, ["Literature"]),
    User(3, ["Food", "Health"]),
    User(4, ["Medicine", "Science"]),
    User(5, ["Sleep", "Coach", "Series", "Television"])
]

print(users[0])