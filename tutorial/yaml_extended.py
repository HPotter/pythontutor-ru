import yaml


class quoted(str):
    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str',
            value.strip(),
            style=''
        )


class literal(str):
    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str',
            value,
            style='|'
        )


class folded(str):
    @staticmethod
    def yaml_representer(dumper, value):
        return dumper.represent_scalar(
            'tag:yaml.org,2002:str',
            value.strip() + '\n',
            style='>'
        )


yaml.add_representer(quoted, quoted.yaml_representer)
yaml.add_representer(literal, literal.yaml_representer)
yaml.add_representer(folded, folded.yaml_representer)


def dump(*args, **kwargs):
    kwargs.update({
        'default_flow_style': False,
        'allow_unicode': True,
        'default_style': None,
        'line_break': None,
        'indent': 2,
    })

    return yaml.dump(*args, **kwargs)  # TODO safe_dump
