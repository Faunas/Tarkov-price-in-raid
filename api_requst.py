import requests


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def main():
    # Ваша переменная
    item_name = "m855a1"

    # Заменяем {{}} в запросе на значение переменной item_name
    new_query = """
    {{
        items(name: "{}") {{
            id
            sellFor {{
                price
                source
            }}
        }}
    }}
    """.format(item_name)

    result = run_query(new_query)
    print(result)


if __name__ == '__main__':
    main()
