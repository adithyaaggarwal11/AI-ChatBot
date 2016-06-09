import re
# import itertools, nltk, string

# def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):

#     # exclude candidates that are stop words or entirely punctuation
#     punct = set(string.punctuation)
#     stop_words = set(nltk.corpus.stopwords.words('english'))
#     # tokenize, POS-tag, and chunk using regular expressions
#     chunker = nltk.chunk.regexp.RegexpParser(grammar)
#     tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
#     all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
#                                                     for tagged_sent in tagged_sents))
#     # join constituent chunk words into a single chunked phrase
#     candidates = [' '.join(word for word, pos, chunk in group).lower()
#                   for key, group in itertools.groupby(all_chunks, lambda (word,pos,chunk): chunk != 'O') if key]

#     return [cand for cand in candidates
#             if cand not in stop_words and not all(char in punct for char in cand)]



# print extract_candidate_chunks('can you unlock my email account')
# print extract_candidate_chunks('User is not able to login to email system via MS Outlook from a company issued computer or mobile device.')
# print extract_candidate_chunks('User is not able to login to web-email from a web browser from a company issued computer, personal computer or mobile device.')
# print extract_candidate_chunks('can you help me change my billing address')
# print extract_candidate_chunks('Customer requests a change to their billing address, but their mailing address remains the same.')
# print extract_candidate_chunks('Customer needs to change both their billing address and mailing address.')

s = [
"Verify the customer's current billing address",
"Verify the customer's current mailing address",
"Verify that the customer is requesting a change to their billing address only or also their mailing address",
"Update their billing address",
"If the customer would like to update their mailing address as well, update their mailing address",
"Confirm the customer's new billing address and, if applicable, their mailing address after the change",
"Resolve the incident by unlocking the email account.",
"Verify with the user that their issue has been resolved.",
"Help the user understand and correct the root cause if necessary."
]


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

for x in s:
    print modify_questions(x)
