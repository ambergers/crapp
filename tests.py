import server

from sqlalchemy import MetaData
from unittest import TestCase
from unittest.mock import patch, Mock
from model import (db, connect_to_db, get_bathrooms_by_lat_long, 
                   get_bathroom_objs_from_request, Bathroom)

class TestBathroomHelpers(TestCase):
    
    def setUp(self):
        """Setup for each test below."""
        
        # Get the Flask test client
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(server.app, "postgresql:///testdb")
     
        # Create tables not currently needed, here for future tests
        # db.create_all()

        
    @patch('model.requests.get')
    def test_get_bathroom_objs_from_request(self, mock_get):
        """Test that when a Response is input, returns list of Bathroom objects."""

        response_json_bathrooms = [
            {"id": 1,
             "name": "Quizno's",
             "street": "422 Geary",
             "city": "San Francisco",
             "state": "CA",
             "accessible": False,
             "unisex": True,
             "latitude": 37.7872185,
             "longitude": -122.4104286,
             "created_at": "2014-02-02T20:52:32.664Z",
             "updated_at": "2014-02-02T20:52:32.664Z",
             "downvote": 1,
             "upvote": 1,
             "country": "US",
             "changing_table": False,
             "edit_id": 2509,
             "approved": True,
             "distance": 0.13262375988183,
             "bearing": "145.137391397972"
            },
            {"id": 2,
             "name": "Academy of Art University",
             "street": "540 Powell St",
             "city": "San Francisco",
             "state": "CA",
             "accessible": False,
             "unisex": True,
             "directions": "entrance level",
             "comment": "Only available for Academy students with ID",
             "latitude": 37.789732,
             "longitude": -122.408567,
             "created_at": "2014-02-02T20:51:17.456Z",
             "updated_at": "2014-02-02T20:51:17.456Z",
             "downvote": 1,
             "upvote": 0,
             "country": "US",
             "changing_table": False,
             "edit_id": 1580,
             "approved": True,
             "distance": 0.175302305487618,
             "bearing": "74.660197543476"
            }]
            
        # Set return value for mock json method to response_json_bathrooms
        mock_get.return_value.json.return_value = response_json_bathrooms

        # Get response
        response = get_bathrooms_by_lat_long('lat', 'long')

        # Use mocked response to get bathroom objects
        bath_objs = get_bathroom_objs_from_request(response)
        
        # Make sure latitude and longitude of each bathroom object returned
        # matches mocked response json latitude and longitude as expected
        self.assertEqual(bath_objs[0].latitude, 
                         response_json_bathrooms[0]["latitude"])
        self.assertEqual(bath_objs[0].longitude, 
                         response_json_bathrooms[0]["longitude"])
        self.assertEqual(bath_objs[1].latitude, 
                         response_json_bathrooms[1]["latitude"])
        self.assertEqual(bath_objs[1].longitude, 
                         response_json_bathrooms[1]["longitude"])


if __name__ == "__main__":
    import unittest
    unittest.main()
