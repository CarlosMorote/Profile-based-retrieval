from typing import List
from nltk.corpus import wordnet
import re

topics = ["t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10"]

# Posible TODO: Guardar las palabras clave ya tokenizadas
topics_keywords = {
    topics[0]: ["k0", "k1"],
    topics[1]: ["k2"],
    topics[2]: ["k0", "k3", "k4"],
    topics[3]: ["k2", "k5"],
    topics[4]: ["k3"],
    topics[5]: ["k6", "k7", "k8"],
    topics[6]: ["k4", "k7"],
    topics[7]: ["k3", "k6", "k9"],
    topics[8]: ["k10", "k13"],
    topics[9]: ["k11"],
    topics[10]: ["k11", "k12", "k14"],
}

class Topic():

    name: str
    keywords: List[str]

    def _keywords_generator(self, word):

        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(re.sub(r"""[-_]""", " ", l.name()))

        return set(synonyms)

    def __init__(self, name) -> None:
        self.name = name
        self.keywords = self._keywords_generator(name)