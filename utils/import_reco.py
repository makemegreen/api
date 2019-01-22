import pandas as pd

from models import Recommendation, BaseObject, FootprintType


def do_import_reco(file_path) -> Recommendation:
    reco_dataframe = pd.read_csv(file_path)
    total_reco = new_reco = 0

    for row in reco_dataframe.itertuples():
        reco = Recommendation.query.get(row.id)
        if not reco:
            reco = Recommendation()
            reco.id = row.id
            new_reco += 1

        reco.title = row.title
        if str(row.how_to) != 'nan':
            reco.content = row.content
        # TODO: temporary with set a default value
        else:
            reco.content = "Contenu non défini"
        if str(row.benefit) != 'nan':
            reco.benefit = row.benefit
        else:
            reco.benefit = 0.0
        if str(row.how_to) != 'nan':
            reco.how_to = row.how_to
        reco.type = FootprintType({'label': row.category})
        total_reco += 1
        BaseObject.check_and_save(reco)

    print('Recommendations updated : %s' % str(total_reco - new_reco))
    print('Recommendations created : %s' % new_reco)
