import flet as ft
import requests

YOUR_API_KEY = "1377836fd8c2ecb2382bb3dd08d1f071"  # Замените на ваш API ключ

def main(page: ft.Page):
    page.title = "BlitzStats - Статистика игроков"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT

    # Заголовок
    title = ft.Text("Поиск игрока", size=30, weight=ft.FontWeight.BOLD)
    page.add(title)

    # Ввод никнейма
    nickname_input = ft.TextField(label="Введите никнейм или ID", width=300)
    page.add(nickname_input)

    # Кнопка поиска
    search_button = ft.ElevatedButton("Поиск", on_click=lambda e: get_player_stats(nickname_input.value, page))
    page.add(search_button)

    # Результаты
    global result_label
    result_label = ft.Text("", size=20)
    page.add(result_label)

def get_player_stats(nickname, page):
    if not nickname:
        ft.SnackBar("Пожалуйста, введите никнейм или ID.").show()
        return

    # Получение информации о игроке
    url = f"https://papi.tanksblitz.ru/wotb/account/list/?application_id={YOUR_API_KEY}&search={nickname}"  # Замените на нужный URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            player_info = data['data'][0]
            account_id = player_info['account_id']
            stats = get_player_statistics(account_id)

            # Отображение статистики
            battles = stats['statistics']['all']['battles']
            wins = stats['statistics']['all']['wins']
            win_rate = (wins / battles * 100) if battles > 0 else 0
            average_damage = stats['statistics']['all']['damage_dealt'] / battles if battles > 0 else 0

            result_text = f"Бои: {battles}\nПобеды: {wins}\nПроцент побед: {win_rate:.2f}%\nСредний урон: {average_damage:.2f}"
            result_label.value = result_text  # Обновление текста результата
            page.update()
        else:
            ft.SnackBar("Игрок не найден.").show()
    except requests.exceptions.RequestException as e:
        ft.SnackBar(f"Ошибка: {e}").show()

def get_player_statistics(account_id):
    url = f"https://papi.tanksblitz.ru/wotb/account/info/?application_id={YOUR_API_KEY}&fields=statistics&account_id={account_id}"  # Замените на нужный URL
    response = requests.get(url)
    data = response.json()
    return data['data'][str(account_id)]

# Запуск приложения в браузере
ft.app(target=main, view=ft.WEB_BROWSER)