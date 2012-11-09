from ofxparse import OfxParser
import json

#TODO: get rid of sample.ofx
def to_obp_json(account_holder, ofx_file):
    #Initiate the ofx object
    ofx = OfxParser.parse(file(ofx_file))
    transactions = []
    
    #TODO making sure end-date and start-date doesnt clash 
    for transaction in ofx.account.statement.transactions:
      obp_transaction = {}

      this_account = {
                "holder":account_holder,
                "number":ofx.account.number,
                "kind":ofx.account.account_type,
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name":"ofx.account.institution.organization"}
                }
     
      other_account = {
                "holder":transaction.payee,
                "number":"unknown",
                "kind":"unknown",
                "bank":{
                    "IBAN":"unknown",
                    "national_identifier":"unknown",
                    "name":"unknown"}
                } 

      details = {
           "type_en":transaction.type,
           "type_de":transaction.type,
           "posted":{"$dt":str(transaction.date) },
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

      transactions.append(obp_transaction)

    #Serializing the object
    obpjson = json.dumps(transactions)
    
    #Return the newly created json
    print '------------------------'
    print 'JSON = ' + obpjson
    return obpjson



if __name__ == "__main__":
    to_obp_json('Hacker Transparencia', 'sample.ofx')

