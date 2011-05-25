function M = pasosBorracho(dim, maxPasos)

	M = zeros(dim, 1);
	llego = 0;

	for i = 1:maxPasos
		pos_anterior = M(:,end);
		direccion = floor(rand() * dim)+1;

		delta = 1;
		if rand() < 0.5
			delta = -1;
		endif
		pos_anterior(direccion) += delta;

		M = [M, pos_anterior];

		if pos_anterior == zeros(dim, 1)
			llego = 1;
			break;
		endif
	endfor

	if (llego == 0)
		M = zeros(dim, 1);
	endif

