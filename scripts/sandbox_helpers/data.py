from models.footprint_type import FootprintType

users_data = [
    {
        "username": "John",
        "email": "john@john.com",
        "password": "testpsswd"
    }
]

recommendations_data = [
    {
        "title": "Je ferme les volets ou les rideaux la nuit pour conserver la chaleur à la maison",
        "content": "En fermant les volets,\n"
                   "on évite que les vitres se refroidissent et qu’une sensation de froid\n"
                   "nous envahisse, bien que la température reste la même au centre de la pièce.\n"
                   "Du coup, on n’aura pas besoin de compenser ce désagrément en montant le chauffage.",
        "benefit_description": "Cela représente 2% de la consommation d'energie totale \n"
                               "La consommation moyenne en 2017 pour un foyer français est de 4 710 kWh \n"
                               "Le nombre de personnes par foyer en France est de 2,09.\n"
                               "Donc Gain par nuit de 0,12 KWh\n"
                               "En France, un kWh électrique produit environ 0,09 kg équivalent CO2\n"
                               "Gain de 0,011 eq.CO2 par jour",
        "benefit": 4.015,
        "fact": "24% de l'énergie du chauffage est perdu à cause d'une mauvaise isolation",
        "how_to": "On vous laisse imaginer la meilleure technique pour fermer des volets !",
        "footprint_type": FootprintType.ENERGY
    },
    {
        "title": "J'installe un réflecteur de chaleur derrière le radiateur",
        "content": "A moins de 10€ le m2, ce panneau brillant renvoie plus efficacement la chaleur rayonnée "
                   "par le radiateur.\nLe coût est amorti en un hiver",
        "benefit_description": "7,5% de la facture de chauffage\n"
                               "1 683€ en 2017 par foyer par an. Et Prix du KwH : 0,14€ : prix de 0,09Kg eq CO2\n"
                               "Revenir à la journée décomptée depuis l'activation de la reco : par jour :\n"
                               "0,075 * 1 683 / 2,09 / 365 / 0,14 = 1,2 Eq CO2 par jour",
        "benefit": 438.0,
        "fact": "21% de l'énergie du chauffage est perdu à cause d'une mauvaise isolation",
        "how_to": "Rendez-vous chez Conforama",
        "footprint_type": FootprintType.ENERGY
    }
]
