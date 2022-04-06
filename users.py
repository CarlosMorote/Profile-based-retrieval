from pydoc_data.topics import topics
from topics import Topic
from typing import List

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
