import logging


class Logger:
    '''
    to implement a common logger functionality based on the given format
    returns logger 
    '''
    
    @staticmethod
    def get_logger():
        '''
        Create a basic logger and return the logger
        '''
        # Create and configure logger
        logging.basicConfig(format='%(asctime)s %(message)s')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        
        return logger