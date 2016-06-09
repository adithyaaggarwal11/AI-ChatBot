from swda import Transcript
import os
from sklearn.externals import joblib
from re import findall, sub



path = "../swda/"
dirs = os.listdir(path)

swdb_files = []

for file in dirs:
    if os.path.isdir(os.path.join(path, file)):
        files = os.listdir(os.path.join(path, file))
        for csvfile in files:
            filename = os.path.join(path, file, csvfile)
            if 'csv' not in filename:
                continue
            swdb_files.append(filename)


tags = {
    "assertive": ['sd', 'ny', 'nn', 'cq', 'na', 'C2', 'qh', 'ng', 'no', 'qrr', 'arp'],
    "expressive": ['sv', '%', 'bh', 'bk', 'br', 'aa', 'ba', 'fc', 'h', 'Ch', 'ar', 'fp', 'bd', 'aap', 'fa', 'ft', 'bCm'],
    "commisive": ['commits'],
    "declarative": ['sd', 'sd^d', 'q^d'],
    "directive": ['qy', 'qw', 'qyCd', 'bh', 'bf', 'ad', 'qo', 'Cg', 'qwCd']
}

goal_tags = ["great day", "good day", "welcome"]

taglist = []
sentences = []

for f in swdb_files:
    print f
    trans = Transcript(f)
    for s in trans.utterances:
        damtag = s.damsl_act_tag()
        for gtag in goal_tags:
            if findall('\\b'+gtag+'\\b', s.text):
                print "gmap", gtag
                taglist.append('goalfull')
                sentences.append(s.text)
                break
        for key, value in tags.iteritems():
            for tag in value:
                if damtag == tag:
                    taglist.append(key)
                    sentences.append(s.text)


print len(sentences), len(taglist)

joblib.dump(taglist, 'taglist.pkl')
joblib.dump(sentences, 'sentences.pkl')

# print joblib.load('taglist.pkl')
# for key, value in tags.iteritems():
#     with open(key, 'w') as xfile:
#         for f in swdb_files:
#             trans = Transcript(f)
#             for s in trans.utterances:
#                 damtag = s.damsl_act_tag()
#                 for tag in value:
#                     if damtag == tag:
#                         for token in utter.tokens:
#                             if token in ['{', '}', '[', ']', '/']:  # ignore literals
#                                 continue



