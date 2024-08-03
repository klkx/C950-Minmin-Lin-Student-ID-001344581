"""
C1:
NAME: MINMIN LIN
STUDENT ID: 001344581

C2. Explain the process and the flow:
1. Load delivery location and package data from files.
2. Use a hash table data structure to store the information of the delivery locations as vertices and edges in a graph.
3. Set up truck data and use Dijkstra's Algorithm to find out the shortest pathes for teach truck dilvery.
"""

from myModels.data_pkgs import get_pkg_hashTable
from myModels.shortestPathAlgo import dijkstra_shortestPath
from myModels.hashTable import hashTable 
from datetime import datetime
from datetime import timedelta




package_HashKeyName_list = ["address", "city", "deadline", "zip", "weight", "status"] # status (i.e., “at the hub,” “en route,” or “delivered”), including the delivery time
pkgs_hashTable = get_pkg_hashTable()




# To find the shortest path, you go though each vetext to defined and compare its all adjacent vertices' distances.
def origin_dijkstra(graph, vertices, origin_VertKey, destination_VertKey):
    # Set a variavle to keep on tracking the vertices you will need to define their distances
    unvisit_vertices_keyList = list(vertices.keys())
    # Set the vertext's distace as 0 as a start point 
    vertices[origin_VertKey]["distance"] = 0

    # Recersively, 
    # 1. You go through each vertex by calculating its all adjacent vertices' distance. You update the adjVertex's distance when you find out shorter one.
    # 2. Then, you remove this vertext from the que list, unvisit_vertices_keyList so you will not define again. 
    # 3. Apply these steps on each adjVertex of current vertex and move on next adjVertex's adjVertex untill nothing in the que list.
    def defin_aVertexDistance(aVertex_keyStr, unvisit_vertices_keyList):
        # You stop this recursive function after you define every vertex
        if len(unvisit_vertices_keyList) == 0:
            return True
        # Define each adjVert's distance by the sum of the current vertex's distance and the weight between them. Update when you find out shorter one
        for curr_adjVerT_key in graph[aVertex_keyStr]:
            curr_adjVert_distance = vertices[aVertex_keyStr]["distance"] + graph[aVertex_keyStr][curr_adjVerT_key]
            # No need to check a vertex again that you have defined its distance already
            if curr_adjVerT_key in unvisit_vertices_keyList:
                # Update the distance and the path when you find out shorter one 
                if curr_adjVert_distance < vertices[curr_adjVerT_key]["distance"]:
                    vertices[curr_adjVerT_key]["distance"] = curr_adjVert_distance
                    vertices[curr_adjVerT_key]["pred"] = vertices[aVertex_keyStr]["pred"] + list(aVertex_keyStr)
        # After all adjacent vertices' distances are given, remove this core vertext from the que list.
        if aVertex_keyStr == destination_VertKey:
            return True
        if aVertex_keyStr in unvisit_vertices_keyList:
            unvisit_vertices_keyList.remove(aVertex_keyStr)
        # Recursively check each level adjVetices to update the distances
        for adjVert_key in graph[aVertex_keyStr]:
            if adjVert_key in unvisit_vertices_keyList:
                defin_aVertexDistance(adjVert_key, unvisit_vertices_keyList)
    
    defin_aVertexDistance(origin_VertKey, unvisit_vertices_keyList)
    return vertices[destination_VertKey]

timeFormat = '%I:%M %p' # hour:m AM/PM

