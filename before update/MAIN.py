import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):   
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():  
        webbrowser.open("https://www.facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com")
    elif "open gmail" in c.lower():
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open stackoverflow" in c.lower():
        webbrowser.open("https://stackoverflow.com")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com")
    elif "open codechef" in c.lower():
        webbrowser.open("https://www.codechef.com")
    elif "open codeforces" in c.lower():
        webbrowser.open("https://codeforces.com")
    elif "open hackerrank" in c.lower():
        webbrowser.open("https://www.hackerrank.com")
    elif "open hackerearth" in c.lower():
        webbrowser.open("https://www.hackerearth.com")
    elif "open jiosaavn" in c.lower():
        webbrowser.open("https://www.jiosaavn.com")
    elif "open geeksforgeeks" in c.lower():
        webbrowser.open("https://www.geeksforgeeks.org")
    elif "open flipkart" in c.lower():
        webbrowser.open("https://www.flipkart.com")
    elif "open amazon" in c.lower():
        webbrowser.open("https://www.amazon.in")
    elif "open google meet" in c.lower():
        webbrowser.open("https://meet.google.com")
    elif "open google classroom" in c.lower():
        webbrowser.open("https://classroom.google.com/u/0/h")
    elif "open google docs" in c.lower():
        webbrowser.open("https://docs.google.com/document/u/0/")
    elif "open google sheets" in c.lower():
        webbrowser.open("https://docs.google.com/spreadsheets/u/0/")
    elif "open google slides" in c.lower():
        webbrowser.open("https://docs.google.com/presentation/u/0/")
    elif "open google forms" in c.lower():
        webbrowser.open("https://docs.google.com/forms/u/0/")
    elif "open google drive" in c.lower():
        webbrowser.open("https://drive.google.com")
    elif "open google translate" in c.lower():
        webbrowser.open("https://translate.google.com")
    elif "open X" in c.lower():
        webbrowser.open("https://www.x.com")
    elif "open google maps" in c.lower():
        webbrowser.open("https://www.google.com/maps")
    elif "open google news" in c.lower():
        webbrowser.open("https://news.google.com")
    elif "open google photos" in c.lower():
        webbrowser.open("https://photos.google.com")
    elif  c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        webbrowser.open("https://news.google.com")
    else:
        speak("Sorry, I didn't get that. Can you please rephrase?")
        


if __name__ == "__main__":
    speak("Initializing Jarvis...")
while True:
    # Listen for the wake word "Jarvis"
    # obtain audio from the microphone
    r = sr.Recognizer()
     
     
    print("Recognizing...")
    try :
          with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
              speak("Ya")
              #listen for command
              with sr.Microphone() as source:
                
                print("Jarvis active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)
                
                
              processCommand(command)
              
              
    except Exception as e:
        print("Error; {0}".format(e))
     
     
