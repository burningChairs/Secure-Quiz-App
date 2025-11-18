from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # IMPORTANT: use an environment variable for production
app.permanent_session_lifetime = timedelta(hours=2)

# Main quiz questions
quiz_questions = [
    {
        "question": "How are Dinosaurs and Pterosaurs Related?",
        "options": [
            "Pterosaurs derive from the dinosaur faction.",
            "Dinosaurs and Pterosaurs do not relate at all.",
            "Dinosaurs and Pterosaurs are both derived from similar ancestors.",
            "Dinosaurs derive from Pterosaurs."
        ],
        "answer": 2,
        "reasoning": "Dinosaurs and Pterosaurs share a common archosaur ancestor."
    },
    {
        "question": "What is a Pterodactyl?",
        "options": [
            "A type of Archosaur",
            "A type of Pterosaur",
            "A type of Dinosaur",
            "A made-up type of pterosaur"
        ],
        "answer": 1,
        "reasoning": "‘Pterodactyl’ usually refers to the pterosaur genus *Pterodactylus*, not a dinosaur."
    },
    {
        "question": "Which era did the first archosaurs appear in?",
        "options": ["Triassic", "Jurassic", "Cretaceous", "Permian"],
        "answer": 0,
        "reasoning": "Archosaurs first diversified in the Triassic period." 
    },
    {
        "question": "Which modern group is most closely related to dinosaurs?",
        "options": ["Birds", "Crocodiles", "Lizards", "Turtles"],
        "answer": 0,
        "reasoning": "Birds are technically living dinosaurs (theropods)."
    },
    {
        "question": "Which of these is a pterosaur?",
        "options": ["Tyrannosaurus", "Rhamphorhynchus", "Triceratops", "Brachiosaurus"],
        "answer": 1,
        "reasoning": "Rhamphorhynchus is a genus of pterosaur."
    },
    {
        "question": "Which is NOT a dinosaur?",
        "options": ["Velociraptor", "Stegosaurus", "Pterodactyl", "Allosaurus"],
        "answer": 2,
        "reasoning": "Pterodactyl (i.e., Pterodactylus) is a pterosaur, not a dinosaur."
    },
    {
        "question": "Which of these lived in the Cretaceous period?",
        "options": ["Allosaurus", "Plateosaurus", "Triceratops", "Dimetrodon"],
        "answer": 2,
        "reasoning": "Triceratops lived during the Late Cretaceous."
    },
    {
        "question": "Which dinosaur was primarily carnivorous?",
        "options": ["Stegosaurus", "Brachiosaurus", "Allosaurus", "Ankylosaurus"],
        "answer": 2,
        "reasoning": "Allosaurus was a large carnivorous theropod."
    },
    {
        "question": "Which archosaur lineage survived to today as crocodiles?",
        "options": ["Pterosaurs", "Non-avian Dinosaurs", "Pseudosuchians", "None"],
        "answer": 2,
        "reasoning": "Modern crocodilians are descended from pseudosuchian archosaurs."  
    },
    {
        "question": "What is your favorite Archosaur?",
        "options": ["Tyrannosaurus", "Velociraptor", "Rhamphorhynchus", "Allosaurus", "Spinosaurus", "Ankylosaurus", "Triceratops", "Stegosaurus"],
        "answer": -1,  # any answer is "correct"
        "reasoning": "Nice choice! Each archosaur is awesome in its own way."
    }
]

# Extra quizzes
extra_eras_questions = [
    {"question": "Which era saw the first dinosaur fossils?", "options": ["Triassic", "Jurassic", "Cretaceous"], "answer": 0, "reasoning": "The Triassic was when the first true dinosaurs appeared."},
    {"question": "Which era had huge sauropods like Brachiosaurus?", "options": ["Triassic", "Jurassic", "Cretaceous"], "answer": 1, "reasoning": "Jurassic was famous for its giant sauropods."},
    {"question": "Which era ended with a mass extinction that wiped out non-avian dinosaurs?", "options": ["Triassic", "Jurassic", "Cretaceous"], "answer": 2, "reasoning": "The Cretaceous ended with the K-Pg extinction event."}
]

extra_species_questions = [
    {"question": "Which is a flying reptile (not dinosaur)?", "options": ["Rhamphorhynchus", "Velociraptor", "Triceratops"], "answer": 0, "reasoning": "Rhamphorhynchus is a pterosaur, not a dinosaur."},
    {"question": "Which dinosaur group includes modern birds?", "options": ["Sauropods", "Theropods", "Ornithopods"], "answer": 1, "reasoning": "Modern birds evolved from theropod dinosaurs."},
    {"question": "Which of these dinosaurs had armor plates?", "options": ["Stegosaurus", "Tyrannosaurus", "Allosaurus"], "answer": 0, "reasoning": "Stegosaurus had large bony plates along its back."}
]

