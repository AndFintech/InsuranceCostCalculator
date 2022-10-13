import unittest
import insuranceCostCalculator

class TestParser(unittest.TestCase):

  def test_insuranceCostCalculator(self):
      event = {"body": '{"financial_doc_json": {"Date": "03/31/2018", "Buildings": [{"name": "Buildings ", "amount": "1,106.68 "}], "Plant and Machinery": [{"name": "Plant and Machinery ", "amount": "2,875.15 "}], "Office Equipments": [{"name": "Electric installation and equipment ", "amount": "5.85 "}, {"name": "Computers and data processing units ", "amount": "92.57 "}, {"name": "Office equipment ", "amount": "34.60 "}], "Furniture & Fixtures": [{"name": "Furniture and Fittings ", "amount": "29.07 "}], "amount_unit": "lakhs"},"policy_doc_json": {}}'}
      result = insuranceCostCalculator.lambda_handler(event, None)
      req_output={'statusCode': 200, 'body': '{"Date": "03/31/2018", "Buildings": [{"name": "Buildings ", "suggested_insurance_cost": 1273.56}], "Plant and Machinery": [{"name": "Plant and Machinery ", "suggested_insurance_cost": 3308.7}], "Office Equipments": [{"name": "Electric installation and equipment ", "suggested_insurance_cost": 6.73}, {"name": "Computers and data processing units ", "suggested_insurance_cost": 106.53}, {"name": "Office equipment ", "suggested_insurance_cost": 39.82}], "Furniture & Fixtures": [{"name": "Furniture and Fittings ", "suggested_insurance_cost": 33.45}], "amount_unit": "lakhs"}'}
      self.assertDictEqual(result, req_output)

if __name__ == '__main__':
    unittest.main()