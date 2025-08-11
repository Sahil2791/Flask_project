from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
# import requests

import os
# Database Configuration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# PostgreSQL URL from Render
DATABASE_URL = "postgresql://stock_db_agv0_user:Qslm3lWo31gs1NEAyCuh9kYsfBh1BAFK@dpg-d2ctp1idbo4c73c49jf0-a/stock_db_agv0"

# Render sometimes gives old-style 'postgres://' instead of 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your-secret-key"

db = SQLAlchemy(app)




app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Pre-filled lists
TYPES = [
    "N/A",
    "LCD",
    "Hard OLED",
    "Soft OLED",
    "Origal Screen",
    "Service Pack",
    "Pull out",
    "Copy Screen",
    "Anti shock case",
    "Megsafe case",
    "CD case",
    "Megsafe new case",
    "Bookcase",
    "Platina stand case",
    "Platina ring case",
    "Normal Screen Protector",
    "Privacy Screen Protector",
    "5D Screen Protector",
    "C to C - Cable",
    "C to C - Braided Cable",
    "USB TO C- Cable",
    "USB TO C- Braided Cable",
    "USB to Lightning - Cable",
    "USB to Lightning - Braided Cable",
    "USB to C OTG",
    "USB To Lighting OTG",
    "Apple Original C Plug",
    "Apple Original Lighting Cable",
    "Apple Original C To Lighting Cable",
    "Apple Original C To C Cable",
    "Apple Original Lighting Handfree",
    "Apple Original C Handfree",
    "USB C Plug",
    "USB A Plug",
    "2 in 1",
    "5K MAH Powerbank",
    "10k MAH Powerbank",
    "20 MAH Powerbank",
    "Battery",
    "Camera",
    "Camera Protector",
    "Camera Lens",
    "Back Glass",
    "Charging Port",
    "Ear Speaker",
    "Sim Tray",
    "Home Buttom",
    "Ear Speaker Flex",
    "Face ID Flex",
    "IPad Case",
    "IPad Digitiser",
    "IPad Screen Protector",
    "Cable",
    "Lighting Ear-phone",
    "Type C Ear-phone",
    "3.5mm Jack Ear-phone",
    "Lighting AUX Cable",
    "Type C AUX Cable",
    "USB Stick",
    "SD Card",
    "USB Card Reader",
    "Type C Card Reader",
]

