def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source, 10, 3)
    said = r.recognize_google(audio)
    print(said)

if __name__ == "__main__":
    listen()