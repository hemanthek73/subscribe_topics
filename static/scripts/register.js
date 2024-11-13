      document.getElementById('registerForm').addEventListener('submit', function(event) {
          event.preventDefault();
  
          const username = document.getElementById('username').value;
  
          // Validate input
          if (!username) {
              alert('Username is required');
              return;
          }
  
          // Send POST request to Flask API
          fetch('http://127.0.0.1:5000/register', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
              },
              body: new URLSearchParams({
                  'username': username
              }).toString() // Make sure to convert the data into a URL-encoded string
          })
          .then(response => response.json())
          .then(data => {
              console.log(data);
              if (data.user_id) {
                  alert('User registered successfully with ID: ' + data.user_id);
              } else {
                  alert('Error: ' + data.error);
              }
          })
          .catch(error => {
              console.error('Error:', error);
          });
      });

  