import json
from dateutil import parser

def calculate_insurance_cost (comm_id, amount, date) :
    indexIncreased = 0
    try:
        result_amt = float(amount.strip().replace(',',''))
    except ValueError:
        result_amt = 0
    if result_amt != 0 :
        with open('rbiIndex.json') as json_file :
            dictionary = json.load(json_file)
            print('INDX'+str(parser.parse(date).strftime("%m")) + str(parser.parse(date).year))
            print(":::: ", dictionary.get(comm_id).get('INDEXES').get('INDX042012')) 
            print(":::: ", dictionary.get(comm_id).get('INDEXES').get('INDX'+str(parser.parse(date).strftime("%m")) + str(parser.parse(date).year)))
            #yeartoSearch =  'INDX'+str(parser.parse(date).strftime("%m") +'2012')
            yeartoSearch = 'INDX042012'
            yearFromFar = 'INDX'+str(parser.parse(date).strftime("%m")) + str(parser.parse(date).year)
            indexIncreased = dictionary.get(comm_id).get('INDEXES').get(yearFromFar)/dictionary.get(comm_id).get('INDEXES').get(yeartoSearch)
            print ("indexIncreased :: ", indexIncreased)
        json_file.close()
    return round((result_amt * indexIncreased),2)


def lambda_handler(event, context):  
    # Document
    try :
        body = json.loads(event['body'])
        financial_doc_json = body['financial_doc_json']
        policy_doc_json = body['policy_doc_json']
        for key in financial_doc_json.keys() :
            if (key == "Date") :               
                date = financial_doc_json[key]
            
            if(key == "Buildings") :
                for building in financial_doc_json[key] :
                    cost = calculate_insurance_cost('1316040002',building['amount'], date)
                    del building["amount"]
                    building.update(suggested_insurance_cost = cost)
                    financial_doc_json[key]=building

            if(key == "Plant and Machinery") :
                for plantAndMachin in financial_doc_json[key] :
                    cost = calculate_insurance_cost('1316040002', plantAndMachin['amount'], date)
                    del plantAndMachin["amount"]
                    plantAndMachin.update(suggested_insurance_cost = cost)
                    financial_doc_json[key]=plantAndMachin

            if(key == "Office Equipments") :
                for officeEquipments in financial_doc_json[key] :
                    cost = calculate_insurance_cost('1316040002', officeEquipments['amount'], date)
                    del officeEquipments["amount"]
                    officeEquipments.update(suggested_insurance_cost = cost)
                    financial_doc_json[key]=officeEquipments

            if(key == "Furniture & Fixtures") :
                for furnitureAndFixture in financial_doc_json[key] :
                    cost = calculate_insurance_cost('1316040002', furnitureAndFixture['amount'], date)
                    del furnitureAndFixture["amount"]
                    furnitureAndFixture.update(suggested_insurance_cost = cost)
                    financial_doc_json[key]=furnitureAndFixture

    except Exception as exp:
        print("##### Exception occured while processing :: ", exp)
        return {
            'statusCode': 500,
            'body': {"message":"Somthing went wrong!!"}

        }
    print ("Success")
    print("Dict ::: ", financial_doc_json)
    return {
        'statusCode': 200,
        'body': json.dumps(financial_doc_json)
    }
