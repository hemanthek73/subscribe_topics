// document.getElementById('subscribeForm').addEventListener('submit', function(event) {
//   event.preventDefault();

//   const userId = document.getElementById('userId').value;
//   const topicId = document.getElementById('topicId').value;

//   // Validate input
//   if (!userId || !topicId) {
//     alert('Please enter User ID and Topic ID');
//     return;
//   }

//   // Send POST request to Flask API to subscribe to the topic
//   fetch('http://127.0.0.1:5000/subscribe', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/x-www-form-urlencoded'
//     },
//     body: new URLSearchParams({
//       'user_id': userId,
//       'topic_id': topicId
//     }).toString() // URL-encode the data
//   })
//   .then(response => response.json())
//   .then(data => {
//     console.log(data);
//     if (data.message) {
//       alert('Successfully subscribed to the topic');
//     } else {
//       alert('Error: ' + data.error);
//     }
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });
// });
document.addEventListener('DOMContentLoaded', () => {
  const userIdInput = document.getElementById('userId');
  const topicDropdownContainer = document.getElementById('topicDropdownContainer');
  const topicIdDropdown = document.getElementById('topicId');
  const subscribeForm = document.getElementById('subscribeForm');

  // Function to fetch topics dynamically from the server
  const fetchTopics = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/topics'); // Endpoint to get topics
      if (!response.ok) {
        throw new Error('Failed to fetch topics');
      }
      const topics = await response.json();

      // Populate the dropdown with fetched topics
      topicIdDropdown.innerHTML = `<option value="" disabled selected>Select a Topic</option>`;
      topics.forEach(topic => {
        const option = document.createElement('option');
        option.value = topic.id;
        option.textContent = topic.name;
        topicIdDropdown.appendChild(option);
      });
    } catch (error) {
      console.error('Error fetching topics:', error);
      alert('Failed to load topics. Please try again later.');
    }
  };

  // Event listener to show dropdown when User ID is entered
  userIdInput.addEventListener('input', () => {
    if (userIdInput.value.trim() !== '') {
      topicDropdownContainer.style.display = 'block';
      fetchTopics(); // Fetch and populate topics when the dropdown is displayed
    } else {
      topicDropdownContainer.style.display = 'none';
    }
  });

  // Event listener for form submission
  subscribeForm.addEventListener('submit', function (event) {
    event.preventDefault();

    const userId = userIdInput.value;
    const topicId = topicIdDropdown.value;

    // Validate input
    if (!userId || !topicId) {
      alert('Please enter User ID and select a Topic');
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
        if (data.message) {
          alert('Successfully subscribed to the topic');
        } else {
          alert('Error: ' + data.error);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to subscribe. Please try again later.');
      });
  });
});
