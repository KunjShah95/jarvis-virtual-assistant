import logging
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
import os
import subprocess
import webbrowser
import pyautogui
import psutil
import requests
from bs4 import BeautifulSoup
import pyjokes
import speedtest
from plyer import notification
import threading

# Configure logging
logging.basicConfig(
    filename='jarvis.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        logging.info(f"Spoken text: {text}")
    except Exception as e:
        logging.error(f"Error in speak function: {e}")


def time_func():
    try:
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        speak("The current time is")
        speak(current_time)
        logging.info(f"Current time spoken: {current_time}")
    except Exception as e:
        logging.error(f"Error fetching time: {e}")


def date_func():
    try:
        now = datetime.datetime.now()
        year = now.year
        month = now.strftime("%B")
        date_num = now.day
        speak("Today's date is")
        speak(f"{date_num} {month} {year}")
        logging.info(f"Current date spoken: {date_num} {month} {year}")
    except Exception as e:
        logging.error(f"Error fetching date: {e}")


def wishme():
    try:
        speak("Welcome back sir!")
        time_func()
        date_func()
        speak("Jarvis at your service. How can I help you?")
        logging.info("Vocal welcome message delivered.")
    except Exception as e:
        logging.error(f"Error in wishme function: {e}")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Listening for user input.")
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        logging.info("Recognizing user input.")
        query = r.recognize_google(audio, language='en-in')
        logging.info(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        logging.warning("Speech Recognition could not understand audio.")
        speak("I didn't catch that. Could you please repeat?")
        return "None"
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        speak("I'm having trouble connecting to the speech service.")
        return "None"
    except Exception as e:
        logging.error(f"Unexpected error in takeCommand: {e}")
        speak("An unexpected error occurred.")
        return "None"


def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email_id', 'your_email_password')  # Use environment variables or a config file for security
        server.sendmail('your_email_id', to, content)
        server.close()
        speak("Email has been sent")
        logging.info(f"Email sent to {to} with content: {content}")
    except Exception as e:
        logging.error(f"Failed to send email to {to}: {e}")
        speak("Sorry, I couldn't send the email.")


def screenshot():
    try:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken.")
        logging.info("Screenshot saved as screenshot.png")
    except Exception as e:
        logging.error(f"Error taking screenshot: {e}")
        speak("Sorry, I couldn't take the screenshot.")


def cpu():
    try:
        usage = str(psutil.cpu_percent())
        speak('CPU is at ' + usage + ' percent')
        logging.info(f"CPU usage: {usage}%")
        battery = psutil.sensors_battery()
        speak("Battery is at")
        speak(str(battery.percent))
        logging.info(f"Battery level: {battery.percent}%")
    except Exception as e:
        logging.error(f"Error fetching CPU/Battery info: {e}")
        speak("Sorry, I couldn't fetch the CPU or battery information.")


def jokes():
    try:
        joke = pyjokes.get_joke()
        speak(joke)
        logging.info(f"Joke told: {joke}")
    except Exception as e:
        logging.error(f"Error fetching joke: {e}")
        speak("Sorry, I couldn't fetch a joke at this time.")


def get_weather():
    api_key = "ec7e9b126d5733473b55542c9c86638b"  # Replace with your actual API key
    location = "AHMEDABAD"  # Modify as needed
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            speak("Sorry, I couldn't fetch the weather information.")
            logging.error(f"Weather API error: {data['message']}")
            return

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        speak(f"The weather in {location} is currently {weather} with a temperature of {temperature} degrees Celsius.")
        logging.info(f"Weather fetched: {weather}, {temperature}°C in {location}")
    except Exception as e:
        logging.error(f"Error fetching weather: {e}")
        speak("Sorry, I encountered an error while fetching the weather information.")


def get_news():
    api_key = "a831ccc87e9f456cbffb1228fe00d927"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])[:5]  # Get top 5 headlines
        if not articles:
            speak("I couldn't find any news articles.")
            logging.warning("No news articles found.")
            return

        speak("Here are the latest news headlines:")
        for idx, article in enumerate(articles, start=1):
            headline = article.get('title', 'No Title')
            speak(f"Headline {idx}: {headline}")
            logging.info(f"News Headline {idx}: {headline}")
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        speak("Sorry, I couldn't fetch the news at this time.")


