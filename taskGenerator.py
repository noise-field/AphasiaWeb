import os, re
import xml.etree.ElementTree as ET
import gensim.models.word2vec as vec
import pymorphy2
import random

class TaskGenerator:
    def __get_sentences(self, filename):
        # Load all sentences from a ruscorpora file in a list
        tree = ET.parse(filename)
        root = tree.getroot()
        result = []
        body = root[1]
        for paragraph in body:
            for sentence in paragraph:
                appending = []
                for word in sentence:
                    if len(word):
                        if word[0].tail:
                            appending.append(word[0].tail.replace('`', ''))
                result.append(appending)
        return result

    def __sentences(self, folder):
        # Merge all sentences from all files
        result = []
        for directory, _, filenames in os.walk(folder):
            for filename in filenames:
                try:
                    path = os.path.join(directory, filename)
                    result += self.__get_sentences(path)
                except:
                    pass
        return result

    def __init__(self, subject_file, tail_file):
        # Create pymorphy and word2vec objects, loading names and tails
        self.__morph = pymorphy2.MorphAnalyzer()
        self.__model = vec.Word2Vec.load('word2vec')

    def __formVerb(self, verb):
        # Puts the given verb in Present Tense and 3rd person form
        return self.__morph.parse(verb)[0].inflect({'3per'}).word;

    def __isBad(self, tag):
        # Check whether the word is a name, surname, etc.
        bad_tags = {'Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Orgn', 'Trad'}
        for bad_tag in bad_tags:
            if {bad_tag} in tag:
                return True
        return False

    def __getTail(self, tail, seed):
        # Generates the tail and a task
        split_tail = tail[0].split()
        noun = split_tail[-1]
        case = tail[1]
        number = ''
        gender = ''

        for row in self.__morph.parse(noun):
            if self.__isBad(row.tag):
                continue
            if {'NOUN', case} in row.tag:
                number = row.tag.number
                gender = row.tag.gender

        far_off = self.__model.most_similar(negative=[noun], topn=seed)
        new_nouns = []

        for word, _ in far_off:
            if not re.search('^[а-я]*$', word):
                continue
            for row in self.__morph.parse(word)[:3]:
                if row.tag.POS in ['ADJF', 'NUMR']:
                    break
                if self.__isBad(row.tag):
                    continue
                if gender and {'NOUN', gender} in row.tag:
                    new_nouns.append(row)

        result = [row.inflect({case, number}).word for row in new_nouns if row.inflect({case, number})]
        result = list(set(result))
        random.shuffle(result)
        result = [noun] + result[:3]
        return (' '.join(split_tail[:-1]) + ' ________.', result)

    def changeTopic(self, topic):
        print(topic)
        self.__names = []
        cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']

        with open(topic + '_subjects.txt', 'r', encoding='utf-8') as subjects:
            for name in subjects:
                self.__names.append(name.strip())

        self.__tails = dict()
        self.__verbs = []
        verb = ''
        with open(topic + '.txt', 'r', encoding='utf-8') as tails:
            for tail in tails:
                if not verb:
                    verb = tail.strip()
                    self.__verbs.append(verb)
                    self.__tails[verb] = []
                elif not tail.strip():
                    verb = ''
                else:
                    stripped_tail = tail.strip().split()
                    if stripped_tail[-1] not in cases:
                        self.__tails[verb].append((tail, 'accs'))
                    else:
                        self.__tails[verb].append((' '.join(stripped_tail[:-1]), stripped_tail[-1]))

    def getRandom(self, seed):
        # Generates a full task
        name = random.choice(self.__names)
        verb = random.choice(self.__verbs)
        tail = random.choice(self.__tails[verb])
        new_tail = self.__getTail(tail, seed)
        return {'task' : name + ' ' + self.__formVerb(verb) + ' ' + new_tail[0], 'options' : new_tail[1]}