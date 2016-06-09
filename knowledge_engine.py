from requests import get
import nltk
import string
import itertools
from senti_classifier import senti_classifier
import re

umbcUrl = "http://swoogle.umbc.edu/SimService/GetSimilarity"
umbcPhraseUrl = "http://swoogle.umbc.edu/StsService/GetStsSim"


def getSimilarity(s1, s2, type='relation', corpus='webbase'):
    try:
        response = get(umbcUrl, params={
                       'operation': 'api', 'phrase1': s1, 'phrase2': s2, 'type': type, 'corpus': corpus})
        return float(response.text.strip())
    except:
        print('Error in getting similarity for %s: %s' % ((s1, s2), response))
        return 0.0


def getPhraseSimilarity(s1, s2):
    try:
        response = get(umbcPhraseUrl, params={
                       'operation': 'api', 'phrase1': s1, 'phrase2': s2})
        return float(response.text.strip())
    except:
        print('Error in getting similarity for %s: %s' % ((s1, s2), response))
        return 0.0


def get_sentiment(userinput):
    userinput = userinput.lower()
    if 'yes' in userinput:
        return True
    (pos, neg) = senti_classifier.polarity_scores([userinput])
    if pos > neg:
        return True
    else:
        return False


def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(
        nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
                  for key, group in itertools.groupby(all_chunks, lambda (word, pos, chunk): chunk != 'O') if key]

    return [cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)]


class GoalMap():

    def __init__(self, sentences, threshold=0.65):
        self.slen = len(sentences)
        self.threshold = threshold
        self.sentences = sentences
        self.state = 0

    def check(self, input):
        prob = getSimilarity(input, self.sentences[self.state])
        if prob < self.threshold:
            return self.confirm()
        else:
            retval = (prob, self.sentences[self.state])
            self.state += 1
            return retval

    def confirm(self):
        return ("Confirm", 0)

    # def test(self):
    #     selected_index = -1
    #     current_threshold = 0
    #     for i, s in enumerate(self.sentences):
    #         if self.activation[i] == 0:
    #             continue

    #         prob = get_similarity(input, s)
    #         if (prob >= self.threshold) and (prob >= current_threshold):
    #             current_threshold = prob
    #             selected_index = i

    #     self.activation[selected_index] = 0
    #     print(self.activation)
    #     return (current_threshold, self.sentences[selected_index])


# class SpeechActIdentifier:

#     def __init__(self):
#         pass


# def speechActIdentifier():
# print getPhraseSimilarity('a small violin is being played by a girl', 'a child is performing on a tiny instrument')
# print getPhraseSimilarity('email account', 'email login')


mappings = {
    "the customer's": "your",
    "the customer is": "your",
    "with the user": "your",
    "their": "your"
}


def modify_questions(userinput):
    if 'customer' not in userinput and 'user' not in userinput:
        userinput = 'I have ' + userinput.lower()
    else:
        userinput = 'Please ' + userinput.lower()
    for idx, value in mappings.iteritems():
        userinput = re.sub(idx, value, userinput)
    return userinput
