# LLVM TO MIPS

## Registers

Bijhouden welke registers in gebruik zijn

### Priorities voor het gebruiken van registers

expressions: $t > $s > memory<br>
arguments: $a > memory<br>
return values: $v > memory<br>

### Steps

#### Symbol table opbouwen

Symbol table bestaat uit informatie van functions (ids) met daarin basic blocks (ids)
die instructies (ids) bijhouden met liveness en usage information van variables (algoritme uit slides)

Per functie kun je de gebruikte $s registers opvragen zodat je deze kan opslaan in het geheugen en terug restoren als
het niet meer nodig is

#### Register and address descriptors

Descriptor: mapt variable name op register of address

Stel assignment of (copy): x = y + z. x wordt in $s0 geplaatst.<br>
Dan moet x in de register descriptor geplaatst worden op $0.

Over alle functies loopen en alle basic blocks

getReg functie implementeren: geeft vrij register terug op basis van algoritme uit de slides

### Stack pointer and frame pointer

Bij het begin van een functie stack verlagen voor het aantal gebruikte s registers

Stel bij grote expressies en berekeningen: <br>
spill into memory, stack pointer beetje verlagen (benodigde hoeveelheid)<br>
en de current offset opslaan in address descriptor. Current offset verhogen met benodigde hoeveelheid

### Implement a visitor for the instructions to generate mips code accordingly