# Grammar Analyzer

As part of my summer internship the company Smart Mahal gave me the task of creating a grammar analysis model of the English text. This model consists of two main parts:
- The first part focuses on creating an algorithm that will transform a text into a simple sequence of sentences. If we divide a text only based on punctuation, we will have complex sentences which will be difficult to analyze later.
- The second part focuses on the creation of an algorithm that will identify the grammatical class of each word to then identify the basic sentence model (Subject-Verb-Object, Subject-Verb-Object indirect-preposition-Object direct. .), the conjugation tenses used, the passive voice, the active voice, the conditional and the direct or indirect speech.

## Sentencizer
Sentencizer is the name of the program that I developed to be able to transform a text into a sequence of sentences. Sentence segmentation is the natural language processing problem of deciding where sentences begin and end. Natural language processing tools often require their input to be broken down into sentences; however, identifying sentence boundaries can be difficult due to the potential ambiguity of punctuation marks and also due to compound and complex sentences. In order to remedy this problem, I based myself on the vanilla approach and an approach based on rules that I have defined myself.

## Tense Analyzer
Tense Analyzeris the name of the program I developed to detect the tense used in a sentence (Simple present, Simple past, Present continuous...)  based on the POS tag. I create a rules-based approach to identify the tense used.

## Sentence structure
Grammar Analyzer is the name of the program that I developed to be able to identify the grammatical class of each word and then identify the basic sentence pattern, the conjugation tenses used, the passive voice, the active voice, the conditional and the direct speech or indirect speech. To identify its patterns, I used the dependency parsing technique, to create rules that will help me find the basic patterns of a sentence. In each sentence model I must present the basic elements of the sentence (subject, verb, verb conjugation tenses, preposition, adverb ...).

## Dependencies
In order to properly run this code, you must have installed:
- Python 3.9.5
- SpaCy 2.3.5
- SpaCy pipeline for english (ex: en_core_web_sm)

## How to use

```Python
import SentenceStructure as struct
import spacy

nlp = spacy.load("en_core_web_lg")
    sentence = "She is uncertain whether she made the right decision."
    print("sentence: %s" % (sentence))
    structure = struct.SentenceStructure(nlp, sentence)
    print(structure.sentence_structure)
```

```
>>> sentence: She is uncertain whether she made the right decision.
[('Sentence type', 'Compound sentence'), [('First clause', whether she made the right decision), ('Verb', ' made'), ('Tense', 'Simple past tense'), ('Direct-Object', the right decision), ('Indirect-Object', None), ('Prepositions', []), ('Adjectives', [right]), ('Adverb', [])], [('Second clause', She is uncertain .), ('Verb', ' is'), ('Tense', 'Simple present tense'), ('Direct-Object', None), ('Indirect-Object', None), ('Prepositions', []), ('Adjectives', [uncertain]), ('Adverb', [])]]

```





