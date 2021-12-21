variablesDict = {} #-1 = unassigned, 0 = false, 1 = true.
clauses = []

numOfVariables = 0
numOfClauses = 0

data = open('test2.cnf','r')
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
failedClauses = []
while clauseCounter < len(clauses):
	clauseSatisfied = False
	#checking each condition in a clause
	for condition in clauses[clauseCounter]:
		if (condition > 0) and (variablesDict[condition] == 1): #true condition and 1 value
			clauseSatisfied = True
			break
		elif (condition < 0) and (variablesDict[(condition * -1)] == 0): #false condition and 0 value
			clauseSatisfied = True
			break
	#ending calculation if an unsatisfied clause is encountered
	if not clauseSatisfied:
		satisfied = False
		for variable in variablesDict:
			#Removing the verbose, unsatisfied variables from unsatisfied clauses (if assigned)
			if (variablesDict[variable] == 0) or (variablesDict[variable] == 1):
				if variable in clauses[clauseCounter]:
					#Removing unsatisfied variable if positive
					clauses[clauseCounter].remove(variable)
				if (variable*-1) in clauses[clauseCounter]:
					#Removing unsatisfied variable if negative
					clauses[clauseCounter].remove(variable*-1)
		failedClauses.append(clauses[clauseCounter])
	#continuing to next clause
	clauseCounter += 1

#Simplifying clause outcome. Likely more efficient to leave verbose clauses in, but for clarity I'll include this.
newClauses = []
for clauseX in failedClauses:
	if not newClauses:
		newClauses.append(clauseX)
	else:
		specialCaseFlag = False
		for clauseY in newClauses:
			if set(clauseX) == set(clauseY):
				#Clause X is a duplicate of Y, ignore X.
				specialCaseFlag = True
				break
			elif set(clauseX).issubset(set(clauseY)) and clauseX:
				#X is a subset of Y and therefore Y is the less efficient, verbose 'copy'.
				newClauses.append(clauseX)
				print("Removing ", clauseY, " cos it's a subset of ", clauseX)
				newClauses.remove(clauseY)
				specialCaseFlag = True
				break
		if not specialCaseFlag:
			#X is unaccounted for (and unsatisfied) and therefore added to following step.
			newClauses.append(clauseX)

#printing result
if satisfied:
	print("The assignment fully satisfies the problem provided.")
else:
	print("The partial assignment has lead to the simplified CNF...")
	print(newClauses)
	

