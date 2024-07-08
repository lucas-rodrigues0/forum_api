from collections import defaultdict

from graphql_api.db import db_session

from graphql_api.models import article_model as am, comment_model as cm
from graphql_api.scalars.article_scalar import (
    Article,
    AddArticle,
    ArticleDeleted,
    UserInfoMissing,
    ArticleContentMissing,
    InvalidUser,
)
from graphql_api.scalars.comment_scalar import Comment
from graphql_api.helper import get_valid_data, validate_user_data, validate_data
from logger import logger


def serialize_article_comments(article_id):
    db = db_session()

    comments = db.query(cm.Comment).filter(cm.Comment.article_id == article_id).all()

    article_comments_list = []
    list_comment_dict = []
    replies_dict = defaultdict(list)
    for comment in comments:
        comment_data_dict = get_valid_data(comment, cm.Comment)
        comment_data_dict["replies"] = None
        comment_data_dict["article"] = None
        if comment.is_reply:
            replies_dict[comment.comment_reply].append(comment_data_dict)
        else:
            list_comment_dict.append(comment_data_dict)

    for comment_dict in list_comment_dict:
        replies = replies_dict.get(comment_dict["comment_id"])
        if replies:
            comment_dict["replies"] = [Comment(**reply) for reply in replies]
        article_comments_list.append(Comment(**comment_dict))

    return article_comments_list


def serialize_article(article: am.Article):
    article_comments = serialize_article_comments(article.article_id)
    article_dict = get_valid_data(article, am.Article)
    article_dict["comments"] = article_comments

    return article_dict


def get_articles():
    db = db_session()

    articles = db.query(am.Article).all()

    articles_data_list = []
    for article in articles:
        article_dict = serialize_article(article)
        articles_data_list.append(Article(**article_dict))

    logger.debug(f"Encontrados {len(articles_data_list)} artigos.")
    return articles_data_list


def get_article_by_id(article_id):
    db = db_session()

    article = db.get_one(am.Article, article_id)

    article_dict = serialize_article(article)
    return Article(**article_dict)


def get_article_by_user(user_id):
    db = db_session()

    articles = db.query(am.Article).filter(am.Article.user_id == user_id).all()

    articles_data_list = []
    for article in articles:
        article_dict = serialize_article(article)
        articles_data_list.append(Article(**article_dict))

    logger.debug(f"Encontrados {len(articles_data_list)} artigos do usuário {user_id}.")
    return articles_data_list


def get_articles_by_period(initial_date, end_date):
    db = db_session()

    articles = (
        db.query(am.Article)
        .filter(
            am.Article.created_at >= initial_date, am.Article.created_at <= end_date
        )
        .all()
    )

    articles_data_list = []
    for article in articles:
        article_dict = serialize_article(article)
        articles_data_list.append(Article(**article_dict))

    logger.debug(
        f"Encontrados {len(articles_data_list)} artigos do periodo {initial_date} até {end_date}."
    )
    return articles_data_list


def add_article(article_dict: dict):
    db = db_session()

    valid_user, missing_info = validate_user_data(article_dict)
    if not valid_user:
        error_msg = f"User info is missing: {missing_info}"
        logger.warning(f"Error: {error_msg}")
        return UserInfoMissing(errors=error_msg)

    article_required_columns = ["title", "content"]
    is_valid, missing_column = validate_data(article_required_columns, article_dict)
    if not is_valid:
        error_msg = f"Article {missing_column} is missing"
        logger.warning(f"Error: {error_msg}")
        return ArticleContentMissing(errors=error_msg)

    article = am.Article(
        user_id=article_dict.get("user_id"),
        user_email=article_dict.get("user_email"),
        user_nickname=article_dict.get("user_nickname"),
        title=article_dict.get("title"),
        content=article_dict.get("content"),
    )

    db.add(article)
    db.commit()

    article_data = get_valid_data(article, am.Article)
    logger.debug(f"Artigo {article.article_id} adicionado com sucesso")
    return AddArticle(**article_data)


def delete_article(article_id, user_id):
    db = db_session()
    article_query = db.query(am.Article).filter(am.Article.article_id == article_id)
    article = article_query.first()

    if article.user_id != user_id:
        logger.warning("Error: Usuário não corresponde ao autor do artigo!")
        return InvalidUser()

    db.query(cm.Comment).filter(cm.Comment.article_id == article_id).delete()
    article_query.delete()
    db.commit()

    logger.debug(f"Artigo {article_id} removido com sucesso")
    return ArticleDeleted(
        message=f"Article {article_id} deleted and all comments related"
    )


def update_article(article_dict: dict):
    db = db_session()

    article_id = article_dict.get("article_id")
    article = db.get_one(am.Article, article_id)

    if article.user_id != article_dict.get("user_id"):
        logger.warning("Error: Usuário não corresponde ao autor do artigo!")
        return InvalidUser()

    article.title = article_dict.get("title") or article.title
    article.content = article_dict.get("content") or article.content

    db.commit()

    article_data = get_valid_data(article, am.Article)
    logger.debug(f"Artigo {article_id} atualizado com sucesso")
    return AddArticle(**article_data)
