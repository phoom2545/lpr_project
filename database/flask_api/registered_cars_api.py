from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = '../lite_lprDB.db'

@app.route('/register_insert', methods=["POST"])
def register_insert():
    data = request.get_json()
    print("THIS is JSON: ",data)
    print("THIS is JSON license no.: ",data['license_number'])

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Exceute SQL command
        cursor.execute("""
            INSERT INTO registered_cars(license_number,license_province,name,phone,email,status,location,current_package_detail,package_start_date,package_end_date)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            """
            ,(
            data['license_number'],
            data['license_province'],
            data['name'],
            data['phone'],
            data['email'],
            data['status'],
            data['location'],
            data['current_package_detail'],
            data['package_start_date'],
            data['package_end_date']
        ))

        # Saves and Confirms all changes made to the database (Need for INSERT, UPDATE, DELETE, CREATE TABLE, DROP TABLE) but not for SELECT
        conn.commit()

        # Close database connection and frees up system resources
        conn.close() 

        
        return jsonify ({"message":"Car Registered Successfully!!!"}),201 # Success for "POST"
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

