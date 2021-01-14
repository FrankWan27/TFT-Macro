from TFTMacro import TFTMacro

tft = TFTMacro()

while True:
	output = tft.doCommand(input('>'))
	print(output, flush=True)