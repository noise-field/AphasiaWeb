import pymorphy2
import random


class SingletonGenerator(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonGenerator, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Generator(metaclass=SingletonGenerator):
    def __init__(self):
        self.__morph = pymorphy2.MorphAnalyzer()

    def getRandom(self, seed):
        # Generates a full task
        name = random.choice(self.__names)
        verb = random.choice(self.__verbs)
        tail = random.choice(self.__tails[verb])
        new_tail = self.__getTail(tail, seed)
        return {'task' : name + ' ' + self.__formVerb(verb) + ' ' + new_tail[0], 'options' : new_tail[1]}
