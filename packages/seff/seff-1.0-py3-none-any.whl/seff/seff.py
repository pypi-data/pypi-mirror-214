# Jerrin Shirks

# native imports
from typing import List, Dict, Union, Set

# custom imports
from .support import *


__ROOT__ = 'ROOT'
__SPLIT__ = '_'
__read_type_mapping: dict = {1: int, 2: float}
__write_type_mapping: dict = {int: 1, float: 2}


def write(filename: str, data: Union[Dict, List[Dict]]):
    """
    Writes Python dictionary or list of dictionaries to a file in binary format.

    :param filename: str. Name of the file to write.
    :param data: dict or list of dicts. Python dictionary or list of dictionaries to write.
    """
    if isList(data):
        data = {__ROOT__: data}

    key_set = set()  # collect keys of the dictionary
    key_list = []

    with open(filename, 'wb') as f:
        writeInt(f, 0)
        __write_data(data, key_list, key_set, f)  # start writing the actual data
        pointer = f.tell()
        __write_dictionary(f, key_list)  # write the initial key dictionary
        f.seek(0)
        writeInt(f, pointer)


def __write_dictionary(f, key_list: List[str]):
    """
    Helper function to write dictionary keys to the file.

    :param f: File object.
    :param key_list: list. List of keys to write.
    """
    writeShort(f, len(key_list))  # Writing dictionary key
    for key in key_list:
        _type = __write_type_mapping.get(type(key), 0)  # Default to 0
        writeByte(f, _type)  # Write type of object
        writeString(f, str(key))  # Write string


def __write_data(data: dict, key_list: List[str], key_set: Set[Union[str, int, float]], f):
    """
    Helper function to write dictionary data to the file.

    :param data: dict. Data to write.
    :param key_list: list. List of keys in the dictionary.
    :param key_set: set. Set of keys in the dictionary.
    :param f: File object.
    """
    tags = [None] * len(data.items())
    nodes = [None] * len(data.items())
    tag_count = 0
    node_count = 0

    # convert all tags, nodes, and lists into only tags and nodes
    for key, value in data.items():

        # add key
        if key not in key_set:
            key_list.append(key)
            key_set.add(key)

        if isDict(value):
            if node_count < len(nodes):
                nodes[node_count] = (key, value)
            else:
                nodes.append((key, value))
            node_count += 1
        elif isList(value):
            for i, element in enumerate(value):
                if isNotDict(element) and isNotList(element):
                    if tag_count < len(tags):
                        tags[tag_count] = (key, element)
                    else:
                        tags.append((key, element))
                    tag_count += 1
                else:
                    if node_count < len(nodes):
                        nodes[node_count] = (key, element)
                    else:
                        nodes.append((key, element))
                    node_count += 1
        else:
            if tag_count < len(tags):
                tags[tag_count] = (key, value)
            else:
                tags.append((key, value))
            tag_count += 1

    del tags[tag_count:]
    del nodes[node_count:]

    # Write all tags
    writeInt(f, len(tags))  # Number of tags
    for key, value in tags:
        writeShort(f, key_list.index(key))  # writing dictionary key
        writeString(f, str(value))  # write string, tag value

    # Write all nodes
    writeInt(f, len(nodes))  # Number of nodes
    for key, value in nodes:
        writeShort(f, key_list.index(key))  # writing dictionary key
        __write_data(value, key_list, key_set, f)




def read(filename: str) -> Union[dict, List[dict]]:
    """
    Reads data from a binary file and returns a Python dictionary or a list of dictionaries.

    :param filename: str. Name of the file to read.
    :return: dict or list of dicts. The data read from the file.
    """
    with open(filename, 'rb') as f:
        pointer = readInt(f)
        f.seek(pointer)
        key_set = __read_dictionary(f)  # Read the dictionary keys
        f.seek(4)
        data, _ = __read_data(f, key_set)  # Read the data

    # pull the data out of root, if it was initially in a list
    if __ROOT__ in data:
        return [data[__ROOT__]]
    return data


def __read_dictionary(f):
    """
    Helper function to read dictionary keys from the file.

    :param f: File object.
    :return: list. List of keys read.
    """
    num_keys = readShort(f)
    key_list = [None] * num_keys
    for index in range(num_keys):
        _type = readByte(f)
        key = readString(f)
        convert_func = __read_type_mapping.get(_type, type(key))  # Default to identity function
        key_list[index] = convert_func(key)
    return key_list


def __read_data(f, key_list: List[Union[str, int, float]]):
    """
    Helper function to read data from the file and construct the dictionary.

    :param f: File object.
    :param key_list: list. List of keys.
    :return: tuple. Dictionary constructed from the data and the new depth.
    """
    def __append_to_dict(_data, _key, _value):
        if _key in _data:
            if isList(_data[_key]):
                _data[_key].append(_value)
            else:
                _data[_key] = [_data[_key], _value]
        else:
            _data[_key] = _value

    data = {}

    # Read all tags
    num_tags = readInt(f)  # Number of tags
    for _ in range(num_tags):
        key_index = readShort(f)  # Reading dictionary key
        key = key_list[key_index]
        value = readString(f)  # Read string
        if "." in value:
            try:
                value = float(value)
            except:
                ""
        elif value.isnumeric():
            value = int(value)
        __append_to_dict(data, key, value)

    # Read all nodes
    num_nodes = readInt(f)  # Number of Nodes
    for _ in range(num_nodes):
        key_index: int = readShort(f)  # Reading dictionary key
        key: str = key_list[key_index]
        value = __read_data(f, key_list)
        __append_to_dict(data, key, value)

    return data
