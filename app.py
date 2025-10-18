from flask import Flask, render_template, request, redirect
from mysql.connector import connection
import random

app = Flask(__name__)


def get_db_connection():
    conn = connection.MySQLConnection(
        user="root",
        host="localhost",
        password="root123",
        database="tours_travels"
    )
    return conn

packages = {
    "WAYANAD, KERALA": 5500,
    "COORG, KARNATAKA": 5000,
    "OOTY, TAMIL NADU": 6000,
    "DUDHSAGAR FALLS, GOA": 7000,
    "LONAVALA, MAHARASTRA": 8500,
    "DARJEELING, WEST BENGAL": 24000,
    "MANALI, HIMACHAL PRADESH": 25000,
    "JAMA MASJID, DELHI": 30000,
    "NOTRE-DAME, PARIS": 30000,
    "HAJI ALI DARGAH, MUMBAI": 15000,
    "VATICAN CITY, ROME": 40000,
    "VAISHNO DEVI KATRA , JAMMU & KASHMIR": 16000,
    "SENSO-JI-TEMPLE, JAPAN": 50000,
    "TIRUPATI BALAJI MANDIR, TAMIL NADU": 12000,
    "ST.FRANCIS XAVIER, GOA": 2000,
    "PURA ULUN DANU BRATAN TEMPLE, BALI": 80000
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view-packages')
def view_packages():
    return render_template('view_packages.html', packages=packages)
@app.route('/book', methods=['GET', 'POST'])
def book_ticket():
    calculated_amount = None
    selected_payment_method = None

    if request.method == 'POST':
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        passengers = int(request.form.get('passengers', 1))
        address = request.form.get('address', '')
        package_name = request.form.get('package', '')
        date = request.form.get('date', '')
        selected_payment_method = request.form.get('payment_method', '')

        # Calculate total
        if package_name in packages:
            calculated_amount = packages[package_name] * passengers

        # If user clicked "Book"
        if 'book' in request.form:
            amount = int(request.form['amount'])
            booking_no = random.randint(10000, 99999)

            upi_id = request.form.get('upi_id')
            upi_pin = request.form.get('upi_pin')
            card_name = request.form.get('card_name')
            card_number = request.form.get('card_number')
            expiry = request.form.get('expiry')
            cvv = request.form.get('cvv')

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Booking_details (Pname, PhNo, NoPsng, Address, Package, DtTrvl, amount, BkNo) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (name, phone, passengers, address, package_name, date, amount, booking_no)
            )
            conn.commit()
            cur.close()
            conn.close()
            return render_template(
                'success.html',
                booking_no=booking_no,
                amount=amount,
                payment_method=selected_payment_method
            )

        return render_template(
            'book_ticket.html',
            packages=packages,
            calculated_amount=calculated_amount,
            selected_payment_method=selected_payment_method,
            request=request
        )
    return render_template('book_ticket.html', packages=packages)





@app.route('/cancel', methods=['GET', 'POST'])
def cancel_ticket():
    if request.method == 'POST':
        bno = int(request.form['booking_no'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Booking_details WHERE BkNo=%s", (bno,))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('success.html', canceled=True)
    return render_template('cancel_ticket.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)
