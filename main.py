import math
import pyodbc
import time
import threading
import functions

# Define a list of available pyodbc drivers
pyodbc_drivers = pyodbc.drivers();

# define server details
driver = '{ODBC Driver 17 for SQL Server}'
server = 'MSI'
db = 'Closest_Neighbor'
table = 'Lat_Longs'

def isSQLAuth(user_name, password):
    if (user_name.strip() or password.strip()):
        return True
    else:
        return False

def testConnection(driver, server, user_name, password, database):
    conn = None
    if isSQLAuth(user_name, password):
        try:
            conn = pyodbc.connect(driver=driver, host=server, uid=user_name, pwd=password, database=database, trusted_connection='no')
            conn.close()
            return True;
        except:
            return False;
    else:
        try:
            conn = pyodbc.connect(driver=driver, host=server, database=database, trusted_connection='yes')
            conn.close()
            return True;
        except:
            return False;

def getDatabases(driver, server, user_name, password, database):
    try:
        if isSQLAuth(user_name, password):
                conn = pyodbc.connect(driver=driver, host=server, uid=user_name, pwd=password, database=database, trusted_connection='no')
        else:
            conn = pyodbc.connect(driver=driver, host=server, database=database, trusted_connection='yes')
    except:
        return []

    cursor = conn.cursor()
    query = '''SELECT name FROM sys.databases'''
    cursor.execute(query)
    data = cursor.fetchall()
    #cursor.close()
    #conn.close()
    
    databases = []
    for i in data:
        if i[0] != "master" and i[0] != "msdb" and i[0] != "model" and i[0] != "Resource" and i[0] != "tempdb":
            databases.append(i[0])

    print(databases)
    query = '''SELECT * FROM Closest_Neighbor.INFORMATION_SCHEMA.TABLES;'''
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    print(data)
    return databases;
        



# # connection string using the details above
# cnxn = pyodbc.connect(driver=driver, host=server, database=db, trusted_connection='yes')
# # create the connection cursor
# cursor = cnxn.cursor()
# # define our query
# query = '''SELECT * FROM ''' + table
# # run query
# cursor.execute(query)
# # get column names
# columns = [column[0] for column in cursor.description]
# # get data
# data = cursor.fetchall()
# # close the connection and remove the cursor
# cursor.close()
# cnxn.close()

########## Radius METHOD 1 ##########

#t0 = time.time()

#results = []

#for i in range (0, len(data)):
#    if i != centralPoint:
#        d = vincenty((data[centralPoint][0], data[centralPoint][1]), (data[i][0], data[i][1]), miles=True)

#        if d <= radius:
#            results.insert(len(results), (centralPoint, i, d))
            #print((centralPoint + 1, i + 1, d))

#t1 = time.time()
#print("len(results) =", len(results))
#print("\nTime:", t1 - t0)



########## Radius METHOD 2 ##########
### Improvements: Takes into account latitude, ruling out what has too high of a latitude value based on the radius given. ###

#t0 = time.time()

#latPerMile = 0.01428571428 # lat/mile, or 1/70 (70 for ~1.5% error margin)
#upperBound = data[centralPoint][0] + (radius * latPerMile)
#lowerBound = data[centralPoint][0] - (radius * latPerMile)

#results = []
#for i in range (0, len(data)):
#    if i != centralPoint:
#        if data[i][0] >= lowerBound and data[i][0] <= upperBound: #Checks if i'th point is within latitude range of radius
#            d = vincenty((data[centralPoint][0], data[centralPoint][1]), (data[i][0], data[i][1]), miles=True)
   
#            if d <= radius:
#                results.insert(len(results), (centralPoint, i, d))
                #print((centralPoint + 1, i + 1, d))

#t1 = time.time()

#print("len(results) =", len(results))
#print("\nTime:", t1 - t0)



########## Radius METHOD 3 ##########
### Improvements: Now takes into account longitude, ruling out what has too high of a longitude value based on the radius given. Now has a "square radius" with somewhat of an error margin to narrow results down. ###

