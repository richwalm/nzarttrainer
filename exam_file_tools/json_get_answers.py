#!/usr/bin/env python3
# Dumps the correct answers for use for real-time grading within 'exam.js'.

import json

InputFile = open('questions.json')
Data = json.load(InputFile)
InputFile.close()

Answers = []

for Block in Data:
    for Question in Block['Questions']:
        Answers.append(Question['Answer'])

print(Answers)