extra_environment_questions = [
    {"question": "Where did many sauropod dinosaurs live?", "options": ["Forests", "Deserts", "Swamps"], "answer": 0, "reasoning": "Many sauropods are thought to have lived in forested floodplains."},
    {"question": "Which environmental event caused the end of the Cretaceous?", "options": ["Asteroid impact", "Volcanoes", "Ice age"], "answer": 0, "reasoning": "A large asteroid is believed to have caused the mass extinction."},
    {"question": "Which habitat would pterosaurs likely use for nesting?", "options": ["Cliffs", "Open ocean", "Dense forest"], "answer": 0, "reasoning": "Many pterosaurs likely nested on cliffs or rocky outcrops."}
]

# Archosaur cards
archasaur_cards = [
    {"name": "Tyrannosaurus", "scientific": "Tyrannosaurus rex", "diet": "Carnivore", "size": "12 m long", "type": "Dinosaur"},
    {"name": "Velociraptor", "scientific": "Velociraptor mongoliensis", "diet": "Carnivore", "size": "2 m long", "type": "Dinosaur"},
    {"name": "Triceratops", "scientific": "Triceratops horridus", "diet": "Herbivore", "size": "9 m long", "type": "Dinosaur"},
    {"name": "Stegosaurus", "scientific": "Stegosaurus stenops", "diet": "Herbivore", "size": "9 m long", "type": "Dinosaur"},
    {"name": "Allosaurus", "scientific": "Allosaurus fragilis", "diet": "Carnivore", "size": "10 m long", "type": "Dinosaur"},
    {"name": "Spinosaurus", "scientific": "Spinosaurus aegyptiacus", "diet": "Piscivore / Carnivore", "size": "15 m long", "type": "Dinosaur"},
    {"name": "Brachiosaurus", "scientific": "Brachiosaurus altithorax", "diet": "Herbivore", "size": "22 m long", "type": "Dinosaur"},
    {"name": "Ankylosaurus", "scientific": "Ankylosaurus magniventris", "diet": "Herbivore", "size": "6 m long", "type": "Dinosaur"},
    {"name": "Rhamphorhynchus", "scientific": "Rhamphorhynchus muensteri", "diet": "Piscivore", "size": "1 m wingspan", "type": "Pterosaur"},
    {"name": "Pteranodon", "scientific": "Pteranodon longiceps", "diet": "Piscivore", "size": "7 m wingspan", "type": "Pterosaur"},
    {"name": "Quetzalcoatlus", "scientific": "Quetzalcoatlus northropi", "diet": "Carnivore / Scavenger", "size": "10–11 m wingspan", "type": "Pterosaur"},
    {"name": "Dimorphodon", "scientific": "Dimorphodon macronyx", "diet": "Carnivore", "size": "1.5 m wingspan", "type": "Pterosaur"},
    {"name": "Istiodactylus", "scientific": "Istiodactylus latidens", "diet": "Carnivore", "size": "4–5 m wingspan", "type": "Pterosaur"},
    {"name": "Tupandactylus", "scientific": "Tupandactylus imperator", "diet": "Likely omnivore", "size": "3–4 m wingspan", "type": "Pterosaur"},
    {"name": "Compsognathus", "scientific": "Compsognathus longipes", "diet": "Carnivore", "size": "1 m long", "type": "Dinosaur"},
    {"name": "Yutyrannus", "scientific": "Yutyrannus huali", "diet": "Carnivore", "size": "9 m long", "type": "Dinosaur"},
    {"name": "Apatosaurus", "scientific": "Apatosaurus louisae", "diet": "Herbivore", "size": "21 m long", "type": "Dinosaur"},
    {"name": "Stegoceras", "scientific": "Stegoceras validum", "diet": "Herbivore", "size": "2 m long", "type": "Dinosaur"},
    {"name": "Parasaurolophus", "scientific": "Parasaurolophus walkeri", "diet": "Herbivore", "size": "10 m long", "type": "Dinosaur"},
    {"name": "Carnotaurus", "scientific": "Carnotaurus sastrei", "diet": "Carnivore", "size": "7.5 m long", "type": "Dinosaur"},
    {"name": "Mosasaurus", "scientific": "Mosasaurus hoffmanni", "diet": "Carnivore", "size": "17 m long", "type": "Marine Squamate (not dinosaur)"},
    {"name": "Pliosaurus", "scientific": "Pliosaurus funkei", "diet": "Carnivore", "size": "12 m long", "type": "Marine reptile (plesiosaur)"},
    {"name": "Archaeopteryx", "scientific": "Archaeopteryx lithographica", "diet": "Carnivore / Insectivore", "size": "0.5 m long", "type": "Dinosaur / Bird-line archosaur"},
    {"name": "Diplodocus", "scientific": "Diplodocus longus", "diet": "Herbivore", "size": "27 m long", "type": "Dinosaur"},
    {"name": "Stegosaursaurus", "scientific": "Stegosaurus ungulatus", "diet": "Herbivore", "size": "9 m long", "type": "Dinosaur"},
    {"name": "Gallimimus", "scientific": "Gallimimus bullatus", "diet": "Omnivore", "size": "6 m long", "type": "Dinosaur"},
    {"name": "Microraptor", "scientific": "Microraptor gui", "diet": "Carnivore", "size": "0.8 m wingspan", "type": "Dinosaur / Bird-line archosaur"}
]

