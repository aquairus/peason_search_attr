query_template={
    "query": {
        "bool": {
            "must": {
                "match": {
                    "lowBlack": "1"
                },
                "match":{
                "   upBlue":"1"
                }
            },
            "filter": {
                "term": {
                    "Female": "1"
                }
            }
        }
    }
}
