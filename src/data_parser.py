import json

data_path = r"D:\cai_dev\PyQt_Widges\data\data.json"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())


class Article(object):
    def __init__(self, datas):
        self.language = datas.get("language")
        self.text = datas.get("text")
        self.segments: list = datas.get("segments")
        self.segments = [Segment(seg_data) for seg_data in datas.get("segments")]


class Segment(object):
    def __init__(self, datas):
        self.id = datas.get("id")
        self.seek = datas.get("seek")
        self.start = datas.get("start")
        self.end = datas.get("end")
        self.text = datas.get("text")
        self.tokens = datas.get("tokens")
        self.temperature = datas.get("temperature")
        self.avg_logprob = datas.get("avg_logprob")
        self.compression_ratio = datas.get("compression_ratio")
        self.no_speech_prob = datas.get("no_speech_prob")
        self.confidence = datas.get("confidence")
        self.words = [Word(word_data) for word_data in datas.get("words")]


class Word(object):
    def __init__(self, datas):
        self.text = datas.get("text")
        self.start = datas.get("start")
        self.end = datas.get("end")
        self.confidence = datas.get("confidence")


article_object = Article(data)