PRODUCTS = [
    "N/A",
    "iPhone SE 2",
    "iPhone SE 3",
    "iPhone 7 ",
    "iPhone 7 Plus",
    "iPhone 8",
    "iPhone 8 Plus",
    "iPhone X",
    "iPhone Xs",
    "iPhone Xs Max",
    "iPhone Xr",
    "iPhone 11",
    "iPhone 11 Pro",
    "iPhone 11 Pro Max",
    "iPhone 12",
    "iPhone 12 Mini",
    "iPhone 12 Pro",
    "iPhone 12 Pro Max",
    "iPhone 13",
    "iPhone 13 Mini",
    "iPhone 13 Pro",
    "iPhone 13 Pro Max",
    "iPhone 14",
    "iPhone 14 Pro",
    "iPhone 14 Plus",
    "iPhone 14 Pro Max",
    "iPhone 15",
    "iPhone 15 Pro",
    "iPhone 15 Plus",
    "iPhone 15 Pro Max",
    "iPhone 16",
    "iPhone 16 Plus",
    "iPhone 16 Pro",
    "iPhone 16 Pro Max",
    "Samsung A12",
    "Samsung A13",
    "Samsung A14",
    "Samsung A15",
    "Samsung A16",
    "Samsung A20e",
    "Samsung A20s",
    "Samsung A21s",
    "Samsung A22 4G",
    "Samsung A22 5G",
    "Samsung A23 4G",
    "Samsung A23 5G",
    "Samsung A24 4G",
    "Samsung A24 5G",
    "Samsung A25 4G",
    "Samsung A25 5G",
    "Samsung A26 5G",
    "Samsung A31",
    "Samsung A32 4G",
    "Samsung A32 5G",
    "Samsung A33 5G",
    "Samsung A34 5G",
    "Samsung A35 5G",
    "Samsung A36 5G",
    "Samsung A40",
    "Samsung A41",
    "Samsung A42 4G",
    "Samsung A42 5G",
    "Samsung A50",
    "Samsung A51 4G",
    "Samsung A51 5G",
    "Samsung A52 5G",
    "Samsung A52s",
    "Samsung A53 5G",
    "Samsung A54 5G",
    "Samsung A55 5G",
    "Samsung A56 5G",
    "Samsung A71 4G",
    "Samsung A71 5G",
    "Samsung A73 5G",
    "Samsung A90 4G",
    "Samsung A90 5G",
    "Samsung A04",
    "Samsung A04s",
    "Samsung A03",
    "Samsung A03s",
    "Samsung A05",
    "Samsung A05s",
    "Samsung S6",
    "Samsung S6 Edge",
    "Samsung S7",
    "Samsung S7 Edge",
    "Samsung S8",
    "Samsung S8 Plus",
    "Samsung S9",
    "Samsung S9 Plus",
    "Samsung S10",
    "Samsung S10 Plus",
    "Samsung S10e",
    "Samsung S10 5G",
    "Samsung S20",
    "Samsung S20 Plus",
    "Samsung S20 Ultra",
    "Samsung S21",
    "Samsung S21 Plus",
    "Samsung S21 Ultra",
    "Samsung S22",
    "Samsung S22 Plus",
    "Samsung S22 Ultra",
    "Samsung S23",
    "Samsung S23 Plus",
    "Samsung S23 Ultra",
    "Samsung S24",
    "Samsung S24 Plus",
    "Samsung S24 Ultra",
    "Samsung S25",
    "Samsung S25 Plus",
    "Samsung S25 Ultra",
    "Google Pixel 4",
    "Google Pixel 4a",
    "Google Pixel 5",
    "Google Pixel 5a",
    "Google Pixel 6",
    "Google Pixel 6a",
    "Google Pixel 6 Pro",
    "Google Pixel 7",
    "Google Pixel 7a",
    "Google Pixel 7 Pro",
    "Google Pixel 8",
    "Google Pixel 8a",
    "Google Pixel 8 Pro",
    "Google Pixel 8 XL",
    "Google Pixel 9",
    "Google Pixel 9a",
    "Google Pixel 9 Pro",
    "Google Pixel 9 XL",
]


# Salary DB model will store one sheet per employee/week
class SalarySheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee = db.Column(db.String(200), nullable=False)
    shop = db.Column(db.String(200), nullable=False)
    week_from = db.Column(db.String(20), nullable=False)
    week_to = db.Column(db.String(20), nullable=False)
    prev_balance = db.Column(db.Float, default=0.0)
    # store daily rows as simple CSV of "shopname|wages|travel|bonus" for 7 days
    monday = db.Column(db.String(400), default='|||')
    tuesday = db.Column(db.String(400), default='|||')
    wednesday = db.Column(db.String(400), default='|||')
    thursday = db.Column(db.String(400), default='|||')
    friday = db.Column(db.String(400), default='|||')
    saturday = db.Column(db.String(400), default='|||')
    sunday = db.Column(db.String(400), default='|||')
    cash_collection = db.Column(db.Float, default=0.0)
    other_collection = db.Column(db.Float, default=0.0)
    bank_transfer = db.Column(db.Float, default=0.0)
    other = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'employee': self.employee,
            'shop': self.shop,
            'week_from': self.week_from,
            'week_to': self.week_to
        }

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sr = db.Column(db.Integer, nullable=False, unique=True)
    type = db.Column(db.String(120), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'Sr': self.sr,
            'Type': self.type,
            'Product': self.product,
            'Description': self.description,
            'Quantity': self.quantity
        }

with app.app_context():
    db.create_all()

def next_sr_smallest_gap():
    # returns smallest missing positive integer in sr sequence starting at 1
    srs = [r[0] for r in db.session.query(StockItem.sr).order_by(StockItem.sr).all()]
    n = 1
    for v in srs:
        if v == n:
            n += 1
        elif v > n:
            break
    return n

@app.route('/')
def home():
    return render_template('home.html')

