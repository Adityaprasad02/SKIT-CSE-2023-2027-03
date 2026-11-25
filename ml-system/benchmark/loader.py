import json
from pathlib import Path

from skills.taxonomy import Taxonomy

from .schemas.models import RoleBenchmark


def load_benchmark(path: str | Path, taxonomy: Taxonomy | None = None) -> RoleBenchmark:
    benchmark_path = Path(path)
    with benchmark_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Benchmark JSON must contain an object.")

    benchmark = RoleBenchmark.from_dict(data)
    if taxonomy is not None:
        benchmark.validate_taxonomy(taxonomy)
    return benchmark


def load_benchmarks(directory: str | Path, taxonomy: Taxonomy | None = None) -> tuple[RoleBenchmark, ...]:
    benchmark_dir = Path(directory)
    if not benchmark_dir.is_dir():
        raise ValueError(f"Benchmark directory does not exist: {benchmark_dir}")

    benchmarks = [
        load_benchmark(path, taxonomy)
        for path in sorted(benchmark_dir.glob("*.json"))
    ]
    if not benchmarks:
        raise ValueError(f"No benchmark JSON files found in: {benchmark_dir}")
    return tuple(benchmarks)
