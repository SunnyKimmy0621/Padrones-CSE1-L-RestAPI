import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from Routes.elements import elements_bp

# ----------------------------------------
# CREATE FLASK APP FIRST
# ----------------------------------------
app = Flask(__name__)

# ----------------------------------------
# JWT CONFIGURATION
# ----------------------------------------
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # change anytime
jwt = JWTManager(app)

# ----------------------------------------
# DATABASE CONFIGURATION
# ----------------------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KIMMYPRETTY'
app.config['MYSQL_DB'] = 'cs_new'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# Pass db instance to blueprint
elements_bp.mysql = mysql

# Register blueprint
app.register_blueprint(elements_bp)

# ----------------------------------------
# RUN APP
# ----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
