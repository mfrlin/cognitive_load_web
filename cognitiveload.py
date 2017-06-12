import string
import random

from flask import Flask, render_template, session, flash, redirect, url_for, g
from flask_bootstrap import Bootstrap
from flask.ext.wtf import FlaskForm
from flask.ext.login import LoginManager
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required

from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = 'Za obisk te strani se je potrebno vpisati.'

db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            login_user(user, remember=True)
        else:
            u = User(email=form.email.data)
            db.session.add(u)
            db.session.commit()
            login_user(u, remember=True)
            # flash('Neobstoječ email.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/hexaco', methods=['GET', 'POST'])
@login_required
def hexaco():
    session['answers'] = {}
    return render_template('hexaco.html')


@app.route('/hexaco/<int:question_number>', methods=['GET', 'POST'])
@login_required
def hexaco_questions(question_number):
    if question_number > len(QUESTIONS):
        g.user.hexaco = '|'.join(str(session['answers'][str(i)]) for i in range(1, len(QUESTIONS) + 1))
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for('answers'))
    form = HexacoQuestionForm()
    if form.validate_on_submit():
        for i, button in enumerate([form.one, form.two, form.three, form.four, form.five], start=1):
            if button.data:
                session['answers'][str(question_number)] = i
                session.modified = True
                break
        return redirect(url_for('hexaco_questions', question_number=question_number + 1))

    question = QUESTIONS[question_number]
    return render_template('hexaco_questions.html', question=question, form=form, question_number=question_number)


@app.route('/answers')
@login_required
def answers():
    def r(i):
        return [0, 5, 4, 3, 2, 1][i]
    scores = {}
    if g.user.hexaco is not None:
        ans = list(map(int, g.user.hexaco.split('|')))
        ans = [0] + ans
        scores = {
            'Odkritost': (ans[6] + r(ans[30]) + ans[54]) / 3,
            'Postenost': (r(ans[12]) + ans[36] + ans[60]) / 3,
            'OgibanjePohlepu': (ans[18] + r(ans[42])) / 2,
            'Skromnost': (r(ans[24]) + r(ans[48])) / 2,
            'Bojecnost': (ans[5] + ans[29] + r(ans[53])) / 3,
            'Tesnobnost': (ans[11] + r(ans[35])) / 2,
            'Odvisnost': (ans[17] + r(ans[41])) / 2,
            'Sentimentalnost': (ans[23] + ans[47] + r(ans[59])) / 3,
            'SocialnaSamozavest': (ans[4] + r(ans[28]) + r(ans[52])) / 3,
            'SocialniPogum': (r(ans[10]) + ans[34] + ans[58]) / 3,
            'Druzabnost': (ans[16] + ans[40]) / 2,
            'Zivahnost': (ans[22] + r(ans[46])) / 2,
            'Odpuscanje': (ans[3] + ans[27]) / 2,
            'Neznost': (r(ans[9]) + ans[33] + ans[51]) / 3,
            'Fleksibilnost': (r(ans[15]) + ans[39] + r(ans[57])) / 3,
            'Potrpezljivost': (r(ans[21]) + ans[45]) / 2,
            'Organiziranost': (ans[2] + r(ans[26])) / 2,
            'Marljivost': (ans[8] + r(ans[32])) / 2,
            'Perfekcionizem': (r(ans[14]) + ans[38] + ans[50]) / 3,
            'Preudarnost': (r(ans[20]) + r(ans[44]) + r(ans[56])) / 3,
            'UzivanjeVEstetiki': (r(ans[1]) + ans[25]) / 2,
            'Vedozeljnost': (ans[7] + r(ans[31])) / 2,
            'Ustvarjalnost': (ans[13] + ans[37] + r(ans[49])) / 3,
            'Nekonvencionalnost': (r(ans[19]) + ans[43] + r(ans[55])) / 3,
        }
    return render_template('answers.html', scores=scores)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Prijavi me')


class HexacoQuestionForm(FlaskForm):
    one = SubmitField(label='se močno ne strinjam')
    two = SubmitField(label='se ne strinjam')
    three = SubmitField(label='sem nevtralen')
    four = SubmitField(label='se strinjam')
    five = SubmitField(label='se močno strinjam')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True)
    ident = db.Column(db.String(5), index=True, unique=True)
    hexaco = db.Column(db.String(119), nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def generate_ident():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

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
    27: 'Moj odnos do ljudi, ki so z mano slabo ravnali, je "odpusti in pozabi".',
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
