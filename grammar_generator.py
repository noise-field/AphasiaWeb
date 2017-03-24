import pymorphy2
import sqlite3
import random
import logging
import os
import sys

DATA_PATH = "data"
CASE_TAGS = ["gent", "datv", "accs", "ablt", "loct"]
PATIENTDB_PATH = "patientdb.db"

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
        conn = sqlite3.connect(PATIENTDB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_markup, subjects_list FROM tasks;")
        try:
            for task in cursor:
                self.data[task[0]] = dict()
                buffer = list()
                self.data[task[0]]['tasks'] = dict()
                for line in task[1].strip().split("\n"):
                    line = line.strip()
                    if line != "":
                        buffer.append(line)
                    else:
                        self.data[task[0]]['tasks'][buffer[0]] = buffer[1:]
                        buffer = list()
                self.data[task[0]]['subjects'] = task[2].strip().split("\n")
        except Exception as e:
            logging.exception(e)
        finally:
            conn.close()
        # with open(os.path.join(DATA_PATH, "topic_index.txt"), encoding="utf-8") as index:
        #     for topic in index:
        #         topic = topic.strip()
        #         self.data[topic] = dict()
        #         with open(os.path.join(DATA_PATH, "{}.txt".format(topic)), encoding="utf-8") as topic_file:
        #             buffer = list()
        #             self.data[topic]['tasks'] = dict()
        #             for line in topic_file:
        #                 line = line.strip()
        #                 if line != "":
        #                     buffer.append(line)
        #                 else:
        #                     self.data[topic]['tasks'][buffer[0]] = buffer[1:]
        #                     buffer = list()
        #         with open(os.path.join(DATA_PATH, "{}_subjects.txt".format(topic)), encoding="utf-8") as subject_file:
        #             self.data[topic]['subjects'] = subject_file.read().strip().split("\n")
        logging.info(self.data)

    def __form_verb(self, verb):
        # Puts the given verb in Present Tense and 3rd person form
        return self.__morph.parse(verb)[0].inflect({'3per'}).word

    def inflect(self, noun, case="accs", adj=None):
        """
        Inflect the adjective-noun pair. Pass two pymorphy2 parse objects to this function
        :param noun: noun parse
        :param case: case to inflect
        :param adj: adjective parse
        :return:
        """
        try:
            cases = CASE_TAGS[:]
            cases.remove(case)
            answers = list()
            answer_cases = list()
            while cases:
                case = cases.pop(random.randint(0, len(cases) - 1))
                candidate = noun.inflect({case}).word
                if candidate not in answers and candidate != noun.word:
                    answers.append(candidate)
                    answer_cases.append(case)
                if len(answers) == 3:
                    break
            if adj is not None:
                for i in range(len(answers)):
                    answers[i] = "{} {}".format(adj.inflect({answer_cases[i]}).word, answers[i])
            if len(answers) < 3:
                answers = answers + ["-"] * (3 - len(answers))
            return answers
        except Exception as e:
            logging.error(str(sys.exc_info()[-1].tb_lineno) + ": " + str(e))
            raise e

    def generate_answers(self, right_answer):
        splitted = right_answer.split()
        # запомним правильный падеж для существительного
        if len(splitted) == 1:
            # только существительное в винительном падеже
            answer_case = "accs"
            answer_noun = right_answer
            parse = self.__morph.parse(answer_noun)[0]
            return [answer_noun] + self.inflect(parse)
        elif len(splitted) == 2:
            if splitted[-1] in CASE_TAGS:
                # существительное и падеж
                answer_case = splitted[-1]
                answer_noun = splitted[0]
                parse = self.__morph.parse(answer_noun)[0]
                return [answer_noun] + self.inflect(parse, answer_case)
            else:
                # существительное и прилагательное или существительное и предлог
                answer_case = "accs"
                answer_adj = splitted[0]
                answer_noun = splitted[1]
                noun_parse = self.__morph.parse(answer_noun)[0]
                adj_or_prep_parse = self.__morph.parse(answer_adj)[0]
                if 'PREP' in adj_or_prep_parse.tag:
                    return [answer_adj + " " + answer_noun] + [answer_adj + " " + inflected for inflected in
                                                               self.inflect(noun_parse)]
                else:
                    return [answer_adj + " " + answer_noun] + self.inflect(noun=noun_parse, adj=adj_or_prep_parse)
        elif len(splitted) == 3:
            if splitted[-1] in CASE_TAGS:
                answer_case = splitted[-1]
                answer_adj = splitted[0]
                answer_noun = splitted[1]
                noun_parse = self.__morph.parse(answer_noun)[0]
                adj_or_prep_parse = self.__morph.parse(answer_adj)[0]
                if 'PREP' in adj_or_prep_parse.tag:
                    return [answer_adj + " " + answer_noun] + [answer_adj + " " + inflected for inflected in
                                                               self.inflect(noun_parse, case=answer_case)]
                else:
                    return [answer_adj + " " + answer_noun] + self.inflect(noun=noun_parse, case=answer_case,
                                                                           adj=adj_or_prep_parse)
            else:
                answer_prep = splitted[0]
                answer_adj = splitted[1]
                answer_noun = splitted[2]
                adj_parse = self.__morph.parse(answer_adj)[0]
                noun_parse = self.__morph.parse(answer_noun)[0]
                return [right_answer] + ["{} {}".format(answer_prep, inflected) for inflected in
                                         self.inflect(noun=noun_parse, adj=adj_parse)]
        else:
            answer_prep = splitted[0]
            answer_adj = splitted[1]
            answer_noun = splitted[2]
            answer_case = splitted[3]
            adj_parse = self.__morph.parse(answer_adj)[0]
            noun_parse = self.__morph.parse(answer_noun)[0]
            return ["{} {} {}".format(answer_prep, answer_adj, answer_noun)] + \
                ["{} {}".format(answer_prep, inflected) for inflected in self.inflect(
                    noun=noun_parse, case=answer_case, adj=adj_parse
                )]

    def get_task(self, topic):
        task_verb = random.choice(list(self.data[topic]['tasks'].keys()))
        task_answer = random.choice(self.data[topic]['tasks'][task_verb])
        task_subject = random.choice(self.data[topic]['subjects'])
        return {"options": self.generate_answers(task_answer),
                "task": task_subject + " " + self.__form_verb(task_verb) + "________"}
        # return {"options": ["работу", "бороду", "постель", "клиентку"], "task": "Марина устраивается на ________."}
