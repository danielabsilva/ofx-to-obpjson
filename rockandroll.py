from ofxparse import OfxParser
import json
import urllib2


#TODO: get rid of sample.ofx
def to_obp_json(account_id, account_holder, ofx_file):
    #Initiate the ofx object
    ofx = OfxParser.parse(file(ofx_file))
    transactions = []
    
    #TODO making sure end-date and start-date doesnt clash 
    for transaction in ofx.account.statement.transactions:
      obp_transaction = {}

      this_account = {
                "holder":account_holder,
                "number":account_id,
                "kind":'current', #ofx.account.account_type,
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name":"Banco do Brasil"} #ofx.account.institution.organization
                }
     
      other_account = {
                "holder":transaction.payee,
                "number":"unknown",
                "kind":"current",
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name":"unknown"}
                } 

      details = {
           "type_en":transaction.type,
           "type_de":transaction.type,
           "posted":{"$dt":str(transaction.date.astimezone(GMT())) },
           "completed":{"$dt":str(transaction.date)},
           "new_balance":{
                "currency":ofx.account.statement.currency,
                "amount":str(ofx.account.statement.balance)
           },
           "value":{
              "currency":ofx.account.statement.currency,
              "amount":str(transaction.amount)
           },
           "other_data":transaction.memo
        }
      
      obp_transaction = {'this_account':this_account, 'other_account':other_account, 'details' : details }

      transactions.append({'obp_transaction':obp_transaction})

    #Serializing the object
    obpjson = json.dumps(transactions)
    
    #Return the newly created json
    return obpjson


def post_to_api():
    #Ijqds901wla#920xmlz
    data = to_obp_json("4300-1-50180-8", 'Hacker Transparencia', 'sample.ofx')
    f1=open('./json.txt', 'w+')
    print >> f1, data
    url = 'https://demo.openbankproject.com/api/tmp/transactions?secret=Ijqds901wla920xmlz'    
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    req = urllib2.Request(url, data, {'Content-type': 'application/json'})
    print url
    f = urllib2.urlopen(req)
    response = f.read()
    print "response: " + response
    f.close()
    

if __name__ == "__main__":
    #to_obp_json('Hacker Transparencia', 'sample.ofx')
    post_to_api()
    

