import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from domain.metrics import Metrics, Scarcity
from domain.command import Command

matplotlib.use('Agg')


def update_metrics(data: Metrics, cmd: Command, offset: int):
    if cmd.command.lower().startswith('v'):
        data.vectorization.total += 1
        if cmd.address is None:
            data.vectorization.rw += 1

    if cmd.address is None:
        return

    data.total_rw_count += 1

    block = cmd.address // 32
    old = data.address_usage.get(block)
    if old is None:
        old = 0
    data.address_usage.update({
        block: old + 1,
    })

    if cmd.address % 0x10 == 0:
        data.alignment.aligned += 1
    else:
        data.alignment.misaligned += 1

    scarcity = data.address_scarcity.get(cmd.address)
    if scarcity is not None:
        distance = offset - scarcity.last_seen + 1
        if scarcity.mean_distance == 0:
            scarcity.mean_distance = distance
        else:
            scarcity.mean_distance = (scarcity.mean_distance + distance) / 2
    else:
        data.address_scarcity.update({
            cmd.address: Scarcity(last_seen=offset)
        })


def analyze_vectorization(data: Metrics) -> float:
    return data.vectorization.rw / data.vectorization.total


def analyze_space_locality(data: Metrics) -> dict[int, float]:
    if data.vectorization.rw == 0:
        return {0: 0.0}

    res = {}
    for address, count in data.address_usage.items():
        res[address] = count / data.total_rw_count
    return res


def analyze_alignment(data: Metrics) -> float:
    if data.alignment.misaligned == 0:
        return data.alignment.aligned

    return data.alignment.aligned / data.alignment.misaligned


def plot_spacial(data: Metrics, top_n=30) -> None:
    spatial_locality = analyze_space_locality(data).items()

    top_items = sorted(
        spatial_locality,
        key=lambda x: x[1],
        reverse=True
    )[:top_n]
    addresses, values = zip(*top_items)

    plt.figure(figsize=(12, 8))
    hex_addrs = [f"0x{addr:08X}" for addr in addresses]
    y_pos = range(len(hex_addrs))
    plt.barh(y_pos, values, align='center')

    plt.yticks(y_pos, hex_addrs)
    plt.xlabel('Величина локализации')
    plt.title(f'Топ-{top_n} значений пространственной локализации')
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    plt.savefig('top_spatial_values.png', dpi=300)
    plt.close()


def plot_temporal(data: Metrics, top_n=40) -> None:
    temporal_data = []
    for address, scarcity in data.address_scarcity.items():
        if scarcity.mean_distance > 0:
            temporal_data.append((address, scarcity.mean_distance))
    if not temporal_data:
        print("Нет данных для временной локализации")
        return

    temporal_data.sort(key=lambda x: x[1], reverse=True)
    top_data = temporal_data[:top_n]
    addresses, values = zip(*top_data)

    hex_addresses = [f"0x{addr:08X}" for addr in addresses]

    plt.figure(figsize=(12, 10))
    y_pos = range(len(hex_addresses))
    plt.barh(y_pos, values, height=0.7, align='center', color='royalblue')

    plt.yticks(y_pos, hex_addresses, fontfamily='monospace', fontsize=9)
    plt.xlabel('Среднее расстояние доступа', fontsize=12)
    plt.ylabel('Адрес памяти', fontsize=12)
    plt.title(f'Топ-{top_n} значений временной локализации', fontsize=14, pad=20)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.gca().invert_yaxis()
    plt.tight_layout()

    plt.savefig('top_temporal_locality.png', dpi=300, bbox_inches='tight')
    plt.close()
