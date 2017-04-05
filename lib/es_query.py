query_template={
    "query": {
        "bool": {
            "must": {
            },
            "filter": {
                "term": {
                    "Female": "1"
                }
            }
        }
    }
}

def get_esquery(keys,gender):
    new_query=query_template.copy()
    for key in keys:
        new_query['query']['bool']['must'][key]="1"
    new_query['query']['bool']['filter']['term']["Female"]=str(genter)
    return new_query
