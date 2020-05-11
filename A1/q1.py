import sys
import re
import csv

def removeExtraSpaces(str):
	str = (re.sub(' +',' ',str)).strip()
	return str

def readFile(filename):
	data = []
	with open(filename, 'rb') as f:
		read = csv.reader(f)
		for line in read:
			data.append(line)
	return data

def printHeader(colList, tableList, metadata):
	string = ""
	for c in colList:
		for t in tableList:
			if c in metadata[t]:
				if not len(string) == 0:
					string += ','
				string = string + t + '.' + c
			else:
				sys.exit("column "+ c +"  does not exist")
	print string
	
	

def printData(data, col, table, metadata):
	
	for d in data:
		
		for c in col:
			sys.stdout.write(d[metadata[table[0]].index(c)]+",")
		sys.stdout.write("\b")
		print ' '

def distinctQry(column, table, metadata):
	# print "column: ",column, "table: ",table, "metadata: ",metadata
	l = []
	temp = []
	l.append(table)
	printHeader(column, l , metadata)
	file = table + '.csv'
	data = readFile(file)
	values = []

	for d in data:
		# print "-->row: ",d
		string = ""
		for col in column:
			# print "---->col: ",col
			val = d[metadata[table].index(col)]
			# print "***temp: ",values
			if val not in values:
				# values.append(val)
				# print val +',',
				# sys.stdout.write(val+",")
				if string != "":
					string += ','
				unique = 1
				string += val
		# values.remove(val)
		if unique == 1:
			unique = 0
			if string not in temp:
				print string
			temp.append(string)
			# sys.stdout.write("\b")
			# print ' ' 

def whereQry(condition, column, table, metadata):
	split_cond = condition.split(" ")
	# print "split : ",split_cond

	if len(column) == 1 and column[0] == '*':
		column = metadata[table]
	l = []
	l.append(table)
	printHeader(column, l, metadata)
	file = table + '.csv'
	data = readFile(file)

	true = 0
	for d in data:
		expr = solveLogical(split_cond, d, table, metadata)
		for c in column:
			if eval(expr):
				idx = metadata[table].index(c)
				true = 1
				# print d[idx] + ',',
				sys.stdout.write(d[idx]+",")
		if true == 1:
			true = 0
			sys.stdout.write("\b")
			print ' '

def solveLogical(split_cond, row, table, metadata):
	expr = ""
	#splitcond eg [A, >, 900], [B, =,9], [C, <=, 10]

	for symbol in split_cond:
		if symbol in metadata[table]: #symbol is a column
			idx = metadata[table].index(symbol) #get the column index
			expr = expr + row[idx] #value at that index
		elif symbol == '=': #change it to ==
			expr = expr + "=="
		elif symbol.lower() == 'and' or symbol.lower() == 'or':
			expr = expr + ' ' + symbol.lower() + ' '
		else: #>, <, >=, <=, or some constant --> as it is in expression
			expr = expr + symbol
	# psssrint "-->returning: ",expr
	# print "--->expr: ",expr
	return expr

def selectQry(column, table, metadata):

	if column[0] == '*' and len(column) == 1:
		column = metadata[table[0]]

	# print "col: ",column

	fileName = table[0] + '.csv'
	# print "file: ", fileName

	printHeader(column, table, metadata)
	data = readFile(fileName)
	# print "data: ",data
	printData(data, column, table, metadata)

