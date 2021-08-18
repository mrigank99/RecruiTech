const progressText = document.getElementById('progressText');
const progressBarFull = document.getElementById('progressBarFull');
const scoreContainer = document.getElementById('score');
const endMessage = document.getElementById('TestEnd');

const section1 = document.getElementById('one')
const section2 = document.getElementById('two')
const section3 = document.getElementById('three')

let availableQuesions = [];
let FinalQuestionIndex = 0;

const timerText = document.getElementById('time');
const scoreText = document.getElementById('value');
const startMinuteTime = 30;
let time = startMinuteTime * 60;

let questionCounter = 0;  
let intervalId = 0

//CONSTANTS
//const CORRECT_BONUS = 10;
const QuestionsPerSection = 7; // Number of questions from each section
const MAX_QUESTIONS = 3 * QuestionsPerSection;

// Adding the Timer 
updateTime = () => {
const minutes = Math.floor(time / 60);
let seconds = time % 60;

if (time === 0) {
	alert("You are out of time")
	return window.location.assign('/apptitude');
			   }

time--;
timerText.innerText = ` ${minutes}:${seconds}`;

}

fetch("static/js/questions.json").then((res) => {
return res.json();
}).then((loadedQuestions) => {
questions = loadedQuestions;
(function(){
  // Functions
  function buildQuiz(){

  	
    //Start Timer
    
    intervalId =  setInterval(updateTime,1000);
    
    // variable to store the HTML output
    const output = [];

    // for each question...
    myQuestions.forEach(
      (currentQuestion, questionNumber) => {

        // variable to store the list of possible answers
        const answers = [];

        // and for each available answer...
        for(letter in currentQuestion.answers){

          // ...add an HTML radio button
          answers.push(
            `<label>
              <div class = "choice-container">
              <input type="radio" name="question${questionNumber}" value="${letter}">
              <p class="choice-prefix">${letter}</p>
              <p class="choice-text">${currentQuestion.answers[letter]}</p>
              </div>
            </label>`
          );
        }

        // add this question and its answers to the output
        output.push(
          `<div class="slide">
            <div class="question"> <p style="line-height:1.3"> ${currentQuestion.question} </p></div>
            <div class="answers"> ${answers.join("")} </div>
          </div>`
        );
      }
    );

    // finally combine our output list into one string of HTML and put it on the page
    quizContainer.innerHTML = output.join('');
  }

  function showResults(){

    // gather answer containers from our quiz
    const answerContainers = quizContainer.querySelectorAll('.answers');

    // keep track of user's answers
    let numCorrect = 0;

    // for each question...
    myQuestions.forEach( (currentQuestion, questionNumber) => {

      // find selected answer
      const answerContainer = answerContainers[questionNumber];
      const selector = `input[name=question${questionNumber}]:checked`;
      const userAnswer = (answerContainer.querySelector(selector) || {}).value;

      // if answer is correct
      if(userAnswer === currentQuestion.correctAnswer){
        // add to the number of correct answers
        numCorrect++;

        // color the answers green
        answerContainers[questionNumber].style.color = 'lightgreen';
      }
      // if answer is wrong or blank
      else{
        // color the answers red
        answerContainers[questionNumber].style.color = 'red';
      }
    });
    scoreContainer.style.display = 'block';
    scoreText.innerText = `${numCorrect}`;
    clearInterval(intervalId)

    $.ajax({
          type: "POST",
          contentType: "application/json",
          url: "/update_score",
          traditional: "true",
          data: JSON.stringify(numCorrect),
          dataType: "json"
          });
     document.getElementById('submit').disabled = true
     endMessage.innerText = ` You have completed the test. Please click on "Home" go back to dashboard`;
  }


  function showSlide(n) {

    questionCounter = n+1;
    progressText.innerText = `Question ${questionCounter}/${MAX_QUESTIONS}`;
    //Update the progress bar
    progressBarFull.style.width = `${(questionCounter / MAX_QUESTIONS) * 100}%`;

    slides[currentSlide].classList.remove('active-slide');
    slides[n].classList.add('active-slide');
    currentSlide = n;
    if(currentSlide === 0){
      previousButton.style.display = 'none';
    }
    else{
      previousButton.style.display = 'inline-block';
    }
    if(currentSlide === slides.length-1){
      nextButton.style.display = 'none';
      submitButton.style.display = 'inline-block';
    }
    else{
      nextButton.style.display = 'inline-block';
      submitButton.style.display = 'none';
    }

    if(questionCounter < 8){
      section1.classList.add('active-section');
      section2.classList.remove('active-section');
      section3.classList.remove('active-section');
    }
    else if(questionCounter < 15){
      section2.classList.add('active-section');
      section1.classList.remove('active-section');
      section3.classList.remove('active-section');
    }
    else {
      section3.classList.add('active-section');
      section2.classList.remove('active-section');
      section1.classList.remove('active-section');
    }

  }

  function showNextSlide() {
    showSlide(currentSlide + 1);
  }

  function showPreviousSlide() {
    showSlide(currentSlide - 1);
  }

  // Variables
  const quizContainer = document.getElementById('quiz');
  const resultsContainer = document.getElementById('results');
  const submitButton = document.getElementById('submit');
  const myQuestions = [...questions];

  // Kick things off
  buildQuiz();

  // Pagination
  const previousButton = document.getElementById("previous");
  const nextButton = document.getElementById("next");
  const slides = document.querySelectorAll(".slide");
  let currentSlide = 0;

  // Show the first slide
  showSlide(currentSlide);

  // Event listeners
  submitButton.addEventListener('click', showResults);
  previousButton.addEventListener("click", showPreviousSlide);
  nextButton.addEventListener("click", showNextSlide);
})();
});
