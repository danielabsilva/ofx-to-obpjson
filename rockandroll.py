from ofxparse import OfxParser
import json

#TODO: get rid of sample.ofx
def to_obpjson(ofxfile='sample.ofx'):
    #Initiate the ofx object
    ofx = OfxParser.parse(file(ofxfile))
    obptransaction = {}
    
    #TODO making sure end-date and start-date doesnt clash 
    for transaction in ofx.account.statement.transactions:
      #obptransaction['id'] = ofx.account.number
      print transaction.type
    #Serializing the object
    print 'JSON before serializing= ' + str(obptransaction)
    obpjson = json.dumps(obptransaction)
    
    #Return the newly created json
    print '------------------------'
    print 'JSON = ' + obpjson
    return obpjson

if __name__ == "__main__":
    to_obpjson()

