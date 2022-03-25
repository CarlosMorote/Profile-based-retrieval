from random import random, randint
from typing import List
from Profiles.users import users, get_users_from_topics
from Profiles.topics import topics_keywords

def corr():
    return random()

def get_relevance(query: str, keywords: List[str]) -> float:
    return random()

def topics_query(query: str, threshold = 0.5, top=3) -> List[tuple[str, float]]:
    relevant_topcis = []
    for topic, keywords in topics_keywords.items():
        relevance = get_relevance(query, keywords)
        if relevance >= threshold:
            relevant_topcis.append((topic, relevance))
            
    top_topics, _ = zip(*sorted(relevant_topcis, key=lambda x: x[1], reverse=True)[:top])
    return top_topics

def compatible_profiles(query: str) -> List[str]:
    topics_infered = topics_query(query)
    return get_users_from_topics(topics_infered)

new_doc = "Dua Lipa beats records"

print(compatible_profiles(new_doc))
