from flask import Flask, render_template, request, jsonify 
from threading import Thread
import threading
import os
import pyaudio
import wave
import sys
import subprocess

app = Flask(__name__)
 
@app.route('/') 
def index(): 
	return render_template('index.html') 
 
@app.route('/', methods=['POST']) 
def play(): 
    directory = request.form['album-title']
    url = request.form['song-link']
    tempo = request.form['song-tempo']
    

    os.environ['SPOTIPY_CLIENT_ID'] = 'fe2356ab41ef42f88445a6c97ba2c575'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '547ce4b034db462bbbcd8f445c6d8f1a'

    subprocess.run(["spotify_dl", "-l", url])
    

    for filename in os.listdir(directory):
         f = os.path.join(directory, filename)
         # checking if it is a file
         if os.path.isfile(f):
             store = f.split(".")
             if store[-1] == "mp3":
                 print("this is an mp3 file")
                 file_name_to_convert = f
                 correct_name = f.split("-")[-1].strip().split(".")[0]
                 correct_name_wav = correct_name + ".wav"
                 subprocess.run(["ffmpeg","-i",file_name_to_convert,correct_name_wav])
                 print(correct_name_wav)
                 thread1 = threading.Thread(target = lambda a: os.system("aplay -D plughw:CARD=USB,DEV=0 " + "'" + a + "'"), args=[correct_name_wav])
                 thread2 = threading.Thread(target = lambda a: subprocess.run(["python3", "../../moveTest.py", a]), args=[tempo])
                 thread1.start()
                 thread2.start()
         print(f)
         print(store)
    return render_template('pass.html', dir=directory, url=url, tempo=tempo)
 
if __name__ == '__main__': 
	app.run(debug=True) 