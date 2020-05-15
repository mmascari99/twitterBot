import time
import sounddevice as sd
from gtts import gTTS

def _playsoundWin(sound, block = True):
    from ctypes import c_buffer, windll
    from random import random
    from time   import sleep
    from sys    import getfilesystemencoding

    def winCommand(*command):
        buf = c_buffer(255)
        command = ' '.join(command).encode(getfilesystemencoding())
        errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))

        return buf.value

    alias = 'playsound_' + str(random())
    winCommand('open "' + sound + '" alias', alias)
    winCommand('set', alias, 'time format milliseconds')
    durationInMS = winCommand('status', alias, 'length')
    winCommand('play', alias, 'from 0 to', durationInMS.decode())

    if block:
        sleep(float(durationInMS) / 1000.0)

def _playsoundOSX(sound, block = True):
    from AppKit     import NSSound
    from Foundation import NSURL
    from time       import sleep

    if '://' not in sound:
        if not sound.startswith('/'):
            from os import getcwd
            sound = getcwd() + '/' + sound
        sound = 'file://' + sound
    url   = NSURL.URLWithString_(sound)
    nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
    if not nssound:
        raise IOError('Unable to load sound named: ' + sound)
    nssound.play()

    if block:
        sleep(nssound.duration())

def _playsoundNix(sound, block=True):
    if not block:
        raise NotImplementedError(
            "block=False cannot be used on this platform yet")

    # pathname2url escapes non-URL-safe characters
    import os
    try:
        from urllib.request import pathname2url
    except ImportError:
        # python 2
        from urllib import pathname2url

    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    if sound.startswith(('http://', 'https://')):
        playbin.props.uri = sound
    else:
        playbin.props.uri = 'file://' + pathname2url(os.path.abspath(sound))

    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise PlaysoundException(
            "playbin.set_state returned " + repr(set_result))
            
    bus = playbin.get_bus()
    bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
    playbin.set_state(Gst.State.NULL)


from platform import system
system = system()

language = 'en'
mytext = 'Say your name after the beep'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("sayYourName.mp3") 
if system == 'Windows':
    _playsoundWin('sayYourName.mp3', True)
elif system == 'Darwin':
    _playsoundOSX('sayYourName.mp3', True)
else:
    _playsoundNix('sayYourName.mp3', True)
time.sleep(1)

mytext = 'beep'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("beep.mp3")
if system == 'Windows':
    _playsoundWin('beep.mp3', True)
elif system == 'Darwin':
    _playsoundOSX('beep.mp3', True)
else:
    _playsoundNix('beep.mp3', True)

import speech_recognition as sr

# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, this is the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    said = r.recognize_google(audio)
    print("You said: " + said)
    if said != 'Michael' && said != 'Bob' && said != 'Michael Mascari':
        mytext = 'Go fuck yourself' + said
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("fucker.mp3") 
        if system == 'Windows':
            _playsoundWin('fucker.mp3', True)
        elif system == 'Darwin':
            _playsoundOSX('fucker.mp3', True)
        else:
            _playsoundNix('fucker.mp3', True)
    else:
        mytext = said + ' is the best guy in the whole world'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("fucker.mp3") 
        if system == 'Windows':
            _playsoundWin('fucker.mp3', True)
        elif system == 'Darwin':
            _playsoundOSX('fucker.mp3', True)
        else:
            _playsoundNix('fucker.mp3', True)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

time.sleep(4)