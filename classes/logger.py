import logging

from settings import LOG_FILE, LOG_PATH

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s:\t%(message)s',
                              datefmt='%H:%M:%S', style='%', validate=True)
Handler = logging.FileHandler(filename=LOG_PATH + LOG_FILE, mode='a')
Handler.setLevel(logging.INFO)
Handler.setFormatter(formatter)

if __name__ == "__main__":
    pass
