from ofxparse import OfxParser
import json
import urllib2
import sys


#TODO: get rid of sample.ofx
def to_obp_json(account_holder, ofx_file):
    #Initiate the ofx object
    ofx = OfxParser.parse(file(ofx_file))
    transactions = []

    #Get Info about the Holders' Account
    account_id = ofx.account.number
    bank = ofx.account.institution.organization
    kind = ofx.account.account_type
    
    #For each transaction transform the OFX transaction to a OBP transaction
    for transaction in ofx.account.statement.transactions:
      obp_transaction = {}

      this_account = {
                "holder":account_holder,
                "number":account_id,
                "kind": kind,
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name": bank}
                }
      other_account = {
                "holder":transaction.payee,
                "number":"unknown",
                "kind": "unknown",
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name":"unknown"}
                }
      details = {
           "type_en":transaction.type,
           "type_de":transaction.type,
           "posted":{"$dt":str(transaction.date)},
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


if __name__ == "__main__":
    #Ijqds901wla920xmlz
    account_holder = sys.argv[1]
    ofx_file = sys.argv[2]
    secret = sys.argv[3]

    data = to_obp_json(account_holder,ofx_file)
    url = 'https://demo.openbankproject.com/api/tmp/transactions?secret={0}'.format(secret)
    req = urllib2.Request(url, data, {'Content-type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
