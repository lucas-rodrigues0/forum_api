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
from logger import logger


def get_article_from_comment(article_id):
    """Busca um artigo indicado pelo parâmetro article_id sem a relação de comentários."""
    db = db_session()

    article = db.get_one(am.Article, article_id)
    article_data_dict = get_valid_data(article, am.Article)
    article_data_dict["comments"] = None
    return Article(**article_data_dict)


def serialize_comment(comment: cm.Comment):
    """Serializa um comentário e o seu artigo."""
    comment_data_dict = get_valid_data(comment, cm.Comment)
    comment_data_dict["article"] = get_article_from_comment(comment.article_id)
    comment_data_dict["replies"] = None
    return comment_data_dict


def get_comments():
    """Busca todos comentários existentes no banco de dados.
    Retorna lista de scalars Comment.
    """
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

    logger.debug(f"Encontrados {len(comments_data_list)} comentários.")
    return comments_data_list


def get_comment_by_id(comment_id):
    """Busca comentário específico com o ID indicado no parâmetro comment_id.
    Retorn um scalar Comment.
    """
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
    """Busca todos comentários pertencentes a um usuário indicado pelo parâmetro user_id.
    Retorna lista de scalars Comment.
    """
    db = db_session()

    comments = db.query(cm.Comment).filter(cm.Comment.user_id == user_id).all()

    comments_data_list = []
    for comment in comments:
        comment_dict = serialize_comment(comment)
        comments_data_list.append(Comment(**comment_dict))

    logger.debug(
        f"Encontrados {len(comments_data_list)} comentários do usuário {user_id}."
    )
    return comments_data_list


def get_comments_by_period(initial_date, end_date):
    """Busca todos comentários criados dentro do período indicado pelos parâmetros
    initial_date e end_date. Retorna lista de scalars Comment.
    """
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

    logger.debug(
        f"Encontrados {len(comments_data_list)} comentários do periodo {initial_date} até {end_date}."
    )
    return comments_data_list


def verify_comment_reply(comment_id):
    """Verifica se o comentário é uma resposta a outro comentário."""
    db = db_session()
    comment = db.get_one(cm.Comment, comment_id)
    if comment.is_reply:
        return False
    return True


def add_comment(comment_dict: dict):
    """Adiciona novo comentário ao banco de dados. Valída os campos necessários de
    usuário e comentário. Verifica se não é um comentário resposta relacionado a
    outro comentário também resposta. Retorna scalar AddComment.
    """
    db = db_session()

    valid_user, missing_info = validate_user_data(comment_dict)
    if not valid_user:
        error_msg = f"User info is missing: {missing_info}"
        logger.warning(f"Error: {error_msg}")
        return UserInfoMissing(errors=error_msg)

    if comment_dict.get("is_reply") and not verify_comment_reply(
        comment_dict["comment_reply"]
    ):
        logger.warning(
            "Error: Comentário não pode ser um reply de outro comentário que já é um reply."
        )
        return CommentReplyNotAllowed()

    comment_required_columns = ["article_id", "content"]
    is_valid, missing_column = validate_data(comment_required_columns, comment_dict)
    if not is_valid:
        error_msg = f"Comment {missing_column} is missing."
        logger.warning(f"Error: {error_msg}")
        return CommentContentMissing(errors=error_msg)

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
    logger.debug(f"Comentário {comment.comment_id} adicionado com sucesso")
    return AddComment(**comment_data)


def delete_comment(comment_id, user_id):
    """Remove comentário indicado pelo parâmetro comment_id. Valída se o usuário
    indicado pelo user_id é o mesmo que inseriu o comentário. Retorna mensagem.
    """
    db = db_session()

    comment_query = db.query(cm.Comment).filter(cm.Comment.comment_id == comment_id)
    comment = comment_query.first()

    if comment.user_id != user_id:
        logger.warning("Error: Usuário não corresponde ao autor do comentário!")
        return InvalidUser()

    comment_query.delete()
    db.commit()

    logger.debug(f"Comentário {comment_id} removido com sucesso")
    return CommentDeleted(message=f"Comment {comment_id} deleted")


def update_comment(comment_dict: dict):
    """Atualiza comentário indicado no parâmetro. Valída se o usuário indicado é o
    mesmo que inseriu o comentário. Retorna scalar AddComment.
    """
    db = db_session()

    comment_id = comment_dict.get("comment_id")
    if not comment_dict.get("content"):
        logger.warning("Error: Conteúdo de comentário não encontrado!")
        return CommentContentMissing()
    comment = db.get_one(cm.Comment, comment_id)

    if comment.user_id != comment_dict.get("user_id"):
        logger.warning("Error: Usuário não corresponde ao autor do comentário!")
        return InvalidUser()

    comment.content = comment_dict.get("content")

    db.commit()

    comment_data = get_valid_data(comment, cm.Comment)
    comment_data["article"] = get_article_from_comment(comment.article_id)
    logger.debug(f"Comentário {comment_id} atualizado com sucesso")
    return AddComment(**comment_data)
