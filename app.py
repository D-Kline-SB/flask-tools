from pickletools import StackObject
from random import choices
import re
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)
app.config['SECRET_KEY'] = "toolbarsecretkey"

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def startpage ():
    """ Shows user the title of the survey, the instructions, and a button to start the survey. """
    surveyname= survey.title
    surveyinstructions = survey.instructions
    return render_template ("landing.html", surveyname=surveyname, surveyinstructions=surveyinstructions)

questionNumber = 0

@app.route("/questions/<int:qid>")
def questionhandler (qid):
    """ Handles Questions"""
    if (qid is None):
        qid = 0
    else:
        qid = len(responses)
    questions = survey.questions[qid]
    print(questions.question)
    # choices = satisfaction_survey.questions.choices
    return render_template("questions.html", question=questions)



@app.route("/answer", methods =["POST"])
def answerhandler ():
    """ Handles Answers """
    questionResponse = request.form['answer']
    responses.append(questionResponse)
    print(responses)
    print(len(survey.questions))
    print(len(responses))
    if (len(responses) == len(survey.questions)):
        return redirect("/thanks")
    else : 
        return redirect(f"/questions/{len(responses)}")

@app.route("/thanks")
def thankshandler ():
    return render_template("thanks.html")
