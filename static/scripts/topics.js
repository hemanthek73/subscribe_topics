document.getElementById('createTopicForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const topicName = document.getElementById('topicName').value;

  // Validate input
  if (!topicName) {
    alert('Topic name is required');
    return;
  }

  // Send POST request to Flask API
  fetch('http://127.0.0.1:5000/topics', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'topic_name': topicName
    }).toString() // URL-encode the data
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    if (data.topic_id) {
      alert('Topic created successfully with ID: ' + data.topic_id);
    } else {
      alert('Error: ' + data.error);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});