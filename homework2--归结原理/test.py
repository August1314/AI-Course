def check(first, second):
    for i in first:
        for j in second:
            if i.startswith('~'):
                pass
            if j.startswith('~'):
                pass
def ResolutionProp(KB):
    stack = []
    for i in KB:
        print(i)
    pass

    for i in KB:
        stack.append(i)
    
    while len(stack) > 1:
        first = stack.pop()
        second = stack.pop()
        end = check(first, second)
        if end != ():
            stack.append(end)
        pass
        



KB = {('FirstGrade',), ('~FirstGrade', 'Child'), ('~Child',)}
ResolutionProp(KB)

