import time
import copy
from os import walk

#This variable is how many times each file is tested to average. Can be modified for faster total runtime.
#Note: This was tested and graphed to reach a conclusion that 90 is appropriate.
timesTestRepeated = 1

"""
Args:
    file (str): The path (from the current directory) to the test file.
Returns:
    clauses (list of int): The clauses that were read (in DIMACs form) from inside the file passed.
    variablesDict (dictionary): All variables encountered, linked to their assignment (-1 at the moment of return).
"""
def readCNF(file):
	variablesDict = {} #-1 = unassigned, 0 = false, 1 = true.
	clauses = []

	data = open(file,'r')
	line = data.readline()
	content = line.strip().split()
	#stepping through each line of text file to add clauses
	while content:
		if line[0] == 'c':
			#ignoring comment lines
			pass
		elif line[0] == 'p':
			#setting variables found in 'p' which are arbitrary but good to have.
			pass
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
		
	return clauses, variablesDict

"""
Args:
    clausesPassed (list of int): The clauses that will be checked for satisfiability.
    assignment (dict): All variables encountered, linked to their assignment (-1 = unassigned)
    latestDecisionVariable (int): Previous decision variable, passed for the clause learning.
Returns:
    bool: If the clauses passed were satisfiable or not. (True = Satisfiable).
"""
def DPLLCL(clausesPassed, assignmentPassed, latestDecisionVariable):
	assignment = assignmentPassed.copy()

	#Unit Propagation of p:
	assignment = unitPropagate(clausesPassed, assignment)
	satisfiedReturn, clauseBroken = checkIfSatisfied(clausesPassed, assignment)

	#returning false if failed, but also learning clause heuristic:
	if satisfiedReturn == 0:
		#FUTURE IMPLEMENTATION NOTE: Edit the following 'if' statement to improve clause learning
		#Simple implementation of 1UIP to prevent this from being re-searched:
		if clauseBroken:
			if (latestDecisionVariable in clauseBroken):
				clauseBroken.remove(latestDecisionVariable)
				clausesPassed = clausesPassed.append(clauseBroken)
			#The same as above, except if the negation occurs:
			if ((-1*latestDecisionVariable) in clauseBroken):
				clauseBroken.remove(-1*latestDecisionVariable)
				clausesPassed = clausesPassed.append(clauseBroken)
		#Resetting assignment as it was a failure:
		for key in assignment:
			assignment[key] = -1
		return False, assignment

	#returning true if success:
	elif satisfiedReturn == 1:
		return True, assignment

	#else, selecting a decision variable to branch on:
	decisionVariable = -1
	for key in assignment:
		if assignment[key] == -1:
			decisionVariable = key
			break

	#branching on the decisionVariable being true:
	assignment[decisionVariable] = 1

	positivePathSatisfiable, _ = DPLLCL(clausesPassed, assignment, decisionVariable)
	if positivePathSatisfiable:
		return True, assignment

	#ensuring decision variable isn't set by unit propagation.
	#If it was set, the decision variable stays the value found
	assignment[decisionVariable] = -1
	assignment = unitPropagate(clausesPassed, assignment)

	if (assignment[decisionVariable] == -1):
		#branching on the decisionVariable being false:
		assignment[decisionVariable] = 0

	negativePathSatisfiable, _ = DPLLCL(clausesPassed, assignment, decisionVariable)
	if negativePathSatisfiable:
		return True, assignment
	
	#Resetting assignment as it was a failure:
	for key in assignment:
		assignment[key] = -1

	return False, assignment

"""
Args:
    previousClauses (list of int): The clauses to be propagated.
    assignment (dict): All variables encountered linked to their assignment.
Returns:
    newAssignment (dict): All variables linked to their assignment, with necessary unit clauses assigned.
"""
def unitPropagate(previousClauses, assignment):
	newAssignment = assignment.copy()
	for clause in previousClauses:
		clauseSatisfied = False
		for literal in clause:
			if (literal > 0) and (assignment[literal] == 1): #true condition and 1 value
				clauseSatisfied = True
				break
			elif (literal < 0) and (assignment[(literal * -1)] == 0): #false condition and 0 value
				clauseSatisfied = True
				break
		#Recursively repeat if a unit clause is found:
		if not clauseSatisfied:
			unassignedLiterals = []
			#Noting unassigned conditions in the clause. If singular, unit clause found.
			for literal in clause:
				if newAssignment[abs(literal)] == -1:
					unassignedLiterals.append(literal)
			if len(unassignedLiterals) == 1:
				if unassignedLiterals[0] > 0:
					newAssignment[unassignedLiterals[0]] = 1
				else:
					newAssignment[unassignedLiterals[0]] = 0
	return newAssignment

"""
Args:
    clausesPassed (list of int): The clauses that will be checked for satisfiability.
    assignment (dictionary): All variables encountered, linked to their assignment (-1 = unassigned)
Returns:
    int: '-1' if unsatisfied but may be possible, '0' if falsified, '1' if satisfied.
    clauseBroken : if '-1', it also returns the conflicting clause. Else returns [].
"""
def checkIfSatisfied(clauses, assignment):
	satisfied = True
	clauseCounter = 0
	while clauseCounter < len(clauses):
		clauseSatisfied = False
		#checking each condition in a clause
		for condition in clauses[clauseCounter]:
			if (condition > 0) and (assignment[condition] == 1): #true condition and 1 value
				clauseSatisfied = True
				break
			elif (condition < 0) and (assignment[(condition * -1)] == 0): #false condition and 0 value
				clauseSatisfied = True
				break
		#ending calculation if an unsatisfied clause is encountered
		if not clauseSatisfied:
			satisfied = False
			#returning '0' if unable to be satisfied:
			ableToBeSatisfied = False
			for condition in clauses[clauseCounter]:
				if (assignment[abs(condition)] == -1): #unassigned variable in unsatisfied clause
					ableToBeSatisfied = True
					break
			if not ableToBeSatisfied:
				return 0, clauses[clauseCounter]
			else:
				return -1, []
		#continuing to next clause
		clauseCounter += 1
	return 1, []

foldername = input("Please name the folder to be tested:")
_, _, filenames = next(walk(foldername))

for testFile in filenames:
	print("Testing file:",testFile)

	#Averaging time to account for small differences:
	totalTime = 0
	satisfiability = bool()
	for i in range(timesTestRepeated):

		clausesRead, assignment = readCNF(foldername+'/'+testFile)
		startTime = time.perf_counter()
		#recalculating satisfiability check each time, just to measure time it took:
		satisfiability = DPLLCL(clausesRead, assignment, -1)
		totalTime = totalTime + ((time.perf_counter() - startTime))
	print("Satisfiability    : ", satisfiability)
	print("Average Time (s) : ", (totalTime/timesTestRepeated))
	print("=====================================================================")