def set_reminder(time_str, message):
    """
    Set a reminder at a specific time.
    time_str: Time in HH:MM format (24-hour)
    message: Reminder message
    """
    try:
        target_time = datetime.datetime.strptime(time_str, "%H:%M")
        now = datetime.datetime.now()
        target_time = target_time.replace(year=now.year, month=now.month, day=now.day)
        if target_time < now:
            target_time += datetime.timedelta(days=1)  # Set for the next day

        time_diff = (target_time - now).total_seconds()

        def reminder():
            speak(f"Reminder: {message}")
            logging.info(f"Reminder triggered: {message} at {time_str}")

        threading.Timer(time_diff, reminder).start()
        speak(f"Reminder set for {time_str} saying: {message}")
        logging.info(f"Reminder set for {time_str}: {message}")
    except ValueError:
        speak("Please provide the time in HH:MM format.")
        logging.error(f"Invalid time format for reminder: {time_str}")
    except Exception as e:
        logging.error(f"Error setting reminder: {e}")
        speak("Sorry, I couldn't set the reminder.")


def set_reminder_command():
    try:
        speak("What time should I set the reminder for? Please say it in HH:MM format.")
        time_input = takeCommand()
        if time_input.lower() in ["none", "no"]:
            speak("Reminder canceled.")
            return
        speak("What should I remind you about?")
        reminder_message = takeCommand()
        if reminder_message.lower() in ["none", "no"]:
            speak("Reminder canceled.")
            return
        set_reminder(time_input, reminder_message)
    except Exception as e:
        logging.error(f"Error setting reminder via command: {e}")
        speak("Sorry, I couldn't set the reminder.")


def play_music():
    try:
        music_dir = 'C:\\Users\\User\\Music'  # Update this path as needed
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            speak("Playing music.")
            logging.info(f"Playing music: {songs[0]}")
        else:
            speak("No music files found.")
            logging.warning("No music files found in the directory.")
    except Exception as e:
        logging.error(f"Error playing music: {e}")
        speak("Sorry, I couldn't play music.")


def play_video():
    try:
        video_dir = 'C:\\Users\\User\\Videos'  # Update this path as needed
        videos = os.listdir(video_dir)
        if videos:
            os.startfile(os.path.join(video_dir, videos[0]))
            speak("Playing video.")
            logging.info(f"Playing video: {videos[0]}")
        else:
            speak("No video files found.")
            logging.warning("No video files found in the directory.")
    except Exception as e:
        logging.error(f"Error playing video: {e}")
        speak("Sorry, I couldn't play video.")


class Jarvis:
    def __init__(self):
        # Initialize any required attributes or services
        logging.info("Jarvis class initialized.")

    def process(self, user_input):
        # Your Jarvis processing logic here
        # For example, respond to greetings
        if "hello" in user_input.lower():
            return "Hello! How can I assist you today?"
        # Add more processing logic as needed
        logging.info(f"Jarvis received input: {user_input}")
        return f"Jarvis received: {user_input}"


