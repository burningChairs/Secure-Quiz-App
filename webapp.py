# I had a couple prompts with perplextiy and google searches with my original idea in this project but 
# 		since it wasnt working the way I wanted it to I ended up restarting and making it completely different. 
# 		so I wont be adding that. i will just be uploading the searches that had to do with the final project
# I had also given up on using perplexity and used google instead because it was getting frusterating and
#		personally confusing (I hope that was okay)

# https://www.google.com/search?q=letting+a+user+choose+any+option+in+a+secure+quiz
# https://www.google.com/search?q=what+is+Pseudosuchia+prehistoric
# https://www.google.com/search?q=what+is+the+prehistoric+crocodiles+clade+called
# https://www.google.com/search?q=what+is+the+prehistoric+crocodilian+clade+called
# https://www.google.com/search?q=common+dinosaurs+and+pterosaurs
# https://www.google.com/search?q=Using+POST+in+html+correctly
# https://www.google.com/search?q=ways+to+make+css+better
# https://www.google.com/search?q=what+is+hover+and+active+in+css
# https://www.google.com/search?q=how+to+use+css+link+color+change
# https://www.google.com/search?q=what+is+input+on+css
# https://www.google.com/search?q=how+to+have+the+ability+to+have+a+%22submit%22+input+on+css
# https://www.google.com/search?q=ways+to+edit+a+button+in+css
# https://www.google.com/search?q=how++to+create+a+button+in+css
# https://www.google.com/search?q=How+should+the+code+look+in+the+html+of+a+secure+quiz
# https://www.google.com/search?q=having+the+user+able+to+retake+a+quiz+using+python+and+html
# https://www.google.com/search?q=allowing+a+user+to+redo+a+website+with+new+data
# https://www.google.com/search?q=having+questions+in+python+to+have+all+the+from+a+quiz+app+answers+in+one+page
# https://www.google.com/search?q=creating+an+app+route+for+request.method+%3D%3D+%27POST%27
# https://www.google.com/search?q=how+to+create+a+quizzes+questions+in+python
# https://www.google.com/search?q=using+navbar+to+create+a+quiz
# https://www.google.com/search?q=how+to+create+a+working+secure+app+with+multiple+pages

import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev") #env var

#quiz questions
quiz = {
	1: {
		"question": "How are Dinosaurs and Pterosaurs Related?",
		"Options": {
			"A": "Pterosaurs derive from the dinosaur faction.",
			"B": "Dinosaurs and Pterosaurs do not relate at all.",
			"C": "Dinosaurs and Pterosaurs both derive from similar ancestors.",
			"D": "Dinosaurs derive from Pterosaurs."
		},
		"answer": "A",
		"reasoning": "Dinosaurs and Pterosaurs share a common ancestor in Archasaurs."
	},
	2: {
		"question": "What is a pterodactyl?",
		"Options": {
			"A": "A type of Archasaur",
			"B": "A type of Pterosaur.",
			"C": "A made up type of pterosaur.",
			"D": "A type of dinosaur."
		},
		"answer": "C",
		"reasoning": "Pterodactyls are a commonly mistaken animal, not a real thing. A myth likely derived from the faction of pterosaurs."
	},
	3: {
		"question": "Which clade includes crocodiles and their extinct ralatives?",
		"Options": {
			"A": "Avemetatarsalia.",
			"B": "Pseudosuchia.",
			"C": "Ornithischia",
			"D": "Saurischia"
		},
		"answer": "B",
		"reasoning": "Pseudosuchia includes modern crocodiles and their extinct ralatives."
	},
	4: {
		"question": "Which group contains all dinosaurs and birds?",
		"Options": {
			"A": "Pseudosuchia",
			"B": "Pterosauria",
			"C": "Theropoda",
			"D": "Avemetetarsalia"
		},
		"answer": "D",
		"reasoning": "Avemetetarsalia include all dinosaurs and all modern birds."
	},
	5: {
		"question": "Which Archasaur out of the following is your favorite?",
		"Options": {
			"Rhamphorhynchus": "Rhamphorhynchus (pterosaur)",
			"Ankylosaurus": "Ankylosaurus (dinosaur)",
			"Spinosaurus": "Spinosaurus (dinosaur)",
			"Dilophosaurus": "Dilophosaurus (dinosaur)",
			"Pteranodon": "Pteranodon (pterosaur)",
			"Brachiosaurus": "Brachiosaurus (dinosaur)",
			"Velociraptor": "Velociraptor (dinosaur)",
			"Triceratops": "Triceratops (dinosaur)",
			"Dimorphodon": "Dimorphodon (pterosaur)",
		},
		"answer": "Any",
		"reasoning": "Nice choice!"
	},
}

TOTAL_QUESTIONS = len(quiz)

# Home page
@app.route('/')
def home():
	session.clear()
	session['current_q'] = 1
	session['answers'] = {}
	return render_template('home.html')
	
# Question
@app.route('/question<int:qnum>', methods=['GET', 'POST'])
def question(qnum):
	if qnum < 1 or qnum > TOTAL_QUESTIONS:
		return redirect(url_for('home'))
	
	if 'answers' not in session:
		session['answers'] = {}
		session['current_q'] = 1
		
	#save answer if first time
	if request.method == 'POST' and str(qnum) not in session['answers']:
		selected = request.form.get('answer')
		if selected:
			session['answers'][str(qnum)] = selected
			session['current_q'] = qnum + 1
		# Redirect to the next question or results
		if qnum < TOTAL_QUESTIONS:
			return redirect(url_for('question', qnum=qnum+1))
		else:
			return redirect(url_for('results'))
		
	#user cant see future questions
	if qnum > session.get('current_q', 1):
		return redirect(url_for('question', qnum=session.get('current_q', 1)))
		
	qdata = quiz[qnum]
	return render_template(f'question{qnum}.html', question=qdata['question'], options=qdata['Options'], qnum=qnum)
		
# Results
@app.route('/results')
def results():
	if 'answers' not in session:
		return redirect(url_for('home'))
		
	score = 0
	detailed_results = []
	
	for qnum, qdata in quiz.items():
		user_answer = session['answers'].get(str(qnum))

		is_any = qdata['answer'] == "Any"
		correct = is_any or (user_answer == qdata['answer'])
		
		if correct:
			score += 1
			
		detailed_results.append({
			"qnum": qnum,
			"question": qdata['question'],
			"user_answer": user_answer or "None",
			"correct_answer": None if correct or is_any else qdata['answer'],
			"correct": correct,
			"reasoning": qdata['reasoning']
		})
		
	percent = int(score / TOTAL_QUESTIONS * 100)
	
	if percent == 100:
		message = "ᓚᘏᗢ Perfect score! Congradulations!"
	elif percent >= 80:
		message = "ᓚᘏᗢ Great job!"
	elif percent >= 50:
		message = "ᓚᘏᗢ Good effort!"
	else:
		message = "ᓚᘏᗢ Try Again!"
		
	return render_template('results.html', score=score, total=TOTAL_QUESTIONS, percent=percent, message=message, results=detailed_results)
	
# Retake
@app.route('/retake')
def retake():
	session.clear()
	return redirect(url_for('home'))
	
#info
@app.route('/info')
def info():
	return render_template('info.html')
	
if __name__ == "__main__":
	app.run(debug=True)
