from pathlib import Path
from typing import List
from nltk.corpus import wordnet
import re
import json

from torch import Tensor
from sentence_transformers import SentenceTransformer
import torch
import utils

model = SentenceTransformer('all-MiniLM-L6-v2')

class Topic:

    name: str
    keywords: List[Tensor]
    keywords_str: List[str]

    def _generate_keywords(self, word):
        word = word.lower()
        synonyms = []

        for syn in wordnet.synsets(word):
            for l in syn.lemmas():
                synonyms.append(re.sub(r"""[-_]""", " ", l.name()))

        synonyms = list(set(synonyms)|set([word]))
        embedding = model.encode(synonyms, convert_to_tensor=True)

        return synonyms, embedding

    def __init__(self, name=None, from_json_filepath=None) -> None:
        # Create a new topic
        if name:
            self.name = name
            self.keywords_str, self.keywords = self._generate_keywords(name)
            # If both `name` and `from_json_filepath` is provided, we infer
            # the new topic will be serialized to `from_json_filepath`.
            if from_json_filepath:
                self.__json_filepath = from_json_filepath
                self._serialize()

        # Otherwise, load it from disk.
        else:
            self.__json_filepath = from_json_filepath
            self._parse_from_json()


    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def _serialize(self):
        utils.makedir(self.__embeddings_dir)
        torch.save(self.keywords, self.__embeddings_filepath)
        with open(self.__json_filepath,'w') as f:
            f.write(
                json.dumps(
                    dict(
                        name = self.name,
                        keywords_str = self.keywords_str 
                    )
                )
            )

    def _parse_from_json(self):
        with open(self.__json_filepath) as f:
            data = json.load(f)
            self.name = data['name']
            self.keywords_str = data['keywords_str']
            self.keywords = torch.load(self.__embeddings_filepath)

    def get_str_keywords(self) -> str:
        return " ".join(self.keywords)


    @property
    def __embeddings_dir(self):
        return Path(self.__json_filepath.parent, 'embeddings')

    @property
    def __embeddings_filepath(self):
        return Path(self.__embeddings_dir, self.name+'-keywords.pt')

def get_all_topics(users: List):
    topics = []
    for user in users:
        topics += user.interested_topics
    return list(set(topics))