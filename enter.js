document.getElementById('loginButton').addEventListener('click', function() {
    // Переход на страницу авторизации
    window.location.href = 'https://api.tanki.su/wot/auth/login/?language=ru&application_id=1377836fd8c2ecb2382bb3dd08d1f071';
});

// После успешной авторизации пользователь будет перенаправлен обратно на ваш сайт
// Вам нужно будет обработать URL, чтобы получить access_token
window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const accessToken = urlParams.get('access_token'); // Предполагается, что access_token передается в URL

    if (accessToken) {
        // Выводим access_token на экран
        document.body.innerHTML += `<p>Access Token: ${accessToken}</p>`;
    }
};