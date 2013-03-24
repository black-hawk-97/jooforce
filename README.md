# jooforce

Jooforce is a small Python application used to test the vulnerability of Joomla installations against brute force attacks. It supports being able to spoof user-agents and has the ability to automatically switch between different proxies to avoid detection.

## Author
- [rastating](http://blog.intninety.co.uk/) ([@iamrastating](https://twitter.com/iamrastating))

## Contributors
- [Phyushin](https://github.com/phyushin) ([@phyushin](https://twitter.com/phyushin))

## Quick Start
1. Download the latest copy of jooforce [here](https://github.com/intninety/jooforce/zipball/master)
2. Open a shell and navigate to the directory you extracted the above file
3. Run the script using the following command; replacing &lt;url&gt; with the URL of the administrator page you wish to attack, &lt;user&gt; with the username you wish to attempt to login as, and &lt;file&gt; with the full path to the file of passwords you want to use in the attack 

        python jooforce.py --url <url> --user <user> --dic <file> -v
    __n.b. each password must appear on a new line in the file.__

4. If the password has been found a message will be displayed presenting you with the matching password (see below).

        [+] Login found!
        [-] Password is: 00734260

## Using Automated Proxies
If you want to automatically switch between proxies once data is failing to post to the page (this in most cases is caused by a temporary ban being placed on the I.P address the data is originating from) then use the --proxies option to pass the full path to a file containing a list of proxies. As with the password file, the proxies in the file must all appear on a new line. If no port number is specified then port 80 is assumed to be the default port e.g. 192.168.1.12 in the file would be transformed to 192.168.1.12:80.

When executing the program in verbose mode (by using the -v switch) a notification will be displayed upon proxy switching, which will look like this:

    [+] Setting proxy to 213.42.124.107:80...
    [+] Starting dictionary attack...
    [-] Trying admin:005500
    [+] Switching proxy to 122.72.112.148:80...

If a proxy switch is initiated and all the proxies in the file have been exhausted, you will be displayed with a message indicating so and you will be given the option to revert to no-proxy mode (see below). Choosing to not revert will make jooforce automatically switch between proxies by starting from the beginning of the list again.

    [!] WARNING: The proxy list has been exhausted.
                 Do you want to revert to no-proxy mode? [yes/no]
             --> yes
    [-] Trying admin:00553236
    [-] Trying admin:00554123
    [-] Trying admin:00561100

__n.b. once reverted to no-proxy mode there is currently no way to re-enable proxy mode without ending the process and starting again.__

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
