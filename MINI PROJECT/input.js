document.addEventListener('DOMContentLoaded', () => {
    const category = localStorage.getItem('selectedCategory');
    document.getElementById('categoryTitle').textContent = `${category.charAt(0).toUpperCase() + category.slice(1)} Recommendations`;

    const typeSelect = document.getElementById('type');
    if (category === 'skincare') {
        const skinTypes = ['dry', 'oily', 'combination', 'sensitive', 'mature'];
        skinTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type.charAt(0).toUpperCase() + type.slice(1);
            typeSelect.appendChild(option);
        });
    } else if (category === 'haircare') {
        const hairTypes = ['straight', 'wavy', 'curly', 'coily', 'fine', 'thick', 'damaged', 'colored'];
        hairTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type.charAt(0).toUpperCase() + type.slice(1);
            typeSelect.appendChild(option);
        });
    }
});

document.getElementById('userInputForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const category = localStorage.getItem('selectedCategory');
    const type = document.getElementById('type').value;
    const concern = document.getElementById('concern').value;

    localStorage.setItem('userType', type);
    localStorage.setItem('userConcern', concern);

    window.location.href = 'recommendations.html';
});