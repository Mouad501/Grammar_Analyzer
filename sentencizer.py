"""
Sentencizer is a class that contains rule-based algorithms created
to split a text into sentences
"""
import nltk as nltk


class Sentencizer:

    def __init__(self, text, split_characters=['.', '?', '!', ':', ';'],
                 delimiter_token='$$'):
        self.raw_text = self.preprocessing(text)
        self._delimiter_token = delimiter_token
        self._split_characters = split_characters
        self.sentences = []
        self.splitter_by_punctuation()
        self.split_skscs()
        self.splitter_by_2grams()
        self.splitter_by_unigrams()
        self.split_kscs()
        self.sentence_cleaning()

    # this method will preprocess the text: basically transform abbreviations
    # to its long form
    def preprocessing(self, text):
        text = text.replace("’", "'")
        keywords = [("he's", "he is"), ("'re", " are"), ("'m", " am"),
                    ("'ll", " will"), ("n't", " not"), ("it's", "it is"),
                    ("she's", "she is"), ("That's", "that is")]
        for keyword in keywords:
            if keyword[0] in text:
                text = text.replace(keyword[0], keyword[1])
        return text

    # this method is based on punctuations to split the text into sentences.
    def splitter_by_punctuation(self):
        work_sentence = self.raw_text
        for character in self._split_characters:
            work_sentence = work_sentence.replace(character, character + "" +
                                                  self._delimiter_token)
        self.sentences = work_sentence.split(self._delimiter_token)

    # this method is based on uni-gram keywords to split the text into
    # sentences
    def splitter_by_unigrams(self):
        self.sentences = filter(None, self.sentences)
        s = []  # list of sentences
        # list of keywords
        unigrams_split = ['because', 'hence', 'consequently', 'while', 'next',
                          'then', 'when', 'but']
        # list of keywords that come after a comma
        unigrams_comma_split = ['moreover', 'so', 'hence', 'particularly',
                                'especially', 'however', 'nevertheless',
                                'although', 'but', 'yet', 'despite', 'whereas',
                                'then', 'which', 'and', "or"]
        for phrase in self.sentences:
            tokens = nltk.word_tokenize(phrase)
            for i in range(len(tokens)):
                for unigram in unigrams_comma_split:
                    # check if it's a keyword
                    if tokens[i] == unigram:
                        # check if there is a comma before the keyword, also
                        # check that the number of words in the
                        # sentence is grater or equal to 3
                        if tokens[i - 1] == ',' and i >= 3 and 2 > (
                                i - len(tokens)):
                            tokens[i] = '$$'
                            tokens[i - 1] = ''
                for unigram in unigrams_split:
                    # check if it's a keyword, also check that the number of
                    # words in the sentence is grater than 3
                    if tokens[i] == unigram and i >= 3 and 2 > (
                            i - len(tokens)):
                        tokens[i] = '$$'
            sentences = ' '.join(tokens)
            sentences = sentences.split('$$')
            for sentence in sentences:
                s.append(sentence)
        self.sentences = s

    # auxiliary method to divide a sentence by a comma: it replaces the
    # following comma with a special character which marks the boundaries
    # of the sentences
    def split_first_comma(self, text, begin):
        for i in range(begin, len(text)):
            if text[i] == ',':
                text[i] = self._delimiter_token
        return text

    # this method is based on keywords which divide the sentences in the form:
    # Keyword + Sentence + comma + Sentence (kscs)
    def split_kscs(self):
        self.sentences = filter(None, self.sentences)
        s = []
        keywords = ['Despite', 'Although', 'While', 'When', 'Even if',
                    'Even though', 'Even']
        for phrase in self.sentences:
            for keyword in keywords:
                if keyword in phrase:
                    phrase = phrase.replace(',', '$$', 1)
                    phrase = phrase.replace(keyword, '')
            sentences = phrase.split('$$')
            for sentence in sentences:
                s.append(sentence)
        self.sentences = s

    # this method is based on keywords which divide the sentences in the form:
    # Sentence + keyword + Sentence + comma + Sentence (kscs)
    def split_skscs(self):
        self.sentences = filter(None, self.sentences)
        s = []
        keywords = ['but when']
        for phrase in self.sentences:
            for keyword in keywords:
                if keyword in phrase:
                    subphrase = phrase[:phrase.find(keyword)]
                    phrase = phrase[phrase.find(keyword):]
                    phrase = phrase.replace(',', self._delimiter_token, 1)
                    phrase = phrase.replace(keyword, self._delimiter_token)
                    phrase = subphrase + phrase
            sentences = phrase.split(self._delimiter_token)
            for sentence in sentences:
                s.append(sentence)
        self.sentences = s

    # this method is based on 2-gram keywords to split the text into sentences
    def splitter_by_2grams(self):
        self.sentences = filter(None, self.sentences)
        s = []
        keywords = ['and then', 'even though', 'but then',
                    'even so', 'and sometimes', 'when sometimes',
                    'as long as', 'as far as', 'as soon as', 'if and only if']
        for phrase in self.sentences:
            for keyword in keywords:
                if keyword in phrase:
                    phrase = phrase.replace(keyword, self._delimiter_token)
            sentences = phrase.split(self._delimiter_token)
            for sentence in sentences:
                s.append(sentence)
        self.sentences = s

    # this function removes transition words like 'In addition', 'To sum
    # up', 'Therefore' ... the transition words are used to link the
    # sentences to each other and do not form sentences so I will delete
    # them .
    def sentence_cleaning(self):
        clean_sentences = []
        self.sentences = filter(None, self.sentences)
        transition_words = ['In addition', 'As a result', 'Thus', 'To sum up',
                            'But', 'In fact', 'In conclusion', 'To summarise',
                            'Due To', 'For example', 'For instance', 'Such as',
                            'Because of', 'In Brief', 'First', 'Firstly',
                            'Second', 'Secondly', 'Next', 'Finally',
                            'Furthermore', 'Also', 'Moreover', 'Therefore',
                            'Consequently', 'Hence', 'Undoubtedly', 'Indeed',
                            'Clearly', 'Because', 'Since', 'However', 'Then',
                            'Although', 'Nevertheless', 'Unfortunately',
                            'Perhaps', 'Maybe']
        for sentence in self.sentences:
            sentence = sentence.lstrip()
            if sentence.startswith(","):
                sentence = sentence[1:]
            for keyword in transition_words:
                if keyword in sentence:
                    sentence = sentence.replace(keyword, "")
            clean_sentences.append(sentence)
        self.sentences = clean_sentences
