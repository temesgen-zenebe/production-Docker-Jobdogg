let stream;
let mediaRecorder;
let recordedChunks = [];
let isRecording = false;
let recordedBlob;
const videoPlayer = document.getElementById('videoPlayer');
const userName = document.getElementById('user-name');


function generateUniqueID() {
  const alphanumericChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let uniqueID = '';

  for (let i = 0; i < 8; i++) {
    const randomIndex = Math.floor(Math.random() * alphanumericChars.length);
    uniqueID += alphanumericChars[randomIndex];
  }

  return uniqueID + userName.innerText;
}

const startRecording = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    videoPlayer.srcObject = stream;
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.addEventListener('dataavailable', event => {
      recordedChunks.push(event.data);
    });

    mediaRecorder.addEventListener('stop', () => {
      recordedBlob = new Blob(recordedChunks, { type: 'video/webm' });
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
  return recordedBlob
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



const recordAgain = () => {
  // Remove the previous recorded video from local storage
  localStorage.removeItem('recordedVideo');
  videoPlayer.srcObject = stream;
  startRecording();

};


const submitVideo = () => {
  const recordedVideoURL = URL.createObjectURL(recordedBlob);
  if (recordedVideoURL) {
    const link = document.createElement('a');
    link.href = recordedVideoURL;
    link.download = generateUniqueID()+'jobdogg-recordedVideo.webm';
    link.click();

    var submit2 = document.getElementById('submit2');
    var submit1 = document.getElementById('submit1');
    submit2.classList.remove('d-none');
    submit2.classList.add('d-block');
    submit1.classList.remove('d-block');
    submit1.classList.add('d-none');
  }
};
