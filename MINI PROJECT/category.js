function selectCategory(category) {
    localStorage.setItem('selectedCategory', category);
    window.location.href = 'input.html';
}