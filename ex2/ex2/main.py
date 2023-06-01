from dummy_impl import DummyImpl
from genetic_algorithm import GAMetrics, GAParams
from impl import Impl
from runner import run_algorithm


def paint_avg_fitness(plt, metrics: GAMetrics):
    import numpy as np

    ypoints = np.array(metrics.avg_fitness)
    y2points = np.array(metrics.avg_topn_fitness)
    y3points = np.array(metrics.avg_botn_fitness)
    y4points = np.array(metrics.best_fitness)

    plt.plot(ypoints, linestyle="dotted", label="avg_fitness")
    plt.plot(y2points, linestyle="dotted", label="avg_topn_fitness")
    plt.plot(y3points, linestyle="dotted", label="avg_botn_fitness")
    plt.plot(y4points, linestyle="dotted", label="best_fitness")
    plt.legend()


def paint_inds_metrics(plt, metrics: GAMetrics):
    import numpy as np

    y4points = np.array(metrics.diff_inds)
    plt.plot(y4points, linestyle="dotted", label="diff_inds")
    plt.legend()


def paint_metrics(metrics: GAMetrics):
    try:
        import matplotlib.pyplot as plt
    except:
        return

    fig, (ax1, ax2) = plt.subplots(2, 1)

    paint_avg_fitness(ax1, metrics)
    paint_inds_metrics(ax2, metrics)
    plt.show()


def main():
    params = GAParams(
        pop_size_init=100, pop_size_max=50, mutation_prob=0.8, crossover_prob=0.1
    )
    impl = Impl(1.0, 0.1, ciphertexts=[open("enc.txt", "r").read()])
    # params = GAParams(
    #     pop_size_init=300, pop_size_max=50, mutation_prob=0.5, crossover_prob=0.2
    # )
    # impl = DummyImpl(50)
    try:
        solution = run_algorithm(impl, params)
        print(f"solution={solution}")
    except KeyboardInterrupt:
        print("stopping...")
    print(f"calls_to_fitness={impl.metrics.fitness_calls}")
    paint_metrics(impl.metrics)


if __name__ == "__main__":
    main()