if __name__ == "__main__":    

    def get_shortes_truckPath(truck_departTimeStr, truckId,  truck_pkgId_list, pkgHashTable):
        # set up truck departing time
        truck_departTime =  datetime.strptime(truck_departTimeStr, timeFormat)
        # Use updated vertices and truck packages to list all associated vetices with distances for each truck; 
        # Remove duplicated vertices.
        #all_deliLctnIdlist = list(map(lambda aPkgId:pkgHashTable.get(aPkgId).get("lctnId"), truck_pkgId_list))
        all_deliLctnIdlist = []
        lctnID_TO_pkgIDlist_HashTable = hashTable()
        for each_pkg_id in truck_pkgId_list:
            aPkg_hashTable = pkgHashTable.get(each_pkg_id)
            all_deliLctnIdlist.append(aPkg_hashTable.get("lctnId"))

            curr_assoPkgID_value = lctnID_TO_pkgIDlist_HashTable.get(aPkg_hashTable.get("lctnId")) 
            if curr_assoPkgID_value is None:
                lctnID_TO_pkgIDlist_HashTable.insert(aPkg_hashTable.get("lctnId"), [each_pkg_id])
            else:
                lctnID_TO_pkgIDlist_HashTable.insert(aPkg_hashTable.get("lctnId"), curr_assoPkgID_value + [each_pkg_id])

        rest_StopVertexId_list = [*set(all_deliLctnIdlist)]

        # Apply dijkstra on each of uniq_deliLctnIdlist:
        truck_shortesPath_list = []
        theOrigin_vertextId = 0
        ttl_distance = 0
        last_stop_arri_time = truck_departTime 
        while len(rest_StopVertexId_list) != 0:
            # After you set a vertex as a orgin, and you find the closest vertex in the rest stops,
            # that means the stops was passed by the truck and no need to back for any reason.
            # get updated_vertices for each stop
            curr_updated_vertices = dijkstra_shortestPath("updated_vertices", theOrigin_vertextId, None)
            curr_closest_vertex = None
            # for each each_restStopVertexId, find least distance or closest vertex
            for each_restStopVertexId in rest_StopVertexId_list:
                aRestStop_vertex = curr_updated_vertices.get(each_restStopVertexId)
                aRestStop_distance = aRestStop_vertex.get("distance")
                if curr_closest_vertex == None:
                    curr_closest_vertex = aRestStop_vertex
                elif curr_closest_vertex.get("distance") > aRestStop_distance:
                    curr_closest_vertex = aRestStop_vertex
            
            # Append the closest vertex path to truck_shortesPath_list  
            truck_shortesPath_list += curr_closest_vertex.get("pred")
            if len(rest_StopVertexId_list) ==1:
                truck_shortesPath_list += [curr_closest_vertex.get("id")]
            ttl_distance += curr_closest_vertex.get("distance")
            # set curr closest vertex as next orgin vertex 
            theOrigin_vertextId = curr_closest_vertex.get("id")
            # based on the next closest vertex, update the associated pkg's deliTime, traMil, truckId            
            for each_pkgID in lctnID_TO_pkgIDlist_HashTable.get(curr_closest_vertex.get("id")):
                thePkg = pkgHashTable.get(each_pkgID)
                travMil = curr_closest_vertex.get("distance")
                travTime = travMil/18
                deliTime = last_stop_arri_time + timedelta(hours = travTime)
                thePkg.insert("deliTime", deliTime)
                thePkg.insert("traMil", travMil)
                thePkg.insert("truckId", truckId)
                last_stop_arri_time = deliTime
            # remove current vertex from rest_StopVertexId_list
            #print("rest_StopVertexId_list: ",rest_StopVertexId_list)
            rest_StopVertexId_list.remove(curr_closest_vertex.get("id"))
        return [ truck_shortesPath_list, ttl_distance]
                
       
    
    # Define package IDs for each truck
    truck1_pkgId_list = [13,15,19,20,16,14,1,29,30,31,34,37,40,2,4,5] 
    truck2_pkgId_list = [6,25,28,32,18,36,38,7,8,10,11,12,17,23,21,22]
    truck3_pkgId_list = [3,9,24,26,27,33,35,39]
    # Combine package IDs for all trucks in a list
    truck_pkg_list = [truck1_pkgId_list, truck2_pkgId_list, truck3_pkgId_list]
    
    # Define departure times for each truck
    truck1_departTime = '08:00 AM'
    truck2_departTime = '09:05 AM'
    truck3_departTime = '11:00 AM'

    # Get shortest path and distance for each truck
    truck1_path_Mil = get_shortes_truckPath(truck1_departTime, 1, truck1_pkgId_list, pkgs_hashTable)
    truck2_path_Mil = get_shortes_truckPath(truck2_departTime, 2,  truck2_pkgId_list, pkgs_hashTable)
    truck3_path_Mil = get_shortes_truckPath(truck3_departTime, 3, truck3_pkgId_list, pkgs_hashTable)
    
    # Loop through each truck's package list and print their delivery status and time
    for each_truck_pkgList in truck_pkg_list:
        for each_pkgId in each_truck_pkgList:
            # show the pkg deli status and deli time.
            thePkg = pkgs_hashTable.get(each_pkgId)
            print(f'pkgId: {thePkg.get("pkgId")}, deadline: {thePkg.get("deadline")}, deliTime: {thePkg.get("deliTime")}, truckId: {thePkg.get("truckId")}, traMil: {thePkg.get("traMil")}')
    
    
    # Calculate the total distance traveled by all trucks
    ttlMil = truck1_path_Mil[1] + truck2_path_Mil[1] + truck3_path_Mil[1]
    print(f'The total mileage traveled by all trucks: {ttlMil}.')

    # Look up a pkg
    def getStr_aPkgStatus(aPkgId, checkingTime):
        # based on truck depTime, deliTime, deadLine and checking time,  show deliStatus with delivered, enRoute or at hub 
        # at hub when checking time before truck depart time
        thePkg = pkgs_hashTable.get(aPkgId)
        deliStatus = None
        truckDptTime = None
        if thePkg.get("truckId") == 1:
            truckDptTime = datetime.strptime(truck1_departTime, timeFormat) 
        if thePkg.get("truckId") == 2:
            truckDptTime = datetime.strptime(truck2_departTime, timeFormat) 
        if thePkg.get("truckId") == 3:
            truckDptTime = datetime.strptime(truck3_departTime, timeFormat) 
        
        if truckDptTime == None:
            print(f'pkgid[{thePkg.get("pkgId")}] is still remained None after the matching.')
            print(f'The package truck id [{thePkg.get("truckId")}]')
        if checkingTime < truckDptTime:
            deliStatus = "AtHub"
        # else if deliTime is none: enRoute
        elif checkingTime < thePkg.get("deliTime"):
            deliStatus = "En-Route"
        # else if delitime is NOT empty: delivred  
        else:
            deliStatus = "Delivered"
        
        # format the print string with required vars
        return(f'PkgID:[{thePkg.get("pkgId")}] Deadline:[{thePkg.get("deadline")}] deliTime:[{thePkg.get("deliTime")}] DeliStatus:[{deliStatus}] truckId:[{thePkg.get("truckId")}] Address:[{thePkg.get("address")}]  City:[{thePkg.get("city")}] Zip:[{thePkg.get("zip")}] weight:[{thePkg.get("weight")}] ')

    def is_time_inRange(timeX, timeA, timeB):
        if timeX > timeA and timeX < timeB:
            return True
        else:
            return False

    timeA = datetime.strptime("12:01 PM", timeFormat)
    timeB = datetime.strptime("01:00 PM", timeFormat)
    #isInRange = is_time_inRange(pkg39_delitime, timeA, timeB)
    #print(isInRange)


