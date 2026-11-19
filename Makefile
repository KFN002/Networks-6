topo: topology.py
	mn --custom topology.py --topo tutorialTopology --controller none --mac --switch lxbr --link tc

clean:
	mn -c
