import requests
import json

#Specify here the shelf number of the RFID READER
shelf_number = 10

def loadData():
    url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/readrecords"
    r = requests.get(url)
    data=json.loads(r.text)
    return data

def findNameFromTag(tag):
    for i in range(0, No_Of_Books):
        if tag in booksData[i]["Tags"]:
            global index
            index = i
            return booksData[i]["Name"]

def addBook(name,tag):
     url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/readlocation?find=" + name
     r = requests.get(url)
     data=json.loads(r.text)
     if ("Shelf " + str(shelf_number)) in data[0]["Location"]:
        arr = data[0]["Location"]["Shelf " + str(shelf_number)]
        arr.append(tag)
        data[0]["Location"]["Shelf " + str(shelf_number)] = arr
     else:
           data[0]["Location"]["Shelf " + str(shelf_number)] = [tag]
     
     updateurl = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/updatebook"
     newData = {
         "bookname" : name,
         "book" : data[0]["Location"]
     }
     print(newData)
     r = requests.post(updateurl, json=newData)
     print(r)

def updateData(tag,regno):
     old_json = booksData[index]['Issued']
     del old_json[tag]
     data={
         "bookname" : book_to_add,
         "updated" : old_json
     }
     print(data)
     url = "https://fv3md359db.execute-api.ap-south-1.amazonaws.com/final/updatebookinrecord"
     r = requests.post(url, json=data)
     print(r)


booksData = loadData()
No_Of_Books = len(booksData)
tag_from_rfid = "707eff2b"
book_to_add = findNameFromTag(tag_from_rfid)
addBook(book_to_add,tag_from_rfid)
updateData(tag_from_rfid,"RA1511008010137")
