import os
import unittest

from datetime import datetime

from stellanow_cli.code_generators import CsharpCodeGenerator
from stellanow_cli.api import StellaEventDetailed, StellaField, StellaEntity


class TestCsharpCodeGenerator(unittest.TestCase):
    def test_generate_class_handles_all_valueTypes(self):
        # Define an event with each valueType
        event = StellaEventDetailed(
            id="1",
            name="test_event",
            entities=[
                StellaEntity(id='', name="entity1"),
                StellaEntity(id='', name="entity2"),
            ],
            fields=[
                StellaField(id='', name="field1", valueType="Decimal"),
                StellaField(id='', name="field2", valueType="Integer"),
                StellaField(id='', name="field3", valueType="Boolean"),
                StellaField(id='', name="field4", valueType="String"),
                StellaField(id='', name="field5", valueType="Date"),
                StellaField(id='', name="field6", valueType="DateTime"),
            ],
            isActive=True,
            createdAt=datetime(2022, 1, 1).strftime("%Y-%m-%dT%H:%M:%S"),
            updatedAt=datetime(2022, 1, 2).strftime("%Y-%m-%dT%H:%M:%S"),
            description="Test event"
        )

        # Generate the class
        generated_class = CsharpCodeGenerator.generate_class(event)

        # Save to file during debug
        # file_path = os.path.join('output', 'test.cs')
        # with open(file_path, "w") as file:
        #     file.write(generated_class)

        # Check that each field is added with the correct conversion
        self.assertIn('AddField("field1", field1.ToString("F2", CultureInfo.InvariantCulture));', generated_class)
        self.assertIn('AddField("field2", field2.ToString());', generated_class)
        self.assertIn('AddField("field3", field3.ToString().ToLower());', generated_class)
        self.assertIn('AddField("field4", field4);', generated_class)
        self.assertIn('AddField("field5", field5.ToString("yyyy-MM-dd"));', generated_class)
        self.assertIn('AddField("field6", field6.ToString("yyyy-MM-ddTHH:mm:ssZ"));', generated_class)


if __name__ == "__main__":
    unittest.main()