COMMANDS = {
    "open google": lambda: webbrowser.open("https://www.google.com"),
    "open facebook": lambda: webbrowser.open("https://www.facebook.com"),
    "open youtube": lambda: webbrowser.open("https://www.youtube.com"),
    "open instagram": lambda: webbrowser.open("https://www.instagram.com"),
    "open gmail": lambda: webbrowser.open("https://mail.google.com/mail/u/0/#inbox"),
    "open github": lambda: webbrowser.open("https://github.com"),
    "open linkedin": lambda: webbrowser.open("https://www.linkedin.com"),
    "open whatsapp": lambda: webbrowser.open("https://web.whatsapp.com"),
    "open stackoverflow": lambda: webbrowser.open("https://stackoverflow.com"),
    "open spotify": lambda: webbrowser.open("https://open.spotify.com"),
    "open codechef": lambda: webbrowser.open("https://www.codechef.com"),
    "open codeforces": lambda: webbrowser.open("https://codeforces.com"),
    "open hackerrank": lambda: webbrowser.open("https://www.hackerrank.com"),
    "open hackerearth": lambda: webbrowser.open("https://www.hackerearth.com"),
    "open jiosaavn": lambda: webbrowser.open("https://www.jiosaavn.com"),
    "open geeksforgeeks": lambda: webbrowser.open("https://www.geeksforgeeks.org"),
    "open flipkart": lambda: webbrowser.open("https://www.flipkart.com"),
    "open amazon": lambda: webbrowser.open("https://www.amazon.in"),
    "open google meet": lambda: webbrowser.open("https://meet.google.com"),
    "open google classroom": lambda: webbrowser.open("https://classroom.google.com/u/0/h"),
    "open google docs": lambda: webbrowser.open("https://docs.google.com/document/u/0/"),
    "open google sheets": lambda: webbrowser.open("https://docs.google.com/spreadsheets/u/0/"),
    "open google slides": lambda: webbrowser.open("https://docs.google.com/presentation/u/0/"),
    "open google forms": lambda: webbrowser.open("https://docs.google.com/forms/u/0/"),
    "open google drive": lambda: webbrowser.open("https://drive.google.com"),
    "open google translate": lambda: webbrowser.open("https://translate.google.com"),
    "open x": lambda: webbrowser.open("https://www.x.com"),
    "open google maps": lambda: webbrowser.open("https://www.google.com/maps"),
    "open google news": lambda: webbrowser.open("https://news.google.com"),
    "open google photos": lambda: webbrowser.open("https://photos.google.com"),
    "play music": lambda: play_music(),
    "play video": lambda: play_video(),
    "open notepad": lambda: os.startfile("C:\\Windows\\notepad.exe"),
    "open command prompt": lambda: os.startfile("C:\\Windows\\System32\\cmd.exe"),
    "open camera": lambda: subprocess.run('start microsoft.windows.camera:', shell=True),
    "open settings": lambda: subprocess.run('start ms-settings:', shell=True),
    "open control panel": lambda: subprocess.run('start control panel', shell=True),
    "open task manager": lambda: subprocess.run('start taskmgr', shell=True),
    "open file explorer": lambda: subprocess.run('start explorer', shell=True),
    "open run": lambda: subprocess.run('start run', shell=True),
    "open system configuration": lambda: subprocess.run('start msconfig', shell=True),
    "open disk cleanup": lambda: subprocess.run('start cleanmgr', shell=True),
    "open disk defragment": lambda: subprocess.run('start dfrgui', shell=True),
    "open registry editor": lambda: subprocess.run('start regedit', shell=True),
    "open system information": lambda: subprocess.run('start msinfo32', shell=True),
    "open system properties": lambda: subprocess.run('start sysdm.cpl', shell=True),
    "open device manager": lambda: subprocess.run('start devmgmt.msc', shell=True),
    "open event viewer": lambda: subprocess.run('start eventvwr', shell=True),
    "open services": lambda: subprocess.run('start services.msc', shell=True),
    "open task scheduler": lambda: subprocess.run('start taskschd.msc', shell=True),
    "open performance monitor": lambda: subprocess.run('start perfmon', shell=True),
    "open resource monitor": lambda: subprocess.run('start resmon', shell=True),
    "open disk management": lambda: subprocess.run('start diskmgmt.msc', shell=True),
    "open computer management": lambda: subprocess.run('start compmgmt.msc', shell=True),
    "open certificate manager": lambda: subprocess.run('start certmgr.msc', shell=True),
    "open windows defender": lambda: subprocess.run('start windowsdefender:', shell=True),
    "open windows security": lambda: subprocess.run('start windowsdefender:', shell=True),
    "open windows update": lambda: subprocess.run('start ms-settings:windowsupdate', shell=True),
    "open windows settings": lambda: subprocess.run('start ms-settings:', shell=True),
    "open windows activation": lambda: subprocess.run('start ms-settings:activation', shell=True),
    "open windows troubleshooting": lambda: subprocess.run('start ms-settings:troubleshoot', shell=True),
    "open windows recovery": lambda: subprocess.run('start ms-settings:recovery', shell=True),
    "open windows backup": lambda: subprocess.run('start ms-settings:backup', shell=True),
    "open windows storage": lambda: subprocess.run('start ms-settings:storagesense', shell=True),
    "open windows update history": lambda: subprocess.run('start ms-settings:windowsupdate-history', shell=True),
    "open windows update troubleshooter": lambda: subprocess.run('start ms-settings:troubleshoot-windows-update', shell=True),
    "open windows activation troubleshooter": lambda: subprocess.run('start ms-settings:activation-troubleshoot', shell=True),
    "open windows recovery environment": lambda: subprocess.run('start ms-settings:recovery-environment', shell=True),
    "open windows reset this pc": lambda: subprocess.run('start ms-settings:resetthispc', shell=True),
    "open windows system restore": lambda: subprocess.run('start rstrui', shell=True),
    "open calculator": lambda: subprocess.run('start calc', shell=True),
    "open openai": lambda: subprocess.run('start https://openai.com/', shell=True),
    "open gemini": lambda: subprocess.run('start https://gemini.com/', shell=True),
    "open blackbox": lambda: subprocess.run('start https://blackbox.vision/', shell=True),
    "open calude": lambda: subprocess.run('start https://calude.org/', shell=True),
    "open perplexity": lambda: subprocess.run('start https://perplexity.ai/', shell=True),
    # Add more commands as needed
}


