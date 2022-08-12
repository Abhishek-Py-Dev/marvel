from typing import Dict, Iterable
import json
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__) + "/../../"))
from lib.log_formatter import Logger

# Global variable
logger = None


# Method definitions
def validate_input_args() -> Dict:
    '''
        Input: <command line arguments>
        Return:
        In case of failure: returns exception to caller
        In case of success: returns dict containing the input args/value to the caller
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_file_fq',
        help='Fully qualified path of input data file in json format',
        required=True
    )

    try:
        args = parser.parse_args()
        return vars(args)
    except SystemExit as ex:
        logger.fatal(ex, exc_info=True)
        raise Exception("Input parameters validation failed!!!")


def display_input_args(data_file_fq: str) -> None:
    '''
        Display command line arguments
    '''
    try:
        logger.info("Data File Path: {}\n".format(data_file_fq))
    except Exception as ex:
        logger.fatal(ex, exc_info=True)
        raise Exception("Display input parameters failed!!!")


def validate_json_file(data_file_fq: str) -> Iterable[Dict]:
    '''
    validate input json file
    '''
    try:
        with open(data_file_fq, 'r') as f:
            return json.load(f)
    except Exception as ex:
        logger.error("Error while reading data file")
        logger.error(ex)
        raise Exception(ex)


def get_formatted_data(data: Iterable[Dict]) -> Dict:
    '''
    convert input data into formatted data which has ratings with each actor
    '''
    formatted_data = {}
    for _data in data:
        for star_name in _data["stars"].split(","):
            # strip the starting and end spaces if any
            star_name = star_name.lstrip().rstrip()
            if star_name not in formatted_data:
                # if the star_name name is not present, creates an empty dictionary and ratings
                formatted_data[star_name] = {}
                formatted_data[star_name]["ratings"] = []
            formatted_data[star_name]["ratings"].append(float(_data["rating"]))

    return formatted_data


def print_data(data: Dict) -> None:
    '''
    print the data in the required format
    '''
    logger.info("Please find stars and their movie ratings information")
    logger.info("==================================================================================")
    sorted_data = {
        k: v
        for k, v in sorted(data.items(), key=lambda item: len(item[1]["ratings"]))
        if len(v["ratings"]) >= 2
    }

    # find the maximum star name length
    max_star_name_length = len(max(sorted_data.keys(), key=lambda name: len(name)))

    for star_name, ratings in sorted_data.items():
        movies = len(ratings["ratings"])
        avg_rating = round(sum(ratings["ratings"]) / movies, 2)
        filling = max_star_name_length - len(star_name)
        logger.info(f"Star Name: '{star_name}'{''.ljust(filling)}  | Movies:  {movies} | AVG Rating: {avg_rating:.2f}")

    logger.info("==================================================================================")
    logger.info("End of the list!!!")


def main():
    '''
    main process which calls different methods sequentially to get the movies information
    '''
    # Create a logger based on the format
    global logger
    logger = Logger.get_logger()

    # Validate and read inputs from command line
    data = validate_input_args()
    data_file_fq = data['data_file_fq']

    # Display input args
    display_input_args(data_file_fq)

    # validate and read json data file
    logger.info("starting validating input argument")
    data = validate_json_file(data_file_fq)
    logger.info("Input argument is a valid json data file")
    logger.info("starting validating input argument...[Done]\n")

    # format json data
    formatted_data = get_formatted_data(data)
    # print(formatted_data)

    # print the data in required format
    print_data(formatted_data)


# Run the program; expects a single argument which is the path of JSON file
if __name__ == "__main__":
    main()