def joinQry(col, table, metadata):
	# print "JOIN"
	file1 = table[0] + '.csv'
	file2 = table[1] + '.csv'

	data1 = readFile(file1) #l2
	data2 = readFile(file2) #l1

	fileData = [] #contains all rows combined

	for i in data2: 
		for j in data1:
			fileData.append(j+i)

	# print "fileDatac: ",fileData
	metadata["new_table"] = []
	# print "new_table: ", metadata["new_table"]

	for i in metadata[table[0]]:
		col1 = table[0] + '.' + i
		metadata["new_table"].append(col1)
	for i in metadata[table[1]]:
		col1 = table[1] + '.' + i
		metadata["new_table"].append(col1)

	metadata["test"] = metadata[table[0]] + metadata[table[1]]
	# print "TEST: ",metadata["test"]
	

	if len(col)	== 1 and col[0] == '*':
		col = metadata["new_table"]
	# print "col: " , col
	for i in col:
		print i + ',',
	sys.stdout.write("\b")
	print ' '

	for d in fileData:
		for c in col:
			if '.' in c:
				sys.stdout.write(d[metadata["new_table"].index(c)]+",")
				# print d[metadata["new_table"].index(c)] + ',',
			else:
				sys.stdout.write(d[metadata["test"].index(c)]+",")

				# print d[metadata["test"].index(c)] + ',',
		sys.stdout.write("\b")
		print ' '

def whereJoinQry(cond, col, table, metadata):
	# print "WHERE JOIN"
	file1 = table[0] + '.csv'
	file2 = table[1] + '.csv'

	data1 = readFile(file1) #l2
	data2 = readFile(file2) #l1

	fileData = [] #contains all rows combined

	for i in data2: 
		for j in data1:
			fileData.append(j+i)

	# print "fileDatac: ",fileData
	metadata["new_table"] = []
	# print "new_table: ", metadata["new_table"]

	for i in metadata[table[0]]:
		col1 = table[0] + '.' + i
		metadata["new_table"].append(col1)
	for i in metadata[table[1]]:
		col1 = table[1] + '.' + i
		metadata["new_table"].append(col1)

	metadata["test"] = metadata[table[0]] + metadata[table[1]]
	# print "TEST: ",metadata["test"]
	

	if len(col)	== 1 and col[0] == '*':
		col = metadata["new_table"]
	# print "col: ",col
	#prints header
	string = ""
	for i in col:
		if not len(string) == 0:
			string += ','
		string = string + i
	print string

	split_cond = cond.split(" ")
	# print "split : ",split_cond
	
	true = 0
	for d in fileData:
		expr = solveLogical(split_cond, d, "new_table", metadata)
		for c in col:
			if eval(expr):
				true = 1
				if '.' in c:
					idx = metadata["new_table"].index(c)
					sys.stdout.write(d[idx]+",")
				else:
					idx = metadata["test"].index(c)
					sys.stdout.write(d[idx]+",")
					# print d[idx] + ',',	
		if true == 1:
			true = 0
			sys.stdout.write("\b")
			print ' '

def aggregate(fun, col, table, metadata):
	file = table + '.csv'

	data = readFile(file)
	# print col
	values = []
	for d in data:
		val = int(d[metadata[table].index(col)])
		# print type(val)
		values.append(val)

	heading = fun+"("+table+"."+col+")"
	if fun.lower() == 'max':
		print heading
		print max(values)
	elif fun.lower() == 'min':
		print heading
		print min(values)
	elif fun.lower() == 'average':
		print heading
		print 1.0 * sum(values)/len(values)
	elif fun.lower() == 'sum':
		print heading
		print sum(values)
	else:
		print "INVALID Function! :("
	

def readMetadata():
	metadata_file = open('metadata.txt','r')
	metadata = {}
	with metadata_file as f:
		begin = 0
		for line in f:
			string = line.strip()
			if string == "<begin_table>":
				begin = 1 #table has begun
				continue
			if begin == 1:
				#table name
				table = string
				metadata[table] = [] #an empty list for col names
				begin = 0
				continue
			if string != '<end_table>':
				metadata[table].append(string) #add col names to table's list
	# print metadata
	return metadata
#first read the metadate file

