from beliefBase import BeliefBase

bb = BeliefBase()

while(True):
    print("")
    print("Press '1' to enter a formula")
    print("Press '2' to check logical entailment")
    print("Press '3' to do belief revision")
    print("Press '4' to print current belief base ")
    print("Press '5' to exit")
    caseswitch = input()

    if caseswitch == '1':
        print("a = AND, o = OR, n = NOT, i = imply, f = if and only if")
        print("Enter a formula, e.g. PiQ")
        formula = input()
        bb.add(formula)
        
        while True:
            print("press ENTER to add another formula or x to exit")
            caseswitch1 = input()
            if caseswitch1 == "":
                print("Enter a formula, e.g. PiQ")
                formula = input()
                bb.add(formula)
            elif caseswitch1 == 'x':
                break

    elif caseswitch == '2':
        print("Enter a formula, e.g. PiQ")
        formula = input()
        print(bb.CheckEntailment(formula))


    elif caseswitch == '3':
        print("Enter a formula, e.g. PiQ")
        formula = input()
        bb.revision(formula)

    elif caseswitch == '4':
        bb.printBeliefBase()

    elif caseswitch == '5':
        break
    else:
        print("not a valid number")

