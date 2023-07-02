For some of the scope screencaps, I plugged D8-D15 into
some pins but didn't label them. They are:
A18 = U18-3 -- this is probably forward signal
U17 = U18=4
A16 = U18-5
A15 = U18-6
A14 = U18-7
TRIG555 = actually the output (pin3) of the 555, not the trigger

U18-3 will cause tape to move forward
U18-4 may (unverified) cause tape to move backward

U18-3 is observed to always deassert on a 0->1 transition of the 555 output

U6-12 precedes U18-3
U17-8,10 precedes U18-3

