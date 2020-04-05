from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from flask import current_app as app
from flask_login import login_required, logout_user
from .forms import UploadForm
from werkzeug.utils import secure_filename
import os, json

main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')     

@main_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    metafiles = os.listdir(os.path.join(app.instance_path, 'static/meta'))
    meta=[json.load(open(os.path.join(app.instance_path, 'static/meta', m))) for m in metafiles]
    return render_template('page.html', meta=meta)
    
@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    upload_form = UploadForm()
    if request.method == 'POST':
        if upload_form.validate_on_submit():
            try:
                lat = float(upload_form.lat.data)
                lng = float(upload_form.lng.data)
            except:
                return render_template('error.html', error=dict(head='lat lng', body='is not float'))
            name = '%s.json' % upload_form.name.data
            desc = upload_form.desc.data
            f = upload_form.photo.data
            filename = secure_filename(f.filename)
            with open(os.path.join(app.instance_path, 'static/meta', name), 'w') as metaf:
                metai = dict(lat=lat, lng=lng, desc=desc, img=filename)
                metaf.write(json.dumps(metai))
            f.save(os.path.join(app.instance_path, 'static/img', filename))
            
    pictures = os.listdir(os.path.join(app.instance_path, 'static/img'))
    return render_template('upload.html', form=UploadForm(), pictures=pictures)

@main_bp.route('/', methods=['GET', 'POST'])
def main():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/home')
    return redirect('/signup')
 
