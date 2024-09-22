COUNTER = 0

def delimiter():
    global COUNTER
    COUNTER += 1
    print()
    print('-' * 10)
    print(f'-- {COUNTER} task --')
    print('-' * 10)
    print()
