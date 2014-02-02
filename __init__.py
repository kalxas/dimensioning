from dimensioning import Dimensioning

def name():
    return "Dimensioning"

def description():
    return "Plugin for dimensioning."

def version():
    return "0.0.2"

def qgisMinimumVersion():
    return "2.0"

def authorName():
    return "Stefan Ziegler"
    
def icon():
	return "icons/dimensioning.png"        

def classFactory(iface):
    return Dimensioning(iface)
