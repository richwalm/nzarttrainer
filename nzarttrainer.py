#!/usr/bin/env python3
# NZART Exam Trainer
# Written by Richard Walmsley <richwalm+nzarttrainer@gmail.com> (ZL1RSW)

from flask import Flask, request, render_template, redirect, url_for, Response, abort

import random
import string

import json
import sys

app = Flask(__name__, static_folder = 's')

# Constants.
Needed = 40
MaxSeedSize = 32

# Load the database and ensure it's valid.
# Also create a cache for the answers.
with app.open_resource('questions.json') as InputFile:
    Data = json.load(InputFile)

Answers = []
Required = Total = 0
for Block in Data:
    if Block['RequiredAnswers'] > len(Block['Questions']):
        sys.exit(1)

    for Q in Block['Questions']:
        if Q['Answer'] > len(Q['Choices']):
            sys.exit(1)

        Answers.append(Q['Answer'])

    Required += Block['RequiredAnswers']
    Total += len(Block['Questions'])

if Required > Total:
    sys.exit(1)

# Common

def GenerateExam(Seed):
    """ Returns a list of questions for each block. """

    random.seed(Seed)

    Blocks = []

    for Block in Data:

        Indexes = []

        for I in range(Block['RequiredAnswers']):
            while True:
                R = random.randrange(len(Block['Questions']))
                if R not in Indexes:
                    break

            Indexes.append(R)

        Blocks.append(Indexes)

    return Blocks

def GenerateFullExam():
    """ Returns the entire exam. """

    Blocks = []
    for Block in Data:
        Indexes = list(range(len(Block['Questions'])))
        Blocks.append(Indexes)

    return Blocks

# Views

@app.errorhandler(404)
def PageNotFound(e):
    return render_template('404.html'), 404

@app.route('/')
def Index():
    return render_template('index.html', MaxSeedSize = MaxSeedSize, Total = Total)

@app.route('/exam', methods = [ 'GET', 'POST' ])
def Exam():

    AllQuestions = request.form.get('aq') or request.args.get('aq')
    if not AllQuestions:

        Seed = request.form.get('s') or request.args.get('s')
        if not Seed:
            if request.method == 'POST':
                abort(403)
            Seed = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(MaxSeedSize))
        else:
            Seed = Seed[:MaxSeedSize]

        Blocks = GenerateExam(Seed)
        T = Required

    else:

        Blocks = GenerateFullExam()
        Seed = None
        T = Total

    if request.method == 'POST':

        # Grading.
        BlockAnswers = []
        Offset = Correct = BlockIndex = 0
        for B in Blocks:
            BCorrect = 0

            for I in B:
                A = request.form.get(str(Offset + I))
                if A:
                    try:
                        A = int(A)
                    except Exception:
                        pass
                if A == Answers[Offset + I]:
                    Correct += 1
                    BCorrect += 1

            BlockAnswers.append(BCorrect)
            Offset += len(Data[BlockIndex]['Questions'])
            BlockIndex += 1

        return render_template('results.html', Seed = Seed, Blocks = Blocks, Data = Data, Needed = Needed, Correct = Correct, Answers = Answers, BlockAnswers = BlockAnswers, Total = T)

    return render_template('exam.html', Seed = Seed, Blocks = Blocks, Data = Data, Needed = Needed, Total = T)

"""
@app.route('/answer/<int:ID>')
def Answer(ID):
    if ID >= len(Answers):
        abort(404)
    return Response(str(Answers[ID]), mimetype='text/plain')
"""

if __name__ == '__main__':
    app.run(debug = False, host='0.0.0.0')

