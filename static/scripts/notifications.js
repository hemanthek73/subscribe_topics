function getUserNotifications() {
  // Get the user ID entered in the input box
  const userId = document.getElementById('userId').value;

  if (!userId) {
    alert('Please enter a user ID');
    return;
  }

  // Send the GET request to the backend to fetch notifications
  fetch(`http://127.0.0.1:5000/notifications/${userId}`)
    .then(response => response.json())
    .then(data => {
      if (data.new_topics && data.new_topics.length > 0) {
        // If there are new topics, display them in the list
        let topicList = data.new_topics.map(topic => `
          <li>Topic: ${topic.name} (ID: ${topic.topic_id})</li>
        `).join('');
        document.getElementById('notificationList').innerHTML = topicList;
      } else {
        // If no new topics, notify the user
        document.getElementById('notificationList').innerHTML = '<li>No new topics for you!</li>';
      }
    })
    .catch(error => console.error('Error fetching notifications:', error));
}