from typing import List, Dict, Union
from datetime import timedelta
import math
import warnings
from difflib import SequenceMatcher
import csv
import os
import hashlib
import json


def remove_business_days(from_date, days_to_remove):
    """Removes a number of days from a date by skipping weeekends"""

    # TODO: be able to add holiday calendar to skip custom days

    if days_to_remove < 0:
        raise ValueError("Days to remove arg must be positive")

    days_to_remove_copy = days_to_remove
    current_date = from_date

    while days_to_remove_copy > 0:
        current_date += timedelta(days=-1)

        if current_date.weekday() >= 5:  # saturday = 5, sunday = 6
            continue
        else:
            days_to_remove_copy -= 1

    return current_date


def build_target_row(row, column_indices, column_names) -> dict:
    # todo: finish docstring
    """_summary_

    Args:
        columns_of_interest (_type_): _description_
        column_indices (_type_): _description_
        row (_type_): _description_

    Returns:
        Dict: A dictionary containing one key value pair for each item in the lists:
            - column_name: row[target_column_index]

    Example:
        > row = ['a', 'AX99', 'b', 'bb', '100', '10', 'c']
        > target_column_indices = [4, 5, 1]
        > target_columns = ['MOQ', 'Rounding', 'Item']
        > _build_target_row(row, target_column_indices, target_columns)
        {'MOQ': '10', 'Rounding': '100', 'Item': 'AX99'}

    """
    assert len(column_indices) == len(
        column_names
    ), f"Length of column indices and names must be equal.\n{column_indices}\n{column_names}"

    target_row = {}
    for i in range(len(column_indices)):
        key = column_names[i]
        value = row[column_indices[i]]
        target_row[key] = value

    return target_row


def read_csv(
    file_path, target_columns: List[str], optional_target_columns: List[str] = []
) -> List[Dict]:
    """
    It reads a csv file and returns a list of dictionaries where the keys are
    the column names and the values the records.

    output example:
        data = [
            {'column1': val1, 'column2': val, 'column3': val},
            {'column1': val1, 'column2': val, 'column3': val},
            {'column1': val1, 'column2': val, 'column3': val},
            {'column1': val1, 'column2': val, 'column3': val},
            {'column1': val1, 'column2': val, 'column3': val},
        ]
    """
    if not is_valid_dir(file_path):
        raise NotADirectoryError("Directory does not exist: ", file_path)

    if not is_valid_csv(file_path):
        raise AttributeError("It must be a csv file: ", file_path)

    output = []
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=",")

        file_columns = next(reader)

        all_target_column_index_pairs = get_value_index_pairs(
            file_columns, target_columns, optional_target_columns
        )

        for row in reader:
            try:
                target_row = build_target_row(
                    row,
                    column_names=all_target_column_index_pairs[0],
                    column_indices=all_target_column_index_pairs[1],
                )
                output.append(target_row)
            except IndexError:
                print(f"File should not contain empty rows. Bad row: {row}")

    return output


def get_value_index_pairs(pairs, target_values, optional_target_values=[]):
    """
    The user gives a series of index-value pairs, select some values and the
    function returns these selected values along with their index

    """
    result_values = []
    result_pairs = []

    for col in target_values:
        try:
            result_pairs.append(pairs.index(col))
            result_values.append(col)
        except ValueError:
            raise ValueError(get_not_found_column_message(col, pairs))

    for col in optional_target_values:
        try:
            result_pairs.append(pairs.index(col))
            result_values.append(col)
        except ValueError:
            warnings.warn(get_not_found_column_message(col, pairs))

    return result_values, result_pairs


def get_not_found_column_message(col, file_columns):
    similar_word = find_similar(col, file_columns)

    if similar_word:
        similar_word_str = f"A similar one found in the file is '{similar_word}'."
    else:
        similar_word_str = ""

    return f"Default column '{col}' not found. {similar_word_str}"


def find_similar(value, possible_values):
    suggested_word = ""
    suggested_word_ratio = 0

    for possible_val in possible_values:
        pval_ratio = SequenceMatcher(a=value, b=possible_val).ratio()

        if pval_ratio > suggested_word_ratio and (0.6 < pval_ratio < 1.0):
            suggested_word = possible_val
            suggested_word_ratio = pval_ratio

    return suggested_word


def to_csv(data, file_path: str):
    """Print data in a csv file"""

    if not is_valid_dir(file_path):
        raise NotADirectoryError("Directory does not exist: ", file_path)

    if not is_valid_csv(file_path):
        raise AttributeError("Path must have csv extension: ", file_path)

    with open(file_path, "w", newline="") as output:
        separator = "\t"
        writer = csv.writer(output, delimiter=separator)

        # write explicitly the first row with separator so csv file opens correctly
        writer.writerow([f"sep={separator}"])
        # write the rest of the data
        for row in data:
            writer.writerow(row)


