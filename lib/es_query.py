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
    for key in keys:
        new_match={"match":{key:"1"}}
        new_query['query']['bool']['must'].append(new_match)
    new_query['query']['bool']['filter']['term']["Female"]=str(gender)
    print new_query
    return new_query
