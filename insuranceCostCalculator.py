import json
import datetime

def calculate_insurance_cost (comm_id, amount, date) :
    indexIncreased = 0
    try:
        result_amt = float(amount.strip().replace(',',''))
    except ValueError:
        result_amt = 0
    if result_amt != 0 :
        with open('rbiIndex.json') as json_file :
            dictionary = json.load(json_file)
            yeartoSearch = 'INDEX20122013'
            if date != "":
                datem = datetime.datetime.strptime(date, "%m/%d/%Y")
                year = str(datem.year)
                last_year = str(datem.year-1)
                yearFromFar = 'INDEX'+last_year + year
            else :
                yearFromFar = "INDEX" + str(dictionary.get("MOST_RECENT_YEAR"))
            # month = datem.month
            # if(month<10):
            #     month = "0"+str(month)
           
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
        commodity_id='1316040002'
        for key in financial_doc_json.keys() :
            if (key == "Date") :               
                date = financial_doc_json[key]
            
            if(key == "Buildings") :
                for building in financial_doc_json[key] :
                    cost = calculate_insurance_cost(commodity_id,building['amount'], date)
                    del building["amount"]
                    building.update(suggested_insurance_cost = cost)

            if(key == "Plant and Machinery") :
                for plantAndMachin in financial_doc_json[key] :
                    cost = calculate_insurance_cost(commodity_id, plantAndMachin['amount'], date)
                    del plantAndMachin["amount"]
                    plantAndMachin.update(suggested_insurance_cost = cost)

            if(key == "Office Equipments") :
                for officeEquipments in financial_doc_json[key] :
                    cost = calculate_insurance_cost(commodity_id, officeEquipments['amount'], date)
                    del officeEquipments["amount"]
                    officeEquipments.update(suggested_insurance_cost = cost)

            if(key == "Furniture & Fixtures") :
                for furnitureAndFixture in financial_doc_json[key] :
                    cost = calculate_insurance_cost(commodity_id, furnitureAndFixture['amount'], date)
                    del furnitureAndFixture["amount"]
                    furnitureAndFixture.update(suggested_insurance_cost = cost)

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
