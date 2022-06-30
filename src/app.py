from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()



if __name__ == '__main__':
    app.run(debug=True)
    

