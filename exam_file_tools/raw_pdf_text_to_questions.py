#!/usr/bin/python3
# A simple script to convert the raw text from the NZART PDFs into a questions.json.
# PDFs can be found here; https://nzart.org.nz/learn/study-guides/
# Images need to be performed manually, though.

# There was one part of the input that needed manually adjustment however.
import sys
import re
from enum import Enum, auto
import json

class ParseState(Enum):
    NEW_QUESTION = auto()
    CHOICES = auto()

class RawExamFile:
    def _PushLine(self, Line):
        self._Lines.insert(0, Line)

    def _GetLine(self):
        while True:
            if self._Lines:
                Line = self._Lines.pop()
            else:
                Line = self.File.readline()
            if not Line:    # EOF. Should always contain a newline.
                return

            if not Line.strip():    # Skip empty lines.
                continue

            if Line.startswith('© NZART 2025'): # Footer/header.
                # Next line should be just a number.
                Next = self.File.readline()
                try:
                    int(Next)
                except ValueError:
                    raise Exception('Next line after header wasn''t an expected number; ''{}'''.format(Next))
                continue

            return Line.replace('\r', '')

    def _GetUntilMatch(self, Match, InitialLine):
        # Keep filling a buffer until a line matches a match.
        #Full = InitialLine[:-1]
        Full = [InitialLine.strip()]
        while True:
            Line = self._GetLine()
            if re.match(Match, Line):
                self._PushLine(Line)    # Push back to FIFO.
                break
            Full.append(Line.strip())
        return ' '.join(Full)

    def _EndBlock(self):
        if self.Block:
            self.Block['Questions'] = self.Questions
            self.Questions = []
            self.Blocks.append(self.Block)
            #print(self.Block['ID'], self.Block['Name'])
            self.Block = {}

    def _HandleNewQuestionFile(self, InitialLine):
        Full = self._GetUntilMatch(r'1\. ', InitialLine)

        self._EndBlock()

        Matches = re.match(r'Question File: (\d+)\. ([A-Za-z\',& ]+): \((\d+) questions?\)', Full)
        if not Matches:
            raise Exception('Not an excepted Question File line; {}'.format(Full))

        # Do some basic order checking.
        ID = int(Matches[1])
        if ID != len(self.Blocks) + 1:
            raise Exception('Question file ID not in correct order; {} != {}'.format(ID, len(self.Blocks) + 1))

        self.Block['Title'] = Matches[2]
        self.Block['RequiredAnswers'] = int(Matches[3])

    def _HandleNewQuestion(self, InitialLine):
        Full = self._GetUntilMatch(r'[a-z]\. ', InitialLine)

        if self.Question:
            raise Exception('Still had a pending question when starting a new one; {}'.format(self.Question))

        Matches = re.match(r'(\d+)\.? ', Full)
        Number = int(Matches[1])
        if Number != len(self.Questions) + 1:
            raise Exception('Question ID isn''t in order; {} != {}'.format(Number, len(self.Questions) + 1))

        self.Question['Question'] = Full[Matches.end():]
        self.State = ParseState.CHOICES

    def _HandleAnswerLine(self, InitialLine):
        Matches = re.match(r'=+\s+Answer is\s+([A-Z])\s+=+', InitialLine)

        Letter = Matches[1].lower()
        Number = ord(Letter) - ord('a')

        if Number >= len(self.Choices):
            raise Exception('Answer choice is out of range; {} != {}'.format(Number, len(self.Choices)))

        # Finished.
        self.Question['Answer'] = Number
        self.Question['Choices'] = self.Choices
        self.Choices = []

        self.Questions.append(self.Question)
        self.Question = {}

        self.State = ParseState.NEW_QUESTION

    def _HandleChoiceLine(self, InitialLine):
        Full = self._GetUntilMatch(r'([a-z]\. |=+)', InitialLine)

        Matches = re.match(r'([a-z])\. ', Full)
        Letter = Matches[1]
        Number = ord(Letter) - ord('a')
        if Number != len(self.Choices):
            raise Exception('Wrong letter order for choice; {} != {}'.format(Number, len(self.Choices)))

        self.Choices.append(Full[Matches.end():])

    def _HandleLine(self):
        Line = self._GetLine()
        if not Line:
            return True

        if self.State == ParseState.NEW_QUESTION:
            if Line.startswith('Question File'):
                self._HandleNewQuestionFile(Line)
            else:
                Matches = re.match(r'\d+\.? ', Line)
                if not Matches:
                    raise Exception('Didn''t get an expected new question line; {}'.format(Line))
                self._HandleNewQuestion(Line)
        elif self.State == ParseState.CHOICES:
            Matches = re.match(r'=+\s+Answer is', Line)
            if Matches:
                self._HandleAnswerLine(Line)
            else:
                self._HandleChoiceLine(Line)

        return False

    def _Process(self):
        while True:
            End = self._HandleLine()
            if End:
                break
        self._EndBlock()
        return self.Blocks

    def __init__(self, File):
        self.File = File
        self._Lines = [] # Before the buffer.
        self.State = ParseState.NEW_QUESTION
        self.Block = {}
        self.Blocks = []
        self.Questions = []
        self.Question = {}
        self.Choices = []

if len(sys.argv) < 2:
    print('Usage: {} InputFile'.format(sys.argv[0]), file = sys.stderr)
    sys.exit(2)
Input = sys.argv[1]
Output = 'questions.json'
with open(Input) as Input:
    R = RawExamFile(Input)
    Data = R._Process()
    with open(Output, 'w') as Output:
        json.dump(Data, Output, indent = 4)
