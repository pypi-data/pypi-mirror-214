import srsly

from .utils import get_data_type, upath


def srsly_convert(
    read_path: str,
    write_path: str = None,
    read_type: str = None,
    write_type: str = None,
    read_skip: bool = None,
    read_use_list: bool = None,
    write_indent: int = None,
    write_append: bool = None,
    write_append_new_line: bool = None,
    write_indent_mapping: int = None,
    write_indent_sequence: int = None,
    write_indent_offset: int = None,
    write_sort_keys: bool = None,
):
    if write_path is None:
        assert write_type, "Either write_path or write_type must be provided."
        write_path = read_path + "." + write_type

    read_path = upath(read_path)
    write_path = upath(write_path)

    if read_type is None:
        read_type = get_data_type(read_path)

    if write_type is None:
        write_type = get_data_type(write_path)

    read_func = getattr(srsly, "read_" + read_type)
    write_func = getattr(srsly, "write_" + write_type)

    read_kwargs = dict()
    if read_skip is not None:
        read_kwargs["skip"] = read_skip
    if read_use_list is not None:
        read_kwargs["use_list"] = read_use_list

    write_kwargs = dict()
    if write_indent is not None:
        write_kwargs["indent"] = write_indent
    if write_append is not None:
        write_kwargs["append"] = write_append
    if write_append_new_line is not None:
        write_kwargs["append_new_line"] = write_append_new_line
    if write_indent_mapping is not None:
        write_kwargs["indent_mapping"] = write_indent_mapping
    if write_indent_sequence is not None:
        write_kwargs["indent_sequence"] = write_indent_sequence
    if write_indent_offset is not None:
        write_kwargs["indent_offset"] = write_indent_offset
    if write_sort_keys is not None:
        write_kwargs["sort_keys"] = write_sort_keys

    data = read_func(read_path, **read_kwargs)
    if read_type == "jsonl":
        data = list(data)
    write_func(write_path, data, **write_kwargs)
