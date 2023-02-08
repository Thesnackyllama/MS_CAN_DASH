import json


    
def dbclookup(dataload,canbusid):
    for i in dataload['params']:
        if i['canId'] == canbusid:
            for x in i['signals']:
                output = [i['canId'],x['category'],x['name'],x['factor'],x['comment']]
                return(output)

def main():
    canbusid = 1512

    with open('msdash.json', 'r') as f:
        db = json.load(f)

    z = dbclookup(db,canbusid)
    print(z)

if __name__ == "__main__":
    main()
     

 