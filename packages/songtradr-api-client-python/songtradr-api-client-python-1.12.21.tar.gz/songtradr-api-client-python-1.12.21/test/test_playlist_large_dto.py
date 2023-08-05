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
from songtradr_api_client_python.models.playlist_large_dto import PlaylistLargeDTO  # noqa: E501
from songtradr_api_client_python.rest import ApiException

class TestPlaylistLargeDTO(unittest.TestCase):
    """PlaylistLargeDTO unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PlaylistLargeDTO
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PlaylistLargeDTO`
        """
        model = songtradr_api_client_python.models.playlist_large_dto.PlaylistLargeDTO()  # noqa: E501
        if include_optional :
            return PlaylistLargeDTO(
                name = '', 
                state = 'active', 
                created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                description = '', 
                asset_url = '', 
                pretzel_tier = '', 
                usage = '', 
                tracks = [
                    songtradr_api_client_python.models.recording_playlist_dto.RecordingPlaylistDTO(
                        recording = songtradr_api_client_python.models.recording_medium_dto.RecordingMediumDTO(
                            spotify_id = '', 
                            genre_predictions = [
                                songtradr_api_client_python.models.recording_genre_prediction_dto.RecordingGenrePredictionDTO(
                                    genre_type = '', 
                                    genre = songtradr_api_client_python.models.genre_minimal_dto.GenreMinimalDTO(
                                        genre_name = '', ), 
                                    probability = 1.337, )
                                ], 
                            tags = [
                                songtradr_api_client_python.models.recording_tag_small_dto.RecordingTagSmallDTO(
                                    tag = songtradr_api_client_python.models.tag_dto.TagDTO(
                                        id = 56, 
                                        categories = [
                                            songtradr_api_client_python.models.category_minimal_dto.CategoryMinimalDTO(
                                                category_name = '', )
                                            ], 
                                        name = '', ), )
                                ], 
                            titles = [
                                songtradr_api_client_python.models.title_dto.TitleDTO(
                                    title_text = '', )
                                ], 
                            musical_features = songtradr_api_client_python.models.musical_features_dto.MusicalFeaturesDTO(
                                space = 'very compact', 
                                primary_mood_cluster_affinity = 1.337, 
                                secondary_mood_cluster = 'aggressive', 
                                secondary_mood_cluster_affinity = 1.337, 
                                tertiary_mood_cluster = 'aggressive', 
                                tertiary_mood_cluster_affinity = 1.337, 
                                vocals_affinity = 1.337, 
                                dominant_instrument_affinity = 1.337, 
                                secondary_instrument = 'electric guitar', 
                                secondary_instrument_affinity = 1.337, 
                                tertiary_instrument = 'electric guitar', 
                                tertiary_instrument_affinity = 1.337, 
                                sound_generation_affinity = 1.337, 
                                rhythm_affinity = 1.337, 
                                primary_sound_character_affinity = 1.337, 
                                tonality_affinity = 1.337, 
                                bpm = 1.337, 
                                production_rating = 'low production quality', 
                                production_rating_affinity = 1.337, 
                                performance_rating = 'low performance quality', 
                                performance_rating_affinity = 1.337, 
                                song_rating = 'low song quality', 
                                song_rating_affinity = 1.337, 
                                audience_age = 'Generation Z', 
                                audience_age_affinity = 1.337, 
                                secondary_audience_age = 'Generation Z', 
                                secondary_audience_age_affinity = 1.337, 
                                tertiary_audience_age = 'Generation Z', 
                                tertiary_audience_age_affinity = 1.337, 
                                audience_gender = 'male', 
                                audience_gender_affinity = 1.337, 
                                audience_region_affinity = 1.337, 
                                secondary_audience_region = 'Australia and New Zealand', 
                                secondary_audience_region_affinity = 1.337, 
                                tertiary_audience_region = 'Australia and New Zealand', 
                                tertiary_audience_region_affinity = 1.337, 
                                origin_region = 'Australia and New Zealand', 
                                origin_region_affinity = 1.337, 
                                origin_decade_affinity = 1.337, 
                                language_of_performance_affinity = 1.337, 
                                curateability_affinity = 1.337, 
                                use_case_affinity = 1.337, 
                                industry_suitability = 'Automobiles and Parts', 
                                industry_suitability_affinity = 1.337, 
                                audience_region = 'Australia and New Zealand', 
                                arousal = 'very calm', 
                                dominant_instrument = 'electric guitar', 
                                energy = 'very quiet', 
                                engagement = 'very unengaging', 
                                groovyness = 'very steady', 
                                harmony = 'very dissonant', 
                                pleasantness = 'very unpleasant', 
                                primary_mood_cluster = 'aggressive', 
                                language_of_performance = 'en', 
                                primary_sound_character = 'brassy', 
                                rhythm = 'common time', 
                                roughness = 'very clear', 
                                scale = 'major key', 
                                sound_generation = 'acoustic', 
                                tempo = 'very slow', 
                                texture = 'very thin', 
                                timbre = 'very warm', 
                                tonality = 'monotonous', 
                                valence = 'very sad', 
                                vocals = 'instrumental', 
                                origin_decade = 'pre-1950s', 
                                curateability = 'curateable', 
                                use_case = 'background', 
                                channel_suitability = 'Spotify', 
                                valence_affinity = 1.337, 
                                arousal_affinity = 1.337, 
                                pleasantness_affinity = 1.337, 
                                engagement_affinity = 1.337, 
                                energy_affinity = 1.337, 
                                tempo_affinity = 1.337, 
                                scale_affinity = 1.337, 
                                timbre_affinity = 1.337, 
                                roughness_affinity = 1.337, 
                                harmony_affinity = 1.337, 
                                texture_affinity = 1.337, 
                                groovyness_affinity = 1.337, 
                                space_affinity = 1.337, 
                                key_affinity = 1.337, 
                                channel_suitability_affinity = 1.337, 
                                key = 'C', ), 
                            recording_party_entities = [
                                songtradr_api_client_python.models.recording_party_dto.RecordingPartyDTO(
                                    contributor_types = [
                                        songtradr_api_client_python.models.contributor_type_dto.ContributorTypeDTO(
                                            type_name = '', )
                                        ], 
                                    party = songtradr_api_client_python.models.party_small_dto.PartySmallDTO(
                                        id = '', 
                                        full_name = '', ), )
                                ], 
                            genres = [
                                songtradr_api_client_python.models.genre_dto.GenreDTO(
                                    id = 56, 
                                    name = '', )
                                ], 
                            language_of_performance = '', 
                            release_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            isrc = '', ), 
                        songtradr_track_guid = '', 
                        assigned_by_id = 56, 
                        sequence = 56, )
                    ], 
                songtradr_playlist_guid = '', 
                usages = [
                    songtradr_api_client_python.models.usage_dto.UsageDTO(
                        name = '', )
                    ]
            )
        else :
            return PlaylistLargeDTO(
                name = '',
        )
        """

    def testPlaylistLargeDTO(self):
        """Test PlaylistLargeDTO"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
