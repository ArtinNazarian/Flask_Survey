from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey



app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

response =[]

@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
      
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/start', methods=["POST"])
def start():
    
    return redirect('/questions/0')


@app.route('/questions/<int:id>')
def questions(id):       
  
    if len(response) == len(satisfaction_survey.questions):
        return redirect('/complete')
        
    # if id != len(response):
    #     return redirect(f"/questions/{len(response)}")

    if len(response) != id:
        # Trying to access questions out of order.
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(response)}")

    survey_question = satisfaction_survey.questions[id]
    return render_template('questions.html', survey_question=survey_question)
    

@app.route('/answer', methods=['POST'] )
def answer():
    answer = request.form['answer']
    response.append(answer)
    if len(response) == len(satisfaction_survey.questions):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(response)}")

@app.route('/complete')
def complete():
    return render_template('thank_you.html')
    