if __name__=='__main__':
	metadata = readMetadata()

	query = str(sys.argv[1])

	if query[-1] != ';':
		sys.exit("Missing semicolon")
	query = query[:-1]
	if "from" in query:
		#correct syntax
		sub_qry = query.split('from')
	else:
		sys.exit("Query without FROM. Incorrect syntax")

	# print sub_qry
	sub_qry[0] = removeExtraSpaces(sub_qry[0]) #before FROM
	sub_qry[1] = removeExtraSpaces(sub_qry[1]) #after from

	# print "final sub_qry: ",sub_qry

	if "select" not in sub_qry[0].lower():
		sys.exit("Query without SELECT. Incorrect syntax")
	
	keywords = []
	keywords.append("select") #first add select
	after_select = sub_qry[0][7:] #take the string after select

	after_select = removeExtraSpaces(after_select)
	# print "after_select, removeExtraSpaces: .",after_select,"."

	if "distinct" in after_select:
		after_select = after_select[9:] #string after distinct
		keywords.append("distinct") #add distinct to list, <select> <distinct>
		

	# print "keywords, distinct: ",keywords #<select> [<distinct>]

	keywords.append(after_select) #cols, if distinct is present
	# print "keywords, [ cols]: ",keywords # <select> [ [ <distinct> <A, B> ],or, [<max(A)..>] ]

	after_select = keywords 
	# print "after_select: ",after_select
	# print "after_select[1]: ",after_select[1] #[distinct] , or [max()]
	
	distinct = "" #will store distinct if <distinct> is present in query
	if "distinct" in after_select[1]:
		# print "DISTINCT",
		distinct = after_select[1] #"distinct" keyword
		# print "distinct: ",distinct
		distinct = removeExtraSpaces(distinct)
		after_select[1] = after_select[2] #swap "distinct" with colNames
		# print "after_select: ", after_select

	colNames = after_select[1]
	# print "colNames: ",after_select[1] #A,B or max(A)

	colNames = removeExtraSpaces(colNames)
	col = colNames.split(',')
	# print "col, split: ",col
	for c in col:
		# print "col.index(",c,"): ", col.index(c), "col[col.index(c)]: ", col[col.index(c)]
		idx = col.index(c)
		col[idx] = removeExtraSpaces(c).strip()

	# print "col: ",col, #A,B or max(A)
	# print "LEN: ",len(col)
	
	after_from = sub_qry[1].split('where')
	
	# print "after_from: ",after_from #table names, [ <where> condition]
	
	tableNames = after_from[0] #<table1> [<table2>]
	# print "tableNames: ",tableNames 
	tableNames = removeExtraSpaces(tableNames)
	table = tableNames.split(',') #table1, [table2]

	for t in table:
		idx = table.index(t)
		table[idx] = removeExtraSpaces(t).strip()
	
	# print "table: ", table #table list


	for t in table:
		if t not in metadata.keys():
			sys.exit("Table name incorrect!")


	if len(after_from) > 1 and len(table) == 1: #has a where condition without join
		after_from[1] = removeExtraSpaces(after_from[1])
		whereQry(after_from[1], col, table[0], metadata)
		sys.exit(0)

	if len(after_from) > 1 and len(table) > 1:
		after_from[1] = removeExtraSpaces(after_from[1])
		whereJoinQry(after_from[1], col, table, metadata)
		sys.exit(0)

	if len(table) > 1:
		joinQry(col, table, metadata)
		sys.exit(0)

	if distinct == "distinct":
		function = distinct
		distinctQry(col, table[0], metadata)
		sys.exit(0)

	if len(col) == 1: #['max(A)'], ['average(B)']
		function = col[0]
		if '(' in function and ')' in function: #if there is () pair then only proceed
			try:
				agg, c = re.match(r"(.*)\((.*)\)" ,function).groups()
			except:
				sys.exit("Syntax Error")
			# print "S: .",agg,", cfol ",c
			c = removeExtraSpaces(c)
			agg = removeExtraSpaces(agg)
			# print "S: .",s,"."
			# print "c:",c, len(c)
			if len(c) > 1:
				sys.exit("cannot take aggregate of all")
				
			else:
				if c not in metadata[table[0]]:
					sys.exit("incorrect column name!")
				
				aggregate(agg, c, table[0], metadata)
				sys.exit(0)

	selectQry(col, table, metadata)