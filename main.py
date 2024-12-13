from back import get_user_input, build_graph, bellman_ford

print("Currency Arbitrage Detection System using Bellman Ford Anant Singh open Ended")

num_currencies, currencies, exchange_rates = get_user_input()


graph = build_graph(num_currencies, exchange_rates)

print("\nChecking for arbitrage opportunities from all starting points...")
arbitrage_found = False
for src in range(num_currencies):
    if bellman_ford(graph, num_currencies, src, currencies, exchange_rates):
        arbitrage_found = True
        break

if not arbitrage_found:
    print("\nNo profitable arbitrage opportunities exist in this market.")


