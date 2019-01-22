"""" import_reco """

from pprint import pprint
import traceback
from flask import current_app as app

from utils.import_reco import do_import_reco


@app.manager.option('-f',
                    '--file',
                    help='Recommendation file path')
def import_reco(file):
    try:
        do_import_reco(file)
    except Exception as e:
        print('ERROR: ' + str(e))
        traceback.print_tb(e.__traceback__)
        pprint(vars(e))
