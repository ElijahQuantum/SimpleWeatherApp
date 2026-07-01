import tkinter as tk
from tkinter import messagebox
import requests

from api import API_KEY



class weatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("400x300")
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20)
        self.result_frame = tk.Frame(self.root)
        
        try:        
            from api import API_KEY
        except ImportError:
            messagebox.showerror("Error", "API_KEY not found")
            
        self.label = tk.Label(self.main_frame, text="Enter a city name:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(self.main_frame)
        self.entry.pack(pady=10)
        
        self.button = tk.Button(self.main_frame, text="Get Weather", command=self.get_weather)
        self.button.pack(pady=10)      
    def get_weather(self):
        user_input = self.entry.get()
        if not user_input or not user_input.strip():
            messagebox.showwarning("Input required", "Please enter a city name")
            return
        try:
            weather_date = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&appid={API_KEY}'
            )
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {e}")
            return
        try:
            data = weather_date.json()
        except ValueError:
            messagebox.showerror("Error", "Invalid response from weather service")
            return

        if weather_date.status_code != 200:
            msg = data.get('message', f"Status code {weather_date.status_code}")
            messagebox.showerror("API Error", f"Failed to get weather: {msg}")
            return

        if 'weather' not in data or 'main' not in data:
            messagebox.showerror("Error", "Unexpected API response structure")
            return

        weather = data['weather'][0].get('main', 'N/A')
        temperature = data['main'].get('temp', 'N/A')
        messagebox.showinfo("Weather Information", f"Weather: {weather}\nTemperature: {temperature}°F")
        

def run():
    run_app = weatherApp()
    run_app.root.mainloop()


if __name__ == "__main__":
    run()