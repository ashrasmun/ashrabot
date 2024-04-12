import re

def trim(name: str):
    match = re.search(r"[-\d]", name)
    return name[:match.start()] if match else name


print(trim('abc'))
print(trim('abc-'))
print(trim('abc1234'))
print(trim('abc-1234'))
