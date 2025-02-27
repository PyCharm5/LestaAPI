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
            text-align: center;
        }
        input, select {
            width: 300px;
            padding: 10px;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 15px;
            font-size: 16px;
            background-color: #007bff; /* Синий цвет */
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3; /* Темнее при наведении */
        }
        .result {
            margin-top: 20px;
            font-size: 20px;
            text-align: center;
        }
        .tank-list, .clan-list {
            margin-top: 20px;
        }
        .tank-item, .clan-item {
            cursor: pointer;
            margin: 5px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .tank-info, .clan-info {
            margin-top: 20px;
        }
        hr {
            border: 1px solid #ccc;
            margin: 20px 0;
        }
    </style>
</head>
<body>

<h1>Поиск игрока</h1>

<main>
    <input type="text" id="nickname" placeholder="Введите никнейм или ID">
    <button id="searchButton">Поиск</button>
    <div class="result" id="resultLabel"></div>
    <hr>

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
        <option value="european">Сборная Европы</option>
        <option value="other">Сборная нация</option>
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
    <hr>

    <h1>Поиск клана</h1>
    <input type="text" id="clanSearch" placeholder="Введите тег или название клана">
    <button id="searchClanButton">Поиск клана</button>
    <div class="clan-list" id="clanList"></div>
    <div class="clan-info" id="clanInfo"></div>
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

    document.getElementById('searchClanButton').addEventListener('click', function() {
        const clanSearch = document.getElementById('clanSearch').value;
        searchClan(clanSearch);
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
        const isPremium = tank.is_premium ? "Премиум" : "Обычный";
        const firepower = tank.default_profile.firepower;
        const hp = tank.default_profile.hp;
        const speed = tank.default_profile.speed_forward;
        const armor = tank.default_profile.armor;
        const dispersion = tank.default_profile.gun.dispersion;
        const reloadTime = tank.default_profile.gun.reload_time;

        // Сокращенные обозначения типов танков
        const tankTypeMap = {
            "lightTank": "ЛТ",
            "mediumTank": "СТ",
            "heavyTank": "ТТ",
            "AT-SPG": "ПТ-САУ"
        };
        const tankType = tankTypeMap[tank.type] || "Неизвестно";

        // Перевод нации на русский
        const nationMap = {
            "ussr": "СССР",
            "germany": "Германия",
            "usa": "США",
            "france": "Франция",
            "uk": "Великобритания",
            "china": "Китай",
            "japan": "Япония",
            "european": "Сборная Европы",
            "other": "Сборная нация"
        };
        const nation = nationMap[tank.nation] || "Неизвестно";

        const tankDetails = `
            <h2>${tank.name} (ID: ${tank.tank_id}) </h2>
            <img src="${tank.images.normal}" alt="${tank.name}" style="width: 300px;">
            <p>Нация: ${nation}</p>
            <p>Уровень: ${tank.tier}</p>
            <p>Тип: ${tankType}</p>
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

    function searchClan(clanSearch) {
        if (!clanSearch) {
            alert("Пожалуйста, введите тег или название клана.");
            return;
        }

        const url = `https://papi.tanksblitz.ru/wotb/clans/list/?application_id=${YOUR_API_KEY}&search=${clanSearch}`;
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Ошибка сети");
                }
                return response.json();
            })
            .then(data => {
                if (data.data && data.data.length > 0) {
                    displayClanList(data.data);
                } else {
                    alert("Кланы не найдены.");
                }
            })
            .catch(error => {
                alert(`Ошибка: ${error.message}`);
            });
    }

    function displayClanList(clans) {
        const clanListDiv = document.getElementById('clanList');
        clanListDiv.innerHTML = ''; // Очистка предыдущих результатов

        clans.forEach(clan => {
            const clanItem = document.createElement('div');
            clanItem.className = 'clan-item';
            clanItem.textContent = `${clan.tag} - ${clan.name} (ID: ${clan.clan_id})`;
            clanItem.addEventListener('click', () => displayClanInfo(clan.clan_id));
            clanListDiv.appendChild(clanItem);
        });
    }

    function displayClanInfo(clanId) {
        const url = `https://papi.tanksblitz.ru/wotb/clans/info/?application_id=${YOUR_API_KEY}&clan_id=${clanId}`;
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Ошибка сети");
                }
                return response.json();
            })
            .then(data => {
                if (data.data && data.data[clanId]) {
                    const clan = data.data[clanId];
                    const createdAt = new Date(clan.created_at * 1000).toLocaleDateString(); // Преобразование Unix time в обычный формат

                    const clanDetails = `
                        <h2>${clan.name} (${clan.tag})</h2>
                        <p>ID клана: ${clanId}</p>
                        <p>Девиз: ${clan.motto}</p>
                        <p>Описание: ${clan.description}</p>
                        <p>Никнейм главы: ${clan.leader_name}</p>
                        <p>Дата создания: ${createdAt}</p>
                    `;
                    document.getElementById('clanInfo').innerHTML = clanDetails;
                } else {
                    alert("Данные о клане не найдены.");
                }
            })
            .catch(error => {
                alert(`Ошибка: ${error.message}`);
            });
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

    function displayPlayerStats(stats) {
        const resultLabel = document.getElementById('resultLabel');
        resultLabel.innerHTML = `
            <h2>${stats.nickname}</h2>
            <p>Уровень: ${stats.level}</p>
            <p>Боёв: ${stats.battles}</p>
            <p>Побед: ${stats.wins}</p>
            <p>Процент побед: ${((stats.wins / stats.battles) * 100).toFixed(2)}%</p>
        `;
    }
</script>
</body>
</html>
