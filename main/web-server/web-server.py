"""Web server script
"""

from logging import warning
from dotenv import load_dotenv
import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from time import sleep
import RPi.GPIO as GPIO
from buzzer import Buzzer
from subprocess import call
import signal
import sys

load_dotenv()

def sigint_handler(sig, frame):
  """Handler for SIGINT signal

  Args:
      sig (signal): signal received
      frame (frame): unused
  """
  buzz.error()
  stopDisplay(True)
  sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler) #associate SIGINT with its handler

UPLOAD_FOLDER = '../img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
RADIAL_RESOLUTION_BOUNDS = {'min':1,'max':48}
ANGULAR_RESOLUTION_BOUNDS = {'min':1,'max':50}

RUN_ALLOWED = False

BUZZER_PIN = 22 #BCM TODO: check 17 otherwise
MOTOR_PIN = 6 #BCM

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

buzz = Buzzer(BUZZER_PIN)
buzz.setEnable(True)

def startSequence():
  """Play a visual and sonor alert to make sure that display is alive
  """
  stopDisplay()
  buzz.start()


def warnBeforeStart():
  """Play a visual and sonor alert before starting the propeller for safety reasons
  """



def getImageToDisplay():
  """Gets the image to be displayed from USB key
  """
  pass

def startDisplay():
  """Starts motor
  """
  warnBeforeStart()

def stopDisplay(skipBuzz = False):
  """Stops display motor

  Args:
      skipBuzz (bool): If true, buzzer won't play any sound
  """
  if not skipBuzz:
    buzz.shutDown()
  

def allowed_file(filename):
  """Evaluates whether the filename can be accepted or not

  Args:
      filename (string): user input filename

  Returns:
      bool: True if filename is accepter, False otherwise
  """
  global ALLOWED_EXTENSIONS
  return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

startSequence()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("flask_secret")

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('../preview', filename, as_attachment=True)

@app.route("/", methods=['GET', 'POST'])
def home():
  global RUN_ALLOWED
  if request.method == 'POST':
    if RUN_ALLOWED:
      if request.form.get('command') == 'run_prop':
        startDisplay()
        flash('Hélice démarrée avec succès','success')
        return render_template('index.html',preview_url="preview.png", RUN_ALLOWED = RUN_ALLOWED)
      elif request.form.get('command') == 'stop_prop':
        stopDisplay()
        flash('Hélice arrêtée avec succès','success')
        return render_template('index.html',preview_url="preview.png", RUN_ALLOWED = RUN_ALLOWED)
    RUN_ALLOWED = False
    angular_res_input = int(request.form.get('angular_resolution'))
    radial_res_input = int(request.form.get('radial_resolution'))
    if not isinstance(angular_res_input, int) :
      flash('La résolution angulaire saisie en 3 doit être un entier',"warning")
      return redirect(request.url)
    if angular_res_input > ANGULAR_RESOLUTION_BOUNDS['max'] or angular_res_input < ANGULAR_RESOLUTION_BOUNDS['min']:
      flash('La résolution angulaire doit être comprise entre %i et %i'%(ANGULAR_RESOLUTION_BOUNDS['min'], ANGULAR_RESOLUTION_BOUNDS['max']),"warning")
      return redirect(request.url)
    if not isinstance(angular_res_input, int) :
      flash('La résolution radiale saisie en 2 doit être un entier',"warning")
      return redirect(request.url)
    if radial_res_input > RADIAL_RESOLUTION_BOUNDS['max'] or radial_res_input < RADIAL_RESOLUTION_BOUNDS['min']:
      flash('La résolution radiale doit être comprise entre %i et %i'%(RADIAL_RESOLUTION_BOUNDS['min'], RADIAL_RESOLUTION_BOUNDS['max']),"warning")
      return redirect(request.url)
    #check image input file
    if 'image_to_display' not in request.files:
        flash('Aucun fichier envoyé',"warning")
        return redirect(request.url)
    file = request.files['image_to_display']
    if file.filename == '':
        flash('Aucun fichier sélectionné', warning)
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash('Fichier image invalide, seuls les fichiers au format .png, .jpg ou .jpeg sont acceptés', 'warning')
        return redirect(request.url)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)
            #TODO: convert image and save preview
            flash('Image importée et traitée avec succès, prévisualisation en cours', 'success')
            RUN_ALLOWED = True
            return render_template('index.html',preview_url="preview.png", RUN_ALLOWED = RUN_ALLOWED)
  return render_template('index.html')

if __name__=="__main__":
  app.debug = True
  app.run()