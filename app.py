import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_mysqldb import MySQL
from routes.elements import elements_bp

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'KIMMYPRETTY'
app.config['MYSQL_DB'] = 'cs_new'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

# Pass MySQL to blueprint
elements_bp.mysql = mysql

# Register routes
app.register_blueprint(elements_bp)

if __name__ == "__main__":
    app.run(debug=True)
