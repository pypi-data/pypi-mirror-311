from abc import ABC, abstractmethod
import re
from jsonschema import validate, ValidationError
import yaml
import json
from typing import Any, Dict
from bs4 import BeautifulSoup

from lxml import html, etree
from typing import List, Dict
from collections import defaultdict

def remove_symbols(text):
    return re.sub(r'[^\w\s]', '', text)

def simplify_xpath_dict(xpath_dict: Dict[str, str]) -> Dict[str, str]:
    """
    Simplifies a dictionary by removing longer keys that have another key as prefix
    when they share the same value.

    Args:
        xpath_dict (Dict[str, str]): Dictionary mapping XPath to text content

    Returns:
        Dict[str, str]: Simplified dictionary with redundant keys removed

    Example:
        Input: {
            "/html/div": "text",
            "/html/div/span": "text",
            "/form": "submit",
            "/form/button": "submit",
            "/form/div/button": "submit"
        }
        Output: {
            "/html/div": "text",
            "/form": "submit"
        }
    """
    # Group keys by their values
    value_to_keys = defaultdict(list)
    for key, value in xpath_dict.items():
        value_to_keys[value].append(key)

    # Process each group of keys with the same value
    keys_to_keep = set()
    for value, keys in value_to_keys.items():
        # Sort keys by length to process shorter keys first
        keys.sort(key=len)

        # For each key, check if it's a prefix of any remaining keys
        for i, current_key in enumerate(keys):
            # If this key is already marked for removal, skip it
            if current_key not in keys_to_keep:
                # Check if this key is a prefix of any other keys
                is_prefix_of_others = False
                for longer_key in keys[i + 1:]:
                    if longer_key.startswith(current_key):
                        is_prefix_of_others = True
                        break

                if is_prefix_of_others:
                    keys_to_keep.add(current_key)
                elif i == 0:  # Always keep at least one key per value
                    keys_to_keep.add(current_key)

    # Create new dictionary with only the kept keys
    simplified_dict = {k: xpath_dict[k] for k in sorted(keys_to_keep)}
    return simplified_dict

def xpath_text_map(full_html: str, xpath_list: List[str]) -> Dict[str, str]:
    """
    Maps XPath expressions to corresponding text content in HTML.

    Args:
        html_content (str): HTML string to parse
        xpath_list (List[str]): List of XPath expressions

    Returns:
        Dict[str, str]: Dictionary mapping XPath to text content

    Example:
        html_str = "<html><body><div>Text</div></body></html>"
        xpaths = ["/html/body/div"]
        result = xpath_text_map(html_str, xpaths)
    """
    try:
        tree = html.fromstring(full_html)
        result = {}

        for xpath in xpath_list:
            try:
                elements = tree.xpath(xpath)
                if elements:
                    # Get text content including text from child elements
                    text = " ".join(elements[0].xpath(".//text()")).strip()
                    if len(text) >= 50:
                        continue
                    if text:
                        result[xpath] = text
                    elif xpath.split("/")[-1] in ['input', 'textarea']:
                        result[xpath] = f"<{xpath.split('/')[-1]}>"
                else:
                    result[xpath] = "No text content"
            except Exception as e:
                result[xpath] = f"Error processing xpath: {str(e)}"

        return result

    except Exception as e:
        raise ValueError(f"Failed to parse HTML: {str(e)}")

def extract_xpaths_from_html(html_content, full_html='', prompt=''):
    r_get_xpaths_from_html = r'xpath=["\'](.*?)["\']'
    xpaths = re.findall(r_get_xpaths_from_html, html_content)
    with open("xpaths.txt", "a") as f:
        for xpath in xpaths:
            f.write(f"{xpath}\n")
    return xpaths

def extract_xpaths_from_html(html_content, full_html='', prompt=''):
    r_get_xpaths_from_html = r'xpath=["\'](.*?)["\']'
    xpaths = re.findall(r_get_xpaths_from_html, html_content)
    keywords = set(remove_symbols(prompt).lower().split())
    with open("html_content.html", "w") as f:
        f.write(full_html)
    if full_html:
        with open("full_html.html", "w") as f:
            f.write(full_html)
        parser = etree.HTMLParser()
        tree = etree.fromstring(full_html, parser)
        root = tree.getroottree()

        # Find all elements
        for element in tree.iter():
            # Get text content (direct text + text from immediate children)
            text = ''.join(element.xpath('.//text()'))

            # Skip elements with no text
            if not text.strip():
                continue

            # Get the full XPath using the root tree
            xpath = root.getpath(element)
            xpaths.append(xpath)
        with open("xpaths.txt", "a") as f:
            for xpath in xpaths:
                f.write(f"{xpath}\n")
        xpaths = [x for x in set(xpaths) if 'span' not in x]
        filtered_xpaths = xpaths.copy()
        # if keywords.intersection(set('input type fill enter'.split())):
        #     return [x for x in set(xpaths) if 'input' in x]
        xpaths_texts_map = xpath_text_map(full_html, xpaths)
        print(xpaths_texts_map)
        filtered_xpaths_map = xpaths_texts_map.copy()
        # print(xpaths)
        # print("==============")
        # print(xpaths_texts_map)
        # add synonyms
        synonyms = [set('type input fill enter name first last'.split())]
        for keyword in keywords.copy():
            for synonym in synonyms:
                if keyword in synonym:
                    keywords.update(synonym)
        # use remove_keywords to filter out keywords
        remove_keywords = set(['button'])
        keywords = keywords - remove_keywords
        # use keywords to filter out xpaths
        filtered_xpaths_map = {k: v for k, v in xpaths_texts_map.items() if keywords.intersection(set(remove_symbols(v).lower().split())) or v.startswith('<')}
        # add the parents
        # for path in filtered_xpaths_map:
        #     parts = path.split('/')
        #     print("=============" + '/'.join(parts[:-1]))
        #     if '/'.join(parts[:-1]) in xpaths_texts_map:
        #         print("1" * 20)
        #         filtered_xpaths_map['/'.join(parts[:-1])] = xpaths_texts_map['/'.join(parts[:-1])]
        #     elif '/'.join(parts[:-2]) in xpaths_texts_map:
        #         print("2" * 20)
        #         filtered_xpaths_map['/'.join(parts[:-2])] = xpaths_texts_map['/'.join(parts[:-2])]
        #     elif '/'.join(parts[:-3]) in xpaths_texts_map:
        #         print("3" * 20)
        #         filtered_xpaths_map['/'.join(parts[:-3])] = xpaths_texts_map['/'.join(parts[:-3])]
        # filtered_xpaths_map = simplify_xpath_dict(filtered_xpaths_map)
        with open("xpaths.txt", "a") as f:
            for xpath, text in filtered_xpaths_map.items():
                f.write(f"{text}: {xpath}\n")

        print("\n")
        print(filtered_xpaths_map)

        res = "\n".join([str(list(filtered_xpaths_map.keys())), "For your reference, the corresponding text of each xpath is provided:", str(filtered_xpaths_map)])
        return res
    else:
        return xpaths


class ExtractionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Error extracting the object: {self.args[0]}"


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> str:
        pass

    @abstractmethod
    def extract_as_object(self, text: str) -> Any:
        pass


class YamlFromMarkdownExtractor(BaseExtractor):
    """
    Extractor for the prompts that end with (or similar to) the following:

    --------------------------------------------
    Completion:
    --------------------------------------------
    """

    def extract(self, markdown_text: str) -> str:
        yml_str = markdown_text.strip()
        # Pattern to match the first ```yaml ``` code block
        pattern = r"```(?:yaml|yml|\n)(.*?)```"

        # Using re.DOTALL to make '.' match also newlines
        match = re.search(pattern, markdown_text, re.DOTALL)
        if match:
            # Return the first matched group, which is the code inside the ```python ```
            yml_str = match.group(1).strip()
        try:
            yaml.safe_load(yml_str)
            return yml_str
        except yaml.YAMLError:
            return None

    def extract_as_object(self, text: str):
        return yaml.safe_load(self.extract(text))


class JsonFromMarkdownExtractor(BaseExtractor):
    """
    Extractor for the prompts that end with (or similar to) the following:

    --------------------------------------------
    Completion:
    --------------------------------------------
    """

    def extract(self, markdown_text: str, shape_validator=None) -> str:
        # Pattern to match the first ```json ``` code block
        pattern = r"```json(.*?)```"

        # Using re.DOTALL to make '.' match also newlines
        match = re.search(pattern, markdown_text, re.DOTALL)

        if shape_validator:
            try:
                # checks if the json returned from the llm matchs the schema
                validate(
                    instance=json.loads(match.group(1).strip()), schema=shape_validator
                )
            except json.JSONDecodeError:
                raise ExtractionError("Invalid JSON format")
            except ValidationError:
                raise ExtractionError("JSON does not match schema")
        else:
            if match:
                # Return the first matched group, which is the code inside the ```python ```
                return match.group(1).strip()
            else:
                # Return None if no match is found
                return None

    def extract_as_object(self, text: str):
        return json.loads(self.extract(text))


class PythonFromMarkdownExtractor(BaseExtractor):
    """
    Extractor for the prompts that end with (or similar to) the following:

    --------------------------------------------
    Completion:
    --------------------------------------------
    """

    def extract(self, markdown_text: str) -> str:
        # Pattern to match the first ```python ``` code block
        pattern = r"```python(.*?)```"

        # Using re.DOTALL to make '.' match also newlines
        match = re.search(pattern, markdown_text, re.DOTALL)
        if match:
            # Return the first matched group, which is the code inside the ```python ```
            return match.group(1).strip()
        else:
            # Return None if no match is found
            return None

    def extract_as_object(self, text: str):
        return eval(self.extract(text))


class UntilEndOfMarkdownExtractor(BaseExtractor):
    """
    Extractor for the prompts that end with (or similar to) the following:

    --------------------------------------------
    Completion:
    ```python
    # Let's proceed step by step.
    --------------------------------------------
    """

    def extract(self, text: str) -> str:
        return text.split("```")[0]

    def extract_as_object(self, text: str) -> Any:
        return self.extract(text)


class DynamicExtractor(BaseExtractor):
    """
    Extractor for typed markdown blocks
    """

    def __init__(self):
        self.extractors: Dict[str, BaseExtractor] = {
            "json": JsonFromMarkdownExtractor(),
            "yaml": YamlFromMarkdownExtractor(),
            "yml": YamlFromMarkdownExtractor(),
            "python": PythonFromMarkdownExtractor(),
        }

    def get_type(self, text: str) -> str:
        types_pattern = "|".join(self.extractors.keys())
        pattern = rf"```({types_pattern}).*?```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            # Try to auto-detect first matching extractor
            for type, extractor in self.extractors.items():
                try:
                    value = extractor.extract(text)
                    if value:
                        return type
                except:
                    pass
            raise ValueError(f"No extractor pattern can be found from {text}")

    def extract(self, text: str) -> str:
        type = self.get_type(text)
        return self.extractors[type].extract(text)

    def extract_as_object(self, text: str) -> Any:
        type = self.get_type(text)
        return self.extractors[type].extract_as_object(text)
