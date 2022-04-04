from typing import List
from nltk.corpus import wordnet
import re
import json

from torch import Tensor, embedding
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

class Topic():

    name: str
    keywords: List[Tensor]
    keywords_str: List[str]

    def _keywords_generator(self, word):

        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(re.sub(r"""[-_]""", " ", l.name()))

        synonyms = list(set(synonyms))
        embedding = model.encode(synonyms, convert_to_tensor=True)

        return (synonyms, embedding)

    def __init__(self, name) -> None:
        self.name = name
        self.keywords_str, self.keywords = self._keywords_generator(name)
        self._serialize()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def _serialize(self):
        torch.save(self.keywords, f'./Serialize/Keywords/{self.name}-keywords.pt')
        with open(f'./Serialize/Topics/{self.name}.json','w') as f:
            f.write(
                json.dumps(
                    self, 
                    default=lambda o: o.__dict__
                )
            )

    def get_str_keywords(self) -> str:
        return " ".join(self.keywords)


def get_all_topics(users: List):
    topics = []
    for user in users:
        topics += user.interested_topics
    return list(set(topics))



if __name__ == '__main__':
    # Generar serializable con los topics
    pass