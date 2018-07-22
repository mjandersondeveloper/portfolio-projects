#!/usr/local/bin/python3

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
first_name = form.getvalue('first_name')
last_name  = form.getvalue('last_name')

if form.getvalue('gender'):
	gender = form.getvalue('gender')
else:
	gender = "None Selected"
	
if form.getvalue('Major'):
	major = form.getvalue('Major')
else:
	major = "None Selected"
	
if form.getvalue('Birthday'):
	birthday = form.getvalue('Birthday')
else:
	birthday = "None Selected"
	
if form.getvalue('family'):
	family = form.getvalue('family')
else:
	family = "None Selected"

print ("Content-type:text/html\r\n\r\n")
print ("<html>")
print ("<head>")
print ("<title>Hello - CGI Program</title>")
print ("</head>")
print ("<body>")
print ("<h2>Thank You %s %s!</h2>" % (first_name, last_name))
print ("<p>Gender: %s </p>" % gender)
print ("<p>Major: %s </p>" % major)
print ("<p>Birthday: %s </p>" % birthday)
print ("<p>Faimly Members: %s </p>" % family)
print ("</body>")
print ("</html>")
