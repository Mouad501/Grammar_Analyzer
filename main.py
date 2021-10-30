# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code. Press Double
# Shift to search everywhere for classes, files, tool windows, actions,
# and settings.
import sentencizer as s
import SentenceStructure as struct
import spacy

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    text = ""

    my_sentencizer = s.Sentencizer(text)
    sentences = my_sentencizer.sentences
        
    """
    sentences = ["I am worried that the snow storm will be severe",
                 "She is uncertain whether she made the right decision.",
                 "It was very obvious that this was the murder weapon.",
                 "Although Nicholas was tired, he stayed awake to finish his report.",
                 "If you didn't wash the dishes, you will be in trouble.",
                 "She said that she was living in London.",
                 "She said that she had bought a car",
                 "She said that she had been walking along the street",
                 "She said that she must study at the weekend",
                 "She asked me where I lived",
                 "She asked me who that fantastic man had been",
                 "He told the child to go to bed",
                 "He explained that he had just turned out the light.",
                 "They told me that they had been living in Paris.",
                 "He says he has missed the train",
                 "the church had been built in 1915",
                 "The Mona Lisa was painted by Leonardo Da Vinci.",
                 "The form can be obtained from the post office",
                 "John threw Steve the ball.",
                 "Darius bought a car for her.",
                 "The teacher gave some homework to the class.",
                 "John brought some flowers for Mary.",
                 "James built Marie a tiny house on the beach."]

    nlp = spacy.load("en_core_web_lg")

    i = 0
    for s in sentences:
        i = i + 1
        print("sentence %d: %s" % (i, s))
        structure = struct.SentenceStructure(nlp, s)
        print(structure.sentence_structure)
        """try:
            print(structure.sentence_structure)
            print(structure.verb_phrase_tense)
        except:
            print("not in grammar")"""
