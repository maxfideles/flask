from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sys
import os
sys.path.append('/cons')
from cons import main
from cons import funcs

app = Flask(__name__)

# @app.route("/upload-pdf", methods=['POST', 'GET'])
# def upload_pdf():
# 	return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])

def index():
	res=[0,0,0,0,0,0,0,0,[0,0,0,0,0,0,0,0,0,0,0,0],
	[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
	[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],0]
	if(request.method=='POST'):
		if(request.files):
			mpdf=request.files['arquivo']
			mpdf.save(os.getcwd()+'\\TEMP\\temp.pdf')
			res=main.principal()
	return render_template('index.html', res=res)

if(__name__=="__main__"):
	app.run(debug=True)