import argparse
from typing import Callable, List
from datasets import TopicDataset, UserDataset
from users import User
from topics import Topic
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')


class ProfileRetrieval:

    __SCORE_FUNC_MAP = dict(
        dot = util.dot_score,
        cos = util.cos_sim,
        euclidean = lambda x, y: torch.tensor([1/(1+torch.nn.functional.pairwise_distance(x, k)) for k in y])
    )

    __similarity_measure = None
    __threshold = None

    def __init__(self, 
                 serial_dir:str, 
                 users_filepath:str, 
                 similarity_measure:str,
                 threshold:float,
                 persist:bool) -> None:
        self.topics = TopicDataset(serial_dir, persist=persist)
        self.users = UserDataset(users_filepath)
        self.similarity_measure = similarity_measure
        self.threshold = threshold

    @property
    def similarity_measure(self) -> Callable:
        return self.__similarity_measure
    
    @similarity_measure.setter
    def similarity_measure(self, similarity_measure:str) -> None:
        self.__similarity_measure = self.__load_similarity_measure(similarity_measure)

    @property
    def threshold(self) -> float:
        return self.__threshold

    @threshold.setter
    def threshold(self, threshold) -> None:
        self.check_threshold_value(threshold)
        self.__threshold = threshold

    def __load_similarity_measure(self, similarity_measure)->bool:
        if similarity_measure and similarity_measure not in self.__SCORE_FUNC_MAP:
            raise ValueError(f'Invalid compare method. Try again with one of {list(self.__SCORE_FUNC_MAP.keys())}.')
        elif similarity_measure:
            return self.__SCORE_FUNC_MAP[similarity_measure]
        else:
            # Explicit None return clause.
            return None

    def check_threshold_value(self, threshold):
        if threshold<0 or threshold>1:
            raise ValueError('Wrong value for the search threshold, "{threshold}. Try to use a value between 0 and 1."')

    def _get_relevance(self, query: str, topic: Topic, score_function:str=None) -> float:
        # Argumento adicional: Tipo de pesado. Estudiar como funciona el metodo deretrieval o rel metodo de la similaridad y codificar la query 'concatenando'
        # Probar. La lista, encodear con Bert y ver lo que devuelve. Puede ser una lista de embedings.

        score_function = self.__load_similarity_measure(score_function) or self.similarity_measure

        query_embedded = model.encode(query, convert_to_tensor=True)

        # keywords = ' '.join(topic.keywords) if cat_k else topic.keywords
        similarity_scores = score_function(query_embedded, topic.keywords)
        
        return torch.max(similarity_scores)

    def _topics_query(self, query: str, threshold:float, print_top=6, verbose=1, **kwargs) -> List[tuple[str, float]]:
        per_topic_score = []

        for topic in self.topics.iterator():
            relevance = self._get_relevance(query, topic, **kwargs)
            per_topic_score.append((topic, relevance))

        topics_sorted = sorted(per_topic_score, key=lambda x: x[1], reverse=True)
        if verbose:
            print(f'Top {min(len(topics_sorted), print_top)} per topic similarity scores: {", ".join(list(map(lambda x: f"({x[0]}:{float(x[1]):.4f})", topics_sorted[:print_top])))}')
        
        top_topics_score = list(filter(lambda x: x[1]>= threshold, topics_sorted))

        if top_topics_score:
            top_topics, _ = zip(*top_topics_score)
            return top_topics
        
        return top_topics_score


    def search(self, query: str, threshold:float=None, **kwargs) -> List[str]:
        if threshold: 
            self.check_threshold_value(threshold)
        else:
            threshold = self.threshold

        topics_inferred = self._topics_query(query, threshold, **kwargs)
        
        print(f'Relevant topics in query: {topics_inferred}')

        return self._get_users_from_topics(topics_inferred)


    def _get_users_from_topics(self, topics_found: List[Topic]) -> List[tuple[User, Topic]]:
        """
        Retrieve the users that has interest in at least one of the topics provide as args
        :param topics_found: List of `Topic` classes
        :type topics_found: List of `Topic`
        :return: Users that has interest in at least one of the topics, with the corresponding topic(s)
        :rtype: List of tuples (User, set of topics)
        """
        resulting_users = []

        if not topics_found:
            return resulting_users

        for user in self.users.get_users():
            # Get the relevant topics which the user is interested
            inter = user.relevant_topics_found(topics_found)

            # If the user has intereset in at least one of them added to the list
            if len(inter):
                resulting_users.append((user, inter))

        return resulting_users


# python profile_based_retrieval.py Serialize Users.jsonl -s cos -thr 0.4
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument("serial_dir",
                help="Directory where to dump/load from disk the serialized topics")
    parser.add_argument("users_filepath", help="Filepath to the file containing the list of users.")
    parser.add_argument("-t", "--topics_filepath",
                help="Filepath to the file containing the list of topics."
                + "Do NOT specify this unless you wish to create a new topics dataset."
                + "If you wish to load existing topics from disk, use the serial_dir argument instead.")
    parser.add_argument("-s", "--similarity_measure", default="cos", choices=["dot", "cos", "euclidean"],
                help="Default similarity score function")
    parser.add_argument("-thr", "--threshold", type=float, default=0.4,
                help="Default threshold to consider a topic as relevant to the query")
    parser.add_argument("-p", "--persist", action="store_true",
                help="Whether to keep loaded topics and their embeddings in main memory.")

    # Parse arguments.
    args = parser.parse_args()
    
    profile_retrieval_search = ProfileRetrieval(args.serial_dir, args.users_filepath, args.similarity_measure, args.threshold, args.persist)


    query = ""

    while query != 'q':
        query = input("Query (type q to quit): ").strip().lower()
        if query == 'q': break
        results = profile_retrieval_search.search(query)
        if results:
            print(f'Query should be delivered to: {", ".join([str(r) for r in results]) if len(results)>1 else results}')
        else:
            print('No users matched for the query.')        
