document.getElementById('reviewForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const rating = document.getElementById('rating').value;
    const comment = document.getElementById('comment').value;

    try {
        const response = await fetch('/api/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rating, comment }),
            credentials: 'include'
        });

        if (response.ok) {
            alert('Thank you for your review!');
            window.location.href = 'category.html';
        } else {
            const data = await response.json();
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});