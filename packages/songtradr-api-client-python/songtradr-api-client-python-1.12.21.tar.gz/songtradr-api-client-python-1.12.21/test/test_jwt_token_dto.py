# coding: utf-8

"""
    Songtradr API

    This is the Songtradr API. Use it to retrieve deep music metadata and trigger processes like auto-tagging.  You can also use the API to manage your account and musicube cloud data.  **Authentication**  1. Reach out to support@songtradr.com to receive a free account or use your login data if you are already signed up.  2. To authenticate, you need to login via the POST /api/v1/user/login endpoint.  3. The endpoint responds with a jwtToken which you can use in all following API requests as a bearer token.  **Rate Limiting**  The current limit is 120 Requests per minute. Reach out to us via support@songtradr.com if you need to request more.  **Getting Started with auto-tagging**  1. If you want to get your own files auto-tagged, use the POST /api/v1/user/file/{name}/initUpload endpoint. It responds with a presigned S3 link where you can upload your file. 2. You can check the processing status of your file via the GET /api/v1/user/file/{name}/filesStatus endpoint. 3. As soon as processing is done, you can request the generated data via the GET /api/v1/user/files endpoint.  **Getting Started with search**  You can either search the released music via the /public/recording endpoints or your own private uploaded music via the /user/file/ endpoints.  1. If you want to search the world's released music, a good starting point is the GET /api/v1/public/recording/search endpoint. Please find the extensive list of parameters that serve as semantic search filters. 2. If you want to search your own previously uploaded music, a good starting point is the GET GET /api/v1/user/files endpoint. It has the same extensive list of parameters that serve as semantic search filters.  # noqa: E501

    The version of the OpenAPI document: 1.12.21
    Contact: info@songtradr.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import unittest
import datetime

import songtradr_api_client_python
from songtradr_api_client_python.models.jwt_token_dto import JwtTokenDTO  # noqa: E501
from songtradr_api_client_python.rest import ApiException

class TestJwtTokenDTO(unittest.TestCase):
    """JwtTokenDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JwtTokenDTO
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `JwtTokenDTO`
        """
        model = songtradr_api_client_python.models.jwt_token_dto.JwtTokenDTO()  # noqa: E501
        if include_optional :
            return JwtTokenDTO(
                jwt_token = '', 
                expiration_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                refresh_token = ''
            )
        else :
            return JwtTokenDTO(
                jwt_token = '',
                expiration_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testJwtTokenDTO(self):
        """Test JwtTokenDTO"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
