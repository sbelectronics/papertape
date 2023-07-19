# save
stty -F /dev/ttyUSB1 raw
dd if=/dev/ttyUSB1 bs=1 of=startrek.sav

# load
dd if=startrek.sav of=/dev/ttyUSB1 bs=1

