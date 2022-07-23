import requests, argparse
from functools import reduce


def make_requests(data: list):
    for item in data:
        for key, value in item.items():
            response = requests.get(
                "https://pokeapi.co/api/v2/type/" + key
            )
            
            if response.status_code == 200:
                response = response.json()["damage_relations"]
                damage = []
                for val in value:
                    for type_ in response["double_damage_to"]:
                        if type_["name"] == val:
                            damage.append(2)
                    for type_ in response["half_damage_to"]:
                        if type_["name"] == val:
                            damage.append(0.5)
                    for type_ in response["no_damage_to"]:
                        if type_["name"] == val:
                            damage.append(0)
                
                if not damage:
                    print("1x")
                else:
                    multiplier = reduce((lambda x, y: x * y), damage)
                    print(str(multiplier) + "x")
            else:
                print("Status code: ", response.status_code)


def parse_data(path: str) -> list:
    with open(path, 'r') as file:
        content = file.read().split('\n')
        content = list(filter(None, content))

    if not content:
        raise ValueError

    parsed = []
    for line in content:
        if not "->" in line:
            print(line)
            raise ValueError
        
        line = list(filter(None, line.split("->")))
        if not line:
            raise ValueError

        parsed.append(
            {
                line[0].replace(" ", ""): [
                    x for x in list(filter(None, line[1].split(" ")))
                ]
            }
        )

    return parsed


def manage_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", type=str, required=True, help="Path to file")
    args = parser.parse_args()

    path = args.p
    
    try:
        data = parse_data(path)
        if not data:
            print("Empty data")
        make_requests(data)
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Incorrect data value")

manage_args()