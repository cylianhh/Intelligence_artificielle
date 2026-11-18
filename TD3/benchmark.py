
from algorithms import minimax, alphabeta, mcts
from game import create_board
import matplotlib.pyplot as plt

def benchmark(board, algorithm, **kwargs):
    algorithms = {
        "minimax": minimax,
        "alphabeta": alphabeta,
        "mcts": mcts
    }

    if isinstance(algorithm, str):
        name = algorithm.lower()
        if name not in algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        function = algorithms[name]
    else:
        function = algorithm
        name = function.__name__

    result = function(board, **kwargs)

    return {
        "algorithm": name,
        "move": result["move"],
        "score": result["score"],
        "nodes_explored": result["nodes_explored"],
        "time": result["time"]
    }


def run_all_benchmarks():
    board = create_board()
    results = []

    # Minimax et Alpha-Beta
    for depth in range(1, 6):
        results.append({"configuration": f"Depth {depth}", **benchmark(board, "minimax", depth=depth)})

        results.append({"configuration": f"Depth {depth}", **benchmark(board, "alphabeta", depth=depth)})

    # MCTS
    for simulations in [100, 500, 1000, 2000]:
        results.append({"configuration": f"{simulations} simulations", **benchmark(board, "mcts", num_simulations=simulations, seed=42)})

    return results


def display_results(results):
    print(
        f"{'Algorithm':<12} "
        f"{'Configuration':<20} "
        f"{'Move':<8} "
        f"{'Nodes':<10} "
        f"{'Time (s)':<12}"
    )

    print("-" * 65)

    for result in results:
        print(
            f"{result['algorithm']:<12} "
            f"{result['configuration']:<20} "
            f"{str(result['move']):<8} "
            f"{result['nodes_explored']:<10} "
            f"{result['time']:<12.6f}"
        )


def plot_results(results):

    # Graphique 1 : Minimax vs Alpha-Beta
    minimax_results = [
        r for r in results if r["algorithm"] == "minimax"
    ]

    alphabeta_results = [
        r for r in results if r["algorithm"] == "alphabeta"
    ]

    depths = range(1, 6)

    plt.figure()
    plt.plot(depths, [r["nodes_explored"] for r in minimax_results], marker="o", label="Minimax")
    plt.plot(depths, [r["nodes_explored"] for r in alphabeta_results], marker="o",label="Alpha-Beta")

    plt.xlabel("Search depth")
    plt.ylabel("Number of explored nodes")
    plt.title("Minimax vs Alpha-Beta")
    plt.legend()
    plt.grid()
    plt.savefig("nodes_comparison.png")
    plt.show()

    # Graphique 2 : temps d'exécution MCTS
    mcts_results = [r for r in results if r["algorithm"] == "mcts"]

    simulations = [100, 500, 1000, 2000]

    plt.figure()
    plt.plot(simulations, [r["time"] for r in mcts_results], marker="o", label="MCTS")

    plt.xlabel("Number of simulations")
    plt.ylabel("Execution time (seconds)")
    plt.title("MCTS execution time")
    plt.legend()
    plt.grid()
    plt.savefig("mcts_execution_time.png")
    plt.show()

if __name__ == "__main__":
    results = run_all_benchmarks()
    display_results(results)
    plot_results(results)