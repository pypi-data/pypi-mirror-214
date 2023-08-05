"""
    CCF-API

    This API provides programmatic access to data registered to the Human Reference Atlas (HRA). See the [HuBMAP HRA Portal](https://humanatlas.io/) for details.   # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ccf_openapi_client
from ccf_openapi_client.model.json_ld_object import JsonLdObject
from ccf_openapi_client.model.tissue_common import TissueCommon
from ccf_openapi_client.model.tissue_dataset import TissueDataset
from ccf_openapi_client.model.tissue_sample_common import TissueSampleCommon
globals()['JsonLdObject'] = JsonLdObject
globals()['TissueCommon'] = TissueCommon
globals()['TissueDataset'] = TissueDataset
globals()['TissueSampleCommon'] = TissueSampleCommon
from ccf_openapi_client.model.tissue_section import TissueSection


class TestTissueSection(unittest.TestCase):
    """TissueSection unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTissueSection(self):
        """Test TissueSection"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TissueSection()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
