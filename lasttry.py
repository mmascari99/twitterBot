import time
from gtts import gTTS
import playsound
import speech_recognition as sr
import os

language = 'en'
mytext = 'Say your name after the beep'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("sayYourName.mp3")
playsound.playsound('sayYourName.mp3', True)
time.sleep(1)
os.remove("sayYourName.mp3")

mytext = 'beep'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("beep.mp3")
playsound.playsound('beep.mp3', True)
os.remove("beep.mp3")


# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print('Say something!')
    audio = r.listen(source)

# Speech recognition using Google Speech Recognition
try:
    said = r.recognize_google(audio)
    print('You said: ' + said)
    test = 0
    if said == 'Michael':
        test = 1
    elif said == 'Michael Mascari':
        test = 1
    elif said == 'Bob':
        test = 1
    elif said == 'Mister Bob':
        test = 1
    if test == 0:
        mytext = 'Screw off ' + said
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("last.mp3") 
        playsound.playsound('last.mp3', True)
        os.remove("last.mp3")
    else:
        mytext = said + ' is the best guy in the whole world'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("last.mp3") 
        playsound.playsound('last.mp3', True)
        os.remove("last.mp3")
except sr.UnknownValueError:
    print('Google Speech Recognition could not understand audio')
except sr.RequestError as e:
    print('Could not request results from Google Speech Recognition service; {0}'.format(e))

time.sleep(4)
