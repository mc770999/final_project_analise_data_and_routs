from returns.result import Success, Failure
from app.db.elastic_database import es_client
from app.queries.elastic_queries import query_search_by_keywords, query_search_by_keywords_and_index, \
    query_search_keyword_in_all_indexes_between_dates


def search_by_keywords(keywords, limit=10):
    try:
        response = es_client.search(index="_all", body=query_search_by_keywords(keywords, limit))
        res = [hit['_source'] for hit in response['hits']['hits']]
        if response:
            return Success(res)
        else:
            return Failure("Find attacks failed. No results found.")
    except Exception as e:
        print(e)


def search_by_keywords_and_index(index_name, keywords, limit=10):
    try:
        response = es_client.search(index=index_name, body=query_search_by_keywords_and_index(keywords,limit))
        res = [hit['_source'] for hit in response['hits']['hits']]
        if response:
            return Success(res)
        else:
            return Failure("Find attacks failed. No results found.")
    except Exception as e:
        print(e)


def search_keyword_in_all_indexes_between_dates(keywords: list, start_date: str, end_date: str, limit: int):
    split_start_date = [int(date) for date in start_date.split("-")]
    split_end_date = [int(date) for date in end_date.split("-")]
    print(keywords, split_start_date, split_end_date)
    try:
        response = es_client.search(index="_all", body=query_search_keyword_in_all_indexes_between_dates(keywords, limit))

        res = [hit['_source'] for hit in response['hits']['hits']]

        res_filtered = list(filter(lambda e: split_start_date[2] < e.get("date", {}).get("year", -1) < split_end_date[2], res))

        res_filtered_month = list(filter(lambda e:
                                         split_start_date[2] == e.get("date", {}).get("year", -1) and
                                         split_start_date[1] < e["date"].get("month", -1) < split_end_date[1],
                                         res))

        res_filtered_month_day = list(filter(lambda e:
                                             split_start_date[2] == e.get("date", {}).get("year", -1) and
                                             split_start_date[1] == e["date"].get("month", -1) == split_end_date[1]
                                             and split_start_date[0] <= e["date"].get("day", -1) <= split_end_date[0]
                                             , res))
        if response:
            return Success(res_filtered + res_filtered_month + res_filtered_month_day)
        else:
            return Failure("Find attacks failed. No results found.")
    except Exception as e:
        print(e)
