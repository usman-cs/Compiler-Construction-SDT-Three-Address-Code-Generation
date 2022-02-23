import string
identifierNfa=[['-', 'A-Z,a-z,_'], ['-', '0-9,a-z,A-Z,_']]
numbersNfa=[['-', '$', '0-9'], ['-', '0-9', '.'], ['-', '-', '0-9']]
stringNfa=[['-', '"', '-', '-'], ['-', '-', '$', '-'], ['-', '-', 'all', '"'], ['-', '-', '-', '-']]
operator=['+' , '-', '*', '=', '==', '<=', '>=', '<', '>','/']
keywords=['asm',	'double',	'new',	'switch',
'auto',	'else',	'operator',	'template',
'break',	'enum',	'private',	'this',
'case',	'extern',	'protected'	,'throw',
'catch',	'float'	,'public',	'try',
'char',	'for',	'register','typedef',
'class',	'friend',	'return',	'union',
'const',	'goto'	,'short'	,'unsigned',
'continue'	,'if',	'signed',	'virtual',
'default'	,'inline',	'sizedof',	'void',
'delete',	'int'	,'static',	'volatile' ,
'do'	,'long'	,'struct',	'while' ]
saperators=[';', ')', '[', ']', ',', '(', '^', '}', '{']

'''-----------------------------------------Lexical Analyzer or Tokenization Part----------------------------------------'''

'''-------------------------------------------------Tested On Following Input--------------------------------------------'''
'''
{
    x = a + b * c + d ;
    return 0 ;
    1hello
}'''
try:
    src=[i.strip().split(' ') for i in open('src.txt','r').readlines() if i.strip()!=''] # Tokens Must be Saperated by Space
except:
    src=[['{'], ['x', '=', 'a', '+', 'b', '*', 'c', '+', 'd', ';'], ['return', '0', ';'], ['1hello'], ['}']]
'''-----------------------------------------------Nfa Code-----------------------------------------------------------'''
def identifier(lexeme):
    global identifierNfa
    file=identifierNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='0-9,a-z,A-Z,_':
                s=set()
                s.update(string.ascii_lowercase)
                s.update(string.ascii_uppercase)
                s.update({str(x) for x in range(0,10)})
                s.update('_')
                file[pos][p]=s
            elif v=='A-Z,a-z,_':
                s=set()
                s.update(string.ascii_lowercase)
                s.update(string.ascii_uppercase)
                s.update('_')
                file[pos][p]=s
    final_state=1
    state={0}
    for inp in lexeme:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if (val==inp or (type(val)==set and (inp in val))) and (val!='-'):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state) and len(lexeme)<31 and (lexeme not in keywords):
        return 1
    else:
        return 0

def numbers(lexeme):
    global numbersNfa
    file=numbersNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='0-9':
                s=set()
                s.update({str(x) for x in range(0,10)})
                file[pos][p]=s
    if lexeme[0]=='.':
        lexeme='0'+lexeme
    final_state=2
    state={0}
    for inp in lexeme:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if (val==inp or (type(val)==set and (inp in val)) or (val=="$")):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state) :
        return 1
    else:
        return 0

def strings(input):
    global stringNfa
    file=stringNfa
    for pos,val in enumerate(file):
        for p,v in enumerate(val):
            if v=='all':
                s=set()
                s.update(string.ascii_letters+string.punctuation)
                s.update({str(x) for x in range(0,10)})
                file[pos][p]=s
    final_state=3
    state={0}
    for inp in input:
        empty_set=set() 
        for ter in state:
            for pos,val in enumerate(file[ter]):
                if val==inp or (type(val)==set and (inp in val) or (val=="$")):
                    empty_set.add(pos)
            state=empty_set
                                
    if (final_state in state):
        return 1
    else:
        return 0

userInput=[]
print('\nToken Type\t\t','Value\n')
for k,i in enumerate(src):
    if i[0]=='//':
        print('Comment: \t\t',*i)
        continue
    for k1,j in enumerate(i):
        if j[0]=='#':
            print('Preprocessor Directive: ',j)
        elif identifier(j):
            print('Identifier: \t\t',j)
            userInput.append(j)
        elif numbers(j):
            print('Constant Or Float: \t',j)
        elif strings(j):
            print('Strings: \t\t',j)
        elif j in operator:
            print('Operator: \t\t',j)
            userInput.append(j)
        elif j in saperators:
            print('Saperator: \t\t',j)
        elif j in keywords:
            print('Keyword: \t\t',j)
        else:
            print('Invalid Token: \t\t',j)
print('-------------------------------------------Parser Input-------------------------------------')
print(userInput)
# terminalSymbolsGrammar=input("Enter Terminal Symbols space Saperated: ").split() # Terminal Symbols in grammar
# NonterminalSymbolsGrammar=input("Enter Non Terminal Symbols space Saperated: ").split() # Non Terminal Symbols in grammar
terminalSymbolsGrammar=['=', '+', '*', 'id']
nonTerminalSymbolsGrammar=['S','E','T','F']
userInputWithoutIndentifiers=['id' if i not in ['=','+','*'] else i for i in userInput] # replace every identifer with 'id'
stack=['0']
userInputWithoutIndentifiers.append('$')
pointerToUserInput=0
try:
    table=[i.strip().split('\t') for i in open('table.txt','r')]
