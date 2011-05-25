
f = input("Filename: ", "s");
s = load(f);
v = []

for i=1:size(s)(1)
	if s(i) != 1
		v = [v, s(i)];
	end
end

printf("De 10000, sólo %d volvieron al inicio\n", size(v)(2));
printf("Promedio de pasos necesarios: %f\n", sum(v)/size(v)(2));

bar(hist(v, [1, 5, 25, 625, 10000]))

