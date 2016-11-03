#! /usr/bin/env python

#Alex Linkoff
#CNS Proj2 dnsproject
#dnsproject.py


import re
import string 


#-------------------------Start function definitions------------------------------#

#separate out only the host names and the timestamps
def parse_for_hosts_times(dns_split):
	dns_host_list = []
	dns_timestamps = []
	for i,w in enumerate(dns_split):
		if (w):
			dns_space = w.split(" ")
			dns_host_list.append(dns_space[13])
			dns_timestamps.append(dns_space[1])
	return dns_host_list,dns_timestamps

#isolate the timestamp and get the total time in milliseconds at each dns request and store in a new array
def find_timestamps_ms(dns_timestamps):
	total_time_ms = []
	i=0
	w=0
	for i,w in enumerate(dns_timestamps):
		if (w):
			time_break = w.split(":")
			hours_in_ms = long(time_break[0]) * 3600000
			mins_in_ms = long(time_break[1]) * 60000
			sec_ms = time_break[2].split(".")
			secs_in_ms = long(sec_ms[0]) * 1000
			ms = long(sec_ms[1])
			total_time_ms.append(hours_in_ms + mins_in_ms + secs_in_ms + ms)
	return total_time_ms

#determine if the timestamp of consecutive dns queries were at least x secs (15) apart and store "most-likely"
#locations of dns queries
def find_potential_host_locs(total_time_ms):
	i=0
	j=0
	w=0
	difference = 0
	possible_host_locs = []
	possible_host_locs.append(0) #append 0 entry as the first host searched
	for i,time in enumerate(total_time_ms):
		if (time):
			difference = abs(time - total_time_ms[i-1])
			if(difference >= 15000):
				print difference
				possible_host_locs.append(i)
	possible_host_locs.pop(1)	#remove garbage 1 entry
	return possible_host_locs


#possible hosts (unfiltered)
def print_potential_hosts(possible_host_locs, dns_host_list):
	print "hosts maybe are:"
	hostnames = []
	i=0
	for i in range(len(possible_host_locs)):
		print dns_host_list[possible_host_locs[i]]
		hostnames.append(dns_host_list[possible_host_locs[i]])
	return hostnames


#filter hostnames and ensure they are the correct dns queries
#if the hostname doesn't "look" like a valid host, replace it with a nearby "valid looking" host
def filter_hosts(hostnames, possible_host_locs):
	j=0
	print "\nnew hosts:"
	for i in range(len(possible_host_locs)):
		if(re.search(r'(!((\S+)(\.)))(\S+)(\.)(?:com|org|edu)', hostnames[i])):
			hostnames.pop(i)
			j=i
			for j in range(j,(len(possible_host_locs)-1)):
				if(dns_host_list[j].count(".") == 3):
					if (re.search(r'(www(\.))?(\S+)(\.)(?:com|org|edu)', dns_host_list[j])):
						possible_host_locs.insert(i,j)
						hostnames.insert(i,dns_host_list[j])
		print hostnames[i]
	return hostnames, possible_host_locs


#find the time stamps for each request
def find_timestamps(hostnames, possible_host_locs, dns_timestamps):
	j=0
	i=0
	hosts_timestamps = []
	diff = 0
	for i,dns_name in enumerate(hostnames):
		if (dns_name):
			hosts_timestamps.append(dns_timestamps[possible_host_locs[i]])
	return hosts_timestamps


#find dns query "count" for each request and find intermediate members between unique dns requests
#shift each difference count forward
def find_count_bet_hosts(dns_host_list, possible_host_locs):
	loc=0
	j=0
	k=0
	hostnames_between = []
	temp_array = []
	subhosts_count = []
	for i,loc in enumerate(possible_host_locs):
		if(loc):
			count = loc - possible_host_locs[i-1] -1
			subhosts_count.append(count)
	#subhosts_count.pop(0)
	subhosts_count.append(abs(len(dns_host_list) - possible_host_locs[-1] - 1))
	print subhosts_count
	return subhosts_count


#find duplicate values in the dns_host_list array and make them "NONE"
#return the number of duplicates for each dns query made
def filter_duplicates(dns_host_list, possible_host_locs, subhosts_count, hosts_timestamps):
	i=0
	nullCountArray = []
	for k, loc in enumerate(possible_host_locs):
		temp = []
		nullCount = 0
		for i in range(loc, (loc + subhosts_count[k])):
			if dns_host_list[i] not in temp:
				temp.append(dns_host_list[i])
			else:
				dns_host_list[i] = None
				nullCount += 1
		nullCountArray.append(nullCount)
	print nullCountArray
	return nullCountArray


#print to .txt file
#first, indexes through known host locations, then prints the host, dns requests and timestamp at that location
#then, prints each "subhost" dns request made for the original query
def print_to_file(dns_host_list, possible_host_locs, subhosts_count, hosts_timestamps, nullCountArray):
	report = open("report_with_blocking.txt", 'w')
	for i,host_loc in enumerate(possible_host_locs):
		report.write("%s: %s times: %s\n" % (dns_host_list[host_loc], (subhosts_count[i] - nullCountArray[i]), hosts_timestamps[i]))
		j=0
		for subhost in range(host_loc, (host_loc + subhosts_count[i])):
			if dns_host_list[subhost] != None:
				j+=1
				report.write("%d. %s\n" % (j,dns_host_list[subhost]))
	report.close()

#-------------------------Start main program------------------------------#

#open dnslog.txt to read in the info and store to local variable
file_in = open('dnslog_with_blocking.txt', 'r')
dnslog = file_in.read()
file_in.close()

#counting total number of dns requests
dnsCount = dnslog.count("IN AAAA")
print ("total dns requests: %d" % dnsCount)

#format the string separating each dns request, ignoring the duplicate (ipv4) requests
dns_split = dnslog.split("\n")
sub = "IN AAAA"

#for i,w in enumerate(dns_split):
#	print("%d. %s" %(i,w))

dns_split = "\n".join(s for s in dns_split if sub.lower() in s.lower()).split("\n")

#for i,w in enumerate(dns_split):
#	print("%d. %s" %(i,w))

dns_host_list = []
dns_timestamps = []

#store all the dns hosts and timestamps in separate arrays
dns_host_list, dns_timestamps = parse_for_hosts_times(dns_split)

#for i,w in enumerate(dns_host_list):
#	print("%d. %s" %(i,w))		0-97??

#find time in ms for each dns query recorded by dns2proxy.py
total_time_ms = find_timestamps_ms(dns_timestamps)

#find locations where each dns query could be
#takes the difference of each pair of timestamps to 
#get the location of a time difference greater than 
#a specified threshold
possible_host_locs = find_potential_host_locs(total_time_ms)

#print out the list to console
potential_hosts = print_potential_hosts(possible_host_locs, dns_host_list)

#filter and check format of the potential hosts and store into new array
hostnames = []
hostnames, new_host_locs = filter_hosts(potential_hosts, possible_host_locs)

print new_host_locs
#determine each host's timestamp when queried
host_time_stamps = find_timestamps(hostnames, new_host_locs, dns_timestamps)

#determine number of hosts associated with each dns query
subhosts_count = find_count_bet_hosts(dns_host_list, new_host_locs)

#find copies within hosts
nullCountArray = []
nullCountArray = filter_duplicates(dns_host_list, new_host_locs, subhosts_count, host_time_stamps)

#print hosts
print_to_file(dns_host_list, new_host_locs, subhosts_count, host_time_stamps, nullCountArray)
