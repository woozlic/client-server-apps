import yaml


def save_obj_to_yaml(obj_dict: dict, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as f:
        data = yaml.dump(obj_dict, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return data


def load_obj_from_yaml(filepath: str) -> dict:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


if __name__ == '__main__':
    yaml_obj = {
        'list': [1, 2, 3],
        4: 4,
        'euros': {
            '1€': '1 €',
            '2€': '2 €',
            '3€': '3 €',
        }
    }

    yaml_file = '../tmp/file.yaml'
    save_obj_to_yaml(yaml_obj, yaml_file)

    res_yaml = load_obj_from_yaml(yaml_file)
    print(yaml_obj)
    print(res_yaml)
    assert res_yaml == yaml_obj
