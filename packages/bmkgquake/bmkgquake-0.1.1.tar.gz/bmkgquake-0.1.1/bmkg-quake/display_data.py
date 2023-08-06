def display_data(data):
    print("Latest Earthquake Information in Indonesia")
    # To handle error/empty data
    if data is None:
        print("Can't find the latest earthquake data")
        return
    for key, value in data.items():
        if type(value) == dict:
            print(f"    {key}:")
            for x, y in value.items():
                print(f"        {x}: {y}")
        else:
            print(f"    {key}: {value}")