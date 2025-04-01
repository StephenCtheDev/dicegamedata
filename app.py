from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import cx_Oracle

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for all routes



# Oracle DB connection function
def get_db_connection():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', sid = 'orcl')  
    conn = cx_Oracle.connect(user='C##dicegame', password='stephen123', dsn=dsn_tns)
    return conn

@app.route('/')
def index():
    # This will serve your main dice game page
    return render_template('indexA.html')

@app.route('/dice_rolls_grid')
def dice_rolls_grid():
    # This will serve the second page for the dice combinations
    return render_template('dice_rolls_grid.html')

@app.route('/roll_dice', methods=['POST'])
def roll_dice():
    # Get the rolled values and save to database
    die1_value = request.json.get('die1')
    die2_value = request.json.get('die2')

    # Save the roll to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dice_rolls (die1, die2) VALUES (:die1, :die2)', die1=die1_value, die2=die2_value)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Roll recorded successfully!'}), 200

@app.route('/get_rolls_count', methods=['GET'])
def get_rolls_count():
    # Get the count of each dice combination from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT die1, die2, COUNT(*) FROM dice_rolls GROUP BY die1, die2 ORDER BY die1, die2')

    rolls_count = {}
    for row in cursor.fetchall():
        rolls_count[f'{row[0]}-{row[1]}'] = row[2]

    conn.close()

    return jsonify(rolls_count), 200

if __name__ == '__main__':
    app.run(debug=True)
