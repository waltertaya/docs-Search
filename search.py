from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.query import DateRange, Term


def search_index(query_str, start_date=None, end_date=None, filetype=None, index_dir="indexdir"):
    ix = open_dir(index_dir)
    parser = MultifieldParser(["title", "content"], schema=ix.schema, group=OrGroup)
    query = parser.parse(query_str)

    results_list = []
    with ix.searcher() as searcher:
        filters = []
        if start_date or end_date:
            filters.append(DateRange("modified", start_date, end_date))
        if filetype:
            filters.append(Term("filetype", filetype.lower()))

        final_filter = None
        if filters:
            from whoosh.query import And
            final_filter = And(filters)

        results = searcher.search(query, limit=10, filter=final_filter)
        for hit in results:
            snippet = hit.highlights("content") or hit["content"][:150]
            results_list.append((hit["title"], hit["modified"], hit["filetype"], snippet))
    return results_list
