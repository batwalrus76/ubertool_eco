"""
	Adds '{% load staticfiles %}' to top of any template
	that uses static files
"""

import os


"""
	'path' variable is commented out so the script isn't acciendently ran
"""
# path = "D:/GitHub/ubertool_src/ubertool_eco/templates/"
directory = os.listdir(path)

for f in directory:
	curr_f = open(path+f, 'r')
	
	contains_static = False

	for line in curr_f:
		# print line
		if "static/" in line:
			contains_static = True

	curr_f.close()

	
	if contains_static == True:
		print f
		curr_f = open(path+f, 'r')	
		temp = curr_f.read()
		curr_f.close()

		curr_f = open(path+f, 'w')		
		curr_f.write("{% load staticfiles %}\n")
		curr_f.write(temp)

	try:
		curr_f.close()
	except:
		pass

print "Done!"



# f = open(os.path.abspath(os.path.dirname(__file__))+"\\templates\\00landing_page.html", 'r')
# content = f.read()
# f.close()

# f = open(os.path.abspath(os.path.dirname(__file__))+"\\templates\\00landing_page.html", 'w')
# f.write("{% load staticfiles %}")
# f.write(content)
# f.close()
