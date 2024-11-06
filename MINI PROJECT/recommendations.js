document.addEventListener('DOMContentLoaded', async () => {
    const category = localStorage.getItem('selectedCategory');
    const type = localStorage.getItem('userType');
    const concern = localStorage.getItem('userConcern');

    try {
        const response = await fetch(`/api/products?category=${category}&type=${type}&concern=${concern}`, {
            credentials: 'include'
        });

        if (response.ok) {
            const products = await response.json();
            const productList = document.getElementById('productList');

            products.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.className = 'product';
                productDiv.innerHTML = `
                    <h3>${product.name}</h3>
                    <p>Type: ${product.type}</p>
                    <p>Concern: ${product.concern}</p>
                    <a href="${product.link}" target="_blank">View Product</a>
                `;
                productList.appendChild(productDiv);
            });
        } else {
            const data = await response.json();
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
});