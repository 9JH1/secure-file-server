with open('test.key','r') as a:
    print(f"server password: {a.readlines(1)[0]}")
