""" app_data """

# home_mate   home_waste     1    Comment triez vous vos déchets ?
# home_mate   packaging     4    Avez vous pour habitude d'utiliser vos propres récipients (gourdes, boites...) pour vos sorties, déjeuners à l'extérieur ... ?Utilisez vous vos propres sacs pour les courses du quotidient ?
# home_mate   going_to_work      5    Quel est votre moyen de transport principal (trajets domicile travail par ex) ?
# home_mate   going_to_work      6    Quelle distance moyenne parcourez-vous avec ce moyen de transport ? (en km par jour)
# home_mate   going_out      7    A quelle fréquence faites vous appel à un taxi / uber / chauffeur privé ?
# home_mate   going_on_holidays      8    En moyenne combien d'heures voyagez vous par an  ?
# home_mate   meal      15    A quelle fréquence consommez-vous du lait ou des produits laitiers tels que le yogourt, le fromage, le beurre ou la crème?
# home_mate   meal      16    A quelle fréquence mangez-vous des plats contenant de la viande rouge ? viande blanche? poisson? végétariens?
# home_mate   food_origin      24    Sur l’ensemble des produits (nourritures) que vous achetez, quelle proportion provient de la France?

# home_mate   water / energy     2    A quelle fréquence réalisez vous des machines de linge ?
# home_mate   goods     3    Quels types de produits cosmétique et d'hygiène utilisez vous ?


final_question_data = [
    {
        "question_name": "home_clothes_number",
        "category_name": "clothes",
        "id": 30,
        "display_text": "Combien de vêtements achetés vous par mois ?"
    },
    {
        "question_name": "home_clothes_composition",
        "category_name": "clothes",
        "id": 29,
        "display_text": "Quelle est la matière de vos vêtements ?"
    },
    {
        "question_name": "home_clothes_origin_coefficient",
        "category_name": "clothes",
        "id": 28,
        "display_text": "Sur l’ensemble des vêtements que vous achetez, quelle proportion provient de la France ?"
    },
    {
        "question_name": "home_change_electric_good",
        "category_name": "goods",
        "id": 27,
        "display_text": "A quelle fréquence changez vous votre électroménager ? (lave-linge)"
    },
    {
        "question_name": "home_change_electronic_good",
        "category_name": "goods",
        "id": 26,
        "display_text": "A quelle fréquence changez vous votre électronique ? (pc, smartphone)"
    },
    {
        "question_name": "home_reconditioned_goods",
        "category_name": "goods",
        "id": 25,
        "display_text": "Privilégiez vous l'achat de produits reconditionnés ?"
    },
    {
        "question_name": "home_electronic_devices",
        "category_name": "energy",
        "id": 24,
        "display_text": "Quel est le nombre d'appareils électroniques en veille "
                        "ou en fonctionnement permanent chez vous ?"
    },
    {
        "question_name": "home_bath",
        "category_name": "water",
        "id": 22,
        "display_text": "Combien de bains prenez-vous par semaine ?"
    },
    {
        "question_name": "home_shower",
        "category_name": "water",
        "id": 23,
        "display_text": "Combien de douches prenez-vous par semaine ?"
    },
    {
        "question_name": "home_area",
        "category_name": "energy",
        "id": 18,
        "display_text": "Quelle est la surface habitable "
                        "(lieux de vie hors cave, grenier, garage) de votre logement ? (en m²)"
    },
    {
        "question_name": "home_mates",
        "category_name": "energy",
        "id": 19,
        "display_text": "Combien de personnes habitent dans votre logement ?"
    },
    {
        "question_name": "home_heat_type",
        "category_name": "energy",
        "id": 20,
        "display_text": "Comment est chauffé votre logement ?"
    },
    {
        "question_name": "home_heat_time",
        "category_name": "energy",
        "id": 22,
        "display_text": "Combien de heures laisser vous votre chauffage allumé ? (par jour)"
    },
    {
        "question_name": "home_temperature",
        "category_name": "energy",
        "id": 21,
        "display_text": "A quelle température moyenne est chauffé votre logement ?"
    },
    {
        "question_name": "food_milk_products",
        "category_name": "meal",
        "id": 35,
        "display_text": "A quelle fréquence consommez-vous du lait ou des produits laitiers tels que le yogourt, le fromage, le beurre ou la crème?"
    },
    {
        "question_name": "food_red_meet_meals",
        "category_name": "meal",
        "id": 36,
        "display_text": "A quelle fréquence mangez-vous des plats contenant de la viande rouge ?"
    },
    {
        "question_name": "food_white_meet_meals",
        "category_name": "meal",
        "id": 59,
        "display_text": "A quelle fréquence mangez-vous des plats contenant de la viande blanche ?"
    },
    {
        "question_name": "food_fish_meals",
        "category_name": "meal",
        "id": 60,
        "display_text": "A quelle fréquence mangez-vous des plats contenant du poisson ?"
    },
    {
        "question_name": "food_veggie_meals",
        "category_name": "meal",
        "id": 61,
        "display_text": "A quelle fréquence mangez-vous des plats végétariens ?"
    },
    {
        "question_name": "food_percent_of_french_products",
        "category_name": "food_origin",
        "id": 62,
        "display_text": "Sur l’ensemble des produits (nourritures) que vous achetez, quelle proportion provient de la France ?"
    }
]

