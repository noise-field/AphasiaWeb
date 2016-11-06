import pymorphy2
import random
import os

DATA_PATH = "data"


class SingletonGenerator(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonGenerator, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TaskGenerator(metaclass=SingletonGenerator):
    def __init__(self):
        self.__morph = pymorphy2.MorphAnalyzer()
        self.data = dict()
        with open(os.path.join(DATA_PATH, "topic_index.txt"), encoding="utf-8") as index:
            for topic in index:
                topic = topic.strip()
                self.data[topic] = dict()
                with open(os.path.join(DATA_PATH, "{}.txt".format(topic)), encoding="utf-8") as topic_file:
                    buffer = list()
                    self.data[topic]['tasks'] = dict()
                    for line in topic_file:
                        line = line.strip()
                        if line != "":
                            buffer.append(line)
                        else:
                            self.data[topic]['tasks'][buffer[0]] = buffer[1:]
                            buffer = list()
        print(self.data)

    def __form_verb(self, verb):
        # Puts the given verb in Present Tense and 3rd person form
        return self.__morph.parse(verb)[0].inflect({'3per'}).word;

    def get_task(self, topic):
        task_verb = random.choice(list(self.data[topic]['tasks'].keys()))
        print(task_verb)
        task_answer = random.choice(self.data[topic]['tasks'][task_verb])
        print(task_answer)
        return {"options": [task_answer] * 4,
                "task": "Марина " + self.__form_verb(task_verb) + "________"}
        # return {"options": ["работу", "бороду", "постель", "клиентку"], "task": "Марина устраивается на ________."}
