from goods.models import Products
from django.db.models import Q
from django.contrib.postgres.search import (
    SearchVector,
    SearchRank,
    SearchQuery,
    SearchHeadline,
)

def q_search(query):
    # If query is a number and of reasonable length (product ID search)
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))

    # Full-text search setup for name and description fields
    vector = SearchVector("name", "description")
    search_query = SearchQuery(query)

    # Perform the search and filter results by rank
    result = Products.objects.annotate(rank=SearchRank(vector, search_query))\
                             .filter(rank__gt=0)\
                             .order_by("-rank")

    # Add headline highlighting for name and description without overwriting result
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            search_query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        ),
        bodyline=SearchHeadline(
            "description",
            search_query,
            start_sel='<span style="background-color: yellow">',
            stop_sel="</span>",
        )
    )

    return result


    # NOTE this is different types of search check Documentation
    # return Products.objects.annotate(search=SearchVector('description', 'name')).filter(search=query)
    # return Products.objects.filter(description__search=query)

    # keywords = [word for word in query.split() if len(word) > 2]

    # q_objects = Q()

    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)

    # return Products.objects.filter(q_objects)
