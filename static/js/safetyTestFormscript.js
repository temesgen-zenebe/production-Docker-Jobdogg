$(document).ready(function() {
    $('#safety-test-form').on('submit', function(event) {
      event.preventDefault();
      
      // Get the user's answers
      var answers = {
        q1: $('#q1').val(),
        q2: $('#q2').val(),
        // Add more answers here
      };
      
      // Evaluate the answers
      var correctAnswers = {
        q1: 'c',
        q2: 'A',
        // Add more correct answers here
      };
      
      var score = 0;
      var totalQuestions = 0;
      
      for (var question in answers) {
        if (answers.hasOwnProperty(question)) {
          totalQuestions++;
          if (answers[question] === correctAnswers[question]) {
            score++;
          }
        }
      }
      
      var passPercentage = 70; // Adjust the pass percentage as needed
      
      // Calculate the result
      var result = (score / totalQuestions) * 100;
      var pass = result >= passPercentage;
      
      // Display the result
      var resultMessage = pass ? 'Congratulations! You passed the test.' : 'Sorry, you did not pass the test. Please retake it.';
      $('#result').html('<h3>Result: ' + resultMessage + '</h3>');
      
      // Update profile building process state using AJAX
      if (pass) {
        var postData = {
          result: result,
          passed: true
        };
        
        $.ajax({
          type: 'POST',
          url: '/update-profile-building-process', // Replace with your Django endpoint URL
          data: postData,
          success: function(response) {
            console.log('Profile building process updated successfully.');
          },
          error: function(xhr, status, error) {
            console.error('An error occurred while updating the profile building process:', error);
          }
        });
      }
    });
  });
  