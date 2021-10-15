import speech_recognition as sr
from gtts import gTTS
import random
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import webbrowser
import smtplib
import requests
import urllib.request
import urllib.parse
import bs4
import datetime
import wolframalpha
from ecapture import ecapture as ec
import time


assistant = "Jarvis"


def talk(audio):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang='en')
        text_to_speech.save('audio.mp3')
        file = "audio.mp3"
        playsound(file)


def my_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')

        except sr.UnknownValueError:
            talk("Pardon me, please say that again")
            print("Pardon me, please say that again")
            command = my_command()

        return command


def jarvis(command):
    errors = [
        "I don't know what you mean",
        "Can you repeat it please?",
        "Excuse me?",
        "I'm sorry, I didn't get it",
        "I didn't understand what you said"
    ]

    #basic conversations
    if 'hello' in command or 'hi' in command or 'hey' in command:
        hellos = [
            "Hello Akeshi, How are you doing?",
        ]
        hello = random.choice(hellos)
        talk(hello)
        talk("What can I do for you?")

    elif 'your name' in command or 'who are you' in command or 'call you' in command:
        talk('My name is '+assistant+'!')
    elif 'you do' in command or 'your job' in command or 'your purpose' in command or 'reason for you' in command:
        talk("I am your AI assistant, I'm here to make your life easier!")
    elif 'created' in command or 'your boss' in command or 'own you' in command:
        talk('I was created by Praveen De Silva')
    elif 'who I am' in command or 'who am I' in command:
        talk('If you can talk, you are definately a human!')
    elif 'where are you from' in command or 'where do you live' in command:
        talk("I actually live inside Praveen's Linux computer")
    elif 'love you' in command or 'have feelings for you' in command:
        talk("I'm not interested, I'm sorry!")
    elif 'will you be my girlfriend' in command:
        talk("I'm a robot, I'm not interested in humans!")
    elif 'how old' in command:
        talk("I'm younger than you Akeshi")

    #Google search
    elif 'search on google' in command or 'google' in command or "what is" in command:
        search_for = ""
        reg_ex = re.search('search(.*)', command)
        if 'search on google' in command:
            search_for = command.split("search on google for ", 1)[1]
        elif 'google' in command:
            search_for = command.split("google for ", 1)[1]
        elif 'what is' in command:
            search_for = command.split("what is ", 1)[1]

        print(search_for)
        url = 'http://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
        talk('Seraching in Google for '+search_for)
        driver = webdriver.Firefox(executable_path='/home/praveen/geckodriver')
        driver.get('http://www.google.com')
        search = driver.find_element_by_name('q')
        search.send_keys(str(search_for))
        search.send_keys(Keys.RETURN)
    #Search a video in Youtube
    elif 'search on youtube' in command or 'search for a video' in command or 'search in youtube' in command or 'youtube' in command:
        talk('Ok!')
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube for ", 1)[1]
            talk('Searching in Youtube for ' + domain)
            query_string = urllib.parse.urlencode({"search_query": domain})
            url = "http://www.youtube.com/results?" + query_string
            webbrowser.open(url)
            pass
    #search on wikipedia
    elif 'wikipedia' in command:
        reg_ex = re.search('wikipedia (.+)', command)
        if reg_ex:
            query = command.split("wikipedia for ", 1)[1]
            talk('Here is the result in Wikipedia for ' + query)
            response = requests.get("https://en.wikipedia.org/wiki/" + query)
            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')
                title = html.select("#firstHeading")[0].text
                paragraphs = html.select("p")
                for para in paragraphs:
                    print(para.text)
                intro = '\n'.join([para.text for para in paragraphs[0:3]])
                print(intro)
                mp3name = 'speech.mp3'
                language = 'en'
                myobj = gTTS(text=intro, lang=language, slow=False)
                myobj.save(mp3name)
                playsound(mp3name)
    elif 'open' in command or 'website' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = command.split("open ", 1)[1]
            talk('Opening the website ' + domain)
            url = "https://www."+domain+".com/"
            webbrowser.open(url)
    elif 'time' in command:
        timenow = datetime.datetime.now().strftime("%H:%M:%S")
        talk(f"The current time is {timenow}")

    elif 'thank' in command:
        welcomes = [
            "Your welcome",
            "My pleasure",
            "Anytime"
        ]
        welcome = random.choice(welcomes)
        talk(welcome)
        exit()
    elif 'stop' in command or 'enough' in command or 'bye' in command:
        byes = [
            "Good bye!",
            "Have a good day!",
            "Bye bye!"
        ]
        bye = random.choice(byes)
        talk(bye)
        exit()
    elif 'camera' in command or 'take a photo' in command or 'take a picture' in command:
        ec.capture(0, assistant+" Camera", "img.jpg")

    elif 'email' in command:
        talk('What is the subject?')
        time.sleep(3)
        subject = my_command()
        talk('What should I say?')
        message = my_command()
        content = 'Subject: {}\n\n{}'.format(subject, message)

        # init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        # identify to server
        mail.ehlo()

        # encrypt session
        mail.starttls()

        # login
        mail.login('praveends1998@gmail.com', 'praveen5768')

        print("Enter the email address of the receiver: ")
        to = input()

        # send message
        mail.sendmail('Praveen De Silva', to, content)

        # end mail connection
        mail.close()

        talk('Email sent.')

    else:
        error = random.choice(errors)
        talk(error)


talk('Hello, I am '+assistant+'! How can I help you?')

while True:
    jarvis(my_command())
