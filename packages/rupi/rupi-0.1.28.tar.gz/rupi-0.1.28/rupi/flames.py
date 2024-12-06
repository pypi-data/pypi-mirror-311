def flames(name1=None, name2=None):
    """
    Play the FLAMES game. The function can work in two ways:
    1. flames(): Prompts the user for input.
    2. flames(name1, name2): Calculates the FLAMES result directly based on the provided names.

    Args:
        name1 (str): First name (optional).
        name2 (str): Second name (optional).

    Returns:
        str: Result of the FLAMES game or an error message if restricted names are used.
    """
    restricted_names = ["tanujairam", "rupali"]

    # Prompt for input if names are not provided
    if not name1 or not name2:
        print("Welcome to the FLAMES game!")
        name1 = input("Enter the first name: ").strip().lower()
        name2 = input("Enter the second name: ").strip().lower()

    # Check for restricted names
    if name1 in restricted_names or name2 in restricted_names:
        print("Sorry, FLAMES cannot be played with one of the names.LOL.")
        return "Restricted Name Error"

    # Remove common characters between names
    def remove_common_chars(n1, n2):
        n1_list, n2_list = list(n1), list(n2)
        for char in n1:
            if char in n2_list:
                n1_list.remove(char)
                n2_list.remove(char)
        return n1_list + n2_list

    # Calculate the FLAMES result
    combined = remove_common_chars(name1, name2)
    count = len(combined)

    if count == 0:
        return "No relationship, as names cancel each other out!"

    flames_dict = {
        0: "Friends",
        1: "Love",
        2: "Affection",
        3: "Marriage",
        4: "Enemies",
        5: "Siblings",
    }
    flames_list = ["F", "L", "A", "M", "E", "S"]

    while len(flames_list) > 1:
        index = (count % len(flames_list)) - 1
        if index >= 0:
            flames_list = flames_list[index + 1 :] + flames_list[:index]
        else:
            flames_list = flames_list[: len(flames_list) - 1]

    result = flames_dict[flames_list.index(flames_list[0])]

    print(f"The relationship between {name1.capitalize()} and {name2.capitalize()} is: {result}.")
    return result
