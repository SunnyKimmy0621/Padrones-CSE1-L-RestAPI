from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

elements_bp = Blueprint('elements', __name__)
mysql = MySQL()

# HOME
@elements_bp.route('/')
def home():
    return jsonify({"message": "CS New REST API is running"})

# GET ALL
@elements_bp.route('/api/elements', methods=['GET'])
def get_elements():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM element")
        rows = cur.fetchall()

        elements = []
        for row in rows:
            elements.append({
                "element_id": row[0],
                "element": row[1],
                "element_state": row[2]
            })

        cur.close()
        return jsonify(elements), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET BY ID
@elements_bp.route('/api/elements/<int:element_id>', methods=['GET'])
def get_element(element_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM element WHERE element_id = %s", (element_id,))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return jsonify({"error": "Element not found"}), 404

        return jsonify({
            "element_id": row[0],
            "element": row[1],
            "element_state": row[2]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE
@elements_bp.route('/api/elements', methods=['POST'])
def add_element():
    data = request.get_json()

    if not data or 'element' not in data or 'element_state' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO element (element, element_state) VALUES (%s, %s)",
            (data['element'], data['element_state'])
        )
        mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()

        return jsonify({
            "message": "Element added successfully",
            "element_id": new_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE
@elements_bp.route('/api/elements/<int:element_id>', methods=['PUT'])
def update_element(element_id):
    data = request.get_json()

    if not data or 'element' not in data or 'element_state' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE element SET element=%s, element_state=%s WHERE element_id=%s",
            (data['element'], data['element_state'], element_id)
        )
        mysql.connection.commit()

        if cur.rowcount == 0:
            cur.close()
            return jsonify({"error": "Element not found"}), 404

        cur.close()
        return jsonify({"message": "Element updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE
@elements_bp.route('/api/elements/<int:element_id>', methods=['DELETE'])
def delete_element(element_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM element WHERE element_id=%s", (element_id,))
        mysql.connection.commit()

        if cur.rowcount == 0:
            cur.close()
            return jsonify({"error": "Element not found"}), 404

        cur.close()
        return jsonify({"message": "Element deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#SEARCH (GET)
@app.route('/api/elements/search', methods=['GET'])
def search_elements():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Search query parameter is required"}), 400

    try:
        cur = mysql.connection.cursor()
        like_query = f"%{query}%"
        
        cur.execute("""
            SELECT * FROM element 
            WHERE element LIKE %s OR element_state LIKE %s
        """, (like_query, like_query))
        
        rows = cur.fetchall()
        cur.close()

        if not rows:
            return jsonify({"message": "No elements found"}), 404

        results = []
        for row in rows:
            results.append({
                "element_id": row[0],
                "element": row[1],
                "element_state": row[2]
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
