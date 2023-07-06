import logging

logging.basicConfig(filename='log.log', filemode='a', format=f'%(asctime)s - %(levelname)s:%(name)s\t%(message)s')
handler = logging.FileHandler(filename='log.log', mode='a')
formater = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s\t%(message)s', datefmt='%H:%M:%S', style='%', validate=True)
handler.setFormatter(formater)

HANDLER = handler