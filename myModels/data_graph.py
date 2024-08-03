import csv

def get_graph_list():

    # load distance csv
    # the data structure of this csv file: eachRow[0] is the location A id; eachRow[1-end] is the distance from location A to that. 
    distance_csvFilePath = './csv/distances_transposed.csv'
    distances_list = [] # The final data structure will be [[locationId, [distance1, distance2, ...]], ...] 
    with open(distance_csvFilePath) as distance_csvfile:
        read_csv = csv.reader(distance_csvfile, delimiter=',')
        for row in read_csv:
            aDistanceList = []
            #append the key of the location
            aDistanceList.append(int(row[0]))
            #append a list of corresponding other locations' distances
            eachRow_distanceList = list()
            for i in range(1, len(row)):
                if len(row[i]) >0:
                    eachRow_distanceList.append(float(row[i]))
                else:
                    eachRow_distanceList.append(None)   
            aDistanceList.append(eachRow_distanceList)
            distances_list.append(aDistanceList)
    return distances_list
