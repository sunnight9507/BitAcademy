def define_dict():
    dct = dict()
    print(dct, type(dct))

    dct = {}

    dct = {"basketball": 5, "baseball": 9}
    dct['soccer'] = 10
    print(dct)

    dct['soccer'] = 11
    print(dct)

    print(len(dct))
    print("baseball in dct?", "baseball" in dct)

    print("baseball in dct?", "baseball" in dct.keys())

    print("10 in dct??", 10 in dct.values())
    print(dct.keys())
    print(dct.values())
    print(dct.items())

    d1 = dict(key1="value1", key2="value2")
    print(d1, type(d1))

    d2 = dict([("key1", "vlaue1"), ("key2", "value2")])
    print(d2)
    keys = ("one", "two", "three", "four")
    values = (1, 2, 3, 4)

    d3 = dict(zip(keys, values))
    print(d3, type(d3))


def using_dict():
    phones = {"홍길동": "010-1234-5678",
              "장길산": "010-9876-5432",
              "임꺽정": "010-5678-9012"}
    print(phones)
    keys = phones.keys()
    print(keys)

    lst_keys = list(keys)
    values = phones.values()
    print(values)

    items = phones.items()
    print(items)

    phones['일지매'] = "010-2345-6789"
    print(phones)
    print(phones["홍길동"])

    if "고길동" in phones:
        print(phones["고길동"])

    print(phones.get("고길동"))
    print(phones.get("고길동", "누구?"))

    del phones["홍길동"]
    print(phones)
    data = phones.pop("일지매")
    print(data)
    print(phones)

    item = phones.popitem()
    print("{} ,{}".format(item[0], item[1]))
    print(phones)

    for k in phones:
        print("key = {}-> value={}".format(k, phones.get(k)))

    print("---------------------------------------------------------------------------")
    for item in phones.items():
        print("{}->{}".format(item[0], item[1]))

    for keys, values in phones.items():
        print("{}->{}".format(keys, values))


def loop():
    print()


if __name__ == "__main__":
    # define_dict()
    using_dict()