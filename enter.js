// Конфигурация Lesta OpenID
const LESTA_OPENID_CONFIG = {
    clientId: "1377836fd8c2ecb2382bb3dd08d1f071", // Ваш Client ID
    authUrl: "https://openid.lesta.ru/auth",
    tokenUrl: "https://openid.lesta.ru/token",
    userInfoUrl: "https://openid.lesta.ru/userinfo",
    redirectUri: encodeURIComponent(window.location.origin + "/auth/callback"),
    responseType: "code",
    scope: "openid profile email",
};

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.getElementById("loginButton");

    if (loginButton) {
        loginButton.addEventListener("click", initiateLestaAuth);
    }

    // Проверяем, находимся ли мы на странице callback
    if (window.location.pathname.includes("auth/callback")) {
        handleLestaCallback();
    }
});

// Инициализация аутентификации
function initiateLestaAuth(event) {
    event.preventDefault();

    const state = generateRandomString(16);
    localStorage.setItem("lesta_auth_state", state);

    const authUrl = `${LESTA_OPENID_CONFIG.authUrl}?client_id=${LESTA_OPENID_CONFIG.clientId}&redirect_uri=${LESTA_OPENID_CONFIG.redirectUri}&response_type=${LESTA_OPENID_CONFIG.responseType}&scope=${LESTA_OPENID_CONFIG.scope}&state=${state}`;

    window.location.href = authUrl;
}

// Обработка callback
function handleLestaCallback() {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const state = params.get("state");
    const error = params.get("error");

    if (error) {
        console.error("Ошибка аутентификации:", params.get("error_description"));
        showAuthError(params.get("error_description"));
        return;
    }

    const savedState = localStorage.getItem("lesta_auth_state");
    if (state !== savedState) {
        console.error("Несоответствие state параметра");
        showAuthError("Ошибка безопасности. Попробуйте снова.");
        return;
    }

    if (code) {
        exchangeCodeForToken(code)
            .then(() => {
                // Перенаправляем на главную страницу после успешной аутентификации
                window.location.href = "/index.html";
            })
            .catch(error => {
                console.error("Ошибка при обмене кода на токен:", error);
                showAuthError(error.message);
            });
    }
}

// Обмен кода на токен
async function exchangeCodeForToken(code) {
    try {
        const response = await fetch("/api/auth/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                code,
                redirect_uri: decodeURIComponent(LESTA_OPENID_CONFIG.redirectUri),
            }),
        });

        if (!response.ok) {
            throw new Error("Ошибка сервера при получении токена");
        }

        const data = await response.json();

        // Сохраняем токен в localStorage
        localStorage.setItem("lesta_access_token", data.access_token);
        localStorage.setItem("lesta_refresh_token", data.refresh_token);

        // Получаем информацию о пользователе
        return getUserInfo(data.access_token);
    } catch (error) {
        console.error("Ошибка при обмене кода на токен:", error);
        throw error;
    }
}

// Получение информации о пользователе
async function getUserInfo(accessToken) {
    try {
        const response = await fetch(LESTA_OPENID_CONFIG.userInfoUrl, {
            headers: {
                "Authorization": `Bearer ${accessToken}`,
            },
        });

        if (!response.ok) {
            throw new Error("Ошибка при получении информации о пользователе");
        }

        const userInfo = await response.json();

        // Сохраняем информацию о пользователе
        localStorage.setItem("lesta_user_info", JSON.stringify(userInfo));

        return userInfo;
    } catch (error) {
        console.error("Ошибка при получении информации о пользователе:", error);
        throw error;
    }
}

// Показать ошибку аутентификации
function showAuthError(message) {
    const errorElement = document.createElement("div");
    errorElement.className = "alert alert-danger";
    errorElement.textContent = message;

    document.body.prepend(errorElement);

    setTimeout(() => {
        errorElement.remove();
    }, 5000);
}

// Генерация случайной строки
function generateRandomString(length) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// Проверка аутентификации
export function isAuthenticated() {
    return !!localStorage.getItem("lesta_access_token");
}

// Получение токена
export function getAccessToken() {
    return localStorage.getItem("lesta_access_token");
}

// Выход
export function logout() {
    localStorage.removeItem("lesta_access_token");
    localStorage.removeItem("lesta_refresh_token");
    localStorage.removeItem("lesta_user_info");
    localStorage.removeItem("lesta_auth_state");
    window.location.href = "/index.html";
}
