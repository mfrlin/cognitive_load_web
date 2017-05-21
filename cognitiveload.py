from flask import Flask, render_template, session, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
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
    if question_number > len(QUESTIONS):
        return redirect(url_for('hexaco_answers'))
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
    1: 'Če bi obiskal umetnostno galerijo, bi se precej dolgočasil.',
    2: 'Da bi se izognil hitenju zadnjo minuto, planiram in organiziram stvari vnaprej.',
    3: 'Redko zamerim, tudi ljudem, ki so mi naredili hudo krivico.',
    4: 'Celostno gledano, sem kar zadovoljen sam s sabo.',
    5: 'Strah bi me bilo potovati v slabih vremenskih razmerah.',
    6: 'Tudi če bi mislil, da bo laskanje pomagalo, ga ne bi uporabil za to, da bi v službi napredoval ali dobil povišico.',
    7: 'Zanima me učenje o zgodovini in politiki drugih držav.',
    8: 'Pogosto se močno priganjam, ko skušam doseči nek cilj.',
    9: 'Ljudje včasih pravijo, da sem preveč kritičen do drugih.',
    10: 'Na skupinskih srečanjih redko izrazim svoja mnenja.',
    11: 'Včasih ne morem nehati biti zaskrbljen za malenkosti.',
    12: 'Če bi vedel, da me ne bodo ujeli, bi bil pripravljen ukrasti milijon evrov.',
    13: 'Užival bi v ustvarjanju umetniškega dela, npr. romana, pesmi, slike.',
    14: 'Ko na nečem delam, ne posvečam veliko pozornosti majhnim podrobnostim.',
    15: 'Ljudje včasih pravijo, da sem preveč trmast.',
    16: 'Raje imam dela, ki vključujejo aktivno interakcijo z drugimi ljudmi, kot samostojno delo.',
    17: 'Ko mi je težko ob boleči izkušnji, potrebujem nekoga, da se ob njem bolje počutim.',
    18: 'Ni mi posebej pomembno imeti mnogo denarja.',
    19: 'Mislim, da je posvečanje pozornosti radikalnim idejam potrata časa.',
    20: 'Odločtive sprejemam bolj po občutku, kot po pazljivem razmisleku.',
    21: 'Ljudje menijo, da sem vzkipljiva oseba.',
    22: 'Večino dni sem dobro razpoložen in optimističen.',
    23: 'Na jok mi gre, kadar vidim druge jokati.',
    24: 'Menim, da si zaslužim več spoštovanja kot povprečna oseba.',
    25: 'Če bi imel priložnost, bi šel na koncert klasične glasbe.',
    26: 'Ko delam, imam včasih težave zaradi svoje neorganiziranosti.',
    27: 'Moj odnos do ljudi, ki so z mano slabo ravnali, je &quot;odpusti in pozabi&quot;.',
    28: 'Čutim, da sem nepriljubljena oseba.',
    29: 'Fizičnih nevarnosti se zelo bojim.',
    30: 'Če hočem nekaj od osebe, se bom smejal njenim najslabšim šalam.',
    31: 'Prebiranje enciklopedije me nikoli ni posebej zabavalo.',
    32: 'Opravim le toliko dela, kolikor je nujno potrebno.',
    33: 'Pri presojanju drugih sem nagnjen k tolerantnosti.',
    34: 'V družabnih situacijah navadno jaz naredim prvo potezo.',
    35: 'Skrbi me mnogo manj kot druge ljudi.',
    36: 'Nikoli ne bi sprejel podkupnine, tudi če bi bila zelo visoka.',
    37: 'Ljudje so mi že velikokrat rekli, da sem poln domišljije.',
    38: 'Pri delu se vedno trudim biti natančen, tudi če zaradi tega porabim več časa.',
    39: 'Ko se ljudje z mano ne strinjajo, sem ponavadi kar fleksibilen glede svojih mnenj.',
    40: 'Ko pridem v novo okolje, vedno najprej poiščem nove prijatelje.',
    41: 'S težkimi situacijami dobro upravljam, ne da bi pri tem potreboval čustveno oporo druge osebe.',
    42: 'Užival bi, če bi posedoval drage, luksuzne dobrine.',
    43: 'Rad imam ljudi, ki imajo neobičajne poglede.',
    44: 'Naredim veliko napak, ker ne premislim, preden nekaj storim.',
    45: 'Večina ljudi se razjezi hitreje, kot jaz.',
    46: 'Večina ljudi je bolj optimističnih in dinamičnih od mene.',
    47: 'Kadar nekdo, ki mi je blizu, odhaja za daljši čas, čutim močna čustva.',
    48: 'Želim, da ljudje vedo, da sem pomembna oseba visokega statusa.',
    49: 'Sebe ne vidim kot umetnika ali ustvarjalno osebo.',
    50: 'Ljudje me pogosto označijo za perfekcionista.',
    51: 'Tudi če ljudje delajo veliko napak, redko rečem kaj negativnega.',
    52: 'Včasih čutim, da sem ničvredna oseba.',
    53: 'Tudi v primeru krizne situacije ne bi čutil panike.',
    54: 'Ne bi se pretvarjal, da nekoga maram, le zato, da bi mi ta oseba delala usluge.',
    55: 'Pogovori o filozofiji me dolgočasijo.',
    56: 'Raje, kot da se držim načrta, delam, kar mi pade na pamet.',
    57: 'Ko mi ljudje povedo, da se motim, je moja prva reakcija pregovarjanje z njimi.',
    58: 'V skupini ljudi sem pogosto jaz tisti, ki govori v imenu skupine.',
    59: 'Tudi v situacijah, kjer večina ljudi postane zelo sentimentalna, ostanem nečustven.',
    60: 'Mikalo bi me, da bi uporabil ponarejen denar, če bi bil prepričan, da me ne bodo ujeli.',
}

if __name__ == '__main__':
    app.run()
