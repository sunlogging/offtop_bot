import glob
import os
import logging

logging.basicConfig(filename='./_module/logs/start.log', level=logging.INFO, filemode='w')

NAMEVENV = 'venv2'

logging.info(f'searth {NAMEVENV}')
if len(glob.glob(NAMEVENV)) < 1:

    logging.info(f'{NAMEVENV} is not create, wait...')
    try:
        os.system(f'python -m venv {NAMEVENV}')
    except KeyboardInterrupt:
        logging.critical(f'user stop create {NAMEVENV}')
    except Exception as e:
        logging.critical('error')
        logging.critical(e)

    logging.info(f'{NAMEVENV} create')
    logging.info('download req')

    os.system(f'start .\\{NAMEVENV}\\Scripts\\python.exe -m pip install -r .\\_module\\logs\\requirements.txt')