# STOCK ROUTES
@app.route('/stock')
def stock():
    items = StockItem.query.order_by(StockItem.sr).all()
    next_sr = next_sr_smallest_gap()
    return render_template('stock.html', items=items, types=TYPES, products=PRODUCTS, next_sr=next_sr)

# New Code for search
@app.route('/stock/data')
def stock_data():
    type_search = request.args.get('type_search', '').strip()
    product_search = request.args.get('product_search', '').strip()

    query = StockItem.query
    if type_search:
        query = query.filter(StockItem.type.ilike(f"%{type_search}%"))
    if product_search:
        query = query.filter(StockItem.product.ilike(f"%{product_search}%"))

    items = query.order_by(StockItem.sr).all()
    return render_template('stock_table.html', items=items)



@app.route('/add', methods=['POST'])
def add_item():
    type_ = request.form.get('type')
    product = request.form.get('product')
    description = request.form.get('description','')
    quantity = int(request.form.get('quantity') or 0)
    sr = int(request.form.get('sr') or next_sr_smallest_gap())
    # ensure sr uniqueness: shift others if collision
    existing = StockItem.query.filter_by(sr=sr).first()
    if existing:
        # increment srs >= sr by 1 to make space
        items = StockItem.query.filter(StockItem.sr >= sr).order_by(StockItem.sr.desc()).all()
        for it in items:
            it.sr = it.sr + 1
        db.session.commit()
    item = StockItem(sr=sr, type=type_, product=product, description=description, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('stock'))

@app.route('/edit/<int:item_id>', methods=['GET','POST'])
def edit_item(item_id):
    item = StockItem.query.get_or_404(item_id)
    if request.method == 'POST':
        new_sr = int(request.form.get('sr') or item.sr)
        # if sr changed and collides, adjust others
        if new_sr != item.sr:
            if StockItem.query.filter(StockItem.sr==new_sr, StockItem.id!=item.id).first():
                # shift the sequence: make space by incrementing srs >= new_sr
                items = StockItem.query.filter(StockItem.sr >= new_sr).order_by(StockItem.sr.desc()).all()
                for it in items:
                    if it.id != item.id:
                        it.sr = it.sr + 1
            item.sr = new_sr
        item.type = request.form.get('type')
        item.product = request.form.get('product')
        item.description = request.form.get('description')
        item.quantity = int(request.form.get('quantity') or 0)
        db.session.commit()
        return redirect(url_for('stock'))
    return render_template('edit.html', item=item, types=TYPES, products=PRODUCTS)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = StockItem.query.get_or_404(item_id)
    sr_deleted = item.sr
    db.session.delete(item)
    db.session.commit()
    # After deletion, re-number srs to be consecutive starting from 1
    items = StockItem.query.order_by(StockItem.sr).all()
    for idx, it in enumerate(items, start=1):
        it.sr = idx
    db.session.commit()
    return redirect(url_for('stock'))

