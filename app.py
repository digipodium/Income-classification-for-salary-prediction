from flask import Flask, render_template, request, jsonify, redirect, session
from predict import predict_salary
from processData import Process
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import plotly

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "bla bla!!"
db = SQLAlchemy(app)

pro = Process('datasets/train_merged.csv')

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(20), nullable = True)
    password = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'

class Search(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    movie = db.Column(db.String(30), nullable = False)
    result = db.Column(db.String(20), nullable = True)
    created = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'

db.create_all()

@app.route('/')
@app.route('/home')
def home():
    if not session.get('user'):
        return redirect('/signin')
    
    return render_template('index.html', loggedin = session.get('user'))

@app.route('/features')
def getFeatures():
    job_type = pro.getJobTypes()
    degree = pro.getDegree()
    major = pro.getMajor()
    industry = pro.getIndustry()

    return jsonify([job_type, degree, major, industry])

@app.route('/signin', methods = ["POST", "GET"])
def Signin():
    
    if request.method == 'POST':
        data = request.form
        
        user = User.query.filter_by(username = data.get('username')).first()
        if user:
            print(user)
            if user.password == data.get('password'):
                print('login success')
                session['user'] = user.username
                return redirect('/home')
                
            else:
                return redirect('/signin')
        else:
            return redirect('/signin')

    return render_template('signin.html')

@app.route('/signup', methods = ["POST", "GET"])
def Signup():
    if request.method == 'POST':
        data = request.form
        user = User(username = data.get('username'), email = data.get('email'), password = data.get('password'))
        db.session.add(user)
        db.session.commit()
        print('data saved!!')
        return redirect('/signin')

    return render_template('signup.html')

@app.route('/logout')
def Logout():
    session['user'] = None
    return redirect('/signin')

@app.route('/showreport')
def showReport():
    if not session.get('user'):
        return redirect('/signin')

    reports = Search.query.all()
    for report in reports:
        report.result = report.result.split(',')
    return render_template('report.html', reports = reports, loggedin = session.get('user'))

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        form = request.form
        print(form)
        job = int(form.get('job'))
        if job == 5:
            job = 6

        degree = int(form.get('degree'))
        if degree == 12 or degree == 14:
            degree = 10

        predict_values = [0 for i in range(31)]
        predict_values[0] = int(form.get('exp'))
        predict_values[1] = int(form.get('distance'))
        predict_values[job] = 1
        predict_values[degree] = 1
        predict_values[int(form.get('major'))] = 1
        predict_values[int(form.get('industry'))+1] = 1
        print(predict_values)

        result = int(predict_salary('PredictionModels/Salary_Prediction_PolynomialModel.csv', predict_values)*1000)
        print(result)
        if len(str(result)) > 6:
            result = "Invalid Parameters"
        else:
            result = '$'+str(result)
        
        return jsonify(result)

@app.route('/showresult')
def showResult():
    if not session.get('user'):
        return redirect('/signin')
    return render_template('predict.html', loggedin = session.get('user'))


@app.route('/viz')
def Visualiztions():
    graphs = []

    df = pro.getMergedData()
    salary = df['Salary']

    # add salary histogram and boxplot
    plotdata = []
    plotdata.append(
                dict(x = salary, type =  'histogram', name = 'Salary')
        )

    graphs.append(plotdata)
    plotdata = []

    plotdata.append(
                dict(y = salary, type= "box")
        )
    graphs.append(plotdata)


    #Mean salaries
    plotdata = []
    for index, i  in enumerate(df['Industry'].unique()):
        data = df[(df['Industry'] == i)][['Major','Salary']].groupby('Major').mean()

        plotdata.append(
                dict(x = data.index, y = data.values.flatten(), name = i, xaxis = f'x{index+1}', yaxis = f'y{index+1}', type="scatter"
                ,title = "Industry")
        )
    graphs.append(plotdata)


    plotdata = []
    for index, var in enumerate(['Job Type', 'Degree', 'Major', 'Industry']):
        data = getDis(var, df)

        plotdata.append(
                dict(x = data.index, y = data.values.flatten(), name = var, xaxis = f'x{index+1}', yaxis = f'y{index+1}', type="scatter")
        )

    graphs.append(plotdata)

    # Salary vs Experience
    df1, jobs = pro.ExpSalary()
    plotdata = []
    plotdata.append(
                dict(x = df1['Experience (Years)'], y = df1['Salary'], name = 'salary', mode = 'markers',type = "scatter",
                text = jobs)
        )

    graphs.append(plotdata)

    

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('visualizations.html', graphJSON = graphJSON)

def getDis(var, train_merged):
    mean = train_merged.groupby(var)['Salary'].mean()
    train_merged[var] = train_merged[var].astype('category').copy()
    levels = mean.sort_values().index.tolist()
    train_merged[var].cat.reorder_categories(levels, inplace=True)
    return train_merged[var].value_counts()

if __name__ == "__main__":
    app.run(debug=True)