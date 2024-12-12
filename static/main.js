// DOM elements
const aphorismText = document.getElementById('aphorism-text');
const aphorismAuthor = document.getElementById('aphorism-author');
const message = document.getElementById('message');

// Fetch and display a random aphorism
document.getElementById('new-aphorism-btn').addEventListener('click', () => {
    fetch('/get_random_aphorism')
        .then(response => response.json())
        .then(data => {
            aphorismText.textContent = `"${data.text}"`;
            aphorismAuthor.textContent = `– ${data.author}`;
        })
        .catch(err => {
            console.error('Error fetching aphorism:', err);
            aphorismText.textContent = 'Could not load aphorism.';
            aphorismAuthor.textContent = '';
        });
});

// Add a new aphorism
document.getElementById('aphorism-form').addEventListener('submit', (event) => {
    event.preventDefault();

    const newAphorism = document.getElementById('new-aphorism').value;
    const newAuthor = document.getElementById('new-author').value;

    fetch('/add_aphorism', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `aphorism=${encodeURIComponent(newAphorism)}&author=${encodeURIComponent(newAuthor)}`
    })
        .then(response => response.json())
        .then(data => {
            message.textContent = data.message;
            document.getElementById('aphorism-form').reset();
        })
        .catch(err => {
            console.error('Error adding aphorism:', err);
            message.textContent = 'Failed to add aphorism.';
        });
});
