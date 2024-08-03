import csv
from myModels.hashTable import hashTable 

def get_vertices_hashTable():
    # Set a list to store each location; the list index is the location id; 
    # load the location csv ==> [lctnAddress1, lctnAddress2, lctnAddress3]; index is the location id
    lctnInfo_csvFilePath = './csv/locations_list.csv'
    lctnInfo_list = [] # [["stAddr", "zip", "compAddr"], ...]
    with open(lctnInfo_csvFilePath) as lctnInfo_csvfile:
        read_csv = csv.reader(lctnInfo_csvfile, delimiter=',')
        for row in read_csv:
            lctnInfo_list.append([row[0], row[1], row[2]])  # each row of the locationInfo csv file should be ["stAddr", "zip", "compAddr"]
    ##print("---lctnInfo_list----")
    ##print(lctnInfo_list)


    # Set a list to store each vertex key name string; the list index is the vertext key name id; 
    vertex_HashkeyName_list = ["distance", "pred", "id"]
    # To set vertices hashTable: [[[lctnId, [distance-pred-hashMap]]], ...] 
    vertices_hashMap = hashTable()
    for lctn_id in range(0, len(lctnInfo_list)):
        vertex_hashMap = hashTable(vertex_HashkeyName_list)
        vertex_hashMap.insert("distance", float('inf')) # init value for each vertex's distance is infinity
        vertex_hashMap.insert("pred", []) # init value for each vertex's pred is a empty list to be store for the shortest path from the orgin to this vertex
        vertex_hashMap.insert("id", lctn_id)
        vertices_hashMap.insert(lctn_id, vertex_hashMap)
    return vertices_hashMap
    