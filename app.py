from surveys import Survey, Question, satisfaction_survey as survey
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def survey_start():
    """Starts the survey passing in the survey instance"""
    return render_template("base.html", survey=survey)

@app.route('/session', methods=['POST'])
def set_session():
    """Sets or resets the responses in session as a blank list"""
    session['responses'] = []
    return redirect('/questions/0')

@app.route(f'/questions/<num>')
def make_question(num):
    """Checks to see if all questions are answered or if URL matches current question, then renders current question"""
    question_number = len(session['responses'])

    if question_number == len(survey.questions):
        return redirect(f'/thank-you')

    if int(num) != question_number:
        flash("Don't cheat! You have to answer the questions in order.")
        return redirect(f'/questions/{question_number}')

    question = survey.questions[question_number]
    return render_template("question.html", question=question, question_number=question_number)

@app.route('/answer', methods=['POST'])
def add_answer():
    """Receives the answer from the submitted question and adds to session."""

    ans = request.form['answer']
    responses = session['responses']
    responses.append(ans)
    session['responses'] = responses

    question_number = len(responses)

    if question_number == len(survey.questions):
        return redirect(f'/thank-you')
    
    return redirect(f'/questions/{question_number}')

@app.route('/thank-you')
def survey_end():
    """Renders thank you page at end of survey and prints answers"""
    responses = session['responses']
    number_of_questions = len(responses)
    return render_template("end.html", questions=survey.questions, responses=responses, idx=number_of_questions)