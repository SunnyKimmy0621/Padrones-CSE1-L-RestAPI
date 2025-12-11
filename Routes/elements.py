from dicttoxml import dicttoxml
from flask import Response, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

elements_bp = Blueprint('elements_bp', __name__)
elements_bp.mysql = None  

#HOME
@elements_bp.route('/')
def home():
    return jsonify({"message": "CS New REST API is running"})

#LOGIN (Generates the JWT Token)
@elements_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "USER" and password == "USER123":
        token = create_access_token(identity=username)
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid username or password"}), 401

#GET ALL (public)
@elements_bp.route('/api/elements', methods=['GET'])
def get_elements():
    try:
        format_type = request.args.get('format', 'json')

        cur = elements_bp.mysql.connection.cursor()
        cur.execute("SELECT * FROM element")
        rows = cur.fetchall()
        cur.close()

        elements = [
            {"element_id": r[0], "element": r[1], "element_state": r[2]}
            for r in rows
        ]

        if format_type == "json":
            return jsonify(elements), 200

        elif format_type == "xml":
            xml_data = dicttoxml(elements, custom_root='elements', attr_type=False)
            return Response(xml_data, mimetype='application/xml')

        return jsonify({"error": "Invalid format. Use xml or json."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#GET BY ID (public)
@elements_bp.route('/api/elements/<int:element_id>', methods=['GET'])
def get_element(element_id):
    try:
        format_type = request.args.get('format', 'json')

        cur = elements_bp.mysql.connection.cursor()
        cur.execute("SELECT * FROM element WHERE element_id = %s", (element_id,))
        row = cur.fetchone()
        cur.close()

        if row is None:
            return jsonify({"error": "Element not found"}), 404

        element_data = {
            "element_id": row[0],
            "element": row[1],
            "element_state": row[2]
        }

        if format_type == "json":
            return jsonify(element_data), 200

        elif format_type == "xml":
            xml_data = dicttoxml(element_data, custom_root='element', attr_type=False)
            return Response(xml_data, mimetype='application/xml')

        return jsonify({"error": "Invalid format. Use xml or json."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#CREATE (POST)
@elements_bp.route('/api/elements', methods=['POST'])
@jwt_required()
def add_element():
    data = request.get_json()

    if not data or 'element' not in data or 'element_state' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        cur = elements_bp.mysql.connection.cursor()
        cur.execute(
            "INSERT INTO element (element, element_state) VALUES (%s, %s)",
            (data['element'], data['element_state'])
        )
        elements_bp.mysql.connection.commit()
        new_id = cur.lastrowid
        cur.close()

        return jsonify({
            "message": "Element added successfully",
            "element_id": new_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#UPDATE (PUT)
@elements_bp.route('/api/elements/<int:element_id>', methods=['PUT'])
@jwt_required()
def update_element(element_id):
    data = request.get_json()

    if not data or 'element' not in data or 'element_state' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        cur = elements_bp.mysql.connection.cursor()
        cur.execute(
            "UPDATE element SET element=%s, element_state=%s WHERE element_id=%s",
            (data['element'], data['element_state'], element_id)
        )
        elements_bp.mysql.connection.commit()
        affected = cur.rowcount
        cur.close()

        if affected == 0:
            return jsonify({"error": "Element not found"}), 404

        return jsonify({"message": "Element updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#DELETE
@elements_bp.route('/api/elements/<int:element_id>', methods=['DELETE'])
@jwt_required()
def delete_element(element_id):
    try:
        cur = elements_bp.mysql.connection.cursor()
        cur.execute("DELETE FROM element WHERE element_id = %s", (element_id,))
        elements_bp.mysql.connection.commit()
        affected = cur.rowcount
        cur.close()

        if affected == 0:
            return jsonify({"error": "Element not found"}), 404

        return jsonify({"message": "Element deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#SEARCH (public)
@elements_bp.route('/api/elements/search', methods=['GET'])
def search_elements():
    query = request.args.get('query')
    format_type = request.args.get('format', 'json')

    if not query:
        return jsonify({"error": "Search query parameter is required"}), 400

    try:
        cur = elements_bp.mysql.connection.cursor()
        like = f"%{query}%"
        cur.execute("""
            SELECT * FROM element
            WHERE element LIKE %s OR element_state LIKE %s
        """, (like, like))
        rows = cur.fetchall()
        cur.close()

        results = [
            {"element_id": r[0], "element": r[1], "element_state": r[2]}
            for r in rows
        ]

        if not results:
            return jsonify({"message": "No elements found"}), 404

        if format_type == "json":
            return jsonify(results), 200

        elif format_type == "xml":
            xml_data = dicttoxml(results, custom_root="search_results", attr_type=False)
            return Response(xml_data, mimetype="application/xml")

        return jsonify({"error": "Invalid format. Use xml or json."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
