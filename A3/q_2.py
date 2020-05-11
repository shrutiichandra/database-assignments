#PART2: UNDO LOG RECOVERY
#./2018202010.sh ../Sample\ Test\ Cases/Part\ 2/input_1.txt 
#cd /home/shruti/Documents/pg2k18/sem2/db/A3/2018202010
import sys
import os
import re
from collections import OrderedDict as od
def readFile(file):
	db_elem_dict = {}
	logs = []
	with open(file, 'r') as fread:
		cnt = 1
		for string in fread:
			line = string.strip()
			if cnt == 1:
				db_elements = line
				tokens = db_elements.split()
				i = 0
				while i < len(tokens):
					db_elem_dict[tokens[i]] = int(tokens[i+1])
					i = i + 2
			elif line:
				logs.append(line)
			cnt += 1
		
	db_elem_dict = od(sorted(db_elem_dict.items()))
	
	return db_elem_dict, logs

def printDict(d):
	line = ""
	for k, v in d.iteritems():
		line = line + str(k) + " "+ str(v) + " "
	line = line.strip()
	return line

def getTransNum(l):
	log_token = l.split()
	trans = log_token[1].split(">") 
	return trans[0]
def processLogs(logs_list, disk_val, output_file):
	n = len(logs_list)
	logs_list.reverse()

	idx = 0
	committed = []
	all_trans = []
	while idx < n:
		if re.search(r'^<START\sT\d+>$', logs_list[idx]): #<START T1/3/2>
			trans = getTransNum(logs_list[idx])
			all_trans.append(trans)

		elif "COMMIT" in logs_list[idx]: 
			trans = getTransNum(logs_list[idx]) #T1, T2, T3
			if any(trans in logs for logs in logs_list):
				committed.append(trans) #[T2]

		idx+=1

	for idx in range(n):
		if re.search(r'^<T\d', logs_list[idx]):

			trans_num, var, val = logs_list[idx].split(',')
			trans_num = trans_num.split('<')[1]
			if trans_num not in committed:
				var, val = var.strip(), val.split('>')[0].strip()
				
				disk_val[var] = val

	f = open(output_file, 'w')
	line = printDict(disk_val)
	print >>f, line
	f.close()



#####-------------main-------------#####

if len(sys.argv) != 2: #input file name
	sys.exit(1)

file_path = sys.argv[1]	

file_exists = os.path.isfile(file_path)

if file_exists == False:
	sys.exit(1)

file_name = file_path.split("/")[-1][:-4]

#read the input file
db_elem_dict, logs = readFile(file_path)

opfile = "2018202010_2.txt"
processLogs(logs, db_elem_dict, opfile)
