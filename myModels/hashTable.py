#The space complexity of the hashTable class is O(n+m), 
# where n is the capacity of the hash table (the size of the mapList) and m is the number of key-value pairs stored in the hash table. 
class hashTable:
    def __init__(self, input_hashKeyNmeList=[], capacity=20, ):
        self.mapList = []
        self.hashKeyNmeList = input_hashKeyNmeList
        for i in range(capacity):
            self.mapList.append([])
    
    #The time complexity: O(1)
    def hashValue(self, key):
        return key%len(self.mapList)
    
    def insert(self, key, value):
        #set up for keyHash, translatedKey(if the key is 0 that will be fine; if the key is str, need to translate in to a int based on self.hashKeyNmeList)
        keyHash = None
        translated_key = None

        # key => hash by key % len(self.mapList)
        if type(key) is str:
            translated_key = self.hashKeyNmeList.index(key)
            keyHash = self.hashValue(translated_key)
        else:
            translated_key = key #if the key is int, it will be the same as it
            keyHash = self.hashValue(key)
        # mapList[theHash].append([key, vlaue]) if empty at this index
        # otherwise, check each list[0] of the chain for the existed item and update its value; if not, just append this.
        ##print("self.mapList ====>")
        ##print(self.mapList)
        if len(self.mapList[keyHash]) == 0:
            self.mapList[keyHash].append([translated_key, value])
        else:
            for eachItem in self.mapList[keyHash]:
                if eachItem[0] == translated_key:
                    eachItem[1] = value
                    return True
            self.mapList[keyHash].append([translated_key, value])
    
    def get(self, key):
        if type(key) is str:
            translated_key = self.hashKeyNmeList.index(key)
            hash = self.hashValue(translated_key)
        else:
            translated_key = key
            hash = self.hashValue(key)
            
        if len(self.mapList[hash]) > 0 or self.mapList[hash] is not None:
            for eachItem in self.mapList[hash]:
                if eachItem[0] is translated_key:
                    return eachItem[1]
        return None
    
    def keys_list(self):
        if len(self.mapList) == 0:
            return None
        theList = list()
        for eachItem in self.mapList:
            for eachSubItem in eachItem:
                theList.append(eachSubItem[0])
        return theList

    def has_theVal(self, input_key, input_val): #each key is uniqe and the value is a simple unstructured data
        target_val = self.get(input_key)
        if target_val is input_val:
            return True
        return False
        """for eachItem in self.mapList: # anItem ==> [id, vlaue]
            ##print("getItem_byValue::::")
            ##print(eachItem)
            if len(eachItem)>0 and eachItem is not None:
                if eachItem[0][1] is value: # consider some are None
                    return True
        return False"""
    
    def searc_byValue_list(self, value):
        # return a list of items that has certain values
        resultList = []
        for itemList in self.mapList:
            for eachItem in itemList: # anItem ==> [id, vlaue]
                if eachItem[1] is value:
                    resultList.append(eachItem)
        return resultList
    
    def searcSndLvlMapTable_byValue_list(self, input_key, input_val):
        # return a list of items that has certain values
        resultList = []
        for itemList in self.mapList:
            for eachItem in itemList: # anItem ==> [id, mapTable]
                if eachItem[1].get(input_key) == input_val:
                    ##print("This pkg added to the list: ", eachItem[0])
                    resultList.append(eachItem)
        return resultList
