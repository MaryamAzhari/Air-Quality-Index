from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    T = TextField('T:', validators=[validators.required()])
    TM = TextField('TM:', validators=[validators.required()])
    Tm = TextField('Tm:', validators=[validators.required()])
    H = TextField('H:', validators=[validators.required()])
    PP = TextField('PP:', validators=[validators.required()])
    VV = TextField('VV:', validators=[validators.required()])
    V = TextField('V:', validators=[validators.required()])

def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(T, TM, Tm ,H,PP,VV,V):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp={}, T={}, TM={}, Tm={},H={}, PP={}, VV={},V={} \n'.format(timestamp, T, TM, Tm,H,PP,VV,V))
    data.close()

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    #print(form.errors)
    if request.method == 'POST':
        T=request.form['T']
        TM=request.form['TM']
        Tm=request.form['Tm']
        H=request.form['H']
        PP=request.form['PP']
        VV=request.form['VV']
        V=request.form['V']

        if form.validate():
            write_to_disk(T,TM,Tm,H,PP,VV,V)
            flash('You entered these values: {} {}'.format(T, TM,Tm,H,PP,VV,V))

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)
    
@app.route('/predict',methods=['POST'])
def predict():
    df=pd.read_csv('AQI.csv')
    my_prediction=loaded_model.predict(df.iloc[:,:-1].values)
    my_prediction=my_prediction.tolist()
    return render_template('results.html',prediction = my_prediction)
    
if __name__ == "__main__":
    app.run()
