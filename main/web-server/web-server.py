"""Web server script
"""
from logging import warning
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
RADIAL_RESOLUTION_BOUNDS = {'min':1,'max':48}
ANGULAR_RESOLUTION_BOUNDS = {'min':1,'max':50}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("flask_secret")

RUN_ALLOWED = False

def run_prop():
  #TODO
  pass

def stop_prop():
  #TODO
  pass

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('../preview', filename, as_attachment=True)

@app.route("/", methods=['GET', 'POST'])
def home():
  global RUN_ALLOWED
  if request.method == 'POST':
    if RUN_ALLOWED:
      if request.form.get('command') == 'run_prop':
        run_prop()
        flash('Hélice démarrée avec succès','success')
        return render_template('index.html',preview_url="preview.png", RUN_ALLOWED = RUN_ALLOWED)
      elif request.form.get('command') == 'stop_prop':
        stop_prop()
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