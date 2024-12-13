import math

def bellman_ford(graph, num_vertices, src, currencies, exchange_rates, epsilon=1e-8):
    distance = [float('inf')] * num_vertices
    predecessor = [None] * num_vertices
    distance[src] = 0

    for i in range(num_vertices - 1):
        for u in range(num_vertices):
            for v, weight in graph[u]:
                if distance[u] != float('inf') and distance[u] + weight < distance[v] - epsilon:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u

    for u in range(num_vertices):
        for v, weight in graph[u]:
            if distance[u] != float('inf') and distance[u] + weight < distance[v] - epsilon:
                visited = set()
                current = v
                cycle = []

                while current not in visited:
                    visited.add(current)
                    cycle.append(current)
                    current = predecessor[current]


                cycle_start = cycle.index(current)
                arbitrage_cycle = cycle[cycle_start:]
                arbitrage_cycle.append(arbitrage_cycle[0])  

                profit = calculate_profit(arbitrage_cycle, exchange_rates)
                
                if profit > 1.0: 
                    print("\nThe following would be the profit: \n")
                    print("Path:", ' -> '.join(currencies[i] for i in arbitrage_cycle))
                    print(f"Profit multiplier: {profit:.4f}x")
                    print(f"Profit percentage: {(profit-1)*100:.2f}%")
                    return True
                else:
                    print("\nNo profitable arbitrage opportunities detected.")
                    return False

def calculate_profit(cycle, exchange_rates):
    profit = 1.0
    for i in range(len(cycle)-1):
        profit *= exchange_rates[cycle[i]][cycle[i+1]]
    return profit

def build_graph(num_currencies, exchange_rates):
    graph = []
    for u in range(num_currencies):
        edges = []
        for v in range(num_currencies):
            if u != v:
                rate = exchange_rates[u][v]

                if rate > 0:
                    weight = -math.log(rate)
                    edges.append((v, weight))
        graph.append(edges)
    return graph

def validate_exchange_rate(rate_str):
    try:
        rate = float(rate_str)
        if rate <= 0:
            print("Exchange rate must be positive!")
            return None
        return rate
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return None

def get_user_input():
    while True:
        try:
            num_currencies = int(input("Enter the number of currencies: "))
            if num_currencies < 2:
                print("Need at least 2 currencies!")
                continue
            break
        except ValueError:
            print("Please enter a valid number!")

    currencies = []


    for i in range(num_currencies):
        while True:
            currency = input(f"Enter the name of currency {i + 1}: ").strip().upper()
            if currency and currency not in currencies:
                currencies.append(currency)
                break
            print("Currency name must be unique and non-empty!")

    exchange_rates = []
    print("\nEnter the exchange rates matrix:")
    for i in range(num_currencies):
        row = []
        for j in range(num_currencies):
            if i != j:
                while True:
                    rate_str = input(f"Enter the exchange rate from {currencies[i]} to {currencies[j]}: ")
                    rate = validate_exchange_rate(rate_str)
                    if rate is not None:
                        row.append(rate)
                        break
            else:
                row.append(1.0)  
        exchange_rates.append(row)

    return num_currencies, currencies, exchange_rates

