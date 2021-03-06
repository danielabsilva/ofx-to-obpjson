from ofxparse import OfxParser
import json
import urllib2
import sys
import os
import datetime



#TODO: get rid of sample.ofx
def to_obp_json(account_holder, ofx_file):
    # if not an ofx file then exist 
    if not ofx_file.endswith('.ofx'):
      return 
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
                "holder": transaction.payee or transaction.id,
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
           "posted":{"$dt":convert_date(transaction.date)},
           "completed":{"$dt":convert_date(transaction.date)},
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

def convert_date(to_convert):
  return datetime.datetime.strftime(to_convert, "%Y-%m-%dT%H:%M:%S.001Z")


if __name__ == "__main__":
    account_holder = sys.argv[1]
    folder = sys.argv[2]
    secret = sys.argv[3]
    url = 'https://demo.openbankproject.com/api/tmp/transactions?secret={0}'.format(secret)
    if not os.path.isdir(folder):
      print "error: can't find the appropriate folder"
    else:
       try:
        for ofx in os.listdir(folder):
            print os.path.join(folder, ofx)
            data = to_obp_json(account_holder, os.path.join(folder, ofx))
            if (data):
              req = urllib2.Request(url, data, {'Content-type': 'application/json'})
              f = urllib2.urlopen(req)
              response = f.read()
              f.close()
              print "transactions successfully added"
            else:
              print "error : couldn't read the data, the ofx file may be corrupted"
       except:
          print "error: the web request failed"

