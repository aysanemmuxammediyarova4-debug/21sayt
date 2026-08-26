from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hotel_booking_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modellar
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), nullable=False)   # Masalan: 302-xona
    room_type = db.Column(db.String(50), nullable=False)     # Standard, Lux, Family, Deluxe
    price_per_night = db.Column(db.Float, nullable=False)   # Kunlik narx (so'm)
    capacity = db.Column(db.Integer, nullable=False)         # Necha kishilik
    image_url = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.String(20), nullable=False)    # Kelish sanasi
    check_out = db.Column(db.String(20), nullable=False)   # Ketish sanasi

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    room_type = request.args.get('room_type')
    if room_type:
        rooms = Room.query.filter_by(room_type=room_type).all()
    else:
        rooms = Room.query.all()
    return render_template('index.html', rooms=rooms, selected_type=room_type)

@app.route('/room/<int:room_id>', methods=['GET', 'POST'])
def room_detail(room_id):
    room = Room.query.get_or_404(room_id)
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        phone = request.form['phone']
        check_in = request.form['check_in']
        check_out = request.form['check_out']

        booking = Booking(
            room_id=room.id,
            guest_name=guest_name,
            phone=phone,
            check_in=check_in,
            check_out=check_out
        )
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('room_detail.html', room=room)

@app.route('/add', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        room_number = request.form['room_number']
        room_type = request.form['room_type']
        price_per_night = float(request.form['price_per_night'])
        capacity = int(request.form['capacity'])
        image_url = request.form['image_url']
        description = request.form['description']

        new_room = Room(
            room_number=room_number, room_type=room_type,
            price_per_night=price_per_night, capacity=capacity,
            image_url=image_url, description=description
        )
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_room.html')

if __name__ == '__main__':
    app.run(debug=True)