@app.route('/salary/<int:id>/edit', methods=['GET', 'POST'])
def salary_edit(id):
    s = SalarySheet.query.get_or_404(id)

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Prepare rows for GET request
    rows = []
    start_date = datetime.strptime(s.week_from, "%Y-%m-%d")
    for i, (dn, day) in enumerate(zip(day_names, days)):
        shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
        rows.append({
            'date': (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            'day_name': dn,
            'shop': shopn,
            'wages': float(wages or 0),
            'travel': float(travel or 0),
            'bonus': float(bonus or 0)
        })

    # Handle POST request
    if request.method == 'POST':
        s.employee = request.form.get('employee')
        s.shop = request.form.get('shop')
        s.week_from = request.form.get('week_from')
        s.week_to = request.form.get('week_to')
        s.prev_balance = float(request.form.get('prev_balance') or 0)

        # Loop over 7 days and update
        for i, day in enumerate(days):
            shopn = request.form.get(f'shop_{i}', '')
            wages = request.form.get(f'wages_{i}', '0')
            travel = request.form.get(f'travel_{i}', '0')
            bonus = request.form.get(f'bonus_{i}', '0')
            setattr(s, day, f"{shopn}|{wages}|{travel}|{bonus}")

        # Update summary fields
        s.cash_collection = float(request.form.get('cash_collection') or 0)
        s.other_collection = float(request.form.get('other_collection') or 0)
        s.bank_transfer = float(request.form.get('bank_transfer') or 0)
        s.other = float(request.form.get('other') or 0)

        db.session.commit()
        flash("Salary sheet updated successfully!", "success")
        return redirect(url_for('salary_view', id=s.id))

    return render_template('salary_edit.html', s=s, rows=rows)


@app.route('/export/excel')
def export_excel():
    items = StockItem.query.order_by(StockItem.sr).all()
    df = pd.DataFrame([i.to_dict() for i in items])
    if df.empty:
        df = pd.DataFrame(columns=['Sr','Type','Product','Description','Quantity'])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Stock Order')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     as_attachment=True, download_name='stock_order.xlsx')

# @app.route('/export/pdf')
# def export_pdf():
#     items = StockItem.query.order_by(StockItem.sr).all()
#     data = [['Sr','Type','Product','Description','Quantity']]
#     for it in items:
#         data.append([it.sr,it.type,it.product,it.description or '',it.quantity])
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20,leftMargin=20,topMargin=30,bottomMargin=18)
#     styles = getSampleStyleSheet()
#     elements = []
#     elements.append(Paragraph('<b>My Phone Bishop #351</b>', styles['Title']))
#     elements.append(Spacer(1,6))
#     elements.append(Paragraph('Stock Order List', styles['Heading2']))
#     elements.append(Spacer(1,12))
#     table = Table(data, repeatRows=1, hAlign='LEFT')
#     table.setStyle(TableStyle([
#         ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#f0f0f0')),
#         ('GRID',(0,0),(-1,-1),0.5,colors.grey),
#         ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
#         ('ALIGN',(0,0),(-1,0),'CENTER')
#     ]))
#     elements.append(table)
#     doc.build(elements)
#     buffer.seek(0)
#     return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='stock_order.pdf')

#lateest without time
# @app.route('/export/pdf')
# def export_pdf():
#     from reportlab.lib.pagesizes import A4
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
#     from reportlab.lib import colors
#     from reportlab.lib.styles import getSampleStyleSheet
#     from io import BytesIO
#     from datetime import datetime

#     # Query stock data
#     items = StockItem.query.order_by(StockItem.sr).all()

#     # Prepare table data
#     data = [['Sr', 'Type', 'Product', 'Description', 'Quantity']]
#     for it in items:
#         data.append([
#             it.sr,
#             it.type,
#             it.product,
#             it.description or '',
#             it.quantity
#         ])

#     # Create PDF buffer
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(
#         buffer,
#         pagesize=A4,
#         rightMargin=15,
#         leftMargin=15,
#         topMargin=20,
#         bottomMargin=20
#     )
#     styles = getSampleStyleSheet()
#     elements = []

#     # Header Section
#     elements.append(Paragraph("<b>My Phone Bishop #351</b>", styles['Title']))
#     elements.append(Spacer(1, 6))
#     elements.append(Paragraph("<b>Stock Order List</b>", styles['Heading2']))
#     elements.append(Spacer(1, 12))

#     # Table with fixed column widths
#     table = Table(
#         data,
#         colWidths=[40, 80, 120, 180, 60],
#         repeatRows=1,
#         hAlign='LEFT'
#     )

#     # Table styling
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('ALIGN', (0, 0), (-1, 0), 'CENTER'),   # Header center
#         ('ALIGN', (-1, 1), (-1, -1), 'CENTER'), # Quantity center
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('TOPPADDING', (0, 0), (-1, -1), 8),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#     ]))

#     elements.append(table)
#     elements.append(Spacer(1, 20))

#     # Footer with printed date
#     printed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     elements.append(Paragraph(f"<font size=9>Printed on: {printed_date}</font>", styles['Normal']))

#     # Build PDF
#     doc.build(elements)
#     buffer.seek(0)
#     return send_file(
#         buffer,
#         mimetype='application/pdf',
#         as_attachment=True,
#         download_name='stock_order.pdf'
#     )

@app.route('/export/pdf')
def export_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from io import BytesIO
    from datetime import datetime
    from flask import send_file

    # Query stock data
    items = StockItem.query.order_by(StockItem.sr).all()

    # Prepare table data
    data = [['Sr', 'Type', 'Product', 'Description', 'Quantity']]
    for it in items:
        data.append([
            it.sr,
            it.type,
            it.product,
            it.description or '',
            it.quantity
        ])

    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15,
        leftMargin=15,
        topMargin=20,
        bottomMargin=20
    )
    styles = getSampleStyleSheet()
    elements = []

    # Header Section
    elements.append(Paragraph("<b>My Phone Bishop #351</b>", styles['Title']))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<b>Stock Order List</b>", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Table with fixed column widths
    table = Table(
        data,
        colWidths=[40, 80, 120, 180, 60],
        repeatRows=1,
        hAlign='LEFT'
    )

    # Table styling
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),   # Header center
        ('ALIGN', (-1, 1), (-1, -1), 'CENTER'), # Quantity center
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Footer with printed date
    printed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"<font size=25>Printed on: {printed_date}</font>", styles['Normal']))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='stock_order.pdf'
    )


