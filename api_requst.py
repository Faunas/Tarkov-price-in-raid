import requests


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))


def main():
    item_name = "TerraGroup Labs access keycard"
    new_query = """
    {{
        items(name: "{}") {{
            id
            name
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
