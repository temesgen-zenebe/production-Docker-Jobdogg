$(document).ready(function() {
  $('#safety-test-form').on('submit', function(e) {
    e.preventDefault();
    var answers = {
      q1: $('#q1').val(),
      q2: $('#q2').val(),
      q3: $('#q3').val(),
      q4: $('#q4').val(),
      q5: $('#q5').val(),
      q6: $('#q6').val(),
      q7: $('#q7').val(),
      q8: $('#q8').val(),
      q9: $('#q9').val(),
      q10: $('#q10').val(),
      q11: $('#q11').val(),
      q12: $('#q12').val(),
      q13: $('#q13').val(),
      q14: $('#q14').val(),
      q15: $('#q15').val(),
      q16: $('#q16').val(),
      q17: $('#q17').val(),
      q18: $('#q18').val(),
      q19: $('#q19').val(),
      q20: $('#q20').val(),
      // Add more answers here
    };
    var testContainer = document.getElementById("fromResultCalculator");
    var resultContainer = document.getElementById("fromResultSubmit");
    var safety_result = document.getElementById("id_safety_result");
    var userResultElement = document.getElementById("userResult");
    var userScoreElement = document.getElementById("userScore");
    

    var userResult = '';
    var score = calculateScore(answers);
    if (score >= 80) {
      userResult = 'pass';
    } else {
      userResult = 'fail';
    }

    if (userResult === 'pass') {
      
      autofill(userResult, score);
      resultContainer.classList.remove('d-none');
      resultContainer.classList.add('d-block');
      testContainer.classList.remove('d-block');
      testContainer.classList.add('d-none');

      userResultElement.textContent = userResult;
      userScoreElement.textContent = score;
     
    } else {
      // Prompt the user to retake the test until they pass
      resultNotPass.classList.remove('d-none');
      resultNotPass.classList.add('d-block');
      $('#result').html('<p>Result: ' + userResult + ' with ' + score + '% </p>');
      userResultElement.textContent = "";
      userScoreElement.textContent = "";
      
    }
  });

  function calculateScore(answers) {
    var correctAnswers = {
      q1: 'c',
      q2: 'a',
      q3: 'b',
      q4: 'b',
      q5: 'c',
      q6: 'b',
      q7: 'a',
      q8: 'c',
      q9: 'a',
      q10: 'c',
      q11: 'c',
      q12: 'd',
      q13: 'a',
      q14: 'a',
      q15: 'b',
      q16: 'a',
      q17: 'd',
      q18: 'a',
      q19: 'a',
      q20: 'a'
      // Add more correct answers here
    };

    var totalQuestions = Object.keys(correctAnswers).length;
    var correctCount = 0;

    for (var question in answers) {
      if (answers.hasOwnProperty(question) && correctAnswers.hasOwnProperty(question)) {
        if (answers[question] === correctAnswers[question]) {
          correctCount++;
        }
      }
    }

    var score = (correctCount / totalQuestions) * 100;
    return score;
  }

  function getCookie(name) {
    var cookieArr = document.cookie.split(';');
    for (var i = 0; i < cookieArr.length; i++) {
      var cookiePair = cookieArr[i].split('=');
      if (name.trim() === cookiePair[0].trim()) {
        return decodeURIComponent(cookiePair[1]);
      }
    }
    return null;
  }
  function autofill(states, score) {
    // Set the value of the 'states' field
    document.getElementById('id_states').value = states;
  
    // Set the value of the 'score' field
    document.getElementById('id_safety_result').value = score;

  }

    // Add this code inside the $(document).ready() function
  $('#RefreshForm').on('click', function() {
    resetForm();
    
  });

  function resetForm() {
    // Clear the form fields by resetting the form
    $('#safety-test-form')[0].reset();
  }
});
 
  