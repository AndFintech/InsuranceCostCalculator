import unittest
import insuranceCostCalculator

class TestParser(unittest.TestCase):

  def test_insuranceCostCalculator(self):
      event = {"body": '{"financial_doc_json": {"Date": "03/31/2018", "Buildings": [{"name": "Buildings ", "amount": "1,106.68 "}], "Plant and Machinery": [{"name": "Plant and Machinery ", "amount": "2,875.15 "}], "Office Equipments": [{"name": "Electric installation and equipment ", "amount": "5.85 "}, {"name": "Computers and data processing units ", "amount": "92.57 "}, {"name": "Office equipment ", "amount": "34.60 "}], "Furniture & Fixtures": [{"name": "Furniture and Fittings ", "amount": "29.07 "}], "amount_unit": "lakhs"},"policy_doc_json": {}}'}
      result = insuranceCostCalculator.lambda_handler(event, None)
      req_output={'statusCode': 200, 'body': '{"Date": "03/31/2018", "Buildings": [{"name": "Buildings ", "suggested_insurance_cost": 1219.8}], "Plant and Machinery": [{"name": "Plant and Machinery ", "suggested_insurance_cost": 3169.04}], "Office Equipments": [{"name": "Electric installation and equipment ", "suggested_insurance_cost": 6.45}, {"name": "Computers and data processing units ", "suggested_insurance_cost": 102.03}, {"name": "Office equipment ", "suggested_insurance_cost": 38.14}], "Furniture & Fixtures": [{"name": "Furniture and Fittings ", "suggested_insurance_cost": 32.04}], "amount_unit": "lakhs"}'}
      self.assertDictEqual(result, req_output)

if __name__ == '__main__':
    unittest.main()