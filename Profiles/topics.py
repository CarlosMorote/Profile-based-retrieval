from typing import List
from nltk.corpus import wordnet
import re



class Topic():

    name: str
    keywords: List[str]

    def _keywords_generator(self, word):

        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(re.sub(r"""[-_]""", " ", l.name()))

        return list(set(synonyms))

    def __init__(self, name) -> None:
        self.name = name
        self.keywords = self._keywords_generator(name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def get_str_keywords(self) -> str:
        return " ".join(self.keywords)

def get_all_topics(users: List):
    topics = []
    for user in users:
        topics += user.interested_topics
    return list(set(topics))
