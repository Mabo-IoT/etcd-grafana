import toml


def set_config(file_path:str='./config/conf.toml') -> dict:
    """
    read toml conf file for latter use.

    :param file_path: absolute path of conf file.
    :return:a dict contains configured infomation.
    """
    with open(file_path) as conf_file:
        config = toml.loads(conf_file.read())

    return config