# SALARY ROUTES (single-sheet per employee/week)
@app.route('/salary')
def salary_list():
    sheets = SalarySheet.query.order_by(SalarySheet.id.desc()).all()
    return render_template('salary_list.html', sheets=sheets)

@app.route('/salary/new', methods=['GET','POST'])
def salary_new():
    if request.method == 'POST':
        employee = request.form.get('employee')
        shop = request.form.get('shop')
        week_from = request.form.get('week_from')
        week_to = request.form.get('week_to')
        prev_balance = float(request.form.get('prev_balance') or 0)

        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

        daily_data = {}
        for d in days:
            shopn = request.form.get(f'{d}_shop', '')
            wages = request.form.get(f'{d}_wages', '0')
            travel = request.form.get(f'{d}_travel', '0')
            bonus = request.form.get(f'{d}_bonus', '0')
            daily_data[d] = f"{shopn}|{wages}|{travel}|{bonus}"

        cash_collection = float(request.form.get('cash_collection') or 0)
        other_collection = float(request.form.get('other_collection') or 0)
        bank_transfer = float(request.form.get('bank_transfer') or 0)
        other = float(request.form.get('other') or 0)

        s = SalarySheet(
            employee=employee,
            shop=shop,
            week_from=week_from,
            week_to=week_to,
            prev_balance=prev_balance,
            cash_collection=cash_collection,
            other_collection=other_collection,
            bank_transfer=bank_transfer,
            other=other,
            **daily_data
        )

        db.session.add(s)
        db.session.commit()

        return redirect(url_for('salary_list'))

    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    return render_template('salary_new.html', days=days, day_names=day_names, zip=zip)



from datetime import datetime, timedelta

from datetime import datetime, timedelta

#Salary Veiw Logic

# @app.route('/salary/<int:id>')
# def salary_view(id):
#     s = SalarySheet.query.get_or_404(id)

#     days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#     day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     # Convert week_from to a date object
#     start_date = datetime.strptime(s.week_from, "%Y-%m-%d")

#     rows = []
#     total_wages = total_travel = total_bonus = 0

#     for i, (dn, day) in enumerate(zip(day_names, days)):
#         shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
#         wages = float(wages or 0)
#         travel = float(travel or 0)
#         bonus = float(bonus or 0)
#         total_wages += wages
#         total_travel += travel
#         total_bonus += bonus

#         # Calculate date for each day
#         day_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

#         rows.append({
#             "date": day_date,
#             "day_name": dn,
#             "shop": shopn,
#             "wages": wages,
#             "travel": travel,
#             "bonus": bonus
#         })

#     total_balance_now = (
#         (s.prev_balance or 0) +
#         total_wages + total_travel + total_bonus +
#         (s.cash_collection or 0) + (s.other_collection or 0) +
#         (s.bank_transfer or 0) + (s.other or 0)
#     )

