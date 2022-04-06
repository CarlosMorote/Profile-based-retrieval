from pydoc_data.topics import topics
from topics import Topic
from typing import List

from random import randint

class User():

    id: int
    interested_topics: List[Topic] = []

    def __init__(self, id: int, interested_topics: List[Topic] = None) -> None:
        self.id = id
        if interested_topics != None:
            self.interested_topics = interested_topics

    def __str__(self) -> str:
        return f"User: {self.id}"

    def __repr__(self) -> str:
        return str(self)

    def has_topic(self, topic: Topic):
        return topic in self.interested_topics

    def has_any_topic(self, topics: Topic):
        return any(self.has_topic(topic) for topic in topics)


    def relevant_topics_found(self, topics: List[Topic]) -> set[Topic]:
        """
        Creates a set with the topics which the user is interested *and* the args argument
        :param topics: List of `Topic` classes
        :type topics: List of `Topic`
        :return: Intersection of sets `self.interested_topics` and `args.topics`
        :rtype: set
        """
        return set(self.interested_topics).intersection(set([t.name for t in topics]))


def get_users_from_topics(topics_found: List[Topic]) -> List[tuple[User, Topic]]:
    """
    Retrieve the users that has interest in at least one of the topics provide as args
    :param topics_found: List of `Topic` classes
    :type topics_found: List of `Topic`
    :return: Users that has interest in at least one of the topics, with the corresponding topic(s)
    :rtype: List of tuples (User, set of topics)
    """
    resulting_users = []
    for user in users:

        # Get the relevant topics which the user is interested
        inter = user.relevant_topics_found(topics_found)

        # If the user has intereset in at least one of them added to the list
        if len(inter):
            resulting_users.append((user, inter))

    return resulting_users

# t_movies = Topic("Movies")
# t_races = Topic("Races")
# t_literature = Topic("Literature")
# t_food = Topic("Food")
# t_health = Topic("Health")
# t_sports = Topic("Sports")
# t_medicine = Topic("Medicine")
# t_science = Topic("Science")
# t_sleep = Topic("Sleep")
# t_couch = Topic("Couch")
# t_series = Topic("Series")
# t_television = Topic("Television")

# users = [
#     User(1, [t_movies, t_races]),
#     User(2, [t_literature]),
#     User(3, [t_food, t_health, t_sports]),
#     User(4, [t_medicine, t_science]),
#     User(5, [t_sleep, t_couch, t_series, t_television])
# ]