def transiter(T, a):
	F = list()
	for t in T:
		trans = t.getTransition(a)
		if (len(trans) > 0):
			for p in trans:
				if p.e not in F:
					F.append(p.e)
	return F