#     return render_template(
#         'salary_view.html',
#         s=s,
#         rows=rows,
#         total_wages=total_wages,
#         total_travel=total_travel,
#         total_bonus=total_bonus,
#         total_balance_now=total_balance_now
#     )

#     s = SalarySheet.query.get_or_404(id)

#     days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#     day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#     # Convert week_from to a date object
#     start_date = datetime.strptime(s.week_from, "%Y-%m-%d")

#     rows = []
#     total_wages = total_travel = total_bonus = 0

#     for i, (dn, day) in enumerate(zip(day_names, days)):
#         shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
#         wages = float(wages or 0)
#         travel = float(travel or 0)
#         bonus = float(bonus or 0)
#         total_wages += wages
#         total_travel += travel
#         total_bonus += bonus

#         # Calculate date for each day
#         day_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")

#         rows.append({
#             "date": day_date,
#             "day_name": dn,
#             "shop": shopn,
#             "wages": wages,
#             "travel": travel,
#             "bonus": bonus
#         })

#     total_balance_now = (
#         (s.prev_balance or 0) +
#         total_wages + total_travel + total_bonus +
#         (s.cash_collection or 0) + (s.other_collection or 0) +
#         (s.bank_transfer or 0) + (s.other or 0)
#     )

#     return render_template(
#         'salary_view.html',
#         s=s,
#         rows=rows,
#         total_wages=total_wages,
#         total_travel=total_travel,
#         total_bonus=total_bonus,
#         total_balance_now=total_balance_now
#     )

@app.route('/salary/<int:id>')
def salary_view(id):
    s = SalarySheet.query.get_or_404(id)

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    start_date = datetime.strptime(s.week_from, "%Y-%m-%d")

    rows = []
    total_wages = 0
    total_travel = 0
    total_bonus = 0

    for i, (dn, day) in enumerate(zip(day_names, days)):
        shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
        wages = float(wages or 0)
        travel = float(travel or 0)
        bonus = float(bonus or 0)
        total_wages += wages
        total_travel += travel
        total_bonus += bonus

        rows.append({
            'date': (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            'day_name': dn,
            'shop': shopn,
            'wages': wages,
            'travel': travel,
            'bonus': bonus
        })

    # Calculate totals
    total_balance = s.prev_balance + total_wages + total_travel + total_bonus

    # Subtract collections & transfers to get Total Balance Now
    total_balance_now = total_balance - (
        (s.cash_collection or 0) +
        (s.other_collection or 0) +
        (s.bank_transfer or 0) +
        (s.other or 0)
    )

    return render_template(
        'salary_view.html',
        s=s,
        rows=rows,
        total_wages=total_wages,
        total_travel=total_travel,
        total_bonus=total_bonus,
        total_balance=total_balance,
        total_balance_now=total_balance_now
    )


#New Salary Layout
from datetime import datetime, timedelta

@app.route('/salary/<int:id>/export_pdf')
def salary_export_pdf(id):
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet

    s = SalarySheet.query.get_or_404(id)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    start_date = datetime.strptime(s.week_from, "%Y-%m-%d")

    buffer = BytesIO()
    # Reduced margins so content fills the page
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15, leftMargin=15, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    elements = []

    # Header Box
    header_data = [
        [Paragraph("<b>Salary Sheet</b>", styles['Title'])]
    ]
    header_table = Table(header_data, colWidths=[520])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6))

    # Employee Info Box
    info_data = [
        [Paragraph(f"<b>Employee Name:</b> {s.employee}", styles['Normal']),
         Paragraph(f"<b>Shop:</b> {s.shop}", styles['Normal'])],
        [Paragraph(f"<b>Week From:</b> {s.week_from}", styles['Normal']),
         Paragraph(f"<b>To:</b> {s.week_to}", styles['Normal'])],
        [Paragraph(f"<b>Previous Balance:</b> {s.prev_balance:.2f}", styles['Normal']), ""]
    ]
    info_table = Table(info_data, colWidths=[260, 260])
    info_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 10))

    # Main Table
    data = [['Date', 'Day', 'Shop Name', 'Wages', 'Travel', 'Bonus']]
    total_w = total_t = total_b = 0
    for i, (dn, day) in enumerate(zip(day_names, days)):
        shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
        wages = float(wages or 0)
        travel = float(travel or 0)
        bonus = float(bonus or 0)
        total_w += wages
        total_t += travel
        total_b += bonus
        day_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        data.append([day_date, dn, shopn, f"{wages:.2f}", f"{travel:.2f}", f"{bonus:.2f}"])

    # Totals row
    data.append(['', 'Total', '', f"{total_w:.2f}", f"{total_t:.2f}", f"{total_b:.2f}"])

    table = Table(data, colWidths=[70, 80, 190, 60, 60, 60])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    # Summary Box
    total_balance = s.prev_balance + total_w + total_t + total_b
    total_balance_now = total_balance - s.cash_collection - s.other_collection - s.bank_transfer - s.other

    summary_data = [
        ["Total Balance", f"{total_balance:.2f}"],
        ["Cash Collection From Sales", f"{s.cash_collection:.2f}"],
        ["Other Cash Collection", f"{s.other_collection:.2f}"],
        ["Bank Transfer", f"{s.bank_transfer:.2f}"],
        ["Other", f"{s.other:.2f}"],
        ["Total Balance Now", f"{total_balance_now:.2f}"]
    ]
    summary_table = Table(summary_data, colWidths=[300, 220])
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(summary_table)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'salary_{s.employee}.pdf')


