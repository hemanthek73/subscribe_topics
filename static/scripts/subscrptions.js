document.getElementById('subscribeForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const userId = document.getElementById('userId').value;
  const topicId = document.getElementById('topicId').value;

  // Validate input
  if (!userId || !topicId) {
    alert('Please enter User ID and Topic ID');
    return;
  }

  // Send POST request to Flask API to subscribe to the topic
  fetch('http://127.0.0.1:5000/subscribe', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'user_id': userId,
      'topic_id': topicId
    }).toString() // URL-encode the data
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    if (data.message) {
      alert('Successfully subscribed to the topic');
    } else {
      alert('Error: ' + data.error);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});
