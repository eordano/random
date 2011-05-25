
recorrido1 = [];
recorrido2 = [];
recorrido3 = [];

while size(recorrido1) < 30 || size(recorrido1) > 100
	recorrido1 = pasosBorracho(1, 10000);
end

while size(recorrido2) < 30 || size(recorrido2) > 100
	recorrido2 = pasosBorracho(2, 10000);
end

while size(recorrido3) < 30 || size(recorrido3) > 100
	recorrido3 = pasosBorracho(3, 10000);
end

plot(1:size(recorrido1)(2), recorrido1)
plot(recorrido2(1,:), recorrido2(2,:))
plot3(recorrido3(1,:), recorrido3(2,:), recorrido3(3,:))


