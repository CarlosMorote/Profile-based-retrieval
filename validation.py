import pandas as pd
import argparse
from profile_based_retrieval import ProfileRetrieval
from datasets import TopicDataset
from statistics import mean
from math import sqrt
from datetime import datetime

col_names = ['text','target']

# python validation.py "/20 news group/20_newsgroup.csv" validation_topics.txt Validation Users.jsonl -s cos -thr 0.4 -p
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument("file_name",
                help="File name of the dataset to validate")
    parser.add_argument("topics_file",
                help="Name of the file that contains the list of topics")
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

    file_name = args.file_name

    if file_name.split(".")[-1] != 'csv':
        print("The file must be csv")
        exit()

    route = f"./data{file_name}"

    print("Loading dataframe")
    df = pd.read_csv(route)

    if not all(x in df.columns.values.tolist() for x in col_names):
        print("The dataframe must consist of a text and a target columns")
        exit()

    further_step = False
    topic_list = []

    try:
        with open(args.topics_file, 'r') as f:
            topic_list = f.readline().strip().split(';')

    except FileNotFoundError:
        print("topcis file does not exist. Creating a new one...")
        further_step = True

    for topic_df in df.target.unique():
        if topic_df not in topic_list:
            topic_list.append(topic_df)
            further_step = True

    if further_step:   
        with open (args.topics_file, 'w') as f:
            f.write(';'.join(topic_list))

        td = TopicDataset(args.serial_dir)
        td.add_topics(*topic_list)

    print("Dataframe loaded")

    print("Initiating Engine ...")
    profile_retrieval_search = ProfileRetrieval(args.serial_dir, args.users_filepath, args.similarity_measure, 0, args.persist)
    print("Engine loaded corectly")

    print("Permorming validation ...")

    scores = []
    predictions = []
    start = datetime.now()

    for index in range(max(df.index)+1):

        test_instance = df.iloc[index]
        predicted_topics = profile_retrieval_search._topics_query(test_instance['text'], 0, verbose=0)
        actual_topic = test_instance['target']

        filtered = list(filter(lambda x: x[0].name==actual_topic, predicted_topics))
        predictions.append(float(filtered[0][1] if filtered else 0))


        if not index % 100:
            print(f"Queries validated: {index}")

    print(f"RMSE: {sqrt((sum(map(lambda x: x-1, predictions))**2)/len(predictions))}")
    print(f"Validation time: {datetime.now()-start}")
