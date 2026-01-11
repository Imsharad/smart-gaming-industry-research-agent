import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, RegexpStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('punkt');
nltk.download('wordnet');
nltk.download('stopwords');

corpus = """I am Rajesh. I work in Accenture. I am very interested to learn AI/ML 
        and Gen AI concepts."""

print(corpus);

### 1. Tokenization ###
#paragraph -> sentence tokenize
print(sent_tokenize(corpus));

documents = sent_tokenize(corpus);
type(documents);

for sentence in documents:
    print(sentence);

#paragraph -> word tokenize
print(word_tokenize(corpus));

for sentence in documents:
    print(word_tokenize(sentence));


### 2. Stemming Techniques ###
### Stemming is a process of reducing a word to its work stem that affixes to suffixes ###
### and prefixes or to the roots of the words known as lemma. Stemming is important in  ###
### NLU (Natural Language Understanding) and NLP(Natural Language Processing).###

stemming = PorterStemmer();
print(stemming.stem("going"));
words = ['going','gone','eating','eaten','playing','played','history', 'historian','congratulation','congratulatury'];
for word in words:
    print(word +"--->"+stemming.stem(word));


### RegexpStemmer ###
regexStemmer = RegexpStemmer('ing$|s$|e$|able$',min = 4);
print(regexStemmer.stem('eating'));


### Snowball Stemmer ###
snowballStemmer=SnowballStemmer("english");
for word in words:
    print(word+"--->"+snowballStemmer.stem(word));


stemming.stem("fairly");
stemming.stem("sportingly");

snowballStemmer.stem("fairly");
snowballStemmer.stem("sportingly");

### 3. Lemmatizer ###
wordnetLemitizer = WordNetLemmatizer();
# pos noun->n (by default), verb-> v, adjective->a, adverb->r
for word in words:
    print(word+"--->"+wordnetLemitizer.lemmatize(word,pos="v"));


### 4. Stop Words ###
### Stop words are like 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll" etc. ###
#print (stopwords.words('english'));
# you can pass different language like german or spanish to get the stop words in that language.
# e.g. stopwords.words('german');

# tokenize the paragraph
sentences = sent_tokenize(corpus);
# apply stop words and then apply stemming
""" for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [stemming.stem(word) for word in words if word not in set(stopwords.words('english'))]
    sentences[i]=' '.join(words) # converting all the words into sentences

print(sentences); """

# Apply stopwords and filter and apply snowball stemming
snowballStemmer=SnowballStemmer("english");
""" for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [snowballStemmer.stem(word) for word in words if word not in set(stopwords.words('english'))]
    sentences[i]=' '.join(words) # converting all the words into sentences

print(sentences); """

# Apply stopwords and filter and apply WordLemmatizer
wordnetLemitizer = WordNetLemmatizer();
for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [wordnetLemitizer.lemmatize(word.lower(), pos='v') for word in words if word not in set(stopwords.words('english'))]
    sentences[i]=' '.join(words) # converting all the words into sentences

print(sentences);
