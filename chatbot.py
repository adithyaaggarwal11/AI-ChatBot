import nltk
import sys
from knowledge_engine import getSimilarity, getPhraseSimilarity, extract_candidate_chunks, get_sentiment, modify_questions
from knowledge_parser import extract_content
import numpy as np


continueCoversation = True
solutionFound = False
count = 1


kbase = extract_content('knowledge')
kbase_index = None


def find_issue(input):
    prob = []
    threshold = .4
    input_nouns = ' '.join(extract_candidate_chunks(input))
    for idx, issue in enumerate(kbase):
        current_prob = []
        for sentence in issue['issue']:
            chunks = ' '.join(extract_candidate_chunks(sentence))
            current_prob.append(getPhraseSimilarity(input_nouns, chunks))
        for sentence in issue['cause']:
            chunks = ' '.join(extract_candidate_chunks(sentence))
            current_prob.append(getPhraseSimilarity(input_nouns, chunks))
        # print current_prob
        prob.append(np.amax(current_prob))

    index = np.argmax(prob)
    # print prob, index, prob[index]
    if prob[index] < threshold:
        return False
    else:
        return index


class Chatterbot(object):

    # 0: issue
    # 1: confirm
    # 2: resolution

    def __init__(self):
        self.current_state = None
        self.current_issue = None
        self.resolution_idx = 0
        self.string_format = "VikingsBot #: {}"
        self.input = ''

    def pass_input(self, user_input):
        self.input = user_input
        if self.current_state is None:
            no = find_issue(user_input)
            # no = 1
            if no is False:
                # print("No issue found ..")
                pass
            else:
                # print("Issue found: ", no)
                self.current_issue = no
                self.current_state = 1

        elif self.current_state == 1:
            # print self.input, get_sentiment(self.input)
            if get_sentiment(self.input):
                self.current_state += 1
            else:
                self.current_state = None

        elif self.current_state == 2:
            if self.resolution_idx == len(kbase[self.current_issue]['resolution']):
                self.current_state = 3

    def sentence_generator(self):
        if self.current_state is None:
            if self.current_issue is None:
                print self.string_format.format('No issue found.. Thank you')
                sys.exit(0)
            else:
                print self.string_format.format('Can you please re phrase the issue')
        elif self.current_state == 1:
            chunks = extract_candidate_chunks(self.input)
            # print chunks
            print self.string_format.format(''.join(['Can you please confirm that your issue is related to ', chunks[0]]))
        elif self.current_state == 2:
            print self.string_format.format(self.sentence_converter())
        else:
            print self.string_format.format("Thank you.. Have a Nice Day")

    def sentence_converter(self):
        text = kbase[self.current_issue]['resolution'][self.resolution_idx]
        self.resolution_idx += 1
        return modify_questions(text)


cbot = Chatterbot()


print "VikingsBot #: {}".format("Hello, Thank you for choosing Allstate, How can I be of any assistance today.")
while continueCoversation:
    userInput = raw_input("User >>> ")
    cbot.pass_input(userInput)
    cbot.sentence_generator()

    if cbot.current_state > 2:
        continueCoversation = False
