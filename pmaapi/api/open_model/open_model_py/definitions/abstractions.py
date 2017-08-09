"""Function and class abstractions."""


def re_readable_read(file):
    """Read file and reset cursor/pointer to allow fast, simple re-read.

    Side Effects:
        Mutates file stream object passed as argument by moving cursor/pointer
        from from position at start of function call and setting it to position
        '0'. If file stream has not been read before calling this function,
        there will be no effective change.

    Returns:
         str: Contents of read file.
    """
    file_contents = file.read()
    file.seek(0)
    return file_contents


def open_and_read(file):
    """Alias: read_contents"""
    read_contents(file)


def read_contents(file):
    """Open file and read it.

    Returns:
        str: File contents.
    """
    # with open(file, 'r') as stream:
    #     return re_readable_read(stream)

    # return re_readable_read(open(file, 'r'))

    return open(file, 'r').read()


def inverse_filter_dict(dictionary, keys):
    """Filter a dictionary by any keys not given.

    Args:
        dictionary (dict): Dictionary.
        keys (iterable): Iterable containing data type(s) for valid dict key.

    Return:
        dict: Filtered dictionary.
    """
    return {
        key: val for key, val in dictionary.items() if key not in keys
    }


def yaml_load_clean(data):
    """Read YAML.

    Handles dependencies.

    Raises:
        YAMLError

    Returns:
        dict: Data.
    """
    from yaml import load, YAMLError
    try:
        return load(read_contents(data))
    except YAMLError:
        raise YAMLError('YAMLError: An unexpected error occurred when '
                        'attempting to read supplied YAML.')


def yaml_dump_clean(data):
    """Dump YAML in highly readable format and preserving key order.

    Handles dependencies.

    # TODO: Upgrade to ruamel package to preserve order -
    # https://stackoverflow.com/questions/31605131
    # /dumping-a-dictionary-to-a-yaml-file-while-preserving-order

    Returns:
        str: YAML formatted string.
    """
    import yaml
    return yaml.dump(data=data, default_flow_style=False)


def set_and_true(key, _dict):
    """Is key in dict and value True?

    Args:
        key (str): Key to lookup in dictionary.
        _dict (dict): The dictionary.

    Returns:
        bool: Is key in dict and value True?
    """
    return key in _dict and _dict[key] is True
