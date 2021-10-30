"""
Sentence structure is a class that contains rule-based grammar parser for
identifying the basic english patterns of a sentence

voice index (self.voice):
    0: Active voice
    1: Passive voice
sentence type:
    2: Conditionnal
    3: Reported speech
    4: Compound sentence
    5: Adverb clauses (sentence with an adverb clause)
    other: basic sentence

"""
import spacy
import TenseAnalyzer as Tense


def passive_or_active_voice(doc):
    for token in doc:
        if "nsubjpass" == token.dep_ or "agent" == token.dep_ or "auxpass" == token.dep_:
            return 1
        else:
            return 0


def conditionnal_or_adv_clause(doc):
    condition1 = 0
    condition2 = 0
    for token in doc:
        if token.dep_ == "advcl":
            condition1 = 1

    for token in doc:
        if token.lemma_ == "if":
            condition2 = 1
    if condition1 == condition2 and condition1 == 1:
        return 2
    elif condition1 == 1:
        return 5

def reported_speech_or_compound(doc):
    condition1 = 0
    condition2 = 0
    for token in doc:
        if token.dep_ == "ccomp" or token.dep_ == "xcomp":
            condition1 = 1

    for token in doc:
        if token.dep_ == "ROOT":
            if token.lemma_ == 'tell' or token.lemma_ == 'say' \
                    or token.lemma_ == "ask" or token.lemma_ == "explain":
                condition2 = 1
    if condition1 == condition2 and condition1 == 1:
        return 3
    elif condition1 == 1:
        return 4

def split_compound_sentence(doc):
    for token in doc:
        if "ccomp" == token.dep_ or "xcomp" == token.dep_:
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            sentence1 = str(doc[start:end])
            sentence2 = str(doc).replace(sentence1, "")
            return sentence1, sentence2

def get_subject(doc):
    for token in doc:
        if ("nsubj" == token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]

