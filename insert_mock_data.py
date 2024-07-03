from graphql_api.db import db_session
from graphql_api.models import Article, Comment


def insert_mock_data_to_db():
    db = db_session()
    print("Init db session!")

    artigo1 = Article(
        user_id="google-oauth2|105486185203565706760",
        user_email="mymail@email.com",
        user_nickname="my_nickname",
        title="Lorem ipsum",
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    )

    artigo2 = Article(
        user_id="auth0|666de16cf0165a500b0fc4ec",
        user_email="nickmail@email.com",
        user_nickname="other_nickname",
        title="Lorem ipsum 2",
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    )

    artigo3 = Article(
        user_id="auth0|667d72f96f074005d6ca6131",
        user_email="test@mail.com",
        user_nickname="test",
        title="Para deletar",
        content="qualquer coisa",
    )

    db.add(artigo1)
    db.add(artigo2)
    db.add(artigo3)

    db.flush()
    print("Added articles!")

    comment1 = Comment(
        user_id="auth0|667d72f96f074005d6ca6131",
        user_email="test@mail.com",
        user_nickname="test",
        content="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.",
        article_id=artigo1.article_id,
    )

    db.add(comment1)
    db.flush()

    comment2 = Comment(
        user_id="auth0|667eafca16bf3a06dc531f7e",
        user_email="somemail@mail.com",
        user_nickname="somemail",
        content="Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.",
        article_id=artigo1.article_id,
        is_reply=True,
        comment_reply=comment1.comment_id,
    )

    comment3 = Comment(
        user_id="google-oauth2|105486185203565706760",
        user_email="mymail@email.com",
        user_nickname="my_nickname",
        content="Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.",
        article_id=artigo1.article_id,
    )

    comment4 = Comment(
        user_id="google-oauth2|105486185203565706760",
        user_email="mymail@email.com",
        user_nickname="my_nickname",
        content="Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?",
        article_id=artigo1.article_id,
        is_reply=True,
        comment_reply=comment1.comment_id,
    )

    comment5 = Comment(
        user_id="google-oauth2|105486185203565706760",
        user_email="mymail@email.com",
        user_nickname="my_nickname",
        content="para deletar",
        article_id=artigo3.article_id,
    )

    db.add(comment2)
    db.add(comment3)
    db.add(comment4)
    db.add(comment5)
    print("Added comments!")

    db.commit()
    print("Commited!")
    db.close()
    print("Session closed!")

    return


if __name__ == "__main__":
    insert_mock_data_to_db()
