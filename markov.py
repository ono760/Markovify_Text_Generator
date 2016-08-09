import nltk
import re
import pprint
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize

class Markovify:

    def __init__(self, chain, length):
        self.corpus_speech = ''
        self.corpus_article = ''
        self.corpus_tweet = ''
        self.chain = chain
        self.length = length
        self.words = []
        self.tokens = []
        self.nltk_text = None
        self.start_words = []
        self.dictionary = {}
        self.parts_of_speech = []

    def import_text(self, text, type):

        if type == 'speech':
            with open(text, 'r') as original:
                self.corpus_speech += original.read()
                self.corpus_speech = unicode(self.corpus_speech, 'utf-8')
            print(sent_tokenize(self.corpus_speech))
            self.words = self.corpus_speech.split(' ')
            self.tokens = word_tokenize(self.corpus_speech)
            self.nltk_text = nltk.Text(self.tokens)
            self.parts_of_speech = nltk.pos_tag(self.tokens)

        elif type == 'article':
            with open(text, 'r') as original:
                self.corpus_article += original.read()
                self.corpus_article = unicode(self.corpus_article, 'utf-8')
            print(sent_tokenize(self.corpus_article))
            self.words = self.corpus_article.split(' ')
            self.tokens = word_tokenize(self.corpus_article)
            self.nltk_text = nltk.Text(self.tokens)
            self.parts_of_speech = nltk.pos_tag(self.tokens)

        elif type == 'tweet':
            with open(text, 'r') as original:
                self.corpus_tweet += original.read()
                self.corpus_tweet = unicode(self.corpus_tweet, 'utf-8')
            print(sent_tokenize(self.corpus_tweet))
            self.words = self.corpus_tweet.split(' ')
            self.tokens = word_tokenize(self.corpus_tweet)
            self.nltk_text = nltk.Text(self.tokens)
            self.parts_of_speech = nltk.pos_tag(self.tokens)


    def create_dictionary(self):

        for i in range(len(self.words) - (self.chain - 1)):
            cur_key = []
            for j in range(self.chain - 1):
                cur_key.append(self.words[i + j])
            cur_key = tuple(cur_key)
            if cur_key in self.dictionary:
                self.dictionary[cur_key].append(self.words[i + self.chain - 1])
            else:
                self.dictionary[cur_key] = [self.words[i + self.chain - 1]]

    def generate_text(self):
        import random
        output_text = []

        # creates a list of words to start the output text (consider
        # refactoring to have only words where prev is .)
        for word in self.words:
            if word[0].upper() + word[1:].lower() == word:
                self.start_words.append(word)

        first_word_idx = int(len(self.start_words) * random.random())
        first_word = self.start_words[first_word_idx]

        cache = [first_word]
        for i, word in enumerate(self.words):
            if word == first_word:
                for j in range(self.chain - 2):
                    cache.append(self.words[i + j + 1])
                break
        # print cache
        output_text += cache

        for i in range(self.length - (self.chain - 1)):
            for key in self.dictionary:
                if tuple(cache) == key:
                    next_word = random.choice(self.dictionary[key])
                    output_text.append(next_word)
                    cache.append(next_word)
                    cache.pop(0)
                    break
        print(' '.join(output_text))

trump = Markovify(5, 15)
trump.import_text('trump.txt', 'tweet')
# trump.import_text('star_wars.txt')
trump.create_dictionary()
trump.generate_text()
