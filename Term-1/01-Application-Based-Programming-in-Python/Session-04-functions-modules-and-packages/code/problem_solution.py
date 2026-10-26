"""Real-life problem: print a nested website menu recursively and count links."""

menu = {
    "Home": None,
    "Programs": {"Diploma in AI": None, "Short Courses": {"Python": None, "Power BI": None}},
    "Admissions": {"Apply": None, "Fee Structure": None},
}


def print_menu(tree, depth=0):
    count = 0
    for title, children in tree.items():
        print("  " * depth + ("[+] " if children else " -  ") + title)
        count += 1 if children is None else print_menu(children, depth + 1)
    return count


if __name__ == "__main__":
    links = print_menu(menu)
    print("Total links:", links)
    assert links == 6
