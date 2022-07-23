from urllib.error import HTTPError
import requests, argparse
from functools import reduce


def make_requests(data: list) -> list:
    result = []

    for item in data:
        if type(item) != dict:
            raise ValueError
        
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
                    result.append("1x")
                else:
                    multiplier = reduce((lambda x, y: x * y), damage)
                    result.append(str(multiplier) + "x")
            else:
                raise Exception("err", response.status_code)
        
    return result


def read_data(path: str) -> str:
    with open(path, 'r') as file:
        content = file.read().split('\n')
        content = list(filter(None, content))

    return content


def parse_data(content: str) -> list:
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
        data = read_data(path)
        data = parse_data(data)
        if not data:
            print("Empty data")
        res = make_requests(data)
        for item in res:
            print(item)
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Incorrect data value")
    except Exception as e:
        print("Status code: ", e.args[1])
