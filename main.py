import argparse
from typing import List
from Profiles.users import users, get_users_from_topics
from Profiles.topics import get_all_topics, Topic

from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_relevance(query: str, topic: Topic) -> float:
    # Argumento adicional: Tipo de pesado. Estudiar como funciona el metodo deretrieval o rel metodo de la similaridad y codificar la query 'concatenando'
    # Probar. La lista, encodear con Bert y ver lo que devuelve. Puede ser una lista de embedings.

    query_embedded = model.encode(query)

    cosine_scores = util.cos_sim(query_embedded, topic.keywords)
    
    return torch.max(cosine_scores)

def topics_query(query: str, threshold, top=3) -> List[tuple[str, float]]:
    relevant_topcis = [('No relevant topics found', 0)]
    for topic in get_all_topics(users):
        relevance = get_relevance(query, topic)
        if relevance >= threshold:
            relevant_topcis.append((topic, relevance))

    top_topics, _ = zip(*sorted(relevant_topcis, key=lambda x: x[1], reverse=True)[:top])
    print(top_topics)
    return top_topics

def compatible_profiles(query: str, threshold: float) -> List[str]:
    topics_infered = topics_query(query, threshold)
    return get_users_from_topics(topics_infered)

#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument("query",
#                help="Query that retrieves the intereseted users")
#    parser.add_argument("-t", "--threshold", default=0.1,
#                help="Threshold to consider a topci as relevant or not")

    # Parse arguments.
#    args = parser.parse_args()

#    print(compatible_profiles(args.query, float(args.threshold)))

print(compatible_profiles("The film adaptation of the novel Dune among the most awarded at the gala", 0.1))
