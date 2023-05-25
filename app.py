from flask import Flask, render_template, request, jsonify, redirect, session
from predict import predict_salary
from processData import Process
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import plotly
import numpy as np
from predict import predict_salary

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.secret_key = "bla bla!!"
db = SQLAlchemy(app)

pro = Process('datasets/Engineering_graduate_salary.csv')

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(20), nullable = True)
    password = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'

@app.route('/')
@app.route('/home')
def home():
    if not session.get('user'):
        return redirect('/signin')
    else:
        return redirect('/dashboard')


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
                session['isauth'] = True
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
    session['isauth'] = False
    return redirect('/signin')

@app.route('/dashboard', methods = ['GET', 'POST'])
def predict():
    gender_choice =  ['f', 'm']
    board_10_choice = ['cbse', 'maharashtra state board,pune', 'icse', 'state board', 'delhi board', '0', 'hse', 'board of school education harayana', 'rbse', 'u p board', 'bse, odisha', 'rajasthan board of secondary education', 'up board', 'council for indian school certificate examination', 'kea', 'uttar pradesh', 'board of secondary education,andhara pradesh', 'wbbse', 'matriculation board', 'board of secondary education - andhra pradesh', 'mp', 'up', 'karnataka', 'ssc', 'kseeb', 'bse', 'gseb', 'uttar pradesh board', 'matriculation', 'karnataka secondary education board', 'maharastra board', 'tn state board', 'board of secondary education', 'sslc', 'board secondary  education', 'karnataka secondary school of examination', 'metric', 'maharashtra state board', 'maharashtra sate board', 'matric', 'hbse', 'state', 'state boardmp board ', 'karnataka board of higher education', 'hsce', 'nagpur divisional board', 'bihar board', 'jkbose', 'secondary state certificate', 'secondary school of education', 'kseb', 'mpboard', 'cbse board', 'up bourd', 'j&k state board of school education', 'board of secondary education,andhra pradesh', 'kerala state board', 'hsc', 'rajasthan board', 'pune', 'karnataka state board', 'upboard', 'gujarat state board', 'state board - west bengal board of secondary education : wbbse', 'karnataka secondary education examination board', 'bseb', 'cgbse', 'uttarakhand board', 'sri kannika parameswari highier secondary school, udumalpet', 'maharashtra satate board', 'kerala state technical education', 'karnataka education board (keeb)', 'ssc regular', 'board of secondary education, andhra pradesh', 'state board (jac, ranchi)', 'gyan bharati school', 'anglo indian', 'west bengal board of secondary education', 'central board of secondary education', 'up baord', 'pseb', 'maharashtra state board of secondary and higher secondary education,pune', 'karnataka state secondary education board', 'karnataka secondary education', 'madhya pradesh board', 'board of ssc education andhra pradesh', 'stateboard', 'board of secondary education, rajasthan', 'ksseb', 'cbsc', 'bharathi matriculation school', 'uttrakhand board', 'nagpur', 'board of secondary education (bse) orissa', 'bseb, patna', 'mpbse', 'kalaimagal matriculation higher secondary school', 'tamilnadu matriculation board', 'karnataka board', 'delhi public school', 'secondary board of rajasthan', 'jseb', 'up(allahabad)', 'bse,orissa', 'rbse (state board)', 'ssc maharashtra board', 'up board,allahabad', 'mp board', 'board of secendary education orissa', 'bihar school examination board', 'apssc', 'up board , allahabad', 'mirza ahmed ali baig', 'maharashtra board', 'aurangabad board', 'jharkhand secondary board', 'kiran english medium high school', 'state board of secondary education, andhra pradesh', 'maharashtra state board for ssc', 'sarada high scchool', 'pune board', 'uttaranchal state board', 'uttranchal board', 'ap state board', 'stjosephs girls higher sec school,dindigul', 'nagpur board', 'aisse', 'mp board bhopal', 'maharashtra state board of secondary and higher secondary education', 'west bengal  board of secondary education', 'hbsc', 'state bord', 'central board of secondary education, new delhi', 'kseeb(karnataka secondary education examination board)', 'wbbsce', 'school secondary education, andhra pradesh', 'nashik board', 'secondary school certificate', 'state board ', 'ssc board of andrapradesh', 'jbse,jharkhand', 'ksbe', 'jharkhand acedemic council', 'jharkhand secondary examination board (ranchi)', 'board ofsecondary education,ap', 'matric board', 'national public school', 'mhsbse', 'hse,orissa', 'karnataka sslc board bangalore', 'icse board', 'jawahar navodaya vidyalaya', 'dav public school,hehal', 'maharashtra board, pune', 'secondary school education', 'board of secondary education,ap', 'stmary higher secondary', 'latur board', 'bse,odisha', 'gujarat board', 'bseb,patna', 'up board allahabad', 'maharashtra state(latur board)', 'andhra pradesh state board', 'maharashtra', 'education board of kerala', 'apsche', 'ksseb(karnataka state board)', 'punjab school education board, mohali', 'bihar school examination board patna', 'ap state board for secondary education', 'cbse ', 'sslc,karnataka', 'karnataka secondory education board', 'board of secondary education orissa', 'bseb patna', 'board of secondary education(bse) orissa', 'maticulation', 'j & k bord', 'msbshse,pune', 'bihar secondary education board,patna', 'hse,board', 'karnataka board of secondary education', 'tamilnadu state board', 'stjoseph of cluny matrhrsecschool,neyveli,cuddalore district', 'karnataka secondary eduction', 'board of high school and intermediate education uttarpradesh', 'andhra pradesh board ssc', 'upbhsie', 'state borad hp', 'little jacky matric higher secondary school', 'board of  secondary education', 'ghseb', 'kolhapur', 'biharboard', 'certificate of middle years program of ib', 'secondary education board of rajasthan', 'icse board , new delhi', 'sss pune', 'maharashtra nasik board', 'ua', 'ssc-andhra pradesh', 'sslc board', 'uttaranchal shiksha avam pariksha parishad', 'bsepatna', 'himachal pradesh board', 'rajasthan board ajmer', 'state board of secondary education, ap', 'jharkhand secondary education board', 'haryana board of school education', 'gsheb', 'bright way college, (up board)', 'u p', 'secondary school cerfificate', 'up bord', 'karnataka state education examination board', 'himachal pradesh board of school education', 'jharkhand academic council', 'board of secondary school education', 'bsemp', 'karnataka education board']
    board_12_choice = ['cbse', 'amravati divisional board', 'state board', 'all india board', '0', 'chse', 'state board of technical education harayana', 'u p board', 'rajasthan board of secondary education', 'up board', 'council for indian school certificate examination', 'kea', 'board of intermediate education,hyderabad', 'wbchse', 'hisher seconadry examination(state board)', 'board fo intermediate education, ap', 'up', 'karnataka state', 'intermediate board', 'directorate of technical education,banglore', 'board of intermediate education', 'hsc', 'icse', 'board of intermediate', 'gsheb', 'uttar pradesh board', 'rbse', 'pre-university board', 'maharashtra board', 'isc', 'tn state board', 'puc', 'baord of intermediate education', 'karnataka pre university board', 'bieap', 'state', 'maharashtra state board', 'intermediate', 'p u board, karnataka', 'hbse', 'board of intermediate ap', 'andhra board', 'pu', 'uttar pradesh', 'pre university board of karnataka', 'ssc', 'madhya pradesh open school', 'nagpur divisional board', 'bihar board', 'jkbose', 'matriculation', 'pu board', 'ipe', 'higher secondary state certificate', 'jaswant modern school', 'mp board', 'up bourd', 'department of technical education', 'j&k state board of school education', 'kerala state board', 'ap board', 'rajasthan board', 'msbte', 'pre university board, karnataka', 'bseb', 'upboard', 'wbbhse', 'state board - west bengal council of higher secondary education : wbchse', 'department of pre-university education', 'pu board ,karnataka', 'cgbse', 'uttarakhand board', 'sbtet', 'hse', 'sri kannika parameswari highier secondary school, udumalpet', 'maharashtra satate board', 'kerala state hse board', 'pu board karnataka', 'board of intermediate education, andhra pradesh', 'karnataka pre-university board', 'state board (jac, ranchi)', 'karnataka state board', 'dav public school', 'uo board', 'karnataka board', 'west bengal council of higher secondary education', 'puboard', 'central board of secondary education', 'bie', 'up baord', 'pseb', 'board of higher secondary examination, kerala', 'sbte, jharkhand', 'department of technical education, bangalore', 'west bengal state council of technical education', 'madhya pradesh board', 'board of secondary school of education', 'board of intmediate education ap', 'bteup', 'pub', 'diploma in computers', 'stateboard', 'board of secondary education, rajasthan', 'pre university board', 'cbsc', 'jaycee matriculation school', 'mp', 'uttrakhand board', 'nagpur', 'certificate for higher secondary education (chse)orissa', 'karnataka pu board', 's j polytechnic', 'bseb, patna', 'mpbse', 'ks rangasamy institute of technology', 'bihar intermediate education council', 'tamilnadu stateboard', 'board of intermediate education,andhra pradesh', 'diploma(msbte)', 'tamilnadu higher secondary education board', 'board of intermidiate', 'department of pre-university education(government of karnataka)', 'karnataka board secondary education', 'secondary board of rajasthan', 'intermediate board examination', 'govt of karnataka department of pre-university education', 'intermedite', 'up(allahabad)', 'chse,orissa', 'mpc', 'rbse (state board)', 'hsc maharashtra board', 'bte up', 'state syllabus', 'up board,allahabad', 'scte vt orissa', 'apbie', 'intermideate', 'up board , allahabad', 'board of technical education', 'state board - tamilnadu', 'aurangabad board', 'jharkhand academic council', 'sri chaitanya junior kalasala', 'state  board of intermediate education, andhra pradesh', 'maharashtra state board for hsc', 'pune board', 'uttaranchal state board', 'uttranchal board', 'ap intermediate board', 'srv girls higher sec school,rasipuram', 'nagpur board', 'dte', 'aissce', 'ibe', 'diploma ( maharashtra state board of technical education)', 'west bengal board of higher secondary education', 'hbsc', 'state bord', 'gseb', 'biec, patna', 'diploma in engg (e &tc) tilak maharashtra vidayapeeth', 'psbte', 'central board of secondary education, new delhi', 'pre university', 'nashik board', 'board of intermediate education,ap', 'karnataka state pre- university board', 'state board ', 'board of intermediate education,andra pradesh', 'jstb,jharkhand', 'jharkhand acedemic council', 'board of school education harayana', 'department of pre university education', 'intermediate board of education,andhra pradesh', 'nios', 'karnataka pre-university', 'tamil nadu polytechnic', 'intermediate board of education', 'andhra pradesh board of secondary education', 'department of pre-university education, bangalore', 'jharkhand acamedic council (ranchi)', 'board of intermediate education, ap', 'jawahar higher secondary school', 'scte and vt ,orissa', 'karnataka secondary education board', 'mp board bhopal', 'isc board', 'biec', 'intermediate board of andhra pardesh', 'science college', 'dav public school,hehal', 'board of technicaleducation ,delhi', 'maharashtra board, pune', 'board of intermediate education:ap,hyderabad', 'aligarh muslim university', 'latur board', 'chse,odisha', 'gujarat board', 'bciec,patna', 'biec,patna', 'staae board', 'up board allahabad', 'cbse board', 'maharashtra state(latur board)', 'karnataka pre unversity board', 'andhra pradesh state board', 'maharashtra', 'punjab state board of technical education & industrial training, chandigarh', 'bihar school examination board patna', 'ap board for intermediate education', 'scte&vt', 'board of intermediate,ap', 'punjab state board of technical education & industrial training', 'andhra pradesh', 'pre-university', 'bice', 'board of higher secondary orissa', 'biec patna', 'electonincs and communication(dote)', 'j & k board', 'msbshse,pune', 'intermediate council patna', 'scte & vt (diploma)', 'karnataka secondary education', 'karnataka board of university', 'chse, odisha', 'tamilnadu state board', 'karnataka pu', 'intermediate state board', 'stjoseph of cluny matrhrsecschool,neyveli,cuddalore district', 'wbscte', 'board of high school and intermediate education uttarpradesh', 'andhpradesh board of intermediate education', 'msbte (diploma in computer technology)', 'upbhsie', 'apbsc', 'sda matric higher secondary school', 'stateboard/tamil nadu', 'board of intermidiate education,ap', 'ghseb', 'kolhapur', 'international baccalaureate (ib) diploma', 'state board of technical eduction panchkula', 'board of intermediate(bie)', 'state board of technical education and training', 'secnior secondary education board of rajasthan', 'karnataka sslc', 'isc board , new delhi', 'hsc pune', 'gshseb', 'maharashtra nasik board', 'ua', 'karnatak pu board', 'state broad', 'dote (diploma - computer engg)', 'pue', 'uttaranchal shiksha avam pariksha parishad', 'biec-patna', 'himachal pradesh board', 'apsb', 'rajasthan board ajmer', 'technical board, punchkula', ' board of intermediate', 'mbose', 'bright way college, (up board)', 'sjrcw', 'u p', 'mpboard', 'up bord', 'intermidiate', 'dept of pre-university education', 'himachal pradesh board of school education', 'dpue', 'board of intermeadiate education', 'bsemp', 'karnataka education board']
    degree_choice =  ['B.Tech/B.E.', 'M.Tech./M.E.', 'MCA', 'M.Sc. (Tech.)']
    specialization_choice = ['instrumentation and control engineering', 'computer science & engineering', 'electronics & telecommunications', 'biotechnology', 'mechanical engineering', 'information technology', 'electronics and communication engineering', 'computer engineering', 'computer application', 'computer science and technology', 'electrical engineering', 'automobile/automotive engineering', 'electronics and electrical engineering', 'information science engineering', 'chemical engineering', 'instrumentation engineering', 'electronics & instrumentation eng', 'ceramic engineering', 'metallurgical engineering', 'aeronautical engineering', 'electronics engineering', 'electronics and instrumentation engineering', 'applied electronics and instrumentation', 'civil engineering', 'computer and communication engineering', 'industrial & production engineering', 'computer networking', 'other', 'electronics and computer engineering', 'control and instrumentation engineering', 'mechanical & production engineering', 'mechanical and automation', 'industrial & management engineering', 'biomedical engineering', 'electrical and power engineering', 'telecommunication engineering', 'industrial engineering', 'mechatronics', 'embedded systems technology', 'electronics', 'information & communication technology', 'information science'] 
    collegestate_choice = ['Delhi', 'Uttar Pradesh', 'Maharashtra', 'Tamil Nadu', 'Punjab', 'West Bengal', 'Telangana', 'Andhra Pradesh', 'Haryana', 'Karnataka', 'Orissa', 'Chhattisgarh', 'Rajasthan', 'Madhya Pradesh', 'Uttarakhand', 'Gujarat', 'Jharkhand', 'Himachal Pradesh', 'Bihar', 'Union Territory', 'Jammu and Kashmir', 'Kerala', 'Assam', 'Sikkim', 'Meghalaya', 'Goa']
    collegecitytier_choice =  [1, 0]
    collegetier_choice =  [1, 2]
    board_10_choice.sort()
    board_12_choice.sort()
    degree_choice.sort()
    specialization_choice.sort()
    collegestate_choice.sort()
    if request.method == 'POST':
        form = request.form
        # print(form, sep='\n')
        gender = form['gender']
        degree = form['degree']
        specialization = form['specialization']
        collegestate = form['college_state']
        collegecitytier = form['collegeCityTier']
        collegetier = form['collegeTier']
        board_10 = form['board10']
        board_12 = form['board12']
        percentage_10 = form['percentage_10']
        percentage_12 = form['percentage_12']
        collegeGPA = form['collegeGPA']
        english = form['english']
        logical = form['logical']
        quant = form['quant']
        math = form['domain']
        age = form['age']
        try:
            salary = predict_salary(
                gender,
                percentage_10, 
                board_10, 
                percentage_12, 
                board_12,
                collegetier, 
                degree, 
                specialization, 
                collegeGPA,
                collegecitytier, 
                collegestate,
                english, 
                logical, 
                quant, 
                age
            )
            # salary = round(np.expm1(result)[0])
            # print(salary)
            return render_template('index.html', salary=salary, degree_choice=degree_choice,
                                   specialization_choice=specialization_choice,
                                      collegestate_choice=collegestate_choice,
                                        collegecitytier_choice=collegecitytier_choice,
                                        collegetier_choice=collegetier_choice,
                                        board_10_choice=board_10_choice,
                                        board_12_choice=board_12_choice,
                                        gender_choice = gender_choice,
                                        )
        except Exception as e:
            print(e)

    return render_template('index.html',degree_choice=degree_choice, 
                           specialization_choice=specialization_choice,
                           collegestate_choice=collegestate_choice, 
                           collegecitytier_choice=collegecitytier_choice, 
                           collegetier_choice=collegetier_choice,
                           board_10_choice=board_10_choice,
                           board_12_choice=board_12_choice,
                           gender_choice=gender_choice)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)