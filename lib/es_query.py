query_template={
    "query": {
        "bool": {
            "must": []
            ,
            "filter": {
                "term": {
                }
            }
        }
    }
}

def get_esquery(keys,gender):
    new_query=query_template.copy()
    new_query['query']['bool']['must']=[]
    for key in keys:
        new_match={"match":{key:"1"}}
        new_query['query']['bool']['must'].append(new_match)
    new_query['query']['bool']['filter']['term']["Female"]=str(gender)
    print new_query
    return new_query

def check_peason(peason):
    contains=0
    layout=peason['layout']
    for part in ["up","mid","leg"]:
        if layout[part]:
            (xC, yC, xD, yD)=layout[part]
            contains+=1
            print layout[part]
    if contains<1:
        return 0
    if layout['mid'] and layout['leg']:
        if layout['mid']<layout['leg']:
            return 0
    return 1
