import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)+"/../../"))
from main.marvel import marvel_movies

class TestPowerCalc(unittest.TestCase):
    '''
    Test cases for power calculator
    '''
    def setUp(self):
        self.valid_file = "src\\test\\resources\\valid_data.json"
        self.invalid_file = "src\\test\\resources\\invalid_data.txt"
        self.valid_data = [
            {
                "name": "Avengers: Endgame",
                "year": "2019",
                "rating": "8.40",
                "director": "Anthony Russo, Joe Russo",
                "stars": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth"
            },
            {
                "name": "Captain America: Civil War",
                "year": "2016",
                "rating": "7.80",
                "director": "Anthony Russo, Joe Russo",
                "stars": "Chris Evans, Robert Downey Jr., Scarlett Johansson, Sebastian Stan"
            }
        ]
        
    def test_validate_json_file_success(self):
        data = marvel_movies.validate_json_file(self.valid_file)
        assert data[0]["name"] == "Avengers: Infinity War"
        assert data[1]["year"] == "2019"
        
    def test_validate_json_file_exception(self):
        with self.assertRaises(Exception):
            marvel_movies.validate_json_file(self.invalid_file)
            
    def test_get_formatted_data(self):
        data = marvel_movies.get_formatted_data(self.valid_data)
        assert data["Robert Downey Jr."]["ratings"] == [8.4, 7.8]
        assert data["Chris Hemsworth"]["ratings"] == [8.4]
            
            
if __name__ == '__main__':
    unittest.main()