def is_valid_dir(path):
    # remove the base name, if any
    only_path = os.path.split(path)[0]
    print(only_path)
    return os.path.exists(only_path)


def is_valid_csv(path):
    file_name = os.path.basename(path)
    return file_name.endswith(".csv")


def convert_to_int(input, item_code: str):
    try:
        return int(input)
    except ValueError:
        print(f"{input} connot be converted to an integer for item code {item_code}.")
        raise


def convert_to_float(input):
    try:
        return float(input)
    except ValueError:
        print(f"{input} could not be converted into a float number.")
        raise


def get_next_multiple(number, multiple):
    return math.ceil(number / multiple) * multiple


def hash_dicts_list(list_dict):
    result_json = json.dumps(list_dict, sort_keys=True)

    return hashlib.sha3_256(result_json.encode()).hexdigest()


def select_fields(
    data: Union[str, List[Dict]],
    mandatory_mapping: Dict[str, str],
    optional_mapping: Dict[str, str] = {},
) -> List[Dict]:
    """
    Extracts data from a CSV file or a list of dictionaries based on the
    specified fields mapping.

    Args:
        - data (Union[str, List[Dict]]): A path to a CSV file or a list of
        dictionaries containing the input data.
        - field_mapping (Dict[str, str]): A dictionary specifying which fields
        to extract or filter from the input data. The keys of the dictionary
        correspond to the same keys in the output dictionaries, and the
        values correspond to the fields in the data that are to be filtered.

    Returns:
        - List[Dict]: A list of dictionaries where the keys are the fields
        specified in the `field_mapping` parameter, and the values are the
        corresponding values to be extracted from the input data. If the
        input is a CSV file, only the columns specified in the
        `field_mapping` parameter will be included in the output. If the
        input is a list of dictionaries, all fields specified in the
        `field_mapping` parameter will be included in the output.

    Raises:
        - TypeError: If the `data` parameter is not a string or a list of
        dictionaries.
        - ValueError: If the input dictionaries in `data` do not have all the
        fields specified in the `field_mapping` parameter.
    """

    if isinstance(data, str):
        data = read_csv(
            data,
            target_columns=mandatory_mapping.values(),
            optional_target_columns=optional_mapping.values(),
        )

    # Rename dict keys
    renamed_data = []
    for item in data:
        renamed_item = {}
        for key, value in item.items():
            if key in mandatory_mapping.values():
                renamed_item[_get_keys_by_values(mandatory_mapping, key)[0]] = value
            elif key in optional_mapping.values():
                renamed_item[_get_keys_by_values(optional_mapping, key)[0]] = value
        renamed_data.append(renamed_item)

    if not isinstance(renamed_data, (str, list)):
        raise TypeError("Unsupported data type.")

    return renamed_data


def _get_keys_by_values(dict, value):
    keys = []
    for key, val in dict.items():
        if val == value:
            keys.append(key)
    return keys


def _rename_keys(data, mandatory_mapping, optional_mapping):
    """
    Rename the keys of each dictionary in the list according to the provided mapping.

    Args:
        data (list): A list of dictionaries.
        mandatory_mapping (dict): A dictionary mapping the mandatory keys.
        optional_mapping (dict): A dictionary mapping the optional keys.

    Returns:
        A list of dictionaries with the renamed keys.
    """
    renamed_data = []
    for item in data:
        renamed_item = {}
        for key, value in item.items():
            if key in mandatory_mapping:
                renamed_item[mandatory_mapping[key]] = value
            elif key in optional_mapping:
                renamed_item[optional_mapping[key]] = value
        renamed_data.append(renamed_item)
    return renamed_data


def are_both_list_of_dicts_equal(list1, list2):
    """
    Checks whether two input lists contain identical dictionaries with the same
    frequencies, accounting for duplicates in the lists. This function does not
    support nested dictionaries.
    
    Args:
        list1 (list[dict]): First list of dictionaries
        list2 (list[dict]): Second list of dictionaries

    Returns:
        bool: True if both lists contain the same dictionaries. False
        otherwise.
    """

    if len(list1) != len(list2):
        return False

    dict_count_pairs_1 = get_dict_frequency(list1)
    dict_count_pairs_2 = get_dict_frequency(list2)

    # dicts are equal when their keys and values are the same.
    # As a reminder: dicts are a unordered collection of values.
    return True if dict_count_pairs_1 == dict_count_pairs_2 else False

def get_dict_frequency(list):
    """
    Returns a dictionary where the keys are the elements in the input list
    of dictionaries and the values are their frequencies.
    """
    result = {}
    for i in list:
        dict_key = tuple(sorted(i.items()))
        result.setdefault(dict_key, 0) 
        result[dict_key] += 1

    return result


