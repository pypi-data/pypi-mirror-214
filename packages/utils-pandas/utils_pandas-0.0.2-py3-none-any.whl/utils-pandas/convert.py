import json

def to_json(df):
    lista_dicionarios = df.to_dict(orient='records')
    json_data = json.dumps(lista_dicionarios, ensure_ascii=False)
    return json_data


def to_json_for_column(df, column=None):
    if column is None:
        column = df.columns[0]
    
    cols = df.columns.difference([column])
    d = (df.groupby(column)[cols]
            .apply(lambda x: x.to_dict('r'))
            .reset_index(name='dados')
            .to_dict(orient='records'))
    
    return d