except:
    table=[['" "', 'id', '=', '+', '*', '$', 'S', 'E', 'T', 'F'],
['0', 's1', '-', '-', '-', '-', '-', '-', '-', '-'],
['1', '-', 's2', '-', '-', '-', '-', '-', '-', '-'],
['2', 's6', '-', '-', '-', '-', '-', '3', '4', '5'],
['3', '-', '-', 's7', '-', 'accept', '-', '-', '-', '-'],
['4', '-', '-', 'r2', 's8', 'r2', '-', '-', '-', '-'],
['5', '-', '-', 'r4', 'r4', 'r4', '-', '-', '-', '-'],
['6', '-', '-', 'r5', 'r5', 'r5', '-', '-', '-', '-'],
['7', 's6', '-', '-', '-', '-', '-', '-', '9', '5'],
['8', 's6', '-', '-', '-', '-', '-', '-', '-', '10'],
['9', '-', '-', 'r1', 's8', 'r1', '-', '-', '-', '-'],
['10', '-', '-', 'r3', 'r3', 'r3', '-', '-', '-', '-']]
print('----------------------------------------------Grammar Table------------------------------------------------')
[print(i) for i in table] # printing table
try:
    grammar=[i.strip() for i in open('grammar.txt','r')]
except:
    grammar=['S->id=E', 'E->E+T', 'E->T', 'T->T*F', 'T->F', 'F->id']
print('----------------------------------------------Grammar------------------------------------------------')
print(grammar)
rules={}
indexesForId=[i for i,j in enumerate(userInputWithoutIndentifiers) if j=='id'][1:];identiferPointer=0;threeAddressCode=[];variables=0
while True:
    row=int(stack[-1])+1 # Plus one because in talbe zero row is for terminal and non terminals
    col= ([i for i,j in enumerate(table[0][1:]) if j==userInputWithoutIndentifiers[pointerToUserInput]][0])+1 #plus one      because zero column is for row indexing
    operationToPerform=table[row][col]
    if operationToPerform[0]=='s':  # means shift operation
        print('--------------------Shift operation Perform---------------')
        print('Stack Before Shift: ',stack)
        print('Input Before Shift: ',userInputWithoutIndentifiers[pointerToUserInput:])
        print('row: ',row-1,'col: ',col-1)
        stack.append(userInputWithoutIndentifiers[pointerToUserInput]) # shift input to stack
        pointerToUserInput+=1 # pointer increment because we shift the current input to stack
        stack.append(operationToPerform[1]) # append the number with shift
        print('Operation Perfomed: ',table[row][col])
        print('Stack After Shift: ',stack)
        print('Input After Shift: ',userInputWithoutIndentifiers[pointerToUserInput:])

    elif operationToPerform[0]=='r': # means reductiton operation
        print('--------------------Reduce operation Perform---------------')
        print('Stack Before Reduce: ',stack)
        print('Input Before Reduce: ',userInputWithoutIndentifiers[pointerToUserInput:])
        print('row: ',row-1,'col: ',col-1)
        print('Operation Perfomed: ',table[row][col])
        production=grammar[int(operationToPerform[1])] # remember grammar prodcution numbering starts with 0
        print('Reduced Production: ',production)
        temp='';calculateTerminalOrNonTerminal=[] # logic to handle terminal sysmbol with length more than one
        for i in production[3:]:
            if i in nonTerminalSymbolsGrammar:
                calculateTerminalOrNonTerminal.append(i)
            elif i not in terminalSymbolsGrammar and i not in nonTerminalSymbolsGrammar:
                temp+=i
                if temp in terminalSymbolsGrammar:
                    calculateTerminalOrNonTerminal.append(temp)
                    temp=''
            else:
                calculateTerminalOrNonTerminal.append(i)
        pop=len(calculateTerminalOrNonTerminal)*2 # pop to pop from stack
        print('POP from stack: ',pop)
        for i in range(pop):
            stack.pop()
        stack.append(production[0]) # append left of prodcution in stack
        row=int(stack[-2])+1 # Plus one because in talbe zero row is for terminal and non terminals
        col= ([i for i,j in enumerate(table[0][1:]) if j==stack[-1]][0])+1 #plus one because zero column is for row indexing
        if table[row][col]=='-':
            print('error')
            break
        stack.append(table[row][col])
        print('Stack After Reduce: ',stack)
        print('Input After Reduce: ',userInputWithoutIndentifiers[pointerToUserInput:])
        if production=='F->id':
            rules['F.place']=str(userInput[indexesForId[identiferPointer]])
            print('Rule: ','F = ',userInput[indexesForId[identiferPointer]])
            identiferPointer+=1
        elif production=='T->F':
            rules['T.place']=rules['F.place']
            print('Rule: ','T = ',rules['F.place'])
        elif production=='T->T*F':
            genratedVar='T'+str(variables)
            variables+=1
            threeAddressCode.append(genratedVar+'='+rules['T.place']+'*'+rules['F.place'])
            rules['T.place']=rules['T.place']+'*'+rules['F.place']
            rules['T.place']=genratedVar 
        elif production=='E->T':
            rules['E.place']=rules['T.place']
            print('Rule: ','E = ',rules['T.place'])
        elif production=='E->E+T':
            genratedVar='T'+str(variables)
            variables+=1
            threeAddressCode.append(genratedVar+'='+rules['E.place']+'+'+rules['T.place'])
            rules['E.place']=rules['E.place']+"+"+rules['T.place']
            rules['E.place']=genratedVar
    elif operationToPerform=='-':
        print('error')
        break
    elif operationToPerform=='accept':
        print('Sucess')
        break
print('-------------------------------------------Three Address Code-------------------------------')
for i in threeAddressCode:
    print(i)