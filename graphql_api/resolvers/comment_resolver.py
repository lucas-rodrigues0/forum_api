from collections import defaultdict

from graphql_api.db import db_session

from graphql_api.models import article_model as am, comment_model as cm
from graphql_api.scalars.article_scalar import Article, UserInfoMissing, InvalidUser
from graphql_api.scalars.comment_scalar import (
    Comment,
    AddComment,
    CommentContentMissing,
    CommentDeleted,
    CommentReplyNotAllowed,
)
from graphql_api.helper import get_valid_data, validate_user_data, validate_data


def get_article_from_comment(article_id):
    db = db_session()

    article = db.get_one(am.Article, article_id)
    article_data_dict = get_valid_data(article, am.Article)
    article_data_dict["comments"] = None
    return Article(**article_data_dict)


def serialize_comment(comment: cm.Comment):
    comment_data_dict = get_valid_data(comment, cm.Comment)
    comment_data_dict["article"] = get_article_from_comment(comment.article_id)
    comment_data_dict["replies"] = None
    return comment_data_dict


def get_comments():
    db = db_session()

    comments = db.query(cm.Comment).all()

    comments_data_list = []
    list_comment_dict = []
    replies_dict = defaultdict(list)
    for comment in comments:
        comment_data_dict = serialize_comment(comment)
        if comment.is_reply:
            replies_dict[comment.comment_reply].append(comment_data_dict)
        else:
            list_comment_dict.append(comment_data_dict)

    for comment_dict in list_comment_dict:
        replies = replies_dict.get(comment_dict["comment_id"])
        if replies:
            comment_dict["replies"] = [Comment(**reply) for reply in replies]
        comments_data_list.append(Comment(**comment_dict))

    return comments_data_list


def get_comment_by_id(comment_id):
    db = db_session()

    comment = db.get_one(cm.Comment, comment_id)
    replies = (
        db.query(cm.Comment)
        .filter(cm.Comment.comment_reply == comment.comment_id)
        .all()
    )

    comment_data_dict = serialize_comment(comment)
    if replies:
        replies_list = []
        for reply in replies:
            reply_dict = serialize_comment(reply)
            replies_list.append(Comment(**reply_dict))
        comment_data_dict["replies"] = replies_list

    return Comment(**comment_data_dict)


def get_comments_by_user(user_id):
    db = db_session()

    comments = db.query(cm.Comment).filter(cm.Comment.user_id == user_id).all()

    comments_data_list = []
    for comment in comments:
        comment_dict = serialize_comment(comment)
        comments_data_list.append(Comment(**comment_dict))

    return comments_data_list


def get_comments_by_period(initial_date, end_date):
    db = db_session()

    comments = (
        db.query(cm.Comment)
        .filter(
            cm.Comment.created_at >= initial_date, cm.Comment.created_at <= end_date
        )
        .all()
    )

    comments_data_list = []
    list_comment_dict = []
    replies_dict = defaultdict(list)
    for comment in comments:
        comment_data_dict = serialize_comment(comment)
        if comment.is_reply:
            replies_dict[comment.comment_reply].append(comment_data_dict)
        else:
            list_comment_dict.append(comment_data_dict)

    for comment_dict in list_comment_dict:
        replies = replies_dict.get(comment_dict["comment_id"])
        if replies:
            comment_dict["replies"] = [Comment(**reply) for reply in replies]
        comments_data_list.append(Comment(**comment_dict))

    return comments_data_list


def verify_comment_reply(comment_id):
    db = db_session()
    comment = db.get_one(cm.Comment, comment_id)
    if comment.is_reply:
        return False
    return True


def add_comment(comment_dict: dict):
    db = db_session()

    valid_user, missing_info = validate_user_data(comment_dict)
    if not valid_user:
        return UserInfoMissing(errors=f"User info is missing: {missing_info}")

    if comment_dict.get("is_reply") and not verify_comment_reply(
        comment_dict["comment_reply"]
    ):
        return CommentReplyNotAllowed()

    comment_required_columns = ["article_id", "content"]
    is_valid, missing_column = validate_data(comment_required_columns, comment_dict)
    if is_valid:
        article = get_article_from_comment(comment_dict["article_id"])

        comment = cm.Comment(
            user_id=comment_dict.get("user_id"),
            user_email=comment_dict.get("user_email"),
            user_nickname=comment_dict.get("user_nickname"),
            content=comment_dict.get("content"),
            is_reply=comment_dict.get("is_reply"),
            comment_reply=comment_dict.get("comment_reply"),
            article_id=article.article_id,
        )

        db.add(comment)
        db.commit()

        comment_data = get_valid_data(comment, cm.Comment)
        comment_data["article"] = article
        return AddComment(**comment_data)

    return CommentContentMissing(errors=f"Comment {missing_column} is missing")


def delete_comment(comment_id, user_id):
    db = db_session()

    comment_query = db.query(cm.Comment).filter(cm.Comment.comment_id == comment_id)
    comment = comment_query.first()
    if comment.user_id == user_id:
        comment_query.delete()
        db.commit()

        return CommentDeleted(message=f"Comment {comment_id} deleted")

    return InvalidUser()


def update_comment(comment_dict: dict):
    db = db_session()

    comment_id = comment_dict.get("comment_id")
    if not comment_dict.get("content"):
        return CommentContentMissing()
    comment = db.get_one(cm.Comment, comment_id)

    if comment.user_id == comment_dict.get("user_id"):
        comment.content = comment_dict.get("content")

        db.commit()

        comment_data = get_valid_data(comment, cm.Comment)
        comment_data["article"] = get_article_from_comment(comment.article_id)
        return AddComment(**comment_data)

    return InvalidUser()
