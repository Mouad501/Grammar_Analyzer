"""
Tense Analyzer is class that analyse and extract the english tense from a verb
phrase using rule based approach based on part-of-speech
"""
import spacy


class TenseAnalyser:

    def __init__(self, nlp, text, voice):
        self.verb_phrase = text
        self.voice = voice
        self.doc = nlp(self.verb_phrase)
        self.struct = self.struct()
        if self.voice == 0:
            self.tense = self.find_tense()
        if self.voice == 1:
            self.tense = self.find_passive_tense()

    def struct(self):
        structure = ""
        for token in self.doc:
            if token.tag_ == "VBP" or token.tag_ == "VBZ":
                if token.lemma_ == "be":
                    structure = " ".join((structure, "be_present"))
                elif token.lemma_ == "have":
                    structure = " ".join((structure, "have_present"))
                else:
                    structure = " ".join((structure, "present"))
            if token.tag_ == "VBD":
                if token.lemma_ == "be":
                    structure = " ".join((structure, "be_past"))
                elif token.lemma_ == "have":
                    structure = " ".join((structure, "have_past"))
                else:
                    structure = " ".join((structure, "past"))
            if token.tag_ == "VBN":
                if token.lemma_ == "be":
                    structure = " ".join((structure, "be_past_participle"))
                elif token.lemma_ == "have":
                    structure = " ".join((structure, "have_past_participle"))
                else:
                    structure = " ".join((structure, "past_participle"))
            if token.tag_ == "VB":
                if token.lemma_ == "be":
                    structure = " ".join((structure, "be"))
                elif token.lemma_ == "have":
                    structure = " ".join((structure, "have"))
                else:
                    structure = " ".join((structure, "v_base"))
            if token.tag_ == "VBG":
                structure = " ".join((structure, "v_ing"))
            if token.lemma_ == "will" or token.lemma_ == "wo" \
                    or token.lemma_ == "'ll":
                structure = " ".join((structure, "will"))
            if token.lemma_ == "would":
                structure = " ".join((structure, "would"))
            if token.tag_ == "MD" and token.lemma_ != "will" \
                    and token.lemma_ != "wo" and token.lemma_ != "'ll" \
                    and token.lemma_ != "would":
                structure = " ".join((structure, "modal"))
        return structure

    def find_tense(self):
        structure = self.struct
        if structure == " present" or structure == " be_present" \
                or structure == " have_present":
            return "Simple present tense"
        if structure == " past" or structure == " be_past" \
                or structure == " have_past":
            return "Simple past tense"
        if structure == " will v_base" or structure == " will be" \
                or structure == " will have":
            return "Simple future tense"
        if structure == " have_present past_participle" \
                or structure == " have_present have_past_participle" \
                or structure == " have_present be_past_participle":
            return "Present prefect tense"
        if structure == " have_past past_participle" \
                or structure == " have_past have_past_participle" \
                or structure == " have_past be_past_participle":
            return "Past prefect tense"
        if structure == " will have past_participle" \
                or structure == " will have have_past_participle" \
                or structure == " will have be_past_participle":
            return "Future prefect tense"
        if structure == " be_present v_ing":
            return "Present continuous tense"
        if structure == " be_past v_ing":
            return "Past continuous tense"
        if structure == " will be v_ing":
            return "Future continuous tense"
        if structure == " have_past be_past_participle v_ing":
            return "Past perfect continuous tense"
        if structure == " have_present be_past_participle v_ing":
            return "Present perfect continuous tense"
        if structure == " will have be_past_participle v_ing":
            return "Future perfect continuous tense"
        if structure == " modal v_base" or structure == " modal be" \
                or structure == " modal have":
            return "Modal verb"
        if structure == " v_base" or structure == " have":
            return "Simple present tense"
        if structure == " would v_base" or structure == " would be" or \
                structure == " would have":
            return "Conditional present"
        if structure == " would have past_participle" or \
                structure == " would have be_past_participle" or \
                structure == " would have have_past_participle":
            return "Conditional perfect"
        if structure == " would have be_past_participle v_ing":
            return "Conditional perfect progressive"
        if structure == " would be v_ing":
            return "Conditional present progressive"

    def find_passive_tense(self):
        structure = self.struct
        if structure == " be_present past_participle":
            return "Present indefinit tense (Passive)"
        if structure == " be_past past_participle":
            return "Past indefinit tense (Passive)"
        if structure == " be_present being past_participle":
            return "Present Continuous tense (Passive)"
        if structure == " be_past being past_participle":
            return "Past Continuous tense (Passive)"
        if structure == " have_present be_past_participle past_participle":
            return "Present perfect tense (Passive)"
        if structure == " have_past be_past_participle past_participle":
            return "Past perfect tense (Passive)"
        if structure == " will be past_participle":
            return "Future indefinit tense (Passive)"
        if structure == " will have be_past_participle past_participle":
            return "Future perfect tense (Passive)"
