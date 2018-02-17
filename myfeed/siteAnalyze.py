import sys
import codecs
import nltk
from nltk.corpus import stopwords

def pageKeywords(message):
    # NLTK's default German stopwords
    default_stopwords = set(nltk.corpus.stopwords.words('english'))

    # We're adding some on our own - could be done inline like this...
    # custom_stopwords = set((u'–', u'dass', u'mehr'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    stopwords_file = './stopwords.txt'
    custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    all_stopwords = default_stopwords | custom_stopwords

    # input_file = "message.txt"

    # fp = codecs.open(input_file, 'r', 'utf-8')

    words = nltk.word_tokenize(message)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 2]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # Stemming words seems to make matters worse, disabled
    # stemmer = nltk.stem.snowball.SnowballStemmer('english')
    # words = [stemmer.stem(word) for word in words]

    # print(bigrams)
    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]
    # bigrams = nltk.bigrams(words)
    # freq_bi = nltk.FreqDist(bigrams)
    # for big in freq_bi.most_common(50):
    #     print(big)

    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)

    # Output top 50 words

    # f=open('frequency.txt','w+')
    # print("i came here")
    words=[]
    for word, frequency in fdist.most_common(5):
        # print(u'{};{}'.format(word, frequency))
        words.append(word)
        # f.write(u'{},{}\n'.format(word, frequency))
    # f=open('message.txt','w+')    
    return words
# pageKeywords()    
