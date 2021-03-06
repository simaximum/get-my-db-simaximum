from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/db_1'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rkkylaxqsavvtz:'+\
        'fe27dec83910b18a94453357b1f00dd0d22d1bb120fa5dde03a39dcf36421d98'+\
            '@ec2-3-233-7-12.compute-1.amazonaws.com:5432/d4j7tg2ng7fm1f'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Stats(db.Model):
    __tablename__ = 'stats'
    Time = db.Column(db.DateTime, primary_key=True)
    customer = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.String(200), primary_key=True)
    cdn = db.Column(db.BigInteger)
    p2p = db.Column(db.BigInteger)
    sessions = db.Column(db.Integer)

    def __init__(self, Time, customer, content, cdn, p2p, sessions):
        self.Time = Time
        self.customer = customer
        self.content = content
        self.cdn = cdn
        self.p2p = p2p
        self.sessions = sessions

def round_minutes(dt):
    # First zero out seconds and micros
    dtTrunc = dt.replace(second=0, microsecond=0)

    # Figure out how many minutes we are past the last interval
    excessMinutes = (dtTrunc.hour*60 + dtTrunc.minute) % 5

    # Subtract off the excess minutes to get the last interval
    return dtTrunc + timedelta(minutes=-excessMinutes)

@app.route('/')
def index():
    return str(round_minutes(datetime.now()))

@app.route('/stats', methods=['GET', 'POST'])
def add_message():
    payload = request.json
    token = payload['token']
    customer = payload['customer']
    content = payload['content']
    timespan = payload['timespan']
    p2p = payload['p2p']
    cdn = payload['cdn']
    sessionDuration = payload['sessionDuration']
    window = round_minutes(datetime.now())

    q = db.session.query(Stats)
    q = q.filter(Stats.Time == window, Stats.customer == customer, Stats.content == content)
    record = q.first()

    if not record:
        if sessionDuration == 30000 : 
            sessions = 1
        else: 
            sessions = 0
        data = Stats(window, customer, content, cdn, p2p, sessions)
        db.session.add(data)
        db.session.commit()
        return 'A row has been inserted'
    
    else:
        if sessionDuration == 30000 :
            record.sessions = record.sessions + 1
        record.cdn = record.cdn + cdn
        record.p2p = record.p2p + p2p
        db.session.commit()
        return 'A row has been updated'



if __name__ == '__main__':
    app.run()
