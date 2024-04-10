import itertools


def generate_sequences_from_regex(regex, limit=5):
    sequences = ['']
    i = 0
    while i < len(regex):
        if regex[i] == '(': 
            j = i
            while regex[j] != ')':
                j += 1
            group = regex[i + 1:j].split('|')
            i = j + 1
            if i < len(regex) and regex[i] in '*+?>':
                quantifier = regex[i]
                i += 1
                if quantifier == '*':
                    group_seqs = ['']
                    for n in range(1, limit + 1):
                        for prod in itertools.product(group, repeat=n):
                            group_seqs.append(''.join(prod))
                    sequences = [s + g for s in sequences for g in group_seqs]
                elif quantifier == '+':
                    group_seqs = []
                    for n in range(1, limit + 1):
                        for prod in itertools.product(group, repeat=n):
                            group_seqs.append(''.join(prod))
                    sequences = [s + g for s in sequences for g in group_seqs]
                elif quantifier == '?':
                    group_seqs = [''] + group
                    sequences = [s + g for s in sequences for g in group_seqs]
                elif quantifier == '>':
                    x = regex[i:].find('<')
                    if x == -1:
                        raise ValueError("No matching '<' for power expression.")
                    power = int(regex[i:i + x])
                    group_seqs = [c * power for c in group]
                    sequences = [s + g for s in sequences for g in group_seqs]
                    i += x + 1
            else:
                sequences = [s + g for s in sequences for g in group]
        else:
            if i < len(regex) - 1 and regex[i + 1:i + 2] in '*+?>':
                char = regex[i]
                quantifier = regex[i + 1]
                i += 2
                if quantifier == '*':
                    sequences = [s + char * n for s in sequences for n in range(limit + 1)]
                elif quantifier == '+':
                    sequences = [s + char * n for s in sequences for n in range(1, limit + 1)]
                elif quantifier == '?':
                    sequences = [s + char * n for s in sequences for n in range(2)]
                elif quantifier == '>':
                    x = regex[i:].find('<')
                    if x == -1:
                        raise ValueError("No matching '<' for power expression.")
                    power = int(regex[i:i + x])
                    sequences = [s + char * power for s in sequences]
                    i += 2
            else:
                sequences = [s + regex[i] for s in sequences]
                i += 1
    return sequences


def describe_regex_processing(regex):
    description = []
    i = 0
    while i < len(regex):
        if regex[i] == '(':
            j = i
            while regex[j] != ')':
                j += 1
            group = regex[i + 1:j]
            description.append(f"\nProcess group '{group}'")
            i = j + 1
            if i < len(regex) and regex[i] in '*+?':
                quantifier = regex[i]
                description.append(f"with quantifier '{quantifier}'")
                i += 1
            elif i < len(regex) and regex[i] == '>':
                end_power = i + regex[i:].find('<')
                if end_power == -1 or i == len(regex) - 1:
                    raise ValueError("No matching '<' for power expression.")
                power = regex[i+1:end_power]
                description.append(f"with power quantifier repeating previous group/char {power} times")
                i = end_power + 1
        elif regex[i] in '*+?':
            description.append(f"\nProcess character '{regex[i-1]}' with quantifier '{regex[i]}'")
            i += 1
        elif regex[i] == '>':
            end_power = i + regex[i:].find('<')
            if end_power == -1 or i == len(regex) - 1:
                raise ValueError("No matching '<' for power expression.")
            power = regex[i+1:end_power]
            description.append(f"with power quantifier repeating previous char {power} times")
            i = end_power + 1
        else:
            description.append(f"\nInclude character '{regex[i]}'")
            i += 1
    return ' '.join(description)



regex = "(a|b)(c|d)E+G?"
#regex = "(P|Q|R|S)T(U|V|W|X)*Z+"
#regex = "1(0|1)*2(3|4)>5<36"
sequences = generate_sequences_from_regex(regex)
description = describe_regex_processing(regex)

print("\nFirst 10 sequences:", sequences[:10], "\n")  
print("Regex description:", description, "\n")
