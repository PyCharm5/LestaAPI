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
        input, select {
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
        .tank-list {
            margin-top: 20px;
        }
        .tank-item {
            cursor: pointer;
            margin: 5px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .tank-info {
            margin-top: 20px;
        }
    </style>
</head>
<body>

<h1>Поиск игрока</h1>

<main>
    <input type="text" id="nickname" placeholder="Введите никнейм или ID">
    <button id="searchButton">Поиск</button>
    <div class="result" id="resultLabel"></div>

    <h1>Поиск танка</h1>
    <select id="nation">
        <option value="">Выберите нацию</option>
        <option value="ussr">СССР</option>
        <option value="germany">Германия</option>
        <option value="usa">США</option>
        <option value="france">Франция</option>
        <option value="uk">Великобритания</option>
        <option value="china">Китай</option>
        <option value="japan">Япония</option>
    </select>
    <select id="tier">
        <option value="">Выберите уровень</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
        <option value="5">5</option>
        <option value="6">6</option>
        <option value="7">7</option>
        <option value="8">8</option>
        <option value="9">9</option>
        <option value="10">10</option>
    </select>
    <select id="type">
        <option value="">Выберите тип техники</option>
        <option value="lightTank">Легкий</option>
        <option value="mediumTank">Средний</option>
        <option value="heavyTank">Тяжелый</option>
        <option value="AT-SPG">ПТ-САУ</option>
    </select>
    <button id="searchTankButton">Поиск танка</button>
    <div class="tank-list" id="tankList"></div>
    <div class="tank-info" id="tankInfo"></div>
</main>

<footer>
    © Леста Игры, 2022–2025. Игры «Мир танков», «Мир кораблей», Tanks Blitz основаны на интеллектуальной собственности третьих лиц. Все права на объекты прав третьих лиц принадлежат их законным правообладателям.
</footer>

<script>
    const YOUR_API_KEY = "1377836fd8c2ecb2382bb3dd08d1f071"; // Замените на ваш API ключ

    document.getElementById('searchButton').addEventListener('click', function() {
        const nickname = document.getElementById('nickname').value;
        getPlayerStats(nickname);
    });

    document.getElementById('searchTankButton').addEventListener('click', function() {
        const nation = document.getElementById('nation').value;
        const tier = document.getElementById('tier').value;
        const type = document.getElementById('type').value;
        searchTank(nation, tier, type);
    });

    function searchTank(nation, tier, type) {
        let url = `https://papi.tanksblitz.ru/wotb/encyclopedia/vehicles/?application_id=${YOUR_API_KEY}`;
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Ошибка сети");
                }
                return response.json();
            })
            .then(data => {
                if (data.data) {
                    const tanks = Object.values(data.data);
                    const filteredTanks = tanks.filter(tank => {
                        return (!nation || tank.nation === nation) &&
                               (!tier || tank.tier == tier) &&
                               (!type || tank.type === type);
                    });
                    displayTankList(filteredTanks);
                } else {
                    alert("Танки не найдены.");
                }
            })
            .catch(error => {
                alert(`Ошибка: ${error.message}`);
            });
    }

    function displayTankList(tanks) {
        const tankListDiv = document.getElementById('tankList');
        tankListDiv.innerHTML = ''; // Очистка предыдущих результатов

        if (tanks.length === 0) {
            tankListDiv.textContent = 'Танки не найдены.';
            return;
        }

        tanks.forEach(tank => {
            const tankItem = document.createElement('div');
            tankItem.className = 'tank-item';
            tankItem.textContent = `${tank.name} (ID: ${tank.tank_id})`;
            tankItem.addEventListener('click', () => displayTankInfo(tank));
            tankListDiv.appendChild(tankItem);
        });
    }

    function displayTankInfo(tank) {
        const tankInfoDiv = document.getElementById('tankInfo');
        const isPremium = tank.is_premium ? "Да" : "Нет";
        const firepower = tank.default_profile.firepower;
        const hp = tank.default_profile.hp;
        const speed = tank.default_profile.speed_forward;
        const armor = tank.default_profile.armor;
        const dispersion = tank.default_profile.gun.dispersion;
        const reloadTime = tank.default_profile.gun.reload_time;

        const tankDetails = `
            <h2>${tank.name} (ID: ${tank.tank_id}) </h2>
            <p>Нация: ${tank.nation}</p>
            <p>Уровень: ${tank.tier}</p>
            <p>Тип: ${tank.type}</p>
            <p>Премиум: ${isPremium}</p>
            <p>Огневая мощь: ${firepower}%</p>
            <p>Прочность: ${hp}</p>
            <p>Максимальная скорость: ${speed} км/ч</p>
            <p>Броня:</p>
            <ul>
                <li>Башня (лоб): ${armor.turret.front}</li>
                <li>Башня (бок): ${armor.turret.sides}</li>
                <li>Башня (зад): ${armor.turret.rear}</li>
                <li>Корпус (лоб): ${armor.hull.front}</li>
                <li>Корпус (бок): ${armor.hull.sides}</li>
                <li>Корпус (зад): ${armor.hull.rear}</li>
            </ul>
            <p>Разброс на 100 м: ${dispersion}</p>
            <p>Время перезарядки: ${reloadTime} с</p>
        `;
        tankInfoDiv.innerHTML = tankDetails;
    }

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