# @app.route('/salary/<int:id>/export_pdf')
# def salary_export_pdf(id):
#     from reportlab.lib.pagesizes import A4
#     from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
#     from reportlab.lib import colors
#     from reportlab.lib.styles import getSampleStyleSheet

#     s = SalarySheet.query.get_or_404(id)
#     days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#     day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     start_date = datetime.strptime(s.week_from, "%Y-%m-%d")

#     buffer = BytesIO()
#     # Reduced margins so content fills the page
#     doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=15, leftMargin=15, topMargin=20, bottomMargin=20)
#     styles = getSampleStyleSheet()
#     elements = []

#     # Header Box
#     header_data = [
#         [Paragraph("<b>Salary Sheet</b>", styles['Title'])]
#     ]
#     header_table = Table(header_data, colWidths=[520])
#     header_table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
#     ]))
#     elements.append(header_table)
#     elements.append(Spacer(1, 6))

#     # Employee Info Box
#     info_data = [
#         [Paragraph(f"<b>Employee Name:</b> {s.employee}", styles['Normal']),
#          Paragraph(f"<b>Shop:</b> {s.shop}", styles['Normal'])],
#         [Paragraph(f"<b>Week From:</b> {s.week_from}", styles['Normal']),
#          Paragraph(f"<b>To:</b> {s.week_to}", styles['Normal'])],
#         [Paragraph(f"<b>Previous Balance:</b> {s.prev_balance:.2f}", styles['Normal']), ""]
#     ]
#     info_table = Table(info_data, colWidths=[260, 260])
#     info_table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
#         ('TOPPADDING', (0, 0), (-1, -1), 6),
#     ]))
#     elements.append(info_table)
#     elements.append(Spacer(1, 10))

#     # Main Table
#     data = [['Date', 'Day', 'Shop Name', 'Wages', 'Travel', 'Bonus']]
#     total_w = total_t = total_b = 0
#     for i, (dn, day) in enumerate(zip(day_names, days)):
#         shopn, wages, travel, bonus = (getattr(s, day) or '|0|0|0').split('|')
#         wages = float(wages or 0)
#         travel = float(travel or 0)
#         bonus = float(bonus or 0)
#         total_w += wages
#         total_t += travel
#         total_b += bonus
#         day_date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
#         data.append([day_date, dn, shopn, f"{wages:.2f}", f"{travel:.2f}", f"{bonus:.2f}"])

#     # Totals row
#     data.append(['', 'Total', '', f"{total_w:.2f}", f"{total_t:.2f}", f"{total_b:.2f}"])

#     table = Table(data, colWidths=[70, 80, 190, 60, 60, 60])
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
#         ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f0f0')),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('TOPPADDING', (0, 0), (-1, -1), 8),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 10))

