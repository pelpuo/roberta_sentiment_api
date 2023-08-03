from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


class Roberta():
    def __init__(self):
        self.model = None
        self.tokenizer = None
    
    def initialize(self):
        MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.config = AutoConfig.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        
    def preprocess(self, text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)
    
    def classify(self, text):
        text = self.preprocess(text)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        
        l = self.config.id2label[ranking[0]]
        s = scores[ranking[0]]
        return {"label": l, "scores": "{:.2f}".format(s)}
        # return "true"
            
roberta = Roberta()