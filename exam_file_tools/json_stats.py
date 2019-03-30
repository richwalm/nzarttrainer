#!/usr/bin/env python3
# Quick script to obtain some interesting stats from the questions.

import json

InputFile = open('questions.json')
Data = json.load(InputFile)
InputFile.close()

Total = 0
for Block in Data:
    Total += len(Block['Questions'])

Choices = [0] * 4

for Block in Data:
    Title = Block['Title']
    Required = Block['RequiredAnswers']
    Questions = Block['Questions']

    print('=== {} ==='.format(Title))
    print('Requires {} of {} ({}%).'.format(Required, len(Questions), Required / len(Questions)))
    print('{}% of total.'.format(Required / Total))
    print()

    SelectionChoices = [0] * 4

    for Question in Questions:
        Answer = Question['Answer']
        SelectionChoices[Answer] += 1
        Choices[Answer] += 1

    for Choice in range(len(Choices)):
        print('{}: {}. ({}%)'.format(Choice, SelectionChoices[Choice], SelectionChoices[Choice] / len(Questions)))

    print()

print('=== OVERALL ===')

for Choice in range(len(Choices)):
    print('{}: {}. ({}%)'.format(Choice, Choices[Choice], Choices[Choice] / len(Questions)))