def get_preposition(doc):
    prep_spans = []
    for token in doc:
        if ("prep" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            prep_spans.append(doc[start:end])
    return prep_spans

def get_adjective(doc):
    prep_spans = []
    for token in doc:
        if "acomp" in token.dep_ or "amod" in token.dep_:
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            prep_spans.append(doc[start:end])
    return prep_spans

def get_adverb(doc):
    prep_spans = []
    for token in doc:
        if ("advmod" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            prep_spans.append(doc[start:end])
    return prep_spans

def get_direct_object(doc):
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def get_attribute(doc):
    for token in doc:
        if "attr" in token.dep_:
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def get_dative(doc):
    for token in doc:
        if "dative" in token.dep_:
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]

def get_agent(doc):
    for token in doc:
        if ("agent" == token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def get_passive_subject(doc):
    for token in doc:
        if "nsubjpass" == token.dep_:
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def get_verb_phrase(doc):
    verb = ""
    aux = ""
    for token in doc:
        if "ROOT" == token.dep_:
            if "VERB" == token.pos_ or "AUX" == token.pos_:
                verb = str(token)
        if "aux" == token.dep_ or "auxpass" == token.dep_:
            if token.lemma_ != "to" and token.lemma_ != "do":
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                aux = aux + " " + str(doc[start:end])
    return str(aux) + " " + str(verb)

def get_compound_verb_phrase(phrase2, doc):
    verb = ""
    aux = ""
    for token in phrase2:
        if "ccomp" == token.dep_ or "xcomp" == token.dep_:
            if "VERB" == token.pos_:
                verb = str(token)
            elif "AUX" == token.pos_:
                verb = str(token)
        if "aux" == token.dep_ or "auxpass" == token.dep_:
            if token.lemma_ != "to" and token.lemma_ != "do":
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                aux = aux + " " + str(doc[start:end])
    return str(aux) + " " + str(verb)

def get_active_voice_structure(nlp, doc):
    subject = get_subject(doc)
    verb = get_verb_phrase(doc)
    direct_object = get_direct_object(doc)
    indirect_object = get_dative(doc)
    preposition = get_preposition(doc)
    adjective = get_adjective(doc)
    adverb = get_adverb(doc)
    subject_complement = get_attribute(doc)
    tense_analyzer = Tense.TenseAnalyser(nlp, verb, 0)
    verb_phrase_tense = tense_analyzer.tense
    return [("Sentence type", "Basic active voice"), ("Subject", subject), ("Verb", verb), ("Tense", verb_phrase_tense),
            ("Subject complement", subject_complement), ("Direct-Object", direct_object),
            ("Indirect-Object", indirect_object),
            ("Prepositions", preposition),
            ("Adjectives", adjective), ("Adverb", adverb)]

def get_passive_voice_structure(nlp, doc):
    agent = get_agent(doc)
    verb = get_verb_phrase(doc)
    preposition = get_preposition(doc)
    adjective = get_adjective(doc)
    adverb = get_adverb(doc)
    passive_subject = get_passive_subject(doc)
    tense_analyzer = Tense.TenseAnalyser(nlp, verb, 1)
    verb_phrase_tense = tense_analyzer.tense
    return [("Sentence type", "Basic passive voice"), ("Passive Subject", passive_subject), ("Verb", verb), ("Tense", verb_phrase_tense),
            ("Agent", agent), ("Prepositions", preposition),
            ("Adjectives", adjective), ("Adverb", adverb)]

def get_reported_speech_structure(nlp, doc):
    phrase1, phrase2 = split_compound_sentence(doc)
    phrase1 = nlp(phrase1)
    phrase2 = nlp(phrase2)
    speech_reporter = get_subject(phrase1)
    verb = get_compound_verb_phrase(phrase2, doc)
    direct_object = get_direct_object(doc)
    indirect_object = get_dative(doc)
    preposition = get_preposition(doc)
    adjective = get_adjective(doc)
    adverb = get_adverb(doc)
    tense_analyzer = Tense.TenseAnalyser(nlp, verb, 0)
    verb_phrase_tense = tense_analyzer.tense
    return [("Sentence type", "reported speech"), ("Speech reporter", speech_reporter), ("Verb", verb), ("Tense", verb_phrase_tense),
            ("Direct-Object", direct_object),
            ("Indirect-Object", indirect_object),
            ("Prepositions", preposition),
            ("Adjectives", adjective), ("Adverb", adverb)]


def get_compound_structure(nlp, doc):
    sentence1, sentence2 = split_compound_sentence(doc)
    sentence1 = nlp(str(sentence1))
    sentence2 = nlp(str(sentence2))
    verb1 = get_verb_phrase(sentence1)
    verb2 = get_verb_phrase(sentence2)
    tense1 = Tense.TenseAnalyser(nlp, verb1, 0)
    tense2 = Tense.TenseAnalyser(nlp,verb2, 0)
    structure_sentence1 = [("First clause", sentence1), ("Verb", verb1), ("Tense", tense1.tense),
            ("Direct-Object", get_direct_object(sentence1)),
            ("Indirect-Object", get_dative(sentence1)),
            ("Prepositions", get_preposition(sentence1)),
            ("Adjectives", get_adjective(sentence1)), ("Adverb", get_adverb(sentence1))]
    structure_sentence2 = [("Second clause", sentence2), ("Verb", verb2), ("Tense", tense2.tense),
            ("Direct-Object", get_direct_object(sentence2)),
            ("Indirect-Object", get_dative(sentence2)),
            ("Prepositions", get_preposition(sentence2)),
            ("Adjectives", get_adjective(sentence2)), ("Adverb", get_adverb(sentence2))]
    return [('Sentence type', 'Compound sentence'), structure_sentence1, structure_sentence2]


def split_adverbial_clause(doc):
    sentence1 = ""
    sentence2 = ""
    for token in doc:
        if ("advcl" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            sentence1 = str(doc[start:end])
            sentence2 = str(doc).replace(sentence1, "")
            return sentence1, sentence2


def get_conditional_structure(nlp, doc):
    sentence1, sentence2 = split_adverbial_clause(doc)
    sentence1 = nlp(sentence1)
    sentence2 = nlp(sentence2)
    verb1 = get_verb_phrase(sentence1)
    verb2 = get_verb_phrase(sentence2)
    tense1 = Tense.TenseAnalyser(nlp, verb1, 0)
    tense2 = Tense.TenseAnalyser(nlp, verb2, 0)
    structure_sentence1 = [("Conditional First clause", sentence1), ("Verb", verb1), ("Tense", tense1.tense),
            ("Direct-Object", get_direct_object(sentence1)),
            ("Indirect-Object", get_dative(sentence1)),
            ("Prepositions", get_preposition(sentence1)),
            ("Adjectives", get_adjective(sentence1)), ("Adverb", get_adverb(sentence1))]
    structure_sentence2 = [("Conditional Second clause", sentence2), ("Verb", verb2), ("Tense", tense2.tense),
            ("Direct-Object", get_direct_object(sentence2)),
            ("Indirect-Object", get_dative(sentence2)),
            ("Prepositions", get_preposition(sentence2)),
            ("Adjectives", get_adjective(sentence2)), ("Adverb", get_adverb(sentence2))]
    return [('Sentence type', 'Conditional sentence'), structure_sentence1, structure_sentence2]


def adverbial_structure(nlp, doc):
    sentence1, sentence2 = split_adverbial_clause(doc)
    sentence1 = nlp(sentence1)
    sentence2 = nlp(sentence2)
    verb1 = get_verb_phrase(sentence1)
    verb2 = get_verb_phrase(sentence2)
    tense1 = Tense.TenseAnalyser(nlp, verb1, 0)
    tense2 = Tense.TenseAnalyser(nlp, verb2, 0)
    structure_sentence1 = [("First clause", sentence1), ("Verb", verb1), ("Tense", tense1.tense),
            ("Direct-Object", get_direct_object(sentence1)),
            ("Indirect-Object", get_dative(sentence1)),
            ("Prepositions", get_preposition(sentence1)),
            ("Adjectives", get_adjective(sentence1)), ("Adverb", get_adverb(sentence1))]
    structure_sentence2 = [("Second clause", sentence2), ("Verb", verb2), ("Tense", tense2.tense),
            ("Direct-Object", get_direct_object(sentence2)),
            ("Indirect-Object", get_dative(sentence2)),
            ("Prepositions", get_preposition(sentence2)),
            ("Adjectives", get_adjective(sentence2)), ("Adverb", get_adverb(sentence2))]
    return [('Sentence type', 'Compound sentence'), structure_sentence1, structure_sentence2]


class SentenceStructure:

    def __init__(self, nlp, text):
        self.sentence = text
        self.doc = nlp(self.sentence)
        self.sentence_structure = ""
        self.type_sentence = reported_speech_or_compound(self.doc)
        if self.type_sentence == 3:
            self.sentence_structure = get_reported_speech_structure(nlp, self.doc)
        elif self.type_sentence == 4:
            self.sentence_structure = get_compound_structure(nlp, self.doc)
        else:
            self.type_sentence = conditionnal_or_adv_clause(self.doc)
            if self.type_sentence == 2:
                self.sentence_structure = get_conditional_structure(nlp, self.doc)
            elif self.type_sentence == 5:
                self.sentence_structure = get_conditional_structure(nlp, self.doc)
            else:
                self.voice = passive_or_active_voice(self.doc)
                if self.voice == 0:
                    self.sentence_structure = get_active_voice_structure(nlp, self.doc)
                if self.voice == 1:
                    self.sentence_structure = get_passive_voice_structure(nlp, self.doc)
