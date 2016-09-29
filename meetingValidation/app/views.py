from app import app
from flask import render_template
from flask import Flask, request
from flaskext.mysql import MySQL

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pyvirtualdisplay import Display

mysql = MySQL()
#app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'AAMeetings'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/index')
@app.route('/')

def index():
	user = {'nickname': 'Sabirat'}  # fake user
	return render_template('index.html',
                           title='Home',
                           user=user)

@app.route("/Authenticate")
def Authenticate():
	cursor = mysql.connect().cursor()
	#cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
	cursor.execute("SELECT * from meetinginformation limit 1")
	data = cursor.fetchone()
	if data is None:
		return "Username or Password is wrong"
	else:
		#return "Logged in successfully
		browser = webdriver.Chrome("D:\Research\chromedriver.exe")
		browser.set_window_size(1080, 320)
		browser.set_window_position(100,100)
		#display = Display(visible=0, size=(900, 600))
		#display.start()
		browser.get(data[4])
		info_elems=browser.find_elements_by_tag_name(data[11])
		for elem in info_elems:
			if elem.get_attribute("outerHTML")==data[10]:

				highlight(elem)
				browser.execute_script("return arguments[0].scrollIntoView();", elem)
		print(browser.title)
		browser.save_screenshot('app/static/images/meetingScreenshot.png')
		return render_template('index.html',
                           title='Home',
                           time=data[2],day=data[1],address=data[3])

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    print("highlighting element")
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].style.background='yellow'",
                              element)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 5px solid red;")
    apply_style("border: 5px solid red;")
    #time.sleep(.3)
    #apply_style(original_style)

@app.route("/Formreturn")
def Formreturn():
	time = request.args.get('time')
	#print time
	return "hello"



@app.route("/EmbeddedPage")
def EmbeddedPage():
	cursor = mysql.connect().cursor()
	#cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
	cursor.execute("SELECT * from meetinginformation limit 1")
	data = cursor.fetchone()
	if data is None:
		return "Username or Password is wrong"
	else:
		#return "Logged in successfully
		return render_template('embedpage.html',
                           title='Home',url=data[4],time=data[2],address=data[3],day=data[1])
