from flask import Flask, render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hexaco', methods=['GET', 'POST'])
def hexaco():
    form = HexacoLoginForm()
    if form.validate_on_submit():
        if form.password.data == 'cognitiveload':
            session['validated'] = True
            return redirect(url_for('hexaco_questions', question_number=1))
        else:
            flash('Invalid code.')
    return render_template('hexaco.html', form=form)


@app.route('/hexaco/<int:question_number>', methods=['GET', 'POST'])
def hexaco_questions(question_number):
    print('MARTIN1')
    if question_number > len(QUESTIONS):
        print('MARTIN2')
        return redirect(url_for('hexaco_answers'))
    print('MARTIN3')
    form = HexacoQuestionForm()
    if form.validate_on_submit():
        for i, button in enumerate([form.one, form.two, form.three, form.four, form.five]):
            if button.data:
                session['answer_{}'.format(question_number)] = i + 1
                break
        return redirect(url_for('hexaco_questions', question_number=question_number + 1))

    question = QUESTIONS[question_number]
    return render_template('hexaco_questions.html', question=question, form=form)


@app.route('/hexaco/answers')
def hexaco_answers():
    return render_template('hexaco_answers.html')


class HexacoLoginForm(Form):
    password = PasswordField('Code', validators=[DataRequired()])
    submit = SubmitField('Start')


class HexacoQuestionForm(Form):
    one = SubmitField(label='se močno ne strinjam')
    two = SubmitField(label='se ne strinjam')
    three = SubmitField(label='sem nevtralen')
    four = SubmitField(label='se strinjam')
    five = SubmitField(label='se močno strinjam')

QUESTIONS = {
    1: 'Kako si?',
    2: 'Kaksno je vreme?',
    3: 'Kaksne barve je sonce?',
}

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
