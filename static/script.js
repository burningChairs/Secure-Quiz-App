// Quiz navigation and preventing multiple submissions
function submitAnswer(questionNum, selected) {
    const answeredKey = `q${questionNum}_answered`;
    
    // Prevent multiple submissions
    if (localStorage.getItem(answeredKey)) {
        alert("You have already answered this question.");
        return false;
    }

    // Save answer
    localStorage.setItem(answeredKey, "true");
    localStorage.setItem(`q${questionNum}`, selected);

    // Submit form via hidden input (if using form submission)
    const form = document.getElementById(`question-form-${questionNum}`);
    if (form) {
        form.submit();
    }

    return true;
}

// Show result pop-up based on score
function showResultPopup(score, total) {
    let percent = (score / total) * 100;
    let message = "";

    if (percent === 100) {
        message = "Perfect! 100% - Congratulations!\nThank you for playing!";
    } else if (percent >= 80) {
        message = `Great job! ${Math.round(percent)}% - Well done!\nThank you for playing!`;
    } else if (percent >= 50) {
        message = `Good effort! ${Math.round(percent)}%\nKeep learning!`;
    } else {
        message = `Try again! ${Math.round(percent)}%\nClick OK to retake the quiz.`;
    }

    alert(message);

    // Redirect to home if score is below 50%
    if (percent < 50) {
        window.location.href = '/';
    }
}

// Optional: clear localStorage when retaking quiz
function clearQuizData() {
    Object.keys(localStorage).forEach(key => {
        if (key.startsWith('q')) {
            localStorage.removeItem(key);
        }
    });
}
