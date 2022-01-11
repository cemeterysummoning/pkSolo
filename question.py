import requests, re, bs4
from selenium import webdriver
from selenium.webdriver.support.ui import Select

import sys
import tkinter as tk
import customtkinter as ctk

from pprint import pprint

def get_html():
    window = webdriver.Firefox(executable_path="/home/ace/geckodriver")
    window.get('https://www.quizdb.org')

    userin = input()
    if userin == "go":
        html = window.page_source
        with open("html.txt", "w") as ptext:
            ptext.write(html)

    window.close()

def get_txt():
    qs = []
    page = bs4.BeautifulSoup(open("html.txt"), features="html.parser")
    for i in page.find_all("div", {"class": "question"}):
        content = i.find("div", {"class": "question-content"})
        txt = content.getText()
        txt = txt.replace("Search for this answerline, with no filtersSearch for this answerline, with the same filters", "")
        qs.append(txt)
    return qs

def parse_txt(qs, mode):
    q_dict = {}
    if mode == "bonus":
        
        qs = [i.split('[10]') for i in qs]
        for i in qs:

            con = '\n'.join(i[:2])

            del i[0]
            i[0] = con

        qs = [j for sub in qs for j in sub]

        for i in qs:
            temp = i.split('ANSWER:')
            q = temp[0].strip()
            a = temp[1].strip()
            
            q_dict[a] = q

            
        return q_dict

    else:
        for i in qs:
            temp = i.split('ANSWER: ')
            q_dict[temp[1]] = temp[0]
    
    return q_dict

def ask(q_dict, mode):
    answer_re = r'\[(.+)\]'
    answer_re2 = r'<.+>'
    answer_re3 = r'\(.+\)'
    score = 0
    if mode == "bonus":
        for answer, question in q_dict.items():
            print(question)

            answerin = input().lower()
            answer = re.sub(answer_re, '', answer)
            answer = re.sub(answer_re2, '', answer)
            answer = re.sub(answer_re3, '', answer)
            answer = answer.strip()
            threshold = len(answer) / 3
            
            if answerin == answer.lower():
                score += 10
                print("correct")
            elif answerin in answer.lower() and len(answerin) >= threshold:
                score += 10
                print("correct")
            else:
                print("incorrect, answer is " + answer)

    elif mode == "answer":
        for answer, question in q_dict.items():
            temp = question.split("(*)")
            print(*temp)
            answerin = input().lower()
            answer = re.sub(answer_re, '', answer)
            answer = re.sub(answer_re2, '', answer)
            answer = re.sub(answer_re3, '', answer)
            answer = answer.strip()

            threshold = len(answer) / 3




# get_html()
# qs = get_txt()
# q_dict = parse_txt(qs, "bonus")
# ask(q_dict, "bonus")
def button_function():
    print("pressed")

class Question:
    def __init__(self, question, answer):
        self.contents = question
        self.answer = answer

class MainGame:
    def __init__(self):
        self.question_set = self.get_qs()
        self.score = 0
        self.question_index = -1

    def get_qs(self):
        self.qs = get_txt()
        if '[10]' in self.qs[0]:
            self.dict_q = parse_txt(self.qs, "bonus")
        else:
            self.dict_q = parse_txt(self.qs, "tossup")

        self.question_list = []
        for answer, question in self.dict_q.items():
            self.question_list.append(Question(question, answer.strip()))

        return self.question_list
    def has_next(self):
        return self.question_index < len(self.question_set)
    
    def next(self):
        self.current = self.question_set[self.question_index]

        self.question_index += 1

        return self.current

    def verify(self, answerin):
        
        correct = self.question_set[self.question_index].answer
        threshold = len(correct) / 10

        if answerin.lower() == correct.lower():
            self.score += 10
            return True
        if answerin.lower() in correct.lower() and len(answerin) >= 3:
            self.score += 10
            return True
        else:
            return False

    def get_score(self):
        return self.score


# pprint(qs[0])
