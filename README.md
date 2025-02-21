<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BlitzStats - Статистика игроков</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            font-size: 30px;
            font-weight: bold;
        }
        input {
            width: 300px;
            padding: 10px;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 15px;
            font-size: 16px;
        }
        .result {
            margin-top: 20px;
            font-size: 20px;
        }
    </style>
</head>
<body>

    <h1>Поиск игрока</h1>
    <input type="text" id="nickname" placeholder="Введите никнейм или ID">
    <button id="searchButton">Поиск</button>
    <div class="result" id="resultLabel"></div>
    <h4>© Леста Игры, 2022–2025. Игры «Мир танков», «Мир кораблей», Tanks Blitz основаны на интеллектуальной собственности третьих лиц. Все права на объекты прав третьих лиц принадлежат их законным правообладателям.</h4>

    <script>
        const YOUR_API_KEY = "1377836fd8c2ecb2382bb3dd08d1f071"; // Замените на ваш API ключ

        document.getElementById('searchButton').addEventListener('click', function() {
            const nickname = document.getElementById('nickname').value;
            getPlayerStats(nickname);
        });

        function getPlayerStats(nickname) {
            if (!nickname) {
                alert("Пожалуйста, введите никнейм или ID.");
                return;
            }

            const url = `https://papi.tanksblitz.ru/wotb/account/list/?application_id=${YOUR_API_KEY}&search=${nickname}`;
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Ошибка сети");
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.data && data.data.length > 0) {
                        const playerInfo = data.data[0];
                        const accountId = playerInfo.account_id;
                        getPlayerStatistics(accountId);
                    } else {
                        alert("Игрок не найден.");
                    }
                })
                .catch(error => {
                    alert(`Ошибка: ${error.message}`);
                });
        }

        function getPlayerStatistics(accountId) {
            const url = `https://papi.tanksblitz.ru/wotb/account/info/?application_id=${YOUR_API_KEY}&fields=statistics&account_id=${accountId}`;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const stats = data.data[accountId].statistics.all;
                    const battles = stats.battles;
                    const wins = stats.wins;
                    const winRate = (wins / battles * 100) || 0;
                    const averageDamage = (stats.damage_dealt / battles) || 0;

                    const resultText = `Бои: ${battles}<br>Победы: ${wins}<br>Процент побед: ${winRate.toFixed(2)}%<br>Средний урон: ${averageDamage.toFixed(2)}`;
                    document.getElementById('resultLabel').innerHTML = resultText;
                });
        }
    </script>

</body>
</html>
