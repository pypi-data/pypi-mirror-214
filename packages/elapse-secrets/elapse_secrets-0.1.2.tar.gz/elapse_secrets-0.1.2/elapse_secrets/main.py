import yaml
import re
import logging
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO)

def clean_regex(regex):
    # remove leading and trailing slashes
    cleaned = regex.strip('/')
    # remove unsupported flag (?-i)
    cleaned = cleaned.replace("(?-i)", "")
    return cleaned

def process_regex(folder,filename, text):
    yaml_file = os.path.join(current_dir,folder,filename)
    with open(yaml_file, 'r') as stream:
        y = yaml.safe_load(stream)

    assert type(y) == dict
    assert "patterns" in y

    for i in y["patterns"]:
        assert "pattern" in i
        assert type(i["pattern"]) == dict
        assert "name" in i["pattern"]
        assert "regex" in i["pattern"]
        assert "confidence" in i["pattern"]
        assert i["pattern"]["confidence"] in ("low", "high")

        r = clean_regex(i["pattern"]["regex"])
        name = i["pattern"]["name"]
        confidence = i["pattern"]["confidence"]

        try:
            pattern = re.compile(r)
            if confidence == 'high':
                text = pattern.sub("********", text)
            else:
                if pattern.search(text):
                    logging.warning(f"Possible match for '{name}' detected with low confidence")
        except re.error as e:
            logging.error(f"Invalid regex pattern '{r}' for '{name}'. Error: {str(e)}")

    stripped_text = text.strip()
    return stripped_text

def filter_elapse_secrets(text: str):
    return process_regex('db','rules-elapse-stable.yml', text)

