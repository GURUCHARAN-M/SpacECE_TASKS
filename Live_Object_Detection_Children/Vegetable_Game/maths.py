import streamlit as st
from time import time
from random import randint, shuffle
import pickle
import bisect

# Constants
NTIMES = 10
SUBTRACTION = True
MULTIPLICATION = True
LO = 0
HI = 10
HIGHSCORE_FNAME = "highscores"

# HighScores Class
class HighScores:
    def __init__(self):
        self.scores = []
        self.num_scores = 10

    def update(self, score):
        """Add a score to the list of high scores.
        Return True if this score is among the top scores, otherwise False.
        """
        if len(self.scores) < self.num_scores:
            self.scores.append(score)
            self.scores.sort()
            return True
        index = bisect.bisect(self.scores, score)
        if index < self.num_scores:
            self.scores.insert(index, score)
            self.scores.pop()
            return True
        return False

    def __str__(self):
        return "\n".join([f"{i + 1:2d}) {score:.2f} sec" for i, score in enumerate(self.scores)])

# Helper Functions
def load_scores():
    try:
        with open(HIGHSCORE_FNAME, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return HighScores()


def save_scores(scores):
    with open(HIGHSCORE_FNAME, 'wb') as f:
        pickle.dump(scores, f)


def generate_question():
    a = randint(LO, HI)
    b = randint(LO, HI)
    question_type = randint(0, 2)  # 0 = addition, 1 = subtraction, 2 = multiplication

    if question_type == 1 and SUBTRACTION:  # Subtraction
        question = f"{a + b} - {b} = ?"
        correct_answer = a
    elif question_type == 2 and MULTIPLICATION:  # Multiplication
        question = f"{a} × {b} = ?"
        correct_answer = a * b
    else:  # Addition
        question = f"{a} + {b} = ?"
        correct_answer = a + b

    options = [correct_answer]
    while len(options) < 4:
        wrong_answer = randint(LO - 5, HI + 5)
        if wrong_answer != correct_answer:
            options.append(wrong_answer)

    shuffle(options)
    return question, options, correct_answer

# Initialize Session State
if "score" not in st.session_state:
    st.session_state.update({
        "score": 0,
        "start_time": None,
        "message": "",
        "current_question": None,
        "correct_answer": None,
        "answered": False,
        "option_selected": None,
    })

# Header and Theme
st.title("🎉 Fun Maths Game for Kids! 🎈")
st.markdown(
    """Welcome to the **Maths Game**! Solve the questions and try to get the fastest score.
    
    🧮 Add, subtract, or multiply numbers, pick the correct answer, and see if you can make it to the **High Scores**! Good luck!
    """
)

st.image("https://via.placeholder.com/800x200.png?text=Welcome+to+the+Maths+Adventure!", use_column_width=True)

# Start the Game
if st.session_state.start_time is None:
    st.session_state.start_time = time()

# Generate a Question
if st.session_state.score < NTIMES and st.session_state.current_question is None:
    question, options, correct_answer = generate_question()
    st.session_state.current_question = (question, options)
    st.session_state.correct_answer = correct_answer

# Display the Question
if st.session_state.current_question:
    question, options = st.session_state.current_question

    st.header(f"🦄 Question {st.session_state.score + 1}:")
    st.subheader(question)

    option_selected = st.radio("Choose your answer:", options, key=f"q{st.session_state.score}")

    if st.button("🐾 Submit Answer") and not st.session_state.answered:
        st.session_state.option_selected = option_selected
        st.session_state.answered = True

    if st.session_state.answered:
        if st.session_state.option_selected == st.session_state.correct_answer:
            st.success("🎉 Hooray! That's correct! You're amazing! 🐻")
            st.balloons()
            st.session_state.score += 1
        else:
            st.error(f"❌ Oh no! The correct answer is {st.session_state.correct_answer}. Keep going, you got this! 🐢")
        
        st.write(f"🌟 Your current score: {st.session_state.score}/{NTIMES}")

        if st.button("🔄 Next Question"):
            st.session_state.answered = False
            st.session_state.current_question = None
            st.experimental_rerun()  # Rerun the app to show the next question

# End of Game
if st.session_state.score == NTIMES:
    elapsed = time() - st.session_state.start_time
    st.balloons()
    st.image("https://via.placeholder.com/800x200.png?text=You+Did+It!", use_column_width=True)
    st.write(f"🎯 **Fantastic!** You completed the game in {elapsed:.2f} seconds! 🏆")

    highscores = load_scores()
    if highscores.update(elapsed):
        st.success(f"🏅 Congratulations! You made it to the top {highscores.num_scores} scores!")

    st.write("📜 **High Scores:**")
    st.text(highscores)
    save_scores(highscores)

    st.write("🎉 **Your Score:**")
    st.write(f"⏱️ Time: {elapsed:.2f} seconds")

    st.session_state.score = 0
    st.session_state.start_time = None
    st.session_state.current_question = None
    st.experimental_rerun()  # Reset the app after the game ends

# Quit Button
if st.button("🚪 Quit"):
    st.session_state.score = 0
    st.session_state.start_time = None
    st.write("🚪 Game has been quit. Refresh the page to restart.")
