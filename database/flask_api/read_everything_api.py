from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = '../lite_lprDB.db'

@app.route('/register_get', methods=["GET"])
def register_car():

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM registered_cars
            """
            )
        
        # Fetch all results (get as a list of tuples where each tuple means each record)
        rows = cursor.fetchall()
        # print("Rows are list of tuples",rows)  # for testing

        # Get Column names (the first index of each item inside cursor.description contains the column name)
        # cursor.description contains metadata about query results (cursor.description is a tuple containing a lot of tuples inside)
        column_names = [description[0] for description in cursor.description]

        # Convert to "list of dictionaries"
        registered = []
        for row in rows:
            registered_dic = dict(zip(column_names,row)) # Map Column names with the data from the same index like id will map with 1 where both are on the 1st index on their list
            # print(registered_dic)
            registered.append(registered_dic)
        
        # Close database connection and frees up system resources
        conn.close()


        return jsonify ({"message":"Car Read Successfully!!!",
                         "count" : len(registered),
                         "data" : registered}),200 # Success for "GET"
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

