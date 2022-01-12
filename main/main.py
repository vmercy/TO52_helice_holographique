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
from converter.converter import *
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
  #sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler) #associate SIGINT with its handler

UPLOAD_FOLDER = 'img_uploaded'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
RADIAL_RESOLUTION_BOUNDS = {'min':1,'max':48}
ANGULAR_RESOLUTION_BOUNDS = {'min':1,'max':50}

RUN_ALLOWED = False

BUZZER_PIN = 22 #BCM TODO: check 17 otherwise
MOTOR_PIN = 6 #BCM

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

buzz = Buzzer(BUZZER_PIN, GPIO)
buzz.setEnable(True)

def startSequence():
  """Play a visual and sonor alert to make sure that display is alive
  """
  stopDisplay()
  flashStrip('green', 200)
  buzz.start()

def warnBeforeStart():
  """Play a visual and sonor alert before starting the propeller for safety reasons
  """
  for i in range(3):
    buzz.warn()
    flashStrip("yellow", 100)

def flashStrip(color, delay):
  """Flashes LED strip 

  Args:
      color (string): The expected color for flashing. Can be red, yellow or green
      delay (int): The time of flashing in milliseconds
  """
  if color not in ['red', 'yellow', 'green']:
    return
  #TODO: call(["./displayer/bin/flash_strip",color,str(delay)])

def getImageToDisplay():
  """Gets the image to be displayed from USB key
  """
  pass #TODO for use with no local network

def startDisplay():
  """Starts motor
  """
  warnBeforeStart()
  GPIO.output(MOTOR_PIN, GPIO.HIGH)

def stopDisplay(skipBuzz = False):
  """Stops display motor

  Args:
      skipBuzz (bool): If true, buzzer won't play any sound
  """
  GPIO.output(MOTOR_PIN, GPIO.LOW)
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

#TODO: make sure that displayer/bin/displayer and displayer/bin/flash_strip are present or compile them with make

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('preview', filename, as_attachment=True)

#TODO: disable start/stop button when pressed until the other is pressed

@app.route("/", methods=['GET', 'POST'])
def home():
  global RUN_ALLOWED
  if request.method == 'POST':
    if RUN_ALLOWED:
      if request.form.get('command') == 'run_prop':
        startDisplay()
        #TODO: call
        flash('Hélice démarrée avec succès','success')
        return render_template('index.html',preview_url="preview/preview.png", RUN_ALLOWED = RUN_ALLOWED)
      elif request.form.get('command') == 'stop_prop':
        #TODO: kill (see https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true)
        stopDisplay()
        flash('Hélice arrêtée avec succès','success')
        return render_template('index.html',preview_url="preview/preview.png", RUN_ALLOWED = RUN_ALLOWED)
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

            # Configuration variables
            nbEllipsesPerDiametralLine = 2*radial_res_input
            imageFileName = fullpath
            outputFileName = 'static/preview.png'
            nbSectors = angular_res_input #number of displaying sectors
            angleStep = int(180/nbSectors)
            zoomFactor = 90 #zoom factor in percent

            sourceImg = Image.open(imageFileName)
            sourceImg.convert('RGBA')
            imgMaxSize = max(sourceImg.size)
            baseImgSize = imgMaxSize*100//zoomFactor
            centeredImage = Image.new('RGB', (baseImgSize,)*2,'black')
            
            centeredImage.paste(sourceImg,((baseImgSize-sourceImg.size[0])//2,(baseImgSize-sourceImg.size[1])//2))

            pickingPoints = getPickingPoints(baseImgSize, nbEllipsesPerDiametralLine, angleStep)
            pickedColors = pickColors(pickingPoints, centeredImage)

            savePickedColors('./displayer/sequenced_image.h', pickedColors, nbSectors)
            renderPickedPointsPreview(outputFileName, pickedColors, 10)

            flash('Image importée et traitée avec succès, prévisualisation en cours', 'success')
            RUN_ALLOWED = True
            
            return render_template('index.html',preview_url="preview/preview.png", RUN_ALLOWED = RUN_ALLOWED)
  return render_template('index.html')

if __name__=="__main__":

  app.debug = True
  app.run(host='0.0.0.0')
