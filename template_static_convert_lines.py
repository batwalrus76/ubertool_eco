"""
	Converts 'src' and 'href' references to static files
	to use Django 'static' template variable.  E.g.
	src='/static/images/home.gif' becomes:
	src='{% static "/images/home.gif" %}'.  This allows 
	for the static url to be set in Django settings file
	"STATIC_URL', which can be easily set to use a cloud
	service such as Amazon S3 or a CDN.

	NOTE: This script fill overwrite the files it is ran 
	on.  Please backup files before running script.
"""

"""
	Known issues:
	history_query.html  :  loader.gif img src in Ajax call gets messed up
"""


import os, sys
from bs4 import BeautifulSoup
import re
import fileinput


"""
	'path' variable is commented out so the script isn't acciendently ran
"""
# path = "D:/GitHub/ubertool_src/ubertool_eco/templates/"
directory = os.listdir(path)

for f in directory:

	for line in fileinput.input(path+f, inplace=True):
		if "/static" in line:
			# Convert the '/static' reference to desired one:
			
			# Determine number of spaces before opening HTML tag
			try:
				spacing = line.index('<')
			except:
				spacing = 1

			# Re-create the spaces before opening HTML tag
			line_spaces = ""
			while (spacing > 0):
				line_spaces = line_spaces + " "
				spacing = spacing - 1

			soup = BeautifulSoup(line, "html.parser")

			src_tags = soup.find_all(True, src=re.compile("/static"))
			href_tags = soup.find_all(True, href=re.compile("/static"))
			
			if len(src_tags) > 0:
				for item in src_tags:
					# Convert '/static' to '{% static '...' %}'
					src = item['src']
					
					static_index = str(src).find('static')
					# print static_index

					src_no_static = str(src)[static_index + len('static') + 1:]

					# Sets the 'src' attribute to the new format in the BS object
					item['src'] = "{% static \"" + src_no_static + "\" %}"
					# print item['src']

					# Re-write line with updated 'src'
					sys.stdout.write(line_spaces + str(item) + '\n')

			if len(href_tags) > 0:
				for item in href_tags:
					# Convert '/static' to '{% static '...' %}'
					href = item['href']
					
					static_index = str(href).find('static')
					# print static_index

					href_no_static = str(href)[static_index + len('static') + 1:]

					# Sets the 'href' attribute to the new format in the BS object
					item['href'] = "{% static \"" + href_no_static + "\" %}"
					# print item['href']

					# Re-write line with updated 'href'
					sys.stdout.write(line_spaces + str(item) + '\n')

		else:
			# Rewrite the line as-is:
			sys.stdout.write(line)

	# curr_f = open(path+f, 'r')
	# # curr_f.read()
	
	# for line in curr_f:
	# 	# Create BS object for each line of the file
	# 	soup = BeautifulSoup(line, "html.parser")	
		
	# 	src_tags = soup.find_all(True, src=re.compile("/static"))
	# 	href_tags = soup.find_all(True, href=re.compile("/static"))
		
	# 	if len(src_tags) > 0:
	# 		for item in src_tags:
	# 			print item['src']
	# 			# if ("ubertool" in item):
	# 				# print f
	# 		# print src_tags
	# 	# if len(href_tags) > 0:
	# 		# for item in href_tags:
	# 			# if ("static" in href_tags):
	# 				# print f
	# 		# print href_tags

	# 	# src_new = []

	# 	# If file contains a line with '/static', proceed:
	# 	# if len(src_tags) > 0:
	# 	# 	print f
	# 	# 	# For each line in file with '/static':
	# 	# 	for item in src_tags:
	# 	# 		# Convert '/static' to '{% static '...' %}'
	# 	# 		src = item['src']
				
	# 	# 		static_index = str(src).find('static')
	# 	# 		# print static_index

	# 	# 		src_no_static = str(src)[static_index + len('static') + 1:]

	# 	# 		# Sets the 'src' attribute to the new format, but this is not
	# 	# 		# what I want because BeautifulSoup cannot resist from changing
	# 	# 		# my code (e.g. adding </body>, </html>, etc...)

	# 	# 		# item['src'] = "{% static \"" + src_no_static + "\" %}"
	# 	# 		# print item['src']

	# 	# 		# Instead I will need to save the correct string and write file iteratively

	# 	# 		src_new.append("{% static \"" + src_no_static + "\" %}")
	# 	# 		# print src_new

	# 	# curr_f.close()
	# 	curr_f = open(path+f, 'r')
	# 	orig_lines = curr_f.readlines()

	# 	# i = 0
	# 	# for line in orig_lines:
	# 	# 	# print "/static" in line
	# 	# 	if "/static" in line:
	# 	# 	# 	print "BLAH = "+orig_lines[i]
	# 	# 		print "line = "+line
	# 	# 	# 	i += 1

	# 	curr_f.close()

	# # with open(path+f, 'wb') as f:
	# # 		f.write(orig_lines)


	# 	# print soup.prettify('utf-8')
	# 	# print soup

	# 	# Write new HTML to file
	# 	# with open(path+f, 'wb') as file:
	# 	# 	file.write(soup)

	# 	# Remove last two lines added by BeautifulSoup:
	# 	# curr_f = open(path+f, 'r')
	# 	# lines = curr_f.readlines()
	# 	# lines = lines[:-2]
	# 	# curr_f.close()

	# 	# curr_f = open(path+f, 'w')
	# 	# curr_f.writelines()
	# 	# curr_f.close()

	try:
		curr_f.close()
	except:
		pass

print "Done!"
