"""Demonstration of TP 2: operation counts, growth and benchmarks."""

from .benchmarks import (
    COURSE_NUMBERS,
    complexity_table,
    format_duration,
    max_instance_sizes,
    measure_prime,
    theoretical_times,
)
from .counting import program1, program2, program3, program4, program5
from .growth import GROWTH_ORDER, theta_class


def main() -> None:
    print("== Elementary operation counts (n = 8) ==")
    for number, program in enumerate((program1, program2, program3, program4, program5), start=1):
        result = program(8)
        print(f"Program {number}: {result.operations:>6} operations, final value {result.value}")

    print("\n== Asymptotic growth (slowest to fastest) ==")
    for position, label in enumerate(GROWTH_ORDER, start=1):
        print(f"{position:>2}. {label:<16} {theta_class(label)}")

    print("\n== Theoretical times for n = 1,000,000 (1 us per operation) ==")
    for complexity, duration in theoretical_times(10**6).items():
        print(f"{complexity:>6}: {duration}")

    print("\n== Prime testing (trial division) ==")
    samples = (1_000_000_007, *COURSE_NUMBERS[:1])
    for measurement in measure_prime(samples):
        print(
            f"{measurement.number} ({measurement.digits} digits): "
            f"{format_duration(measurement.seconds)}, "
            f"{measurement.iterations:,} iterations"
        )

    print("\n== Largest instance in one second (1 us per operation) ==")
    for instance in max_instance_sizes(1.0):
        print(f"{instance.complexity:>7}: {instance.display}")

    print("\n== Extract of the time/size table ==")
    for row in complexity_table():
        print(" | ".join(f"{cell:>12}" for cell in row))


if __name__ == "__main__":
    main()
