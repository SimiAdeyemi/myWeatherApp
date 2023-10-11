from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
import os

key = os.environ.get('API_key')

url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config["api_key"]["key"]


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # (city, country, temp_celsius, temp_fahrenheit, icon, weather, description)
        city = json["name"]
        country = json["sys"]["country"]
        temp_kelvin = json["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (9 / 5) * (temp_kelvin - 273.15) + 32
        icon = json["weather"][0]["icon"]
        weather = json["weather"][0]["main"]
        description = json["weather"][0]["description"]
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather, description)
        return final
    else:
        return None


def search():
    global img
    global lang_config  # Make lang_config global
    city = city_text.get()
    weather = get_weather(city)
    lang_config = ConfigParser()
    lang_config.read(lang_file, encoding='utf-8')
    if weather:
        location_lbl["text"] = lang_config["labels"]["location_label"].format(weather[0], weather[1])
        img["file"] = "weather_icons/{}@2x.png".format(weather[4])
        temp_lbl["text"] = lang_config["labels"]["temperature_label"].format(weather[2], weather[3])
        weatherText_lbl["text"] = lang_config["labels"]["weather_text_label"].format(weather[5])
        description_lbl["text"] = lang_config["labels"]["description_label"].format(weather[6])
    else:
        messagebox.showerror(lang_config["labels"]["error_title"], lang_config["labels"]["error_message"].format(city))


def change_language():
    global lang_config
    global lang_file
    global search_btn  # Also update the text of the search button
    selected_language = language_var.get()
    lang_file = f"translations/strings_{selected_language}.ini"
    lang_config = ConfigParser()
    lang_config.read(lang_file, encoding='utf-8')
    search_btn["text"] = lang_config["labels"]["search_button"]
    app.title(lang_config["labels"]["app_title"])


app = Tk()
app.title("Weather App")
app.geometry("600x375")
app["background"] = "#1e1e1e"  # Dark background

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, font=("Helvetica", 12))
city_entry.pack()

search_btn = Button(app, text="Search Weather", width=16, command=search, font=("Helvetica", 11))
search_btn.pack()

# Set a modern color scheme
app["background"] = "#1e1e1e"  # Dark background
city_entry["bg"] = "#444"  # Slightly lighter background for input field
city_entry["fg"] = "#fff"  # White text
search_btn["bg"] = "#FF4081"  # Pink button color
search_btn["fg"] = "#fff"  # White text on button

# Use a more modern font
font_style = ("Helvetica", 11)

# Apply consistent padding and spacing
city_entry.pack(pady=(20, 10))
search_btn.pack(pady=(0, 20))

# Set labels' font and color
label_style = {"font": font_style, "bg": "#1e1e1e", "fg": "#fff", "border": 0}

location_lbl = Label(app, text="", **label_style)
location_lbl.config(font=("Helvetica", 20, "bold"))
location_lbl.pack()

# Add a subtle shadow to the labels
label_style["bd"] = 1

img = PhotoImage(file="")
image = Label(app, image=img, **label_style)
image.pack()

temp_lbl = Label(app, text="", **label_style)
temp_lbl.config(font=("Helvetica", 18, "bold"))
temp_lbl.pack()

weatherText_lbl = Label(app, text="", **label_style)
weatherText_lbl.config(font=("Helvetica", 12, "bold"))
weatherText_lbl.pack()

description_lbl = Label(app, text="", **label_style)
description_lbl.config(font=("Helvetica", 12, "bold"))
description_lbl.pack()

language_var = StringVar(value="en")  # Default language is English

# Language selection dropdown
language_menu = OptionMenu(app, language_var, "en", "fr", "es", "de", "ar", "zh")
language_menu.pack()

# Language change button
change_language_btn = Button(app, text="Update Language", command=change_language)
change_language_btn.pack()

language_menu.pack()

# Initial language file and configuration
lang_file = "translations/strings_en.ini"
lang_config = ConfigParser()
lang_config.read(lang_file, encoding='utf-8')

app.mainloop()
