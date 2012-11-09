from ofxparse import OfxParser
import json

#TODO: get rid of sample.ofx
def to_obp_json(ofx_file):
    #Initiate the ofx object
    ofx = OfxParser.parse(file(ofx_file))
    transactions = []
    #TODO making sure end-date and start-date doesnt clash 
    for transaction in ofx.account.statement.transactions:
      obp_transaction = {}
      #THIS HOLDER

      this_holder = {'name':ofx.account.number}
      #details = {'amount': ofx.account.statement.transactions.amount }
      
      other_holder = {}
      obp_transaction = {'this_holder':this_holder, 'other_holder':other_holder, 'other_date':'' }

      transactions.append(obp_transaction)

    #Serializing the object
    print 'JSON before serializing= ' + str(obp_transaction)
    obpjson = json.dumps(transactions)
    
    #Return the newly created json
    print '------------------------'
    print 'JSON = ' + obpjson
    return obpjson



if __name__ == "__main__":
    to_obp_json('sample.ofx')

