USER_INFO_COLUNS = ["user_id", "user_email", "user_nickname"]


def get_valid_data(model_data_object, model_class):
    data_dict = {}
    for column in model_class.__table__.columns:
        try:
            data_dict[column.name] = getattr(model_data_object, column.name)
        except:
            pass
    return data_dict


def validate_user_data(object_data: dict):
    for column in USER_INFO_COLUNS:
        if not object_data.get(column):
            return False, column

    return True, None


def validate_data(model_columns, object_data: dict):
    for column in model_columns:
        if not object_data.get(column):
            return False, column

    return True, None
