import re
import itertools

regex_letters = "A-ZĄĘĆŃÓŻŹŁŚ"
all_digits = list(map(lambda x: int(x), set("0123456789")))


def to_number_eval(word):
    eval_num_str = ""
    for i in range(0, len(word)):
        eval_num_str += word[i] + "*" + str(10 ** (len(word) - i - 1))
        if i != len(word) - 1:
            eval_num_str += "+"
    return eval_num_str


def get_span(match: re.match):
    return match.span()


def expanded_condition(condition: str):
    matches = re.finditer(f"[{regex_letters}]" + "{2,}", condition)
    condition_temp = list(condition)
    additional_conditions = ""
    matches = sorted(matches, key=get_span, reverse=True)
    for match in matches:
        span = match.span()
        additional_conditions += f" and {condition[span[0]]} != 0"
        condition_temp[span[0]:span[1]] = list(f"({to_number_eval(condition_temp[span[0]:span[1]])})")
    return "".join(condition_temp) + additional_conditions


def build_permutations(letters: dict):
    return list(
        filter(lambda arr: len(arr) == len(set(arr)) and arr[0] != 0, list(itertools.product(*letters.values()))))


def is_compliant(n, scheme):
    return len(str(n)) == len(set(scheme))


def possible_from_condition(condition):
    possible_permutations = []
    variables = list(set(re.findall(f"[{regex_letters}]", condition)))
    permutations = list(
        itertools.product(*list(map(lambda var: all_digits, variables))))
    permutations = list(map(lambda _permutation: dict(zip(variables, _permutation)),
                            list(filter(lambda arr: len(arr) == len(set(arr)), permutations))))
    for permutation in permutations:
        for letter, value in permutation.items():
            locals()[letter] = value
        if eval(condition):
            possible_permutations.append(permutation)
    return possible_permutations


def solve(n_arr, operator, w, conditions):
    base_condition = expanded_condition(f"{operator.join(n_arr)}=={w}")
    conditions_merged = " and ".join(list(map(lambda condition: expanded_condition(condition), conditions)))
    conditional_permutations = possible_from_condition(conditions_merged)

    for conditional_permutation in conditional_permutations:
        remaining_digits = [digit for digit in all_digits if digit not in conditional_permutation.values()]
        remaining_letters = [letter for letter in set("".join(n_arr) + w) if
                             letter not in conditional_permutation.keys()]
        permutations = list(
            itertools.product(*list(map(lambda var: remaining_digits, remaining_letters))))
        permutations = list(map(lambda _permutation: dict(zip(remaining_letters, _permutation)),
                                list(filter(lambda arr: len(arr) == len(set(arr)), permutations))))
        for permutation in permutations:
            for letter, value in (permutation | conditional_permutation).items():
                locals()[letter] = value
            if eval(base_condition):
                n_arr_res = n_arr
                for letter, value in (permutation | conditional_permutation).items():
                    for i in range(0, len(n_arr)):
                        n_arr_res[i] = n_arr[i].replace(letter, str(value))
                    w = w.replace(letter, str(value))
                return n_arr, w
    return None


if __name__ == '__main__':
    equation = str.upper(input("Equation: ")).split("=")
    n_arr = re.findall(f"[{regex_letters}]+", equation[0])
    operator = equation[0][re.search("[+-/*]", equation[0]).span()[0]]
    w = equation[1]
    conditions = []
    while True:
        condition = str.upper(input("Condition:"))
        if "==" not in condition:
            break
        else:
            conditions.append(condition)
    print(solve(n_arr, operator, w, conditions))
