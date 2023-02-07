import json
import os


    
def dbclookup(dataload,canbusid):
    for i in dataload['params']:
        if i['canId'] == canbusid:
        #signals for 1512
        #print(i['signals'])
            for x in i['signals']:
            #print(x['name'])
                output = [x['name'],x['comment']]
                return(output)

def main():
    canbusid = 1512


    
    with open('ms2dash.json', 'r') as f:
        db = json.load(f)

    
    z = dbclookup(db,canbusid)
    print(z)



if __name__ == "__main__":
    main()
        #print(f"found")
    #print(i['name'])
    #for x in i['signals']:
        #print(x['name'])


    #print(i['signals'])

 