#PART1: UNDO LOGS
#./2018202010.sh ../Sample\ Test\ Cases/Part\ 1/input.txt 3
#cd /home/shruti/Documents/pg2k18/sem2/db/A3/2018202010
import sys
import os
import re
from collections import OrderedDict as od

def readFile(file):
	pattern = re.compile("^([T]\d+\s\d+)$") #T1 8
	begin = 0
	trans_dict = {}
	db_elem_dict = {}
	num_inst_list = []
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

			if pattern.match(line):
				# a transaction has begun
				tokens = line.split()
				num_inst_list.append(int(tokens[1]))
				inst = 0
				trans_num = int(tokens[0][1:])
				begin = 1
				trans_list = []
				
			elif line and begin == 1:
				inst += 1
				if inst == int(tokens[1]):
					line = line + ", last" #last inst
				trans_list.append(line)

			if not line and begin == 1:
				# transaction has ended
				begin = 0
				inst = 0
				trans_dict[trans_num] = trans_list
			cnt += 1
	
	trans_dict[trans_num] = trans_list
	db_elem_dict = od(sorted(db_elem_dict.items()))

	return db_elem_dict, trans_dict, num_inst_list

def doRoundRobin(dict_of_list, q,num_inst_list):
	i = 0
	rr_list = []
	maxi = max(num_inst_list)
	while i < maxi:
		for trans_num, trans_list in dict_of_list.items():
			if i < len(trans_list):
				j = i
				while j < i+q and j < len(trans_list):
					rr_list.append((trans_num, trans_list[j]))
					j += 1
		i += q
	
	return rr_list, len(num_inst_list)

def printDict(d):
	line = ""
	for k, v in d.iteritems():
		line = line + str(k) + " "+ str(v) + " "
	line = line.strip()
	return line

def processTransactions(transactionList, output_file, disk_val,n):
	mm_val = {}
	
	local = {} # all local vars are shared b/w transactions
	f = open(output_file, 'w')
	active_trans = []
	read_stmt, write_stmt, op_stmt = "READ", "WRITE", "OUTPUT"
	for idx in range(len(transactionList)):
		
		num_trans, oper = transactionList[idx][0], transactionList[idx][1]
		#check if this is the first occurrence of trans num
		if num_trans not in active_trans:
			print>> f, "<START T" + str(num_trans) + ">"
			
			#write values in main memory
			mm_val = od(sorted(mm_val.items()))
			
			line = printDict(mm_val)
			print >> f, line
			
			#write values in disk
			line = printDict(disk_val)
			print >> f, line
			
			active_trans.append(num_trans)

		#check for read, write o/p commands
		if read_stmt in oper:
			token = oper[5: len(oper)-1].split(',') # [A, t]
			token[1] = token[1].strip()
			
			if token[0] not in mm_val:
				mm_val[token[0]] = disk_val[token[0]] #var loaded in main memory {A: 8, ..}

			
			local[token[1]] = mm_val[token[0]] #[{1:{t:8}}]

			
		elif write_stmt in oper:
			token = oper[6: len(oper)-1].split(',') # [A, t]
			token[1] = token[1].strip()
			old_val = mm_val[token[0]]
			print >> f, "<T"+str(num_trans)+", "+token[0]+", "+str(old_val)+">"
			
			#write values in main memory
			
			mm_val[token[0]] = local[token[1]]
			mm_val = od(sorted(mm_val.items()))
			line = printDict(mm_val)
			print >>f, line
			
			#write values in disk
			line = printDict(disk_val)
			print >> f, line

		elif op_stmt in oper:
			token = oper[7:8] #A
			disk_val[token] = mm_val[token] #copy to disk
			if "last" in oper:
				print >>f, "<COMMIT T"+str(num_trans)+">"
				#write values in main memory
				mm_val = od(sorted(mm_val.items()))
				line = printDict(mm_val)
				print >>f, line
				
				#write values in disk
				line = printDict(disk_val)
				print >> f, line
			
		#some operation occured
		elif ":=" in oper:
			temp = oper.split(':=') #[t, t*2]
			temp[0] = temp[0].strip()
			operation = temp[1]	 
			local[temp[0]]  = eval(operation, local)
			
			
	f.close()
	

#####-------------main-------------#####

if len(sys.argv) != 3: #input file name, x
	sys.exit(1)

file_path = sys.argv[1]	
x = int(sys.argv[2])

file_exists = os.path.isfile(file_path)

if file_exists == False:
	sys.exit(1)

#read the input file
db_elem_dict, trans_dict, num_inst_list = readFile(file_path)

# print db_elem_dict
line = printDict(db_elem_dict)

#shuffle trans a/c to x value
trans_q, n = doRoundRobin(trans_dict, x, num_inst_list)

opfile = "op.txt"

processTransactions(trans_q,opfile,db_elem_dict, n)
