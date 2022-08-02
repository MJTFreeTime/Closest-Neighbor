import math
import pyodbc
import time
import calculation.functions as functions

# Define a list of available pyodbc drivers
pyodbc_drivers = pyodbc.drivers();

# define server details
driver = '{ODBC Driver 17 for SQL Server}'
server = 'MSI'
db = 'Closest_Neighbor'
table = 'Lat_Longs'

# pyodbc extra details
SQL_ATTR_CONNECTION_TIMEOUT = 113
connection_timeout = 1
timeout = 1

global data

def testConnection(connString):
	try:
		conn = pyodbc.connect(connString, timeout=timeout, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
		conn.close()
		return True
	except:
		return False

def getDatabases(connString):
	if (not testConnection(connString)):
		return 1

	conn = pyodbc.connect(connString, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
	cursor = conn.cursor()
	query = '''SELECT name FROM sys.databases'''
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	conn.close()

	databases = []
	for i in data:
		# Exclude system databases from results
		if i[0] != "master" and i[0] != "msdb" and i[0] != "model" and i[0] != "Resource" and i[0] != "tempdb":
			databases.append(i[0])

	return databases;
		
def getTables(connString, database):
	if (not testConnection(connString)):
		return 1

	conn = pyodbc.connect(connString, timeout=timeout, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
	cursor = conn.cursor()
	query = f'''SELECT * FROM {database}.sys.tables'''
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	conn.close()

	tables = []
	for i in data:
		tables.append(i[0])

	return tables;

def getColumns(connString, table):
	if (not testConnection(connString)):
		return 1
	
	conn = pyodbc.connect(connString, timeout=timeout, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
	cursor = conn.cursor()
	query = f'''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \'{table}\''''
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	conn.close()

	columns = []
	for i in data:
		columns.append(i[0])
	
	return columns

def selectAllData(connString, table):
	global data
	# connection string using the details above
	conn = pyodbc.connect(connString, timeout=timeout, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
	# create the connection cursor
	cursor = conn.cursor()
	# define our query
	query = '''SELECT * FROM ''' + table
	# run query
	cursor.execute(query)
	# get column names
	columns = [column[0] for column in cursor.description]
	# get data
	data = cursor.fetchall()
	# close the connection and remove the cursor
	cursor.close()
	conn.close()

	return data

def outputToCSV(data, fileName, fileDestination):
	f = open((fileDestination + "/" + fileName), "x")
	f.write("ID1,ID1_Lat,ID1_Long,ID2,ID2_Lat,ID2_Long,Distance\n")
	for i in range(len(data)):
		for j in range(len(data[i])):
			f.write(str(data[i][j]))
			if j != len(data[i]) - 1:
				f.write(",")

		if i != len(data) - 1:
			f.write("\n")

	f.close()

# Estimates if point is within radius by using rough rectangular-ish bound around central point
def withinEstimatedBounds(centralLat, centralLong, currLat, currLong, radius):
	latPerMile = 0.01459854014 # lat/mile, or 1/68.5 (68.5 for error margin)

	upperBound = centralLat + (radius * latPerMile)
	lowerBound = centralLat - (radius * latPerMile)
	leftBound = centralLong - abs(1/(math.cos(centralLat) * 69.172) * radius)
	rightBound = centralLong + abs(1/(math.cos(centralLat) * 69.172) * radius)

	if currLat >= lowerBound and currLat <= upperBound: # Checks if i'th point is within latitude range of radius
		if currLong >= leftBound and currLong <= rightBound: # Checks if i'th point is within longitude range of radius
			return True
	
	return False

def inRadius(pointID, radius, sortOutput, fileDestination):
	# Find index of central point by its ID
	centralPoint = functions.linearSearch(pointID, data)

	results = []
	for i in range(0, len(data)):
		if i == centralPoint:
			continue

		if not withinEstimatedBounds(data[centralPoint][1], data[centralPoint][2], data[i][1], data[i][2], radius):
			continue

		d = functions.vincenty(data[centralPoint][1], data[centralPoint][2], data[i][1], data[i][2])
		if d <= radius:
			results.insert(len(results), [data[centralPoint][0], data[centralPoint][1], data[centralPoint][2], data[i][0], data[i][1], data[i][2], functions.vincenty(data[centralPoint][1], data[centralPoint][2], data[i][1], data[i][2])])

	if (sortOutput):
		functions.quickSort(results, 0, len(results) - 1, 6)

	# Output results to CSV file
	outputToCSV(results, "output.csv", fileDestination)

def closestNeighbor(pointID, neighbors, fileDestination):
	# Adjusts number of neighbors if too few are entered
	if (neighbors < 1):
		neighbors = 1

	# Adjusts number of neighbors if too many are entered
	if (neighbors > len(data) - 1):
		neighbors = len(data) - 1

	# Find index of central point by its ID
	centralPoint = functions.linearSearch(pointID, data)

	results = []
	for i in range(0, len(data)):
		if i == centralPoint:
			continue

		results.insert(len(results), [data[centralPoint][0], data[centralPoint][1], data[centralPoint][2], data[i][0], data[i][1], data[i][2], functions.vincenty(data[centralPoint][1], data[centralPoint][2], data[i][1], data[i][2])])

	del results[len(results) - (len(results) - neighbors) : len(results)]

	functions.quickSort(results, 0, len(results) - 1, 6)

	# Output results to CSV file
	outputToCSV(results, "output.csv", fileDestination)