from __future__ import division
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline


def lsa():
    v = CountVectorizer(analyzer="word",
                        tokenizer=None,
                        preprocessor=None,
                        stop_words=None,
                        max_features=10000)

    data = joblib.load('models/sentences.pkl')
    tags = joblib.load('models/taglist.pkl')

    bagofwords = v.fit_transform(data)
    print bagofwords.shape
    tfidf_transformer = TfidfTransformer()
    xtrain = tfidf_transformer.fit_transform(bagofwords)
    print xtrain.shape
    pipeline = Pipeline(
            [
                ('svd', TruncatedSVD(n_components=50)),
                ('nn', KNeighborsClassifier()),
            ]
        )

    print('Training.')
    pipeline.fit(xtrain, tags)
    print("dump models")
    # save models
    joblib.dump(v, 'models/bagofwords_gen.pkl')
    joblib.dump(tfidf_transformer, 'models/tfidf_gen.pkl')
    joblib.dump(pipeline, 'models/svd.pkl')


def get_tag(s):
    v = joblib.load('models/bagofwords_gen.pkl')
    tfidf_transformer = joblib.load('models/tfidf_gen.pkl')
    # print v.vocabulary_.items()
    pipeline = joblib.load('models/svd.pkl')

    bw = v.transform(s)
    print bw.shape, bw.todense()
    tfidf = tfidf_transformer.transform(bw)
    # print tfidf.shape
    print pipeline.predict(tfidf)

# lsa()
# get_tag(["This restaurant makes the best burritos", "Stop making large trades when you have small margins",
#         "I am going to update your account information", "I am sorry that you lost access to your account",
        # "This restaurant just lost my business"])
