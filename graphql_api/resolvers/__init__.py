from graphql_api.resolvers.article_resolver import (
    get_articles,
    get_article_by_id,
    get_article_by_user,
    get_articles_by_period,
    add_article,
    delete_article,
    update_article,
)

from graphql_api.resolvers.comment_resolver import (
    get_comments,
    get_comment_by_id,
    get_comments_by_user,
    get_comments_by_period,
    add_comment,
    delete_comment,
    update_comment,
)
