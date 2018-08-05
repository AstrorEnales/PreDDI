#!/usr/bin/env python3


def manual_name_mapping(name: str) -> str or None:
    # Fixed with next DrugBank dump
    # Atracurium
    if name == 'atracurium':
        return 'DB13295'
    # Tenofovir
    if name == 'tenofovir':
        return 'DB14126'

    # Medroxyprogesterone acetate
    if name == 'medroxyprogesterone':
        return 'DB00603'
    # Doxacurium chloride
    if name == 'doxacurium':
        return 'DB01135'
    # Rotigotine
    if name == 'rotigotine/transdermal/patch' or name == 'rotigotine transdermal patch':
        return 'DB05271'

    # Source 2 specific
    # Teriparatide
    if name == 'ly 333334':
        return 'DB06285'
    # Nystatin
    if name == 'nistatin':
        return 'DB00646'
    # Azathioprine
    if name == 'azathioprin':
        return 'DB00993'
    # Desirudin
    if name == 'cgp 39393':
        return 'DB11095'
    # Sodium chloride
    if name == 'nacl':
        return 'DB09153'
    # Budesonide
    if name == 'rhinocort':
        return 'DB01222'
    # Doxycycline
    if name == 'vibramycin':
        return 'DB00254'
    # Cloperastine
    if name == 'hustazol':
        return 'DB09002'

    return None


def name_to_drugbank_id(name: str) -> str or None:
    # name_lower = name.lower().replace('/', ' ')
    # if name_lower in drugbank_name_id_map:
    #     return drugbank_name_id_map[name_lower]
    # if name_lower in drugbank_product_name_id_map:
    #     return drugbank_product_name_id_map[name_lower]
    return manual_name_mapping(name)


def drugbank_id_to_name(drugbank_id: str) -> str or None:
    return None


def is_camel(s):
    return s != s.lower() and s != s.upper()