answer_data = [
    {
        "id": 1,
        "answer_name": "fuel",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 466.0,
    },
    {
        "id": 6,
        "answer_name": "gas",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 222.0,
    },
    {
        "id": 7,
        "answer_name": "electricity",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 105.0,
    },
    {
        "id": 8,
        "answer_name": "granules",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 42.0,
    },
    {
        "id": 9,
        "answer_name": "wood",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 40.0,
    },
    {
        "id": 10,
        "answer_name": "heat_pump",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 20.0,
    },
    {
        "id": 11,
        "answer_name": "no_info",
        "display_text": "",
        "question_name": "home_heat_type",
        "value": 127.86,
    },
    {
        "id": 2,
        "answer_name": "home_area",
        "display_text": "",
        "question_name": "home_area",
        "value": 1.0,
    },
    {
        "id": 3,
        "answer_name": "home_temperature",
        "display_text": "",
        "question_name": "home_temperature",
        "value": 1.0,
    },
    {
        "id": 12,
        "answer_name": "home_heat_time",
        "display_text": "",
        "question_name": "home_heat_time",
        "value": 1.0,
    },
    {
        "id": 13,
        "answer_name": "home_bath",
        "display_text": "",
        "question_name": "home_bath",
        "value": 1.0,
    },
    {
        "id": 14,
        "answer_name": "home_shower",
        "display_text": "",
        "question_name": "home_shower",
        "value": 1.0,
    },
    {
        "id": 15,
        "answer_name": "only_new",
        "display_text": "Non je préfère les produits neufs",
        "question_name": "home_reconditioned_goods",
        "value": 1.0,
    },
    {
        "id": 16,
        "answer_name": "reconditioned_textile",
        "display_text": "Oui pour le textile",
        "question_name": "home_reconditioned_goods",
        "value": 1.0,
    },
    {
        "id": 17,
        "answer_name": "reconditioned_electriconic_goods",
        "display_text": "Oui pour l'électroménager",
        "question_name": "home_reconditioned_goods",
        "value": 1.0,
    },
    {
        "id": 18,
        "answer_name": "reconditioned_electric_goods",
        "display_text": "Oui pour l'électronique",
        "question_name": "home_reconditioned_goods",
        "value": 1.0,
    },
    {
        "id": 19,
        "answer_name": "home_electronic_devices",
        "display_text": "",
        "question_name": "home_electronic_devices",
        "value": 1.0,
    },
    {
        "id": 21,
        "answer_name": "home_change_electric_good",
        "display_text": "",
        "question_name": "home_change_electric_good",
        "value": 1.0,
    },
    {
        "id": 22,
        "answer_name": "home_clothes_origin_coefficient",
        "display_text": "",
        "question_name": "home_clothes_origin_coefficient",
        "value": 1.0,
    },
    {
        "id": 23,
        "answer_name": "home_clothes_composition",
        "display_text": "",
        "question_name": "home_clothes_composition",
        "value": 1.0,
    },
    {
        "id": 24,
        "answer_name": "home_clothes_number",
        "display_text": "",
        "question_name": "home_clothes_number",
        "value": 1.0,
    },
    {
        "id": 35,
        "answer_name": "food_milk_products",
        "display_text": "",
        "question_name": "food_milk_products",
        "value": 1.0,
    },
    {
        "id": 36,
        "answer_name": "food_red_meet_meals",
        "display_text": "",
        "question_name": "food_red_meet_meals",
        "value": 1.0,
    },
    {
        "id": 59,
        "answer_name": "food_white_meet_meals",
        "display_text": "",
        "question_name": "food_white_meet_meals",
        "value": 1.0,
    },
    {
        "id": 60,
        "answer_name": "food_fish_meals",
        "display_text": "",
        "question_name": "food_fish_meals",
        "value": 1.0,
    },
    {
        "id": 61,
        "answer_name": "food_veggie_meals",
        "display_text": "",
        "question_name": "food_veggie_meals",
        "value": 1.0,
    },
    {
        "id": 62,
        "answer_name": "food_percent_of_french_products",
        "display_text": "",
        "question_name": "food_percent_of_french_products",
        "value": 1.0,
    },
    {
        "id": 20,
        "answer_name": "home_change_electronic_good",
        "display_text": "",
        "question_name": "home_change_electronic_good",
        "value": 1.0,
    },
]


# CATEGORY
category_data = [
    {
        "id": 1,
        "label": "energy",
        "type": "home",
    },
    {
        "id": 2,
        "label": "water",
        "type": "home",
    },
    {
        "id": 3,
        "label": "goods",
        "type": "home",
    },
    {
        "id": 4,
        "label": "clothes",
        "type": "home",
    },
    {
        "id": 5,
        "label": "meal",
        "type": "food",
    },
    {
        "id": 7,
        "label": "food_origin",
        "type": "food",
    },
    {
        "id": 8,
        "label": "packaging",
        "type": "food",
    },
    {
        "id": 9,
        "label": "going_to_work",
        "type": "road",
    },
    {
        "id": 10,
        "label": "going_out",
        "type": "road",
    },

]