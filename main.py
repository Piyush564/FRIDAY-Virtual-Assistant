import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "c7c80263a91d4b568c1e4949a6723cb0"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="<API key>",
)

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-r1:free",
    messages=[
        {"role": "system", "content":"you are a virtual assistant named friday skilled in general tasks like Alexa and Google Cloud"},
        {"role": "user","content": command}
        
    ]
    )
    return (completion.choices[0].message.content)
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
        speak("Opening Google...")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
        speak("Opening facebook...")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
        speak("Opening YouTube...")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
        speak("Opening LinkedIn...")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song] 
        webbrowser.open(link) 
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?c ountry=us&apiKey=c7c80263a91d4b568c1e4949a6723cb0")
        if r.status_code == 200:
            #parse the jason response
            data = r.jason()

            #Extract the articles
            articles = data('articles', [])

            #print the headlines
            for article in articles:
                speak(article,['titles'])

    else:
        #let openAI handle the request
        output = aiProcess(c)
        speak(output)         



if __name__ == '__main__':
    speak("Initializing Friday...")
    while True:

        # listen for the wakeup "FRIDAY"
        # obtain from the microphone

        r =sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio)
                if(word.lower() == "friday"):
                    speak("yes Sir")

                    # listen for the command
                    with sr.Microphone() as source:
                        print("FRIDAY Active...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio)

                        processCommand(command)


        except Exception as e:
            print("Error;{0}".format(e)) 
