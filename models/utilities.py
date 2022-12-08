def map_dict_to_options(dict):
    out = []
    for k,v in dict.items():
       out.append( {'label': k, 'value': v}) 
    return out
