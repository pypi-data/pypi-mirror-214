import json
import click

from dbtgenlib import genyml

@click.command()

def get_manifest_data():
    with open('target/manifest.json') as manifest_file:
        manifest_data = json.load(manifest_file)
    return manifest_data

def find_keys():
    manifest_data = get_manifest_data()
    keys_dict = {}
    for node,data in manifest_data['nodes'].items():
        if 'unrendered_config' in data.keys():
            for keys, value in data['unrendered_config'].items():
                node = node.split('.')[-1]
                if 'unique_key' in keys:
                    keys_dict[node] = value.strip()
    return keys_dict


def check_skeys():
    model_keys = genyml.dbtdocgen()
    skeys = find_keys()
    models_missing_keys = []

    flag = True

    for model_name, skey in skeys.items():
        if skey.strip() not in model_keys:
            models_missing_keys.append(model_name.strip())
            flag = False
        else:
            pass

    return flag, models_missing_keys

if __name__ == '__main__':
    flag, models_missing_keys = check_skeys()

    if flag == False:
        # print("The test has failed!")
        click.echo("The test has failed!")
        for model_name in models_missing_keys:
            # print(f"For the model: {model_name}, the key: {skey} is not unique!")
            click.echo("The model: {model_name} is missing a unique key!")
    else:
        click.echo("The test has been successful!")
        # print("The test has been successful!")