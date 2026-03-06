import getpass

import yaml


def replace_username_in_dict(d, username: str, placeholder: str = "{USERNAME}"):
    """
    Recursively replaces all instances of a placeholder in a dictionary or list with
    the provided username.

    Parameters
    ----------
    d : dict, list, or str
        The input data structure where the placeholder should be replaced. Can be a
        dictionary, list, or string.
    username : str
        The username to replace the placeholder with.
    placeholder : str, optional
        The string to be replaced by the username. Default is "{USERNAME}".

    Returns
    -------
    dict, list, or str
        The updated data structure with the placeholder replaced by the provided username.
    """
    if isinstance(d, dict):
        return {k: replace_username_in_dict(v, username, placeholder) for k, v in d.items()}
    elif isinstance(d, list):
        return [replace_username_in_dict(i, username, placeholder) for i in d]
    elif isinstance(d, str):
        return d.replace(placeholder, username)
    else:
        return d


def load_config(
    config_path: str = "./area_classification/config.yaml", placeholder: str = "{USERNAME}"
) -> dict:
    """
    Loads a YAML configuration file and replaces placeholders with the username.

    Parameters
    ----------
    config_path : str, optional
        Path to the YAML configuration file. Default is "./area_classification/config.yaml".
    placeholder : str, optional
        The string to be replaced by the username. Default is "{USERNAME}".

    Returns
    -------
    dict
        The configuration dictionary with placeholders replaced by the username.
    """
    username = getpass.getuser()

    # Read the YAML file
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Replace placeholders with the username
    config = replace_username_in_dict(config, username, placeholder)

    return config
