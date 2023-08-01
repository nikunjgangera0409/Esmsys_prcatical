from flask import Flask, jsonify, request, abort
import pyodbc

server = ' mssql.esmsys.in,14251'
database = 'interview'
username = 'interview'
password = 'Interview@123'
driver = 'ODBC Driver 17 for SQL Server' 

connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

app = Flask(__name__)

def execute_query(query, params=None):
    with pyodbc.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result


@app.route('/data', methods=['GET'])
def get_data():
    district_data = execute_query('SELECT * FROM district')
    taluka_data = execute_query('SELECT * FROM taluka')
    village_data = execute_query('SELECT * FROM village')

    district_count = len(district_data)
    taluka_count = len(taluka_data)
    village_count = len(village_data)

    response = {
        'districts': district_data,
        'talukas': taluka_data,
        'villages': village_data,
        'district_count': district_count,
        'taluka_count': taluka_count,
        'village_count': village_count
    }
    return jsonify(response)

# POST API 
@app.route('/add', methods=['POST'])
def add_data():
    data = request.json  

    district_query = 'INSERT INTO District (id,d_name) VALUES (?)'
    taluka_query = 'INSERT INTO Taluka (d_id,t_id,t_name) VALUES (?)'
    village_query = 'INSERT INTO Village (t_id,v_id,v_name) VALUES (?)'

    with pyodbc.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(district_query, data.get('d_name'))
            cursor.execute(taluka_query, data.get('t_name'))
            cursor.execute(village_query, data.get('v_name'))
            connection.commit()

    return jsonify({'message': 'Data added successfully!'})

# DELETE API 
@app.route('/delete/<table>/<int:id>', methods=['DELETE'])
def delete_data(table, id):
    
    if table == 'district':
        delete_query = 'DELETE FROM District WHERE id = ?'
    elif table == 'taluka':
        delete_query = 'DELETE FROM Taluka WHERE t_id = ?'
    elif table == 'village':
        delete_query = 'DELETE FROM Village WHERE v_id = ?'
    else:
        return jsonify({'error': 'Invalid table name!'})

    with pyodbc.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(delete_query, id)
            connection.commit()

    return jsonify({'message': f'Data with ID {id} deleted successfully from {table.capitalize()} table!'})

if __name__ == '__main__':
    app.run(debug=True)