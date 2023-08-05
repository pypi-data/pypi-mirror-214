# coding: utf-8

"""
    Songtradr API

    This is the Songtradr API. Use it to retrieve deep music metadata and trigger processes like auto-tagging.  You can also use the API to manage your account and musicube cloud data.  **Authentication**  1. Reach out to support@songtradr.com to receive a free account or use your login data if you are already signed up.  2. To authenticate, you need to login via the POST /api/v1/user/login endpoint.  3. The endpoint responds with a jwtToken which you can use in all following API requests as a bearer token.  **Rate Limiting**  The current limit is 120 Requests per minute. Reach out to us via support@songtradr.com if you need to request more.  **Getting Started with auto-tagging**  1. If you want to get your own files auto-tagged, use the POST /api/v1/user/file/{name}/initUpload endpoint. It responds with a presigned S3 link where you can upload your file. 2. You can check the processing status of your file via the GET /api/v1/user/file/{name}/filesStatus endpoint. 3. As soon as processing is done, you can request the generated data via the GET /api/v1/user/files endpoint.  **Getting Started with search**  You can either search the released music via the /public/recording endpoints or your own private uploaded music via the /user/file/ endpoints.  1. If you want to search the world's released music, a good starting point is the GET /api/v1/public/recording/search endpoint. Please find the extensive list of parameters that serve as semantic search filters. 2. If you want to search your own previously uploaded music, a good starting point is the GET GET /api/v1/user/files endpoint. It has the same extensive list of parameters that serve as semantic search filters.  # noqa: E501

    The version of the OpenAPI document: 1.12.21
    Contact: info@songtradr.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from songtradr_api_client_python.models.musical_features_dto import MusicalFeaturesDTO

class RecordingMinimalWithMusicalFeaturesDTO(BaseModel):
    """
    Recording in its minimal form, but with AI-predicted musical features.
    """
    musical_features: Optional[conlist(MusicalFeaturesDTO)] = Field(None, alias="musicalFeatures")
    isrc: StrictStr = Field(...)
    __properties = ["musicalFeatures", "isrc"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RecordingMinimalWithMusicalFeaturesDTO:
        """Create an instance of RecordingMinimalWithMusicalFeaturesDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in musical_features (list)
        _items = []
        if self.musical_features:
            for _item in self.musical_features:
                if _item:
                    _items.append(_item.to_dict())
            _dict['musicalFeatures'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RecordingMinimalWithMusicalFeaturesDTO:
        """Create an instance of RecordingMinimalWithMusicalFeaturesDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RecordingMinimalWithMusicalFeaturesDTO.parse_obj(obj)

        _obj = RecordingMinimalWithMusicalFeaturesDTO.parse_obj({
            "musical_features": [MusicalFeaturesDTO.from_dict(_item) for _item in obj.get("musicalFeatures")] if obj.get("musicalFeatures") is not None else None,
            "isrc": obj.get("isrc")
        })
        return _obj

