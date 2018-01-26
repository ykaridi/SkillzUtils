import csv


def setAttribute(driver, element, att, v):
    driver.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);",
                          element, att, v)


def to_csv(path, arr, attributes):
    with open(path, "w") as f:
        wr = csv.writer(f, delimiter=",")
        wr.writerow(attributes.keys())
        for elem in arr:
            wr.writerow([getattr(elem, "get_" + x)() if attributes[x] is None else attributes[x](elem) for x in attributes])