#     # Summary Box
#     total_balance = s.prev_balance + total_w + total_t + total_b
#     total_balance_now = total_balance - s.cash_collection - s.other_collection - s.bank_transfer - s.other

#     summary_data = [
#         ["Total Balance", f"{total_balance:.2f}"],
#         ["Cash Collection From Sales", f"{s.cash_collection:.2f}"],
#         ["Other Cash Collection", f"{s.other_collection:.2f}"],
#         ["Bank Transfer", f"{s.bank_transfer:.2f}"],
#         ["Other", f"{s.other:.2f}"],
#         ["Total Balance Now", f"{total_balance_now:.2f}"]
#     ]
#     summary_table = Table(summary_data, colWidths=[300, 220])
#     summary_table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 0.75, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('TOPPADDING', (0, 0), (-1, -1), 8),
#         ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
#     ]))
#     elements.append(summary_table)

#     # Build PDF
#     doc.build(elements)
#     buffer.seek(0)
#     return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'salary_{s.employee}.pdf')


@app.route('/stock/clear')
def clear_all():
    StockItem.query.delete()
    db.session.commit()
    return redirect(url_for('stock'))


@app.route('/salary/<int:id>/export_excel')
def salary_export_excel(id):
    s = SalarySheet.query.get_or_404(id)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day_names = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    rows = []
    for dn,d in zip(day_names,days):
        parts = getattr(s,d).split('|')
        rows.append({'Date':'','Day':dn,'Shop Name':parts[0],'Wages':parts[1],'Travel':parts[2],'Bonus':parts[3]})
    # totals
    df = pd.DataFrame(rows + [{'Date':'','Day':'Total','Shop Name':'','Wages':sum(float(r['Wages'] or 0) for r in rows),'Travel':sum(float(r['Travel'] or 0) for r in rows),'Bonus':sum(float(r['Bonus'] or 0) for r in rows)}])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Salary Sheet')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f'salary_{s.employee}.xlsx')

@app.route('/salary/<int:id>/delete', methods=['POST'])
def salary_delete(id):
    s = SalarySheet.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Salary sheet deleted successfully.', 'success')
    return redirect(url_for('salary_list'))

@app.route('/cex')
def cex_price_page():
    return render_template('cex_price.html')

#Cex price search

# -----------------------
# CEX PRICE CHECKER ROUTES
# -----------------------

# @app.route('/cex')
# def cex_page():
#     """Render the main CEX price checker page."""
#     return render_template('cex_price.html')

@app.route('/cex')
def cex_price():
    return render_template('cex_price.html')


@app.route('/cex/fetch_price')
def cex_fetch_price():
    """Fetch price from CEX API for a given product."""
    product = request.args.get('product', '')
    if not product:
        return {"price": None}

    url = "https://wss2.cex.uk.webuy.io/v3/boxes"
    try:
        resp = requests.get(url, params={'q': product}, timeout=6, verify=True)
        data = resp.json()
        boxes = data.get('response', {}).get('data', {}).get('boxes', [])
        if boxes:
            price = boxes[0].get('sellPrice', None)
            return {"price": price}
        return {"price": None}
    except Exception as e:
        return {"price": None, "error": str(e)}

@app.route('/cex/suggestions')
def cex_suggestions():
    """Return autocomplete suggestions from CEX API."""
    query = request.args.get('query', '')
    if not query:
        return {"suggestions": []}

    url = "https://wss2.cex.uk.webuy.io/v3/boxes"
    try:
        resp = requests.get(url, params={'q': query}, timeout=6, verify=True)
        data = resp.json()
        suggestions = [
            item['boxName']
            for item in data.get('response', {}).get('data', {}).get('boxes', [])
        ]
        return {"suggestions": suggestions}
    except Exception:
        return {"suggestions": []}

@app.route('/_debug_cex')
def _debug_cex():
    """Debug route to test raw CEX API output."""
    q = request.args.get('q', 'iphone 12')
    try:
        r = requests.get('https://wss2.cex.uk.webuy.io/v3/boxes', params={'q': q}, timeout=6, verify=True)
        return {"ok": True, "status": r.status_code, "data": r.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}




if __name__ == '__main__':
    app.run(debug=True)
