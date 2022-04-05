from typing import Union
import json
from topics import Topic
from pathlib import Path
from users import User
import utils

class UserDataset:
    
    def __init__(self, filepath:Union[str, Path]):
        self.filepath = filepath
        with open(self.filepath, 'r') as jsonl:
            self.users = {u['id']: User(u['id'], u['topics']) for u in [json.loads(l) for l in list(jsonl)]}

    def __len__(self):
        return len(self.users.keys())

    @property
    def ids(self):
        return self.users.keys()

    def __setitem__(self, idx, topics):      
        new_user = User(idx, topics)
        self.users[idx] = new_user

        self.__serialize(idx=idx, topics=topics)

    def __getitem__(self,idx):
        return self.users[idx]

    def __serialize(self, idx=None, topics=None):
        if idx not in self.ids:
            with open(self.filepath, 'w') as jsonl:
                jsonl.write('\n')
                jsonl.write(
                    json.dumps(dict(id = idx, topics = topics))
                )
        else:
            with open(self.filepath, 'w') as jsonl:
                for i, user in enumerate(self.users.values()):
                    jsonl.write(
                        json.dumps(dict(id = user.id, topics = user.interested_topics))
                    )
                    if i < len(self)-1: jsonl.write('\n')



class TopicDataset:
    
    def __init__(self, serial_dir:Union[str, Path], persist=False):
        self.serial_dir = serial_dir

        utils.makedir(self.serial_dir)

        self.__persist = persist

        if self.__persist:
            self._load_topics_to_mm()


    def add_topics(self, *topics):
        for topic in topics:
            Topic(name=topic, from_json_filepath=Path(self.serial_dir,topic+'.json'))
        # Reload contents to main memory
        if self.__persist:
            self._load_topics_to_mm()

    @property
    def serial_dir(self):
        return self.__serial_dir

    @serial_dir.setter
    def serial_dir(self, serial_dir:Union[str, Path]=None):
        if serial_dir: self.__serial_dir = Path(serial_dir)


    def _load_topics_to_mm(self):
        self.__topics = {str(topic.name).replace('.json', ''):Topic(from_json_filepath=topic) 
                            for topic in self.serial_dir.glob('**/*.json')}

    def __len__(self):
        return len(list(self.serial_dir.glob('**/*.json')))

    def __getitem__(self,name):
        return self.__topics[name] if self.__persist else \
            Topic(from_json_filepath=Path(self.serial_dir,name+'.json'))


if __name__ == '__main__':
    # Arg a el doc de topics
    with open('topics.txt', 'r') as jsonl:
        topic_list = jsonl.readline().strip().split(';')
    # Generate dataset
    td = TopicDataset('SerialTest')
    td.add_topics(*topic_list)

    # # Load dataset
    # td = TopicDataset('SerialTest')
    # movies = td['Movies']

    # # Load dataset and keep it in mem.
    # td2 = TopicDataset('SerialTest', persist=True)
    # movies2 = td2['Movies']
    # print('hi')

    # ud = UserDataset('Users.jsonl')
    # # Add user
    # ud[51] = ["a", "b", "c"]
    # ud[3] = ["a", "b", "c"]
    # ud[54] = ["x", "y", "z"]
    # # Length
    # print(len(ud))
    # # Get item
    # a = ud[51]

    # print('a')