import csv
from myModels.hashTable import hashTable

def get_pkg_hashTable():
    # To set hashTable for packages
    # pkg_hashTable will be [ [[pkgId, [key-value-hashMap]] ,... ]  ,....] 
    pkgCsv_filePath = "./csv/packages.csv"
    package_HashKeyName_list = ["pkgId","lctnId", "address", "city", "zip", "deadline", "weight", "deliTime", "traMil", "truckId"]
    pkgs_hashTable = hashTable() # the key is the pkg id
    with open(pkgCsv_filePath) as pkg_csvfile:
        read_csv = csv.reader(pkg_csvfile, delimiter=',')
        for row in read_csv:
            aPkg_hashTable = hashTable(package_HashKeyName_list) # the keys for a pkg are diff strs
            aPkg_hashTable.insert("pkgId", int(row[0])) 
            aPkg_hashTable.insert("lctnId", int(row[1])) 
            aPkg_hashTable.insert("deadline", row[5]) #deadline
            aPkg_hashTable.insert("weight", float(row[6])) 

            aPkg_hashTable.insert("address", row[2]) 
            aPkg_hashTable.insert("city", row[3])
            aPkg_hashTable.insert("zip", row[4])

            aPkg_hashTable.insert("deliTime", None) #weight
            aPkg_hashTable.insert("traMil", None) #status; the csv file doesnt include status info
            aPkg_hashTable.insert("truckId", None) #weight
            pkgs_hashTable.insert(int(row[0]), aPkg_hashTable)

    return pkgs_hashTable


