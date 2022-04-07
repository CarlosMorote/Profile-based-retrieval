# Profile-based-retrieval

### Lorenzo Alfaro, David

### Morote García, Carlos

#### ETSIINF, UPM

---

</br>

## Motivation

We utilize Sentence-BERT to derive semantically meaningful sequence representations to measure semantic textual similarity between sentences and short texts by means of cosine-similarity. Based on the learned sentences embeddings, we propose an efficient semantic information retrieval system, providing search latencies suitable for real-time applications.

---

</br>

## Run the code

In this section it is exposed how to run the code. As long as we perform the queries over pre-generated serialized embeddings and classes there are several methods to run in this project. Moreover, we provide a script that allows to validate the engine with a external dataset.

Nevertheless, all the executable scripts (`profile_based_retrieval.py`, `datasets.py` and `validation`) can take the argument `-h` or `--help` in order to provide to the user with some information about the parameters and the functionalities of that script.

</br>

### 1. Perform a query search

The main script corresponds to `profile_based_retrieval.py`. This script initializes the engine with the provided parameters and waits to a user's query in order to retrieve the users that may be interested in that query. The script takes as parameters:
 - **serial_dir**: Directory where to dump/load from disk the serialized topics
 - **users_filepath**: Filepath to the file containing the list of users
 - **-t --topics_filepath**: Filepath to the file containing the list of topics. Do NOT specify this unless you wish to create a new topics dataset. If you wish to load existing topics from disk, use the serial_dir argument instead.
 - **-s --similarity_measure**: Default similarity score function. _Values_: "dot", "cos", "euclidean". _Default_: "cos"
 - **-thr --threshold**: Default threshold to consider a topic as relevant to the query. _Default_: 0.4
 - **-p --persist**: Whether to keep loaded topics and their embeddings in main memory

A example to run the code might be: 

    python profile_based_retrieval.py Serialize Users.jsonl -s cos -thr 0.4

</br>

### 2. Generate the serialize objects

If we want to speed up the process we can serialize the objects and embedding. Thanks to that we do not require to compute the embedding every time we load the engine. To do that we execute the script `datasets.py`. The script takes as parameters:
 - **topics_file**: Name of the file that contains the list of topics
 - **folder_name**: Name of the folder that contains the serialized files

A example to run the code might be:

    python datasets.py topics.txt Serialize


</br>

### 3. Perform a validation with a dataset

In order to validate and test the performance of our engine we have created a script capable of performing this operation. **NOTWITHSTANDING**, this script only works with datasets intended and conceived for classification, so these validations are not representative of the true power of our model.

The structure of the dataset injected to the script must have named columns [`text`, `target`], where `text` must be the new query to predict and `target` the topic related to it.

This script autogenerates the serialization of the topics and its corresponding emeddings. Also detect the topcis within the dataset and generates or modifies the topics file.

The script takes as parameters:
 - **file_name**: File name of the dataset to validate
 - **topics_file**: Name of the file that contains the list of topics
 - **serial_dir**: Directory where to dump/load from disk the serialized topics
 - **users_filepath**: Filepath to the file containing the list of users
 - **-t --topics_filepath**: Filepath to the file containing the list of topics. Do NOT specify this unless you wish to create a new topics dataset. If you wish to load existing topics from disk, use the serial_dir argument instead.
 - **-s --similarity_measure**: Default similarity score function. _Values_: "dot", "cos", "euclidean". _Default_: "cos"
 - **-thr --threshold**: Default threshold to consider a topic as relevant to the query. _Default_: 0.4
 - **-p --persist**: Whether to keep loaded topics and their embeddings in main memory

A example to run the code might be:

    python validation.py "/20 news group/20_newsgroup.csv" validation_topics.txt Validation Users.jsonl -s cos -thr 0.4 -p

---

</br>

## Folder sctructure

    .
    ├── README.md
    ├── Serialize --> Folder that contains the serialized objects
    │   ├── "Topics.json"*
    │   └── embeddings
    │       └── "Topic-keyword.pt"*
    ├── Users.jsonl --> File that describes the users
    ├── data --> Folder to store the validation data
    │   └── 20 news group
    │       └── 20_newsgroup.csv
    ├── datasets.py
    ├── profile_based_retrieval.py
    ├── requirements.txt
    ├── topics.py
    ├── topics.txt --> File that lists all the topics
    ├── users.py
    ├── utils.py
    └── validation.py

---

</br>

## Code dependences

 - `nltk` (3.6.5)
 - `pandas` (1.3.4)
 - `sentence_transformers` (2.2.0)
 - `torch` (1.11.0)
 - `typing` (3.7.4.3)
