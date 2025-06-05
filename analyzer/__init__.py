from domain.metrics import Metrics, Scarcity
from domain.command import Command


def update_metrics(data: Metrics, cmd: Command, offset: int):
    if cmd.command.lower().startswith('v'):
        data.vectorization.total += 1
        if cmd.address is None:
            data.vectorization.rw += 1

    if cmd.address is None:
        return

    old = data.address_usage.get(cmd.address)
    if old is None:
        old = 0
    data.address_usage.update({
        cmd.address: old + 1,
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
    res = {}
    for address, count in data.address_usage.items():
        res[address] = count / data.vectorization.rw
    return res

def analyze_alignment(data: Metrics) -> float:
    return data.alignment.aligned / data.alignment.misaligned
