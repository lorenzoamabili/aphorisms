// Fetch a random aphorism when the "Show a new aphorism" button is clicked
document.getElementById("new-aphorism-btn").addEventListener("click", function() {
    fetch("/get_random_aphorism")
        .then(response => response.json())
        .then(data => {
            document.getElementById("aphorism-text").textContent = `"${data.text}"`;
            document.getElementById("aphorism-author").textContent = `- ${data.author}`;
        })
        .catch(error => {
            console.error("Error fetching aphorism:", error);
        });
});

// Handle the submission of a new aphorism form
document.getElementById("aphorism-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const newAphorism = document.getElementById("new-aphorism").value;
    const newAuthor = document.getElementById("new-author").value;

    const formData = new FormData();
    formData.append("aphorism", newAphorism);
    formData.append("author", newAuthor);

    fetch("/add_aphorism", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").textContent = data.message;
        if (data.message === 'Aphorism added successfully!') {
            // Clear form fields
            document.getElementById("new-aphorism").value = '';
            document.getElementById("new-author").value = '';
        }
    })
    .catch(error => {
        console.error("Error adding aphorism:", error);
        document.getElementById("message").textContent = 'Failed to add aphorism.';
    });
});
