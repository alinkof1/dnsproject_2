In this case I chose to edit out:

.domain.com 192.168.1.1
.scorecardresearch.com 192.168.127.127
.doubleclick.net 192.168.127.127
.googletagmanager.com 192.168.127.127
.bluekai.com 192.168.127.127
.truste.com 192.168.127.127
.effectivemeasure.net. 192.168.127.127
.googlesyndication.com. 192.168.127.127
.effectivemeasure.net. 192.168.127.127
.imrworldwide.com. 192.168.127.127
.turner.com. 192.168.127.127
.optimizely.com. 192.168.127.127
.postrelease.com. 192.168.127.127
.krxd.net. 192.168.127.127
.criteo.com. 192.168.127.127
.amazon-adsystem.com. 192.168.127.127
.usabilla.com. 192.168.127.127
.visualrevenue.com. 192.168.127.127
.go-mpulse.net. 192.168.127.127
.pivit.io. 192.168.127.127
.zqtk.net. 192.168.127.127
.ugdturner.com. 192.168.127.127
.yieldmo.com. 192.168.127.127
.outbrain.com. 192.168.127.127
.digicert.com. 192.168.127.127



I edited the dns2proxy file with the following lines 
to prevent it from printing the blocked hosts:

in "def requestHandler(address, message)":

domains_names = []
domains = ""
with open("domains.cfg", "r") as hosts:
	for domains in hosts:
		domains_names.append(domains.split(" ")[0])


dns_host = str(q)
block_count = 0
for d in domains_names:
	DEBUGLOG('d is ' + d)
	if(dns_host.find(d) >= 0):
		block_count = 1
if(block_count != 1):
	save_req(LOGREQFILE, 'Client IP: ' + address[0] + '    request is    ' + str(q) + '\n')