import tkinter as tk
from tkinter import ttk
import requests

def fetch_weather():
    # Получаем введенные пользователем данные
    country = country_var.get()
    # Пример URL для API OpenWeatherMap (замените YOUR_API_KEY на ваш ключ)
    url = f'http://api.openweathermap.org/data/2.5/weather?q={country}&appid=68861be603d94e8a199d5277615370ba'
    response = requests.get(url)
    weather_data = response.json()
    # Выводим информацию о погоде в текстовое поле
    if response.status_code == 200:
        weather_info = f"Weather: {weather_data['weather'][0]['main']}\n"
        weather_info += f"Temperature: {round(weather_data['main']['temp']-273, 2)} C\n"
        weather_info += f"Pressure: {weather_data['main']['pressure']} hPa\n"
        weather_info += f"Humidity: {weather_data['main']['humidity']}%\n"
        output_text.delete('1.0', tk.END)
        output_text.insert('1.0', weather_info)
    else:
        output_text.delete('1.0', tk.END)
        output_text.insert('1.0', 'Failed to get weather data')

# Создаем главное окно
root = tk.Tk()
root.title("Weather App")

# Создаем переменные для хранения ввода пользователя
country_var = tk.StringVar()

# Создаем виджеты
country_label = ttk.Label(root, text="Type your city/country:")
country_label.pack(pady=5)

country_entry = ttk.Entry(root, textvariable=country_var)
country_entry.pack(pady=5)

fetch_button = ttk.Button(root, text="Fetch Weather", command=fetch_weather)
fetch_button.pack(pady=10)

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

# Запускаем главный цикл обработки событий
root.mainloop()