def inRadius(pointID, radius, fileDestination):
    def callBack():
        t0 = time.time()

        centralPoint = functions.linearSearch(pointID, data)

        latPerMile = 0.01459854014 # lat/mile, or 1/68.5 (68.5 for error margin)

        upperBound = data[centralPoint][1] + (radius * latPerMile)
        lowerBound = data[centralPoint][1] - (radius * latPerMile)
        leftBound = data[centralPoint][2] - abs(1/(math.cos(data[centralPoint][1]) * 69.172) * radius)
        rightBound = data[centralPoint][2] + abs(1/(math.cos(data[centralPoint][1]) * 69.172) * radius)

        results = []
        for i in range (0, len(data)):
            if i != centralPoint:
                if data[i][0] >= lowerBound and data[i][1] <= upperBound: # Checks if i'th point is within latitude range of radius
                    if data[i][1] >= leftBound and data[i][2] <= rightBound: # Checks if i'th point is within longitude range of radius
                        d = functions.vincenty((data[centralPoint][1], data[centralPoint][2]), (data[i][1], data[i][2]), miles=True)

                        if d <= radius:
                            results.insert(len(results), [data[centralPoint][0], data[centralPoint][1], data[centralPoint][2], data[i][0], data[i][1], data[i][2], functions.vincenty((data[centralPoint][1], data[centralPoint][2]), (data[i][1], data[i][2]), miles=True)])

        t1 = time.time()

        functions.quickSort(results, 0, len(results) - 1, 6)

        print("\nTime:", t1 - t0)
        print(fileDestination + "/output.csv")
        f = open((fileDestination + "/output.csv"), "x")

        f.write("ID1,ID1_Lat,ID1_Long,ID2,ID2_Lat,ID2_Long,Distance\n")

        for i in range(len(results)):
            for j in range(len(results[i])):
                f.write(str(results[i][j]))
                if j != len(results[i]) - 1:
                    f.write(",")

            if i != len(results) - 1:
                f.write("\n")

        f.close()
    t = threading.Thread(target=callBack)
    t.start()

# ########## Closest Neighbors METHOD 1 ##########

results = []

def withinBounds(pointID, radius):
    global data
    global results

    results = []

    centralPoint = functions.linearSearch(pointID, data)
    latPerMile = 0.01459854014 # lat/mile, or 1/68.5 (68.5 for error margin)

    upperBound = data[centralPoint][1] + (radius * latPerMile)
    lowerBound = data[centralPoint][1] - (radius * latPerMile)
    leftBound = data[centralPoint][2] - abs(1/(math.cos(data[centralPoint][1]) * 69.172) * radius)
    rightBound = data[centralPoint][2] + abs(1/(math.cos(data[centralPoint][1]) * 69.172) * radius)

    for i in range (0, len(data)):
        if i != centralPoint:
            if data[i][1] >= lowerBound and data[i][1] <= upperBound: # Checks if i'th point is within latitude range of radius
                if data[i][2] >= leftBound and data[i][2] <= rightBound: # Checks if i'th point is within longitude range of radius
                    results.insert(len(results), [data[centralPoint][0], data[centralPoint][1], data[centralPoint][2], data[i][0], data[i][1], data[i][2], functions.vincenty((data[centralPoint][1], data[centralPoint][2]), (data[i][1], data[i][2]), miles=True)])

    return 0

def closestNeighbor(pointID, neighbors):
    global data
    global results

    t0 = time.time()

    results = []

    radius = 5

    lastAction = None

    while (len(results) < neighbors) and len(results) != neighbors:
        results = []
        withinBounds(pointID, radius)

        if len(results) == neighbors:
            break
        elif len(results) > neighbors:
            if lastAction and lastAction < 1:
                radius *= lastAction - .25
                lastAction -= .25
            else:
                radius *= .75
                lastAction = .75
        elif len(results) < neighbors:
            if lastAction and lastAction > 1:
                radius *= lastAction + .25
                lastAction += .25
            else:
                radius *= 1.25
                lastAction = 1.25

    functions.quickSort(results, 0, len(results) - 1, 6)
    del results[len(results) - (len(results) - neighbors) : len(results)]

    t1 = time.time()

    print("Time:", t1 - t0)

    f = open("output.csv", "x")

    f.write("ID1,ID1_Lat,ID1_Long,ID2,ID2_Lat,ID2_Long,Distance\n")

    for i in range(len(results)):
        for j in range(len(results[i])):
            f.write(str(results[i][j]))
            if j != len(results[i]) - 1:
                f.write(",")

        if i != len(results) - 1:
            f.write("\n")

    f.close()
