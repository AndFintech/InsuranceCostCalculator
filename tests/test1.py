import unittest
import insuranceCostCalculator
import json

class TestParser(unittest.TestCase):

  def test_insuranceCostCalculator(self):
      print("Running test_insuranceCostCalculator")
      event = {"body": '{"financial_doc_json": {"Date": "03/31/2018","Buildings": [{"name": "Buildings ","amount": "1,106.68 "}],"Plant and Machinery": [{"name": "Plant and Machinery ","amount": "2,875.15 "}],"Office Equipments": [{"name": "electric installation and equipment","amount": "5.85 "}, {"name": "refrigrator ","amount": "92.57 "}, {"name": "Office equipment ","amount": "34.60 "}],"Furniture & Fixtures": [{"name": "Furniture and Fittings ","amount": "29.07 "}]},"amount_unit": "lakhs","policy_doc_json": {},"occupancy_category": "Dwelling & others","occupancy_subcategory": "Dwellings - Annual"}'}
      result = insuranceCostCalculator.lambda_handler(event, None)
      req_output={'statusCode': 200, 'body': '{"Date": "03/31/2018", "Buildings": [{"name": "Buildings ", "suggested_insurance_cost": 0.0}], "Plant and Machinery": [{"name": "Plant and Machinery ", "suggested_insurance_cost": 2053.68}], "Office Equipments": [{"name": "electric installation and equipment", "suggested_insurance_cost": 7.39}, {"name": "computers and data processing units ", "suggested_insurance_cost": 116.9}, {"name": "Office equipment ", "suggested_insurance_cost": 43.69}], "Furniture & Fixtures": [{"name": "Furniture and Fittings ", "suggested_insurance_cost": 33.18}], "amount_unit": "lakhs"}'}
      #results = json.loads(result)
      #self.assertEqual(results['Date'],"03/31/2018")
      #self.assertDictEqual(result, req_output)
      
if __name__ == '__main__':
    unittest.main()
