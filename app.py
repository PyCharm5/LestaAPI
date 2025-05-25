from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']

# Главные маршруты
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter')
def enter():
    auth_url = f"https://api.tanki.su/wot/auth/login/?application_id=1377836fd8c2ecb2382bb3dd08d1f071&redirect_uri={app.config['REDIRECT_URI']}"
    print(auth_url)  # Для отладки
    return render_template('enter.html', auth_url=auth_url)

@app.route('/auth')
def auth():
    # Извлекаем параметры из URL
    access_token = request.args.get('access_token')
    account_id = request.args.get('account_id')
    nickname = request.args.get('nickname')

    if access_token:
        # Сохраняем токен и данные пользователя в сессии
        session['access_token'] = access_token
        session['account_id'] = account_id
        session['nickname'] = nickname

        # Для отладки: выводим токен в консоль
        print(f"Access Token: {access_token}")

        # Перенаправляем пользователя на профиль
        return redirect(url_for('profile'))

    # Если токен отсутствует, перенаправляем на страницу входа
    return redirect(url_for('enter'))

@app.route('/profile')
def profile():
    if 'access_token' not in session:
        return redirect(url_for('enter'))

    stats = get_player_stats(session['account_id'])
    return render_template('profile.html', stats=stats)

@app.route('/exit')
def exit():
    session.clear()
    return render_template('exit.html')

# API Endpoints
@app.route('/api/search_player')
def search_player():
    nickname = request.args.get('nickname')
    if not nickname:
        return jsonify({'error': 'Введите никнейм'}), 400

    response = requests.get(
        f"{app.config['API_URL']}/account/list/?application_id={app.config['API_KEY']}&search={nickname}"
    )
    data = response.json()

    if data.get('data'):
        account_id = data['data'][0]['account_id']
        stats = get_player_stats(account_id)
        return jsonify(stats)
    return jsonify({'error': 'Игрок не найден'}), 404

@app.route('/api/search_tank')
def search_tank():
    nation = request.args.get('nation')
    tier = request.args.get('tier')
    tank_type = request.args.get('type')

    try:
        response = requests.get(
            f"{app.config['API_URL']}/encyclopedia/vehicles/?application_id={app.config['API_KEY']}"
        )
        data = response.json()

        if data.get('data'):
            filtered_tanks = filter_tanks(data['data'], nation, tier, tank_type)
            return jsonify(filtered_tanks[:50])  # Ограничиваем 50 танками
        return jsonify({'error': 'Танки не найдены'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tank_details/<int:tank_id>')
def tank_details(tank_id):
    try:
        response = requests.get(
            f"{app.config['API_URL']}/encyclopedia/vehicles/{tank_id}/?application_id={app.config['API_KEY']}"
        )
        data = response.json()

        if not data.get('data'):
            return jsonify({'error': 'Танк не найден'}), 404

        tank = data['data'][str(tank_id)]
        result = {
            'name': tank['name'],
            'nation': tank['nation'],
            'tier': tank['tier'],
            'type': tank['type'],
            'description': tank.get('description', 'Нет описания')
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_clan')
def search_clan():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Введите тег или название клана'}), 400

    try:
        response = requests.get(
            f"{app.config['API_URL']}/clans/list/?application_id={app.config['API_KEY']}&search={query}"
        )
        data = response.json()

        if data.get('data'):
            clans = []
            for clan in data['data'][:20]:  # Ограничиваем 20 кланами
                clans.append({
                    'clan_id': clan['clan_id'],
                    'name': clan['name'],
                    'tag': clan['tag'],
                    'members_count': clan.get('members_count', 0),
                    'created_at': clan.get('created_at')
                })
            return jsonify(clans)
        return jsonify({'error': 'Кланы не найдены'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clan_details/<int:clan_id>')
def clan_details(clan_id):
    try:
        # Получаем основную информацию о клане
        clan_response = requests.get(
            f"{app.config['API_URL']}/clans/info/?application_id={app.config['API_KEY']}&clan_id={clan_id}"
        )
        clan_data = clan_response.json()

        if not clan_data.get('data'):
            return jsonify({'error': 'Клан не найден'}), 404

        clan = clan_data['data'][str(clan_id)]
        result = {
            'name': clan['name'],
            'tag': clan['tag'],
            'leader_name': clan['leader_name'],
            'members_count': clan['members_count'],
            'created_at': clan.get('created_at'),
            'recruiting_options': clan.get('recruiting_options'),
            'members': []
        }

        # Получаем информацию об участниках
        if clan['members_count'] > 0:
            member_ids = [str(m['account_id']) for m in clan['members']]
            accounts_response = requests.get(
                f"{app.config['API_URL']}/account/info/?application_id={app.config['API_KEY']}&account_id={','.join(member_ids)}&fields=statistics.all,nickname"
            )
            accounts_data = accounts_response.json().get('data', {})

            for member in clan['members']:
                account_id = str(member['account_id'])
                account = accounts_data.get(account_id, {})
                stats = account.get('statistics', {}).get('all', {})

                battles = stats.get('battles', 0)
                wins = stats.get('wins', 0)

                result['members'].append({
                    'account_id': account_id,
                    'nickname': account.get('nickname', 'Неизвестный игрок'),
                    'role': member['role'],
                    'battles': battles,
                    'wins': wins,
                    'win_rate': (wins / battles * 100) if battles > 0 else 0
                })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Вспомогательные функции
def get_player_stats(account_id):
    response = requests.get(
        f"{app.config['API_URL']}/account/info/?application_id={app.config['API_KEY']}&account_id={account_id}&fields=statistics.all"
    )
    data = response.json().get('data', {}).get(str(account_id), {})
    stats = data.get('statistics', {}).get('all', {})

    battles = stats.get('battles', 0)
    wins = stats.get('wins', 0)

    return {
        'battles': battles,
        'wins': wins,
        'win_rate': (wins / battles * 100) if battles > 0 else 0,
        'avg_damage': (stats.get('damage_dealt', 0) / battles) if battles > 0 else 0,
        'max_frags': stats.get('max_frags', 0),
        'ban_info': stats.get('ban_info', 'Нет информации о бане'),
        'credits': stats.get('credits', 0),
        'free_xp': stats.get('free_xp', 0),
        'gold': stats.get('gold', 0),
        'premium_expires_at': stats.get('premium_expires_at', 'Нет информации о премиуме')
    }

def filter_tanks(tanks, nation=None, tier=None, type_=None):
    filtered = []
    for tank in tanks.values():
        if (not nation or tank['nation'] == nation) and \
                (not tier or str(tank['tier']) == tier) and \
                (not type_ or tank['type'] == type_):
            filtered.append({
                'id': tank['tank_id'],
                'name': tank['name'],
                'nation': tank['nation'],
                'tier': tank['tier'],
                'type': tank['type'],
                'is_premium': tank.get('is_premium', False),
                'images': tank.get('images', {})
            })
    return filtered

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
