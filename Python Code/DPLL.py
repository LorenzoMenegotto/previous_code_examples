import time
import copy
from os import walk

#This variable is how many times each file is tested to average. Can be modified for faster total runtime.
#Note: This was tested and graphed to reach a conclusion that 90 is appropriate.
timesTestRepeated = 20

"""
Args:
    file (str): The path (from the current directory) to the test file.
Returns:
    clauses (list of int): The clauses that were read (in DIMACs form) from inside the file passed.
"""
def readCNF(file):
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
				variableCounter += 1
			clauses.append(tempClause)

		#moving to next line when finished:
		line = data.readline()
		content = line.strip().split()
		
	return clauses

"""
Args:
    clausesPassed (list of int): The clauses that will be checked for satisfiability.
Returns:
    bool: If the clauses passed were satisfiable or not. (True = Satisfiable).
"""
def DPLL(clausesPassed):
	nextIterationsClauses = clausesPassed

	#Setting variables present for this iteration:
	variablesFound = set()
	for clause in nextIterationsClauses:
		variablesFound.update(clause)

	#Case of only one unsatisfied clause, to allow next conflict-check to be done with more readability:
	if not nextIterationsClauses:
		return False

	#Success case where no contradictions are found (consistent set of literals) being searched:
	NoConflictsInVariables = True
	for variable in variablesFound:
		if (variable * -1) in variablesFound:
			NoConflictsInVariables = False
			break
	if NoConflictsInVariables:
		return True
	
	#Failure case where an empty clause is found and therefore unsatisfied clause exists:
	unitClausesFound = []
	for clause in nextIterationsClauses:
		#Searching for empty clause case, in which case false:
		if not clause:
			return False
		#Checking things to be unit propagated soon (to prevent re-searching space)
		#Note: Not unit propagating here already, incase empty clause case is met
		if len(clause) == 1:
			unitClausesFound.append(clause[0])

	#Propagating all previously found unit clauses:
	for unitClause in unitClausesFound:
		nextIterationsClauses = unitPropagate(unitClause, nextIterationsClauses)

	#update variables found on newest 'clause':
	variablesFound = set()
	for clause in nextIterationsClauses:
		variablesFound.update(clause)
	#Using variablesFound to assign pure literals (variables that occur with no negation):
	for variable in variablesFound:
		if not (variable * -1) in variablesFound:
			nextIterationsClauses = unitPropagate(variable, nextIterationsClauses)

	#Catching the case of if the first variable happens to be an empty clause, to prevent error chosing arbitrary value below,
	#As this would be a failed case (but would return false in 1 iteration regardless of branch)
	if (not nextIterationsClauses) or (not nextIterationsClauses[0]):
		return False

	arbitraryVariable = nextIterationsClauses[0][0]

	#Left call is if the variable is true, Right call is if variable is false.
	#Note: Arbitrary variable chosen may be a negated value, in which case it's opposite. This makes no difference, but just note for clarity.
	return DPLL(unitPropagate(arbitraryVariable, nextIterationsClauses)) or DPLL(unitPropagate((arbitraryVariable * -1), nextIterationsClauses))

"""
Args:
    literalPropagated (int): The variable that's true.
    previousClauses (list of int): The clauses to be propagated.
Returns:
    list: a list of ints representing the simplified clauses.
"""
def unitPropagate(literalPropagated, previousClauses):
	newClauses = []
	for clause in previousClauses:
		clauseSatisfied = False
		for literal in clause:
			#If the clause is satisfied, flag it not to be added to newClauses:
			if literalPropagated == literal:
				clauseSatisfied = True
			#If the literal is unsatisfied, remove it:
			elif literalPropagated == (literal * -1):
				clause.remove(literal)
		#If unsatisfied, add the clause to the newClauses for the next step:
		if not clauseSatisfied:
			if clause:
				newClauses.append(clause)
	return newClauses

foldername = input("Please name the folder to be tested:")
_, _, filenames = next(walk(foldername))

for testFile in filenames:
	print("Testing file:",testFile)

	#Averaging time to account for small differences:
	totalTime = 0
	satisfiability = bool()
	for i in range(timesTestRepeated):

		clausesRead = readCNF(foldername+'/'+testFile)
		startTime = time.perf_counter()
		#recalculating satisfiability check each time, just to measure time it took:
		satisfiability = DPLL(clausesRead)
		totalTime = totalTime + ((time.perf_counter() - startTime))
	print("Satisfiability    : ", satisfiability)
	print("Average Time (ms) : ", (totalTime/timesTestRepeated))