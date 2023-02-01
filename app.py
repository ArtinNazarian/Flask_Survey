from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions          
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/start', methods=["POST"])
def start():    
    session['responses']=[]
    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def questions(id):    
    responses = session.get('responses')   
  
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
        
    if len(responses) != id:      
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    survey_question = satisfaction_survey.questions[id]
    return render_template('questions.html', survey_question=survey_question)
    

@app.route('/answer', methods=['POST'] )
def answer():
    answer = request.form['answer']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def complete():
    return render_template('thank_you.html')


    
