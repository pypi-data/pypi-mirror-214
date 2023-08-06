import re
from collections import defaultdict


class Incantation:
    """
    A class to read and deserialize a file containing prompts and their content, making the content accessible using
    dot notation and supporting interpolation of placeholders in the content.

    Attributes:
        data (DotNotationDict): A dictionary-like object that allows access to the deserialized content using dot notation.
    """

    def __init__(self, file_path):
        raw_data = self.deserialize(file_path)
        self.data = DotNotationDict(raw_data)

    def deserialize(self, file_path):
        """
        Reads the input file and returns a defaultdict containing the deserialized content.

        Args:
            file_path (str): The path to the input file.

        Returns:
            defaultdict: A defaultdict containing the deserialized content.
        """
        with open(file_path, "r") as f:
            content = f.read()

        lines = content.split("\n")
        result = defaultdict(dict)
        current_key = ""
        triple_quote = '"""'
        in_triple_quotes = False
        triple_quoted_string = ""
        sub_key = ""
        for line in lines:
            if not line.strip() and not in_triple_quotes:
                continue

            if triple_quote in line:
                in_triple_quotes = not in_triple_quotes
                if not in_triple_quotes:
                    result[current_key][sub_key.strip()] = triple_quoted_string.strip()
                    triple_quoted_string = ""
                else:
                    sub_key = line.split(triple_quote)[0].strip().rstrip(":")
                continue

            if in_triple_quotes:
                triple_quoted_string += line + "\n"
            else:
                if not line.startswith(" "):
                    current_key = line.strip().replace(":", "")
                else:
                    sub_key, value = line.strip().split(":", 1)
                    result[current_key][sub_key.strip()] = value.strip()

        return result

    def interpolate(self, content, values):
        """
        Replaces placeholders in the content string with their corresponding values from the values dictionary.

        Args:
            content (str): The content string containing placeholders to be replaced.
            values (dict): A dictionary containing the values to replace the placeholders with.

        Returns:
            str: The content string with placeholders replaced with their corresponding values.

        Raises:
            KeyError: If a placeholder key is not found in the provided values.
        """
        match = re.findall(r"\${(\w+)}", content)
        placeholders = set(match)

        for placeholder in placeholders:
            if placeholder in values:
                content = content.replace(f"${{{placeholder}}}", values[placeholder])
            else:
                raise KeyError(
                    f"Error: The {placeholder} key was not found in the provided values."
                )

        return content

    def __getattr__(self, attr):
        return self.data.__getattr__(attr)

    def __call__(self, **values):
        return self.interpolate(self.data, values)


class DotNotationDict(dict):
    """
    A dictionary subclass that allows access to its elements using dot notation.
    """

    def __getattr__(self, item):
        value = self[item]
        if isinstance(value, dict):
            return DotNotationDict(value)
        else:
            return value
