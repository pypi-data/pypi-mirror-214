def line_contains_property(line_tokens, property):
    for token in line_tokens:
        if token["type"] == "property" and token["content"] == property:
            return True
    return False


def line_contains_value(line_tokens, value):
    for token in line_tokens:
        if token["type"] == "value" and token["content"] == value:
            return True
    return False


# Checks if a line contains a value from a iterable of values
# Returns the value found, otherwise returns None
def line_contains_any_values(line_tokens, values):
    for token in line_tokens:
        if token["type"] == "value" and token["content"] in values:
            return token["content"]
    return None


# Gets all children and their index with a property
def get_children_with_property_shallow(section, property) -> list:
    return [
        (i, x)
        for i, x in enumerate(get_children(section))
        if line_contains_property(x, property)
    ]


# Gets all children and their index with a property and value
def get_children_with_property_and_value_shallow(section, property, value) -> list:
    return get_lines_with_property_and_value(get_children(section), property, value)


def get_lines_with_property_and_value(children, property, value) -> list:
    return [
        (i, child)
        for i, child in enumerate(children)
        if line_contains_property_and_value(child, property, value)
    ]


def get_section_property_value(section, property):
    for line_tokens in section:
        value = get_line_property_value(line_tokens, property)
        if value:
            return (value, line_tokens)
    return None


def get_line_property(line_tokens):
    for token in line_tokens:
        if token["type"] == "property":
            return token["content"]


def get_line_property_value(line_tokens, property):
    for token in line_tokens:
        type_ = token["type"]
        content = token["content"]
        if type_ == "property" and content != property:
            return None
        if type_ == "value":
            return content
    return None


# removes all of a property from a section
def remove_property_from_section(section, property):
    children = get_children(section)
    for i in range(len(children) - 1, -1, -1):
        if line_contains_property(children[i], property):
            children.pop(i)


# removes all of any property in properties from a section
def remove_properties_from_section(section, properties):
    children = get_children(section)
    for i in range(len(children) - 1, -1, -1):
        property = get_line_property(children[i])
        if property in properties:
            children.pop(i)


def get_values_of_properties_of_children_shallowly(section, property):
    matches = [None] * len(section)
    for i, child in enumerate(section):
        c_props = get_children(child)
        if c_props:
            matches[i] = get_section_property_value(c_props, property)
    return matches


def set_line_value(line_tokens, val):
    for i, token in enumerate(line_tokens):
        if token["type"] == "value":
            line_tokens[i]["content"] = str(val)


# Indent lines or sections
def indent(section: list, count=1, recursive=True):
    content = section[0]["content"]

    if section[0]["type"] == "extra" and "\t" in content:
        section[0]["content"] = content + ("\t" * count)
    else:
        section.insert(0, {"type": "extra", "content": ("\t" * count)})

    # TODO: Why have the option to disable recursion?
    if not recursive:
        return

    children = get_children(section)
    if children:
        for x in children:
            indent(x, count)


def get_indent(line_tokens):
    first_token = line_tokens[0]
    if first_token["type"] == "extra" and "\t" in first_token["content"]:
        return len(first_token["content"])
    return 0


def get_children(section):
    if has_children(section):
        return section[-1]["content"]
    return None


def has_children(section):
    return "type" in section[-1] and section[-1]["type"] == "children"


def line_contains_property_and_value(line_tokens, property, value):
    hasProp = False
    for token in line_tokens:
        if not hasProp and token["type"] == "property" and token["content"] == property:
            hasProp = True
        elif token["type"] == "value" and token["content"] == value:
            return True
    return False


def children_contain_property_shallowly(children, property):
    for line_tokens in children:
        for token in line_tokens:
            if token["type"] == "property" and token["content"] == property:
                return True
    return False


def change_line_property(line_tokens, property):
    for i, token in enumerate(line_tokens):
        if token["type"] == "property":
            line_tokens[i]["content"] = property
            return
    raise ValueError("Property doesn't exist in the line!")


def change_line_value(line_tokens, value):
    for i, token in enumerate(line_tokens):
        if token["type"] == "value":
            line_tokens[i]["content"] = value
            return
    raise ValueError("Value doesn't exist in the line!")


# replace the value of line if property (and value) matches, ignores children
def replace_value_of_property(line_tokens, property, value, old_value=None):
    has_right_property = False

    for token in line_tokens:
        type_ = token["type"]
        content = token["content"]

        if has_right_property:
            if type_ == "value" and (old_value == None or old_value == content):
                token["content"] = value
        else:
            if type_ == "children":
                return
            if type_ == "property" and content == property:
                has_right_property = True


def replace_property_names_of_children_shallowly(section, old_property, new_property):
    children = get_children(section)
    for child in children:
        for i, token in enumerate(child):
            if token["type"] == "property":
                if token["content"] == old_property:
                    child[i]["content"] = new_property
                break  # Since every line only has one property, stop looking at this line


def append(foo, depth):
    """
    This function should replace the .append() calls in ini_rules.py.
    This depth argument should be used to indent stuff the right amount.
    """


# this might belong in utils but i'm keeping it here for now
# this can work recursively if needed in case the entity might
# be nested inside a section (material presets, for example)
# def rename_section_preset(section, entity, old, new, recursive=False):
#     """Renames a preset name from old to new of specified entity.
#     Ideally, we should be able to put these in a JSON file, but for now, it'll be in here.

#     AddBackgroundLayer = <entity>
#             PresetName = <old>
#             AddToGroup = Near Backdrops
#     ->
#     AddBackgroundLayer = <entity>
#             PresetName = <new>
#             AddToGroup = Near Backdrops
#     """

#     if not section:
#         return
#     if not ini_rules_utils.has_children(section):
#         return

#     children = ini_rules_utils.get_children(section)
#     if recursive:
#         for line_tokens in children:
#             rename_section_preset(line_tokens, entity, old, new, recursive)

#     if not ini_rules_utils.line_contains_value(section, entity):
#         return

#     for line_tokens in children:
#         ini_rules_utils.replace_value_of_property(line_tokens, "PresetOf", new, old)
