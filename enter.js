// enter.js

// Функция для выполнения запроса
async function fetchAccessToken() {
    const url = 'https://api.tanki.su/wot/auth/login/?application_id=1377836fd8c2ecb2382bb3dd08d1f071&expires_at=1746154041&redirect_uri=index.html';

    try {
        // Отправляем запрос
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Проверяем, успешен ли ответ
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        // Получаем JSON-ответ
        const data = await response.json();

        // Извлекаем access_token
        const accessToken = data.access_token;

        // Выводим access_token на экран
        console.log('Access Token:', accessToken);
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

// Вызываем функцию
fetchAccessToken();