# Routes
@app.route('/')
def home():
    session.clear()
    return render_template('home.html')

@app.route('/question/<int:q_num>', methods=['GET', 'POST'])
def question(q_num):
    if 'answers' not in session:
        session['answers'] = {}
    if q_num >= len(quiz_questions):
        return redirect(url_for('results'))

    if request.method == 'POST':
        if str(q_num) not in session['answers']:
            session['answers'][str(q_num)] = request.form.get('answer')
        next_q = q_num + 1
        if next_q < len(quiz_questions):
            return redirect(url_for('question', q_num=next_q))
        else:
            return redirect(url_for('results'))

    question_data = quiz_questions[q_num]
    return render_template('question.html', q_num=q_num, question=question_data, total=len(quiz_questions))

@app.route('/results')
def results():
    if 'answers' not in session:
        return redirect(url_for('home'))

    score = 0
    feedback = []
    for idx, q in enumerate(quiz_questions):
        user_ans = session['answers'].get(str(idx))
        correct_ans = q['answer']
        correct = False
        if correct_ans == -1:
            correct = True
        elif user_ans is not None and user_ans.isdigit() and int(user_ans) == correct_ans:
            correct = True

        if correct:
            score += 1

        feedback.append({
            "question": q["question"],
            "your": user_ans,
            "correct_answer": correct_ans,
            "correct": correct,
            "reasoning": q["reasoning"]
        })

    percent = score / len(quiz_questions) * 100
    if percent == 100:
        message = "Perfect! Congratulations! 🦕"
    elif percent >= 80:
        message = "Great job! You did really well! 🎉"
    elif percent >= 50:
        message = "Good effort! Keep learning! 👍"
    else:
        message = "Try again! You’ve got this! 💪"

    return render_template('results.html', score=score, total=len(quiz_questions), feedback=feedback, message=message)

# Function to generate extra quizzes dynamically
def register_extra_quiz(quiz_name, questions, session_key, route_prefix):
    def q_route(q_num):
        if session_key not in session:
            session[session_key] = {}
        if q_num >= len(questions):
            return redirect(url_for(f"{route_prefix}_results"))

        if request.method == 'POST':
            if str(q_num) not in session[session_key]:
                session[session_key][str(q_num)] = request.form.get('answer')
            next_q = q_num + 1
            if next_q < len(questions):
                return redirect(url_for(f"{route_prefix}_question", q_num=next_q))
            else:
                return redirect(url_for(f"{route_prefix}_results"))

        q = questions[q_num]
        return render_template('extra_question.html', quiz_name=quiz_name, question=q, q_num=q_num, total=len(questions))

    def res_route():
        if session_key not in session:
            return redirect(url_for('home'))

        score = 0
        feedback = []
        for i, q in enumerate(questions):
            user_ans = session[session_key].get(str(i))
            correct = False
            if q["answer"] == -1:
                correct = True
            elif user_ans is not None and user_ans.isdigit() and int(user_ans) == q["answer"]:
                correct = True
                score += 1
            elif correct:
                score += 1
            if correct:
                score += 1
            feedback.append({
                "question": q["question"],
                "your": user_ans,
                "correct_answer": q["answer"],
                "correct": correct,
                "reasoning": q["reasoning"]
            })

        percent = score / len(questions) * 100
        if percent == 100:
            message = "Perfect! 🎯"
        elif percent >= 80:
            message = "Really good job! 👍"
        elif percent >= 50:
            message = "Nice effort! 😊"
        else:
            message = "Keep trying! 💡"

        return render_template('extra_results.html', quiz_name=quiz_name, score=score, total=len(questions), feedback=feedback, message=message)

    app.add_url_rule(f"/{route_prefix}/question/<int:q_num>", f"{route_prefix}_question", q_route, methods=["GET", "POST"])
    app.add_url_rule(f"/{route_prefix}/results", f"{route_prefix}_results", res_route)

# Register extra quizzes
register_extra_quiz("Extra Eras Quiz", extra_eras_questions, "eras_answers", "extra_eras")
register_extra_quiz("Extra Species Quiz", extra_species_questions, "species_answers", "extra_species")
register_extra_quiz("Extra Environment Quiz", extra_environment_questions, "environment_answers", "extra_environment")

# Info and cards pages
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/cards')
def cards():
    return render_template('cards.html', cards=archasaur_cards)

@app.route('/search_cards', methods=['POST'])
def search_cards():
    query = request.form.get('query', "").lower()
    matched = [c for c in archasaur_cards if query in c["name"].lower()]
    return jsonify(matched)

@app.route('/retake')
def retake():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
