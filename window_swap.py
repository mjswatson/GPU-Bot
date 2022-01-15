import pygetwindow
a=pygetwindow.getAllTitles()
for x in a:
	there=x.find('Chrome')
	if there>0:
		break
chrome = pygetwindow.getWindowsWithTitle(x)[0]
chrome.maximize()
