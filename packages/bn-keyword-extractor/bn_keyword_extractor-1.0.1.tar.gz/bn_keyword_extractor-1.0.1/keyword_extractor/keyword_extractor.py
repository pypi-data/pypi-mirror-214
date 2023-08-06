import torch
from transformers import AutoTokenizer, AutoModel
import requests
import pandas as pd
import random


class KeywordExtractor:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.bn_stop_words = None

    def load_model(self):
        model_name = 'csebuetnlp/banglabert'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def load_stop_words(self):
        url = 'https://github.com/AuthoredByTonmoy/stopwords/raw/main/bangla_stopwords.xlsx'
        filename = 'bangla_stopwords.xlsx'
        response = requests.get(url)

        with open(filename, 'wb') as f:
            f.write(response.content)

        df_stop_words = pd.read_excel(filename)
        self.bn_stop_words = df_stop_words["word_list"].values.tolist()

    def score_words(self, sentence):
        input_ids = torch.tensor([self.tokenizer.encode(
            sentence, max_length=512, padding='max_length', truncation=True)])

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids)
            embeddings = outputs.last_hidden_state.squeeze(0)

        mean_embedding = embeddings.mean(dim=0)
        word_scores = []
        for i in range(embeddings.size(0)):
            cos_sim = torch.nn.functional.cosine_similarity(
                embeddings[i], mean_embedding, dim=0)
            word_scores.append(
                (self.tokenizer.decode(input_ids[0][i]), cos_sim.item()))

        return word_scores

    def clean(self, sen):
        strs = ''
        for i in range(len(sen)):
            if sen[i] != '।':
                strs = strs + sen[i]
        return strs.split()

    def print_top_values(self, data):
        data_shuffled = random.sample(data, len(data))
        top_values = int(len(data_shuffled) * 0.6)
        if top_values < 10:
            top_values = int(len(data_shuffled) * 0.7)
        if top_values < 4:
            top_values = int(len(data_shuffled) * 0.8)

        finalLst = []
        for i in range(top_values):
            finalLst.append(data_shuffled[i][0])

        return finalLst

    def keysOfSentence(self, sentence):
        lst = self.clean(sentence)
        lst2 = []
        final = []
        word_scores = self.score_words(sentence)

        for i in range(len(word_scores)):
            if i > 0:
                if word_scores[i][0] != '।':
                    lst2.append(word_scores[i][1])
        for i in range(len(lst)):
            final.append(tuple([lst[i], lst2[i]]))

        finalKeysLst = self.print_top_values(final)
        finalKeys = finalKeysLst

        return finalKeys

    def extract_keywords(self, text):
        self.load_model()
        self.load_stop_words()
        return self.keysOfSentence(text)
