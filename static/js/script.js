# ----- Ячейка 5: Создание JavaScript-файла -----
%%writefile static/js/script.js
// Вставьте сюда ВЕСЬ код JS (версия с AI), но с одним изменением в fetch
document.addEventListener('DOMContentLoaded', () => {
    const preferencesForm = document.getElementById('preferences-form');
    const generateButton = document.getElementById('generate-button');
    const namesList = document.getElementById('names-list');
    const resultsSection = document.getElementById('results-section');
    const favoriteNamesList = document.getElementById('favorite-names-list');
    let favorites = [];

    async function generateNames(event) {
        event.preventDefault();
        const buttonOriginalText = generateButton.innerHTML;
        generateButton.innerHTML = "Думаем... 🤔";
        generateButton.disabled = true;

        const selectedGender = document.querySelector('input[name="gender"]:checked').value;
        const selectedChars = Array.from(document.querySelectorAll('input[name="character"]:checked')).map(el => el.value).join(', ');
        const selectedStyle = document.querySelector('input[name="style"]:checked').value;
        const keywords = document.getElementById('keywords').value;

        let prompt = `Сгенерируй 10 креативных и подходящих имен для домашнего питомца. Важно: верни ответ в виде чистого JSON-массива строк, например: ["Имя1", "Имя2", "Имя3"]. Никакого лишнего текста или форматирования. Вот информация о питомце: - Пол: ${selectedGender} - Характер: ${selectedChars || 'не указан'} - Желаемый стиль имени: ${selectedStyle} - Ключевые слова и ассоциации от владельца: ${keywords || 'нет'}`;

        try {
            // ВАЖНОЕ ИЗМЕНЕНИЕ! Путь стал относительным.
            const response = await fetch('/generate-names', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt }),
            });

            if (!response.ok) throw new Error(`Ошибка сервера: ${response.statusText}`);
            const data = await response.json();
            displayNames(data.names);
        } catch (error) {
            console.error("Ошибка:", error);
            namesList.innerHTML = '<p>Ой, что-то пошло не так... Попробуйте еще раз!</p>';
            resultsSection.style.display = 'block';
        } finally {
            generateButton.innerHTML = buttonOriginalText;
            generateButton.disabled = false;
        }
    }

    function displayNames(names) {
        namesList.innerHTML = '';
        if (!names || names.length === 0) {
            namesList.innerHTML = '<p>AI не смог придумать имена... Попробуйте другие настройки!</p>';
        } else {
            names.forEach(name => {
                const isFavorited = favorites.includes(name);
                const card = `<div class="name-card"><span>${name}</span><button class="favorite-button ${isFavorited ? 'favorited' : ''}" data-name="${name}" aria-label="Добавить в избранное">♥</button></div>`;
                namesList.insertAdjacentHTML('beforeend', card);
            });
        }
        resultsSection.style.display = 'block';
    }

    function toggleFavorite(event) {
        const button = event.target.closest('.favorite-button');
        if (!button) return;
        const name = button.dataset.name;
        if (favorites.includes(name)) {
            favorites = favorites.filter(fav => fav !== name);
            button.classList.remove('favorited');
        } else {
            favorites.push(name);
            button.classList.add('favorited');
        }
        updateFavoritesList();
        saveFavoritesToLocalStorage();
    }

    function updateFavoritesList() {
        favoriteNamesList.innerHTML = '';
        favorites.forEach(name => {
            const li = document.createElement('li');
            li.textContent = name;
            favoriteNamesList.appendChild(li);
        });
    }

    function saveFavoritesToLocalStorage() {
        localStorage.setItem('vibePetNamesFavorites', JSON.stringify(favorites));
    }

    function loadFavoritesFromLocalStorage() {
        const storedFavorites = localStorage.getItem('vibePetNamesFavorites');
        if (storedFavorites) favorites = JSON.parse(storedFavorites);
    }

    resultsSection.style.display = 'none';
    loadFavoritesFromLocalStorage();
    updateFavoritesList();
    preferencesForm.addEventListener('submit', generateNames);
    namesList.addEventListener('click', toggleFavorite);
});