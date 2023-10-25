number = int(input())


def recursive_increment(n: int) -> str:
    result = ''
    for num in range(n + 1):
        result += str(num) * num
    return result


print(recursive_increment(number))
