import argparse
import time
import random
import string
from string_set import StringSet


def generate_random_string():
    length = random.randint(6, 15)
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_input():
    n = random.randint(100, 10**3)
    used_strings = []
    result = []
    for _ in range(n):
        action = random.choice(["+", "-", "?"])
        use_existing = used_strings and random.random() >= 0.5
        word = ""
        if use_existing:
            word = random.choice(used_strings)
        else:
            word = generate_random_string()
            used_strings.append(word)
        result.append(f"{action} {word}\n")

    filename = f"generated_input_{int(time.time())}.in"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(result)
        f.write("#\n")
    return filename


def main():
    string_set = StringSet()

    def handle_command(command: str):
        [action, word] = command.split()
        if action == "+":
            string_set.add(word)
        elif action == "-":
            string_set.remove(word)
        elif action == "?":
            print("yes" if word in string_set else "no")
        elif action == "*":
            if word == "group":
                print(string_set.get_groups())
            elif word == "z":
                print(string_set.get_z_functions())

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if args.generate:
        filename = generate_input()
        print(f"generated input in {filename}")
        return

    if args.file:
        filename = args.file
        with open(filename, "r", encoding="utf-8") as f:
            for command in f:
                if command.strip() == "#":
                    return
                handle_command(command)
        return

    while True:
        try:
            command = input()
            if command == "#":
                break
            handle_command(command)
        except (EOFError, KeyboardInterrupt):
            break
        except ValueError:
            print("invalid command")


if __name__ == "__main__":
    main()
