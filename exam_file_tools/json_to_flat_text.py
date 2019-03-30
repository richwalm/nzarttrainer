#!/usr/bin/env python3
# Convert questions to flat text format for an Anki import.

import json

Sep = '\t'   # Never used.

InputFile = open('questions.json')
Data = json.load(InputFile)
InputFile.close()

TagTranslate = str.maketrans(' ', '_', '\',')

OutputFile = open('output.txt', 'w', encoding = 'utf-8')

for Block in Data:
    Title = Block['Title']
    # Covert the title to a tag.
    Tag = Title.lower().translate(TagTranslate)

    Questions = Block['Questions']
    for Question in Questions:
        QString = Question['Question']
        Answer = Question['Answer']
        AString = Question['Choices'][Answer]
        Image = Question.get('Image')

        if Image:
            ImageHTML = '<img src="{}"><br>'.format(Image)
            QString = ImageHTML + QString

        Output = [QString, AString, Tag]
        OutputLine = Sep.join(Output) + '\n'
        OutputFile.write(OutputLine)

OutputFile.close()

