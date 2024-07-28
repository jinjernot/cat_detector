
function switchStream() {
  fetch('/switch_stream', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
          console.log('Switched to stream:', data.current_stream);
          const videoStream = document.getElementById('video-stream');
          videoStream.src = "/video_feed" + '?' + new Date().getTime();
          console.log('Video stream reloaded:', videoStream.src);
      })
      .catch(error => console.error('Error switching stream:', error));
}

window.switchStream = switchStream;