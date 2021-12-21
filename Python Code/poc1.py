#HARDCODE FILE NAME HERE FOR TESTING:
filename = "test1.cnf"
print("Running solver on...", filename)

variablesDict = {} #-1 = unassigned, 0 = false, 1 = true.
clauses = []

numOfVariables = 0
numOfClauses = 0

data = open(filename,'r')
line = data.readline()
content = line.strip().split()
#stepping through each line of text file to add clauses
while content:
	if line[0] == 'c':
		#ignoring comment lines
		pass
	elif line[0] == 'p':
		#setting variables found in 'p' which are arbitrary but good to have.
		numOfVariables = content[2]
		numOfClauses = content[3]
	else:
		variableCounter = 0
		tempClause = []
		#looping through each variable of clauses:
		while content[variableCounter] != '0':
			#adding each variable to the clauses list:
			currentVariable = int(float(content[variableCounter]))
			tempClause.append(currentVariable)
			#checking if already in dict (adding positive variable if not):
			baseVariable = currentVariable if (currentVariable > 0) else (currentVariable * -1)
			if baseVariable not in variablesDict:
				variablesDict[baseVariable] = -1
			variableCounter += 1
		clauses.append(tempClause)
	#moving to next line when finished:
	line = data.readline()
	content = line.strip().split()

#taking arbitrary values for variables
for variable in variablesDict:
	try:
		variablesDict[variable] = int(input("Input the truth value for %s: " %str(variable)))
	except:
		variablesDict[variable] = -1

#checking if satisfied
satisfied = True
clauseCounter = 0
while clauseCounter < len(clauses):
	clauseSatisfied = False
	#checking each condition in a clause
	for condition in clauses[clauseCounter]:
		if (condition > 0) and (int(variablesDict[condition]) == 1): #true condition and 1 value
			clauseSatisfied = True
			break
		elif (condition < 0) and (int(variablesDict[(condition * -1)]) == 0): #false condition and 0 value
			clauseSatisfied = True
			break
	#ending calculation if an unsatisfied clause is encountered
	if not clauseSatisfied:
		satisfied = False
		break
	#continuing to next clause, if satisfied
	clauseCounter += 1

#printing result
print("The assignment...")
print(variablesDict)
if satisfied:
	print("              ...DOES satisfy the problem provided.")
else:
	print("              ...DOES NOT satisfy the problem provided.")
