""" install """


def install_scripts():
    from models.activity import Activity
    from models.api_errors import ApiErrors
    from models.base_object import BaseObject
    from models.user import User
    from models.footprint import Footprint
    from models.footprint_type import FootprintType
    from models.recommendation import Recommendation

    import scripts.sandbox
    import scripts.import_reco