# Verify pkg6,28,32
print("Package #6 #28 #32 will arrive in the hub at 9:05 to deliver. To verify the requirements, select times of 9:04 AM, 9:29 AM, 11:00AM and display the information of the packages' statuses:")
print("At time 09:04 AM:")
print(getStr_aPkgStatus(6, datetime.strptime("09:04 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(28, datetime.strptime("09:04 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(32, datetime.strptime("09:04 AM", timeFormat)))
print("  ")

print("At time 9:29 AM:")
print(getStr_aPkgStatus(6, datetime.strptime("9:29 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(28, datetime.strptime("9:29 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(32, datetime.strptime("9:29 AM", timeFormat)))
print("  ")

print("At time 11:00 AM:")
print(getStr_aPkgStatus(6, datetime.strptime("11:00 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(28, datetime.strptime("11:00 AM", timeFormat)))
print("  ")
print(getStr_aPkgStatus(32, datetime.strptime("11:00 AM", timeFormat)))
print("  ")

# look up a pkg by 1.Id 2.deliTime 3.in a time range
print("For displaying all packages' statuses by an input time,")
print("please input a checking time following this format, '12:01 PM'")
input_time = input()
for eachChain in pkgs_hashTable.mapList:
    for eachPkgArry in eachChain:
        print(getStr_aPkgStatus(eachPkgArry[1].get("pkgId"), datetime.strptime(input_time, timeFormat)))
        print("  ")
