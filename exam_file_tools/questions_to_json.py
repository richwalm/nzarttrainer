#!/usr/bin/env python3
# NZART Examination Questions to JSON Convertor
# Written by Richard Walmsley <richwalm+nzarttrainer@gmail.com> (ZL1RSW)

import sys
import json
from html.parser import HTMLParser

class TextAndImageExtractor(HTMLParser):

    def __init__(self):
        self.__Text = ''
        self.__Images = []
        HTMLParser.__init__(self)

    def handle_starttag(self, Tag, Attrs):
        if Tag == 'img':
            for Attr in Attrs:
                if Attr[0] == 'src':
                    self.__Images.append(Attr[1])

    def handle_data(self, Data):
        self.__Text += Data

    @property
    def Text(self):
        return self.__Text
    @property
    def Images(self):
        return self.__Images

def MakeQuestion(Fields, Answer, LineNumber):
    """ Returns a question dict from what we have. """

    if not Fields:
        return None

    if not Answer:
        print('Warning! Question block ending on line #{} is missing an answer.'.format(LineNumber), file = sys.stderr)
        return None

    Question = {}

    Choices = Fields[1:]
    if not Choices:
        print('Warning! Question block ending on line #{} is missing choices.'.format(LineNumber), file = sys.stderr)
        return None

    Answer -= 1
    if Answer < 0 or Answer > len(Choices):
        print('Warning! Question block ending on line #{} has an invalid choice.'.format(LineNumber), file = sys.stderr)
        return None

    Question['Choices'] = Choices
    Question['Answer'] = Answer

    # Strip out any HTML tags and record image.
    try:
        Parser = TextAndImageExtractor()
        Parser.feed(Fields[0])
        if not Parser.Text:
            raise ValueError
    except Exception:
        print('Error! Failed to parse text and images from question in question block ending on line #{}.'.format(LineNumber), file = sys.stderr)
        return None

    Question['Question'] = Parser.Text.strip()  # Stripping tags may cause padding.

    if Parser.Images:
        if len(Parser.Images) > 1:
            print('Error! Question in question block ending on line #{} has mutiple images.'.format(LineNumber), file = sys.stderr)
            return None
        Question['Image'] = Parser.Images[0]

    return Question

def ParseQuestionFile(Filename, QuestionPrefix):
    """ Parses a question file. """

    File = open(Filename, encoding = 'cp1252')

    Questions = []

    Fields = []
    Answer = None
    Data = ''

    Start = False   # One file 'N5.TXT' has its third line missing a comment so we'll use this to avoid the warning.

    TitleLine = None
    Title = None

    LineNumber = 0
    for Line in File:
        LineNumber += 1

        # Comments.
        if Line.startswith('%'):

            # Title handling.
            if not Title:
                if not TitleLine:
                    Line = Line.split(maxsplit = 2)
                    if len(Line) > 1 and Line[1] == 'FILENAME':
                        TitleLine = LineNumber + 1
                elif TitleLine == LineNumber:
                    Line = Line.split(maxsplit = 1)
                    if len(Line) > 1:
                        Title = Line[-1].rstrip()

            # Seems like the answer is stored within a comment so we'll attempt to extract it.
            elif Start:
                Line = Line.split()
                if len(Line) > 2 and Line[1] == 'ans':
                    Ans = None
                    try:
                        Ans = int(Line[2])
                    except Exception:
                        pass
                    if Ans:
                        Answer = Ans

            continue

        # If empty line, flush the field we have.
        if not Line or Line.isspace():
            if Data:
                Fields.append(Data)
                Data = ''
            continue

        # Anything else, we'll collect.

        # Is this a question?
        if not Data and Line.startswith(QuestionPrefix):
            Start = True
            
            # Crop the first word.
            Line = Line.split(maxsplit = 1)
            Line = Line[-1]

            # Flush the previous question.
            Question = MakeQuestion(Fields, Answer, LineNumber)
            if Question:
                Questions.append(Question)
            Answer = None
            Fields = []

        if Start:
            if Data:
                Data += ' '
            Data += Line.strip()

    File.close()

    # In case there is no newline at end of file, flush everything.
    if Data:
        Fields.append(Data)
    Question = MakeQuestion(Fields, Answer, LineNumber)
    if Question:
        Questions.append(Question)

    return Questions, Title

if __name__ == '__main__':
    ParmsFilename = 'PARAMS'

    try:
        ParmsFile = open(ParmsFilename, encoding = 'cp1252')
    except Exception as E:
        print('Failed to open \'{}\' file; {}'.format(ParmsFilename, E), file = sys.stderr)
        sys.exit(1)

    Start = False
    QuestionFiles = []

    # Load the parms file.
    LineNumber = 0
    for Line in ParmsFile:
        LineNumber += 1

        if Line.startswith('%') or (Line and Line.isspace()):    # Comment
            continue

        if Line.startswith('-') and 'parameters start' in Line:
            Start = True
            continue

        # Here's the actual data.
        Data = Line.split()
        if len(Data) != 4:
            print('Data on line #{} has missing/extra data.'.format(LineNumber), file = sys.stderr)
            ParmsFile.close()
            sys.exit(1)

        # Basic error checking.
        try:
            Data[2] = int(Data[2])
            Data[3] = int(Data[3])
        except Exception as E:
            print('Data on line #{} isn\'t expected intergers; {}'.format(LineNumber, E), file = sys.stderr)
            ParmsFile.close()
            sys.exit(1)

        Data = tuple(Data)
        QuestionFiles.append(Data)

    ParmsFile.close()

    # Load the question files.
    Blocks = []
    for File in QuestionFiles:

        # Parse.
        try:
            Questions, Title = ParseQuestionFile(File[0].upper(), File[1])
        except Exception as E:
            print('Failed to prase question file {}; {}'.format(File[0], E), file = sys.stderr)
            sys.exit(1)

        Parms = {}

        Parms['Title'] = Title
        Parms['RequiredAnswers'] = File[3]
        Parms['Questions'] = Questions

        if len(Questions) != File[2]:
            print('Warning! File \'{}\' has {} questions. Expected {}.'.format(File[0], len(Questions), File[2]), file = sys.stderr)
        if File[3] > len(Questions):
            print('Warning! File \'{}\' has requires more answers ({}) then there are questions ({}).'.format(File[0], File[3], len(Questions)), file = sys.stderr)

        Blocks.append(Parms)

    # Dump everything.
    try:
        Output = open('questions.json', 'w')
        json.dump(Blocks, Output, indent = 4)
    except Exception as E:
        print('Failed to write output file \'{}\'; {}'.format(OutputFilename, E), file = sys.stderr)
        sys.exit(1)

    Output.close()