def processCommand(c):
    try:
        command_handled = False
        for command, action in COMMANDS.items():
            if command in c.lower():
                action()
                command_handled = True
                logging.info(f"Executed command: {command}")
                break

        if not command_handled:
            if "weather" in c.lower():
                get_weather()
            elif "news" in c.lower():
                get_news()
            elif "set reminder" in c.lower():
                set_reminder_command()
            elif "internet speed" in c.lower():
                try:
                    wifi = speedtest.Speedtest()
                    upload_net = wifi.upload() / 1048576  # Convert to MBps
                    download_net = wifi.download() / 1048576  # Convert to MBps
                    speak(f"Wifi download speed is {download_net:.2f} megabits per second")
                    speak(f"Wifi upload speed is {upload_net:.2f} megabits per second")
                    logging.info(f"Wifi Upload Speed is {upload_net:.2f} MBps")
                    logging.info(f"Wifi download speed is {download_net:.2f} MBps")
                except Exception as e:
                    logging.error(f"Error fetching internet speed: {e}")
                    speak("Sorry, I couldn't fetch the internet speed.")
            elif "shutdown the system" in c.lower():
                speak("Are you sure you want to shutdown?")
                shutdown = input("Do you wish to shutdown your computer? (yes/no): ").lower()
                if shutdown == "yes":
                    speak("Shutting down the system.")
                    logging.info("User initiated system shutdown.")
                    os.system("shutdown /s /t 1")
                elif shutdown == "no":
                    speak("Shutdown canceled.")
                    logging.info("System shutdown canceled by user.")
                else:
                    speak("Invalid input. Shutdown canceled.")
                    logging.warning("Invalid input for system shutdown.")
            elif "change password" in c.lower():
                speak("Password functionality has been removed.")
                logging.warning("Attempted to change password, but password protection is disabled.")
            elif "ipl score" in c.lower():
                try:
                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, "html.parser")
                    teams = soup.find_all(class_="cb-ovr-flo cb-hmscg-tm-nm")
                    scores = soup.find_all(class_="cb-ovr-flo")

                    if len(teams) >= 2 and len(scores) >= 11:
                        team1 = teams[0].get_text()
                        team2 = teams[1].get_text()
                        team1_score = scores[8].get_text()
                        team2_score = scores[10].get_text()

                        notification.notify(
                            title="IPL SCORE",
                            message=f"{team1} : {team1_score}\n{team2} : {team2_score}",
                            timeout=15
                        )
                        speak(f"The current IPL score is {team1} at {team1_score} and {team2} at {team2_score}.")
                        logging.info(f"IPL Scores - {team1}: {team1_score}, {team2}: {team2_score}")
                    else:
                        speak("Couldn't retrieve IPL scores at the moment.")
                        logging.warning("Insufficient data scraped for IPL scores.")
                except Exception as e:
                    logging.error(f"Error fetching IPL score: {e}")
                    speak("Sorry, I couldn't fetch the IPL scores right now.")
            elif "screenshot" in c.lower():
                try:
                    im = pyautogui.screenshot()
                    im.save("ss.jpg")
                    speak("Screenshot taken.")
                    logging.info("Screenshot saved as ss.jpg")
                except Exception as e:
                    logging.error(f"Error taking screenshot: {e}")
                    speak("Sorry, I couldn't take the screenshot.")
            else:
                speak("I didn't understand that command.")
                logging.warning(f"Unrecognized command: {c}")
    except Exception as e:
        logging.error(f"Error processing command '{c}': {e}")
        speak("Sorry, I encountered an error while processing your command.")


def main():
    try:
        wishme()
        jarvis = Jarvis()
        while True:
            query = takeCommand().lower()
            if 'jarvis' in query:
                speak("Yes sir?")
                command = takeCommand().lower()
                if command != "none":
                    processCommand(command)
    except KeyboardInterrupt:
        logging.info("Jarvis terminated by user.")
        speak("Goodbye!")
    except Exception as e:
        logging.error(f"Unexpected error in main loop: {e}")
        speak("An unexpected error occurred.")


if __name__ == "__main__":
    main()