let stream;
let mediaRecorder;
let recordedChunks = [];
let isRecording = false;
const videoPlayer = document.getElementById('videoPlayer');


const startRecording = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoPlayer.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.addEventListener('dataavailable', event => {
      recordedChunks.push(event.data);
    });

    mediaRecorder.addEventListener('stop', () => {
      const recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
      recordedChunks = [];

      // Save the recorded video to local storage
      const recordedVideoURL = URL.createObjectURL(recordedBlob);
      localStorage.setItem('recordedVideo', recordedVideoURL);
    });

    mediaRecorder.start();
    isRecording = true;

    setTimeout(() => {
      if (isRecording) {
        stopRecording();
      }
    }, 60000); // Stop recording after 1 minute (60000 milliseconds)
  } catch (error) {
    console.error('Error starting the recording:', error);
  }
};


const stopRecording = () => {
  if (isRecording) {
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());
    isRecording = false;
  }
};


const previewVideo = () => {
  const recordedVideoURL = localStorage.getItem('recordedVideo');
  if (recordedVideoURL) {
    videoPlayer.srcObject = null;
    videoPlayer.src = recordedVideoURL;
    videoPlayer.controls = true;
    videoPlayer.autoplay = true;
  }
};

const previewVideo1 = () => {
  const recordedVideoURL = localStorage.getItem('recordedVideo');
  if (recordedVideoURL) {
    const previewVideoElement = document.createElement('video');
    previewVideoElement.src = recordedVideoURL;
    previewVideoElement.controls = true;
    previewVideoElement.autoplay = true;
    
    // Remove previous preview video, if any
    const existingPreviewVideoElement = document.querySelector('#previewVideoElement');
    if (existingPreviewVideoElement) {
      existingPreviewVideoElement.remove();
    }
    
    previewVideoElement.id = 'previewVideoElement';
    videoPlayer.parentNode.insertBefore(previewVideoElement, videoPlayer);
  }
};

const recordAgain = () => {
  // Remove the previous recorded video from local storage
  localStorage.removeItem('recordedVideo');
  videoPlayer.srcObject = stream;
};

const submitVideo = () => {
  const recordedVideoURL = localStorage.getItem('recordedVideo');
  const csrfmiddlewaretoken1 = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  if (recordedVideoURL) {
    // Log the recorded video URL and the fetch request
    console.log('Recorded Video URL:', recordedVideoURL);
    
    const requestOptions = {
      method: 'POST',
      
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', // Set the X-Requested-With header
        'X-CSRFToken': csrfmiddlewaretoken1,
        // Add other required headers if necessary
      },
      
      body: JSON.stringify({ recordedVideoURL }),
    };
    console.log('Fetch Request:', requestOptions);
    
    // Send the recorded video URL to the server using AJAX
    fetch('/recorded-video-resume-submit/', requestOptions)
      .then(response => response.json())
      .then(data => {
        console.log('Video submitted:', data.message);
      })
      .catch(error => {
        console.error('Error submitting video:', error);
      });
  } else {
    console.error('No recorded video available to submit.');
  }
};
