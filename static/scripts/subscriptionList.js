function fetchSubscribedTopics() {
  // Get the user ID from input
  const userId = document.getElementById('userId').value;
  
  if (!userId) {
    alert("Please enter a User ID");
    return;
  }

  // Fetch subscribed topics from the API
  fetch(`http://127.0.0.1:5000/subscriptions/${userId}`)
    .then(response => response.json())
    .then(data => {
      const subscriptionList = document.getElementById('subscriptionList');
      subscriptionList.innerHTML = ''; // Clear previous results

      // Check if there are any subscribed topics
      if (data.subscribed_topics && data.subscribed_topics.length > 0) {
        data.subscribed_topics.forEach(topic => {
          // Create a list item for each subscribed topic
          const listItem = document.createElement('li');
          listItem.className = 'list-group-item';
          listItem.textContent = `ID: ${topic.topic_id} - ${topic.name}`;
          subscriptionList.appendChild(listItem);
        });
      } else {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.textContent = "No subscriptions found for this user.";
        subscriptionList.appendChild(listItem);
      }
    })
    .catch(error => {
      console.error('Error fetching subscriptions:', error);
      alert('Error fetching subscriptions. Please check the console for details.');
    });
}