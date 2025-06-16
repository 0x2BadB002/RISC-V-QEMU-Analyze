import typer

from parser import parse
from analyzer import update_metrics, analyze_vectorization, analyze_space_locality, analyze_alignment, plot_spacial, plot_temporal
from domain.metrics import Metrics


def analyze(filename: str) -> None:
    f = open(filename, 'r')

    data = Metrics()
    memory_access_count = 0
    for line in f:
        cmd = parse(line)
        update_metrics(data, cmd, memory_access_count)
        if cmd.address is not None:
            memory_access_count += 1

    print("Объем векторизованных вычислений на единицу данных: ",
          analyze_vectorization(data))

    print("Пространственная локализация данных: ")
    for address, locality in analyze_space_locality(data).items():
        print(hex(address), "\t->\t", locality)

    plot_spacial(data)

    print("Временная локализация данных: ")
    for address, scarcity in data.address_scarcity.items():
        print(hex(address), "\t->\t", scarcity.mean_distance)

    plot_temporal(data)

    print("Выравнивание данных: ", analyze_alignment(data))


def run() -> None:
    typer.run(analyze)
