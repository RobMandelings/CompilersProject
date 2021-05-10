# LLVM TO MIPS

## Registers

Bijhouden welke registers in gebruik zijn

### Priorities voor het gebruiken van registers

expressions: $t > $s > memory<br>
arguments: $a > memory<br>
return values: $v > memory<br>

### Registers class

Misschien handig om registers op te vragen voor de juiste zaken (bvb $v0, $a, $s,...)

STACK POINTER FRAME POINTER

## MIPS Function class

Inladen van een variable -> in $s registers geplaatst. Expressie uitrekenen die daarna gewoon gebruikt wordt -> $t
registers

### Zullen we ook werken met aparte MIPSInstruction classes?

### Steps

#### 1. Symbol table opbouwen

Symbol table bestaat uit informatie van functions (ids) met daarin basic blocks (ids)
die instructies (ids) bijhouden met liveness en usage information van variables (algoritme uit slides)

Per functie kun je de gebruikte $s registers opvragen zodat je deze kan opslaan in het geheugen en terug restoren als
het niet meer nodig is. Elke functie begint zonder enige $s registers te gebruiken, maar alle $s worden wel bezien als
vrij in het begin. Nadat de instructies zijn omgezet weten we welke $s registers gebruikt worden, dus kunnen we aan de
initializatie van een mips functie ook deze registers storen wat automatisch kan gebeuren.

#### Register and Address descriptors

Descriptor: mapt id(LLVMRegister) op register of address

Stel assignment of (copy): x = y + z. x wordt in $s0 geplaatst.<br>
Dan moet x in de register descriptor geplaatst worden op $0.<br>
Bij ons zal de descriptor geen variabele naam mappen op een address of register<br>
maar een LLVMRegister mappen op een mips register of adres waarin dit momenteel steekt<br>
(want de namen van de variabelen zijn we kwijt na conversie van llvm).

Over alle functies loopen en alle basic blocks.

Opvragen van een bepaalde locatie:

#### GetRegisterForVariable

Haalt voor jou een register op uit MIPS om mee te werken, zodat je je geen zorgen hoeft te maken over het inladen van
een variabele uit een bepaalde memory locatie. Je kan dan gewoon deze functie gebruiken en werken met het MIPS register
alsof het al in de register descriptor zat, terwijl achterliggend misschien eerst een load word instructie toegevoegd
is.

#### LLVMVariableRegister

Register dat ook ineens een variable name bijhoudt voor het makkelijker te maken. Handig?

we kunnen een functie implementeren die eerst gaat kijken in de register descriptor om te kijken of een bepaalde
LLVMRegister zich bevindt in een register

#### getFreeRegister

getFreeReg functie implementeren: geeft vrij register terug op basis van algoritme uit de slides

### Stack pointer and frame pointer

Bij het begin van een functie stack verlagen voor het aantal gebruikte s registers

Stel bij grote expressies en berekeningen: <br>
spill into memory, stack pointer beetje verlagen (benodigde hoeveelheid)<br>
en de current offset opslaan in address descriptor. Current offset verhogen met benodigde hoeveelheid

### Implement a visitor for the instructions to generate mips code accordingly

### Converteren van specifieke instructies

#### Expressies

In llvm wordt elke berekening geplaatst in een nieuw register.<br>
Bij MIPS kan dit niet, dus moeten we gebruik maken van de <i>getRegister</i>
functie die ons een vrij register toekent om de uitkomst in te plaatsen.<br>
<i>getRegister</i> zal ook ineens 'spillen' into memory als dit nodig is om een register vrij te maken Als het een
werkelijke assignment was op het einde, vindt er zich een store plaats.<br>
We kunnen dan gewoon kijken in de register descriptor tabel om het juiste huidige register in MIPS overeenkomend met
het 'register to store' uit LLVM.

#### Storen van een nieuwe waarde in een bepaalde variabele

In llvm moet je steeds een store instruction gebruiken om in een variabele een nieuwe waaarde te steken,<br>
En een load om de waarde uit een variabele te halen. Hoe zetten we deze instructies om naar mips?

e.g. store i32 %5, i32* %1, align 4 e.g.<br>
e.g %7 = load i32, i32* %1, align 4<br>

Volgens mij moet dit gewoon vertaald worden naar de overeenkomstige store word en load word instructies.<br>
Als je een berekende waarde hebt om vervolgens in een variabele te plaatsen,<br>
moet je enkel weten met welk register de huidige waarde om te storen overeenkomt (bvb hier %5)<br>
en je gaat dit register gebruiken om te plaatsen in de juiste <i>Address descriptor</i>