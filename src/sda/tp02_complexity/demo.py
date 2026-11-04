"""Démonstration du TP 2 : comptages d'opérations, croissance et mesures de performance."""

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
    print("== Comptages d'opérations élémentaires (n = 8) ==")
    for number, program in enumerate((program1, program2, program3, program4, program5), start=1):
        result = program(8)
        print(
            f"Programme {number} : {result.operations:>6} opérations, "
            f"valeur finale {result.value}"
        )

    print("\n== Croissance asymptotique (du plus lent au plus rapide) ==")
    for position, label in enumerate(GROWTH_ORDER, start=1):
        print(f"{position:>2}. {label:<16} {theta_class(label)}")

    print("\n== Temps théoriques pour n = 1 000 000 (1 us par opération) ==")
    for complexity, duration in theoretical_times(10**6).items():
        print(f"{complexity:>6}: {duration}")

    print("\n== Test de primalité (division par essais successifs) ==")
    samples = (1_000_000_007, *COURSE_NUMBERS[:1])
    for measurement in measure_prime(samples):
        print(
            f"{measurement.number} ({measurement.digits} chiffres) : "
            f"{format_duration(measurement.seconds)}, "
            f"{measurement.iterations:,} itérations"
        )

    print("\n== Plus grande instance en une seconde (1 us par opération) ==")
    for instance in max_instance_sizes(1.0):
        print(f"{instance.complexity:>7}: {instance.display}")

    print("\n== Extrait du tableau temps/taille ==")
    for row in complexity_table():
        print(" | ".join(f"{cell:>12}" for cell in row))


if __name__ == "__main__":
    main()
