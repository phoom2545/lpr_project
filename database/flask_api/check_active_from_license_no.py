from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = '../lite_lprDB.db'

# Add this when returning the thai character
app.json.ensure_ascii = False

# API ENDPOINTS

@app.route('/check_no', methods=["GET"])
def check_activation_from_license_no():

    try:
        # Get data from 
        data = request.get_json()
        license_no = data['license_no']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT license_number, status FROM registered_cars
            WHERE license_number = ?
            '''
            ,(license_no,) # Put , (comma) to treat it as a tuple because Sqlite wants a tuple as a parameter. So, even a single parameter is passed, make it a tuple
            )
        
        result = cursor.fetchone() # use fetchall() if want more than one record
        conn.close()

        # from cursor.fetchone() we will get a tuple, we only want the first one
        status = result[1]
        
        return jsonify ({"message" : "Success",
                         "license_status" : status}), 200
    
    # Get into this 
    except TypeError:
        return jsonify({"type_error_message": "The license number inserted can't be found"}) , 404
        
    except Exception as e:
        return jsonify({"error_message": str(e)}),404
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)