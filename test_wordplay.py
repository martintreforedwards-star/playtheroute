from builder.wordplay import load_dictionary
from builder.wordplay import analyse_station

dictionary = load_dictionary()

print(analyse_station("Blackhorse Road", dictionary))
print(analyse_station("Inverkeithing", dictionary))
print(analyse_station("New Barnet", dictionary))
print(analyse_station("Three Bridges", dictionary))