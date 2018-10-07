import csv

f = open("Sample.csv")

#valid_values = [["YELLOW", "PURPLE"], ["SMALL", "LARGE"], ["STRETCH", "DIP"], ["ADULT", "CHILD"]]
#valid_values = [["SUNNY", "RAINY"], ["WARM", "COLD"], ["NORMAL", "HIGH"], ["STRONG"], ["WARM", "COOL"], ["SAME", "CHANGE"]]
valid_values = [["BIG", "SMALL"], ["RED", "BLUE"], ["CIRCLE", "TRIANGLE"]]
positive_value = "T"
negative_value = "F"

dataset = csv.reader(f)
D = []
for x in dataset:
	D.append(x)

S = [[0] * (len(D[0]) - 1)]
G = [['?'] * (len(D[0]) - 1)]

data_length = len(D[0])


#.....Funtion to check inconsistency.....#
def checkConsistency(data, h):
	#print(data, h)
	for i in range(len(h)):
		if data[data_length - 1] == negative_value:
			if h[i] == 0 or (h[i] != "?" and h[i] != data[i]):
				return True
		else:
			if h[i] != "?" and h[i] != data[i]:
				return False

	if data[data_length - 1] == negative_value:
		return False
	else:
		return True

#.....End of function checkInconsistency().....#



#.....Funtion to remove inconsistent hypotheses.....#
def removeInconsistent(data, H):
	rem_h = []
	for h in H:
		#print(h, H)
		if not checkConsistency(data, h):
			rem_h.append(h)
	for h in rem_h:
		H.remove(h)	
			
#.....End of function removeInconsistent().....#



#.....Function to get the set of next minimally generic hypotheses.....#
def nextMinimallyGeneric(data, h):
	temp_h = []
	for i in range(len(h)):
		if h[i] == 0:
			temp_h.append(data[i])
		elif h[i] != "?" and h[i] != data[i]:
			temp_h.append("?")
		else:
			temp_h.append(h[i])
	return temp_h
		
#.....End of function nextMinimallyGeneric().....#



#.....Function to get the set of next minimally specific hypotheses.....#
def nextMinimallySpecific(data, h):
	next_h_list = []
	for i in range(len(h)):
		temp_h = []
		temp_h.extend(h[:i])
		temp = list(temp_h)
		if h[i] == "?":
			for j in range(len(valid_values[i])):
				temp_h = list(temp)
				if(data[i] != valid_values[i][j]):
					temp_h.append(valid_values[i][j])
					temp_h.extend(h[i + 1:])
					next_h_list.append(temp_h)
					#print("\n\n" + str(D.index(data)) + "\n\n")
					for k in range(D.index(data)):
						if not checkConsistency(D[k], temp_h):
							next_h_list.remove(temp_h)
							break
	return next_h_list
			
		
#.....End of function nextMinimallySpecific().....#



#.....Funtion to find inconsistent hypotheses.....#
def findInconsistent(data, H):
	for h in H:
		if not checkConsistency(data, h):
			if data[data_length - 1] == positive_value:
				H.append(nextMinimallyGeneric(data, h))
			else:
				H.extend(nextMinimallySpecific(data, h))
			H.remove(h)

#.....End of function findInconsistent().....#


for d in D:
	#print(d)
	if d[data_length - 1] == negative_value:
		#print("Negative Example")
		removeInconsistent(d, S)
		findInconsistent(d, G)
	else:
		#print("Positive Example")
		removeInconsistent(d, G)
		findInconsistent(d, S)
	print(S, G)
	if len(S) == 0 or len(G) == 0:
		print("Noisy Data")
		break


print("S: ", S)
print("G: ", G)
