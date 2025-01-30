with open('test.key','r') as a:
    print(f"server password: {a.readlines(1)[0]}")
    print(f"file password: {a.readlines(2)[0]}")