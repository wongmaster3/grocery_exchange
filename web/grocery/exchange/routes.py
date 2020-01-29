from flask import Blueprint, request, render_template, redirect, url_for, flash
from grocery.models import Items, db
from flask_login import current_user
from grocery.exchange.forms import ItemsEntryForm, FileForm
from flask_login import login_required
import pytesseract as pytess
from werkzeug.utils import secure_filename
from grocery import ALLOWED_EXTENSIONS, app
import json
from PIL import Image

exchange = Blueprint("exchange", __name__, url_prefix="/exchange")

@exchange.route('/load', methods=['GET'])
@login_required
def load():
    # Return list of goods in exchange
    item_list = Items.query.filter(Items.exchange_id == current_user.id).all()
    checked_list = json.dumps([])
    return render_template("home.html", formadd=ItemsEntryForm(), fileform=FileForm(), items=item_list, cost=0.0, checked=checked_list, tax=current_user.tax, tip=current_user.tip)


@exchange.route('/calculate', methods=['POST'])
@login_required
def calculate():
    # Return list of goods in exchange
    item_list = Items.query.filter(Items.exchange_id == current_user.id).all()
    checked_list = []
    total = 0
    for item in item_list:
        if request.form.get(str(item.id)):
            total += item.price
            checked_list.append(item.id)


    tax = float(request.form['Tax'])
    tip = float(request.form['Tip'])
    if tax > 1:
        tax = tax/100
    if tip > 1:
        tip = tip/100

    total = round(total * (1+tax+tip), 2)
    checked_list = json.dumps(checked_list)

    return render_template("home.html", formadd=ItemsEntryForm(), fileform=FileForm(), items=item_list, cost=total, checked=checked_list, tax=current_user.tax, tip=current_user.tip)


@exchange.route('/add', methods=['POST'])
@login_required
def add():
    # Add Item to list of goods
    form = ItemsEntryForm()
    if form.split.data < 1:
        flash('Split has to be >= 1!')
    elif form.price.data < 0:
        flash('Price cannot be negative!')
    else:
        item = Items(
            name=form.name.data,
            price=round(form.price.data/form.split.data, 2),
            split=form.split.data,
            exchange_id=current_user.id
        )

        db.session.add(item)
        db.session.commit()

    return redirect(url_for('exchange.load'))

@exchange.route('/upload', methods=['POST'])
@login_required
def upload():
    file_form = FileForm()
    file_name = file_form.file.data.filename

    if request.method == 'POST':
        filename = secure_filename(file_name)
        file_form.file.data.save(app.config['UPLOAD_FOLDER'] + "/" + filename)
        flash('Successfully Uploaded!')
        # # check if the post request has the file part
        # if file_name not in request.files:
        #     flash('No file part')
        # file = request.files[file_name]
        # # if user does not select file, browser also
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        # if not file and allowed_file(file_name):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        curr_file = Image.open(app.config['UPLOAD_FOLDER'] + "/" + filename)
        flash(pytess.image_to_string(curr_file))


    return redirect(url_for('exchange.load'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS