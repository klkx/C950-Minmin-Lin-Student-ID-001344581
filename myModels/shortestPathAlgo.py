from myModels.data_vertices import get_vertices_hashTable
from myModels.data_graph import get_graph_list


# Time complexity: O(V + E), where V is the number of vertices and E is the number of edges in the graph.
# Space complexity: O(V).
# To find the shortest path, it goes though each vetext to defined and compare its all adjacent vertices' distances.
def dijkstra_shortestPath(which_result, origin_VertKey, destination_VertKey):
    graph_list = get_graph_list()
    vertices_hashTable = get_vertices_hashTable()
    # Set a variavle to keep on tracking the vertices you will need to define their distances
    unvisited_vertices_keyList = vertices_hashTable.keys_list()
    # Set the vertext's distace as 0 as a start point 
    vertices_hashTable.get(origin_VertKey).insert("distance", 0)
    LeastDist_vertexId_list = [None] #use list to include it in order to be referenced
    

    # Recersively, 
    # 1. You go through each vertex by calculating its all adjacent vertices' distance. You update the adjVertex's distance when you find out shorter one.
    # 2. Then, you remove this vertext from the que list, unvisit_vertices_keyList so you will not define again. 
    # 3. Apply these steps on each adjVertex of current vertex and move on next adjVertex's adjVertex untill nothing in the que list.
    def defin_aVertexDistance(aVertex_key, unvisit_vertices_keyList):
        # You stop this recursive function after you define every vertex
        if len(unvisit_vertices_keyList) == 0:
            return True

        # Define each adjVert's distance by the sum of the current vertex's distance and the weight between them. Update when you find out shorter one
        len_adjVertices = len(graph_list[aVertex_key][1])
        for curr_adjVerT_key in range(0, len_adjVertices):
            if graph_list[aVertex_key][1][curr_adjVerT_key] is not None:
                curr_adjVert_distance = vertices_hashTable.get(aVertex_key).get("distance") + graph_list[aVertex_key][1][curr_adjVerT_key] #refer to the file, data_graph.py for the dataS. to understand why use graph_list[aVertex_key][1][curr_adjVerT_key]
                # No need to check a vertex again that you have defined its distance already
                if curr_adjVerT_key in unvisit_vertices_keyList:
                    # Update the distance and the path when you find out shorter one 
                    if curr_adjVert_distance < vertices_hashTable.get(curr_adjVerT_key).get("distance"):
                        ##print("** the vertex got updated")
                        vertices_hashTable.get(curr_adjVerT_key).insert("distance", curr_adjVert_distance)
                        vertices_hashTable.get(curr_adjVerT_key).insert("pred", vertices_hashTable.get(aVertex_key).get("pred") + [aVertex_key])
                        vertices_hashTable.get(curr_adjVerT_key).insert("id", curr_adjVerT_key)
        
        # update current the vertex id that has the least distance
        if LeastDist_vertexId_list[0] == None:
            if vertices_hashTable.get(aVertex_key).get("distance") > 0:
                LeastDist_vertexId_list[0] = aVertex_key
        elif vertices_hashTable.get(LeastDist_vertexId_list[0]).get("distance") > vertices_hashTable.get(aVertex_key).get("distance"):
            LeastDist_vertexId_list[0] = aVertex_key
            
            
        # After all adjacent vertices' distances are given, remove this core vertext from the que list.
        if aVertex_key in unvisit_vertices_keyList:
            unvisit_vertices_keyList.remove(aVertex_key)
        # Recursively check each level adjVetices to update the distances
        for adjVert_key in range(0, len(graph_list[aVertex_key][1])):
            if graph_list[aVertex_key][1][adjVert_key] != 0 and adjVert_key != None:
                if adjVert_key in unvisit_vertices_keyList:
                    return defin_aVertexDistance(adjVert_key, unvisit_vertices_keyList)
                

    defin_aVertexDistance(origin_VertKey, unvisited_vertices_keyList)
    if which_result == "lstDist_vertex":
        return vertices_hashTable.get(LeastDist_vertexId_list[0])
    if which_result == "updated_vertices":
        return vertices_hashTable
    if which_result == "desti_vertex":
        return vertices_hashTable.get(destination_VertKey)

    
   
     
