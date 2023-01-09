import json
import datetime
import traceback

def calculate_insurance_cost (comm_id, amount, date) :
    comm_id= str(comm_id)
    indexIncreased = 0
    try:
        result_amt = float(amount.strip().replace(',',''))
        print ("Result Amount is - ", result_amt)
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
                print ("Year from FAR is- ",yearFromFar)
            else :
                yearFromFar = "INDEX" + str(dictionary.get("MOST_RECENT_YEAR"))
                print ("Year from FAR is absent so picking MOST RECENT YEAR- ",yearFromFar)
            
            indexIncreased = dictionary.get(comm_id).get('INDEXES').get(yearFromFar)/dictionary.get(comm_id).get('INDEXES').get(yeartoSearch)
            print ("RBI indexIncreased :: from - ",yearFromFar, "to current year is ",indexIncreased)
        json_file.close()
    final_amt = round((result_amt * indexIncreased),2)
    print ("Suggested Value is - ",final_amt,"\n Equation is - \n", result_amt, "*",indexIncreased)
    return round((result_amt * indexIncreased),2)


def lambda_handler(event, context):  
    print("Running Lambda Handler")
    try :
        body = json.loads(event['body'])
        print("Body of request is - ",body)
        financial_doc_json = body['financial_doc_json']
        #policy_doc_json = body['policy_doc_json']
        occ_category = body['occupancy_category']
        occ_subcategory = body['occupancy_subcategory']
        with open('commcode.json') as json_file :
            commcodedictionary = json.load(json_file)
            for key in financial_doc_json.keys() :
                if (key == "Date") : 
                    date = financial_doc_json[key]
                
                if(key == "Buildings") :
                    for building in financial_doc_json[key] :
                        del building["amount"]
                    building.update(suggested_insurance_cost = 0.0)

                if(key == "Plant and Machinery") :
                    for plantAndMachin in financial_doc_json[key] :
                        print("P&M for Given Catgory And Subcatgeory - ",commcodedictionary.get(occ_category).get(occ_subcategory).get('P&M'))
                        cost = calculate_insurance_cost(str(commcodedictionary.get(occ_category).get(occ_subcategory).get('P&M')), plantAndMachin['amount'], date)
                        del plantAndMachin["amount"]
                        plantAndMachin.update(suggested_insurance_cost = cost)

                if(key == "Office Equipments") :
                    print("inside O$E IF Block")
                    for officeEquipments in financial_doc_json[key] :
                        with open('oemapping.json') as json_file :
                            oedict = json.load(json_file)
                            oec = officeEquipments["name"].strip().lower()
                            print("OEC Taxonomy found - ",oec,"\n Its Mapped to Code - \n",oedict.get(oec))
                            cost = calculate_insurance_cost(oedict.get(oec), officeEquipments['amount'], date)
                            del officeEquipments["amount"]
                            officeEquipments.update(suggested_insurance_cost = cost)

                if(key == "Furniture & Fixtures") :
                    print("inside F&F IF Block")
                    for furnitureAndFixture in financial_doc_json[key] :
                        cost = calculate_insurance_cost(str(commcodedictionary.get(occ_category).get(occ_subcategory).get('F&F')), furnitureAndFixture['amount'], date)
                        del furnitureAndFixture["amount"]
                        furnitureAndFixture.update(suggested_insurance_cost = cost)
    except Exception :
        # as exp:
        #print("##### Exception occured while processing :: ", exp.)
        traceback.print_exc()
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
