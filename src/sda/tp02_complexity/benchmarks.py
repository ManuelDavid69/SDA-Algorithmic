"""Runtime measurements and complexity tables for TP 2.

The theoretical tables use the hypothesis of the statement: one elementary
operation costs one microsecond.  Durations are formatted with ASCII units so
that the output is identical on every platform.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

SECOND = 1.0
MINUTE = 60.0
HOUR = 3600.0
DAY = 86400.0
MONTH = 30 * DAY
YEAR = 365 * DAY
CENTURY = 100 * YEAR

BUDGETS: dict[str, float] = {
    "1 second": SECOND,
    "1 minute": MINUTE,
    "1 hour": HOUR,
    "1 day": DAY,
    "1 month": MONTH,
    "1 year": YEAR,
    "1 century": CENTURY,
}

COURSE_NUMBERS = (
    4_337_894_221,
    118_922_974_492_981,
    7_138_449_485_398_663,
    35_831_403_792_388_187,
    621_467_444_825_020_319,
    8_939_187_427_700_486_623,
)


@dataclass(frozen=True)
class PrimeMeasurement:
    number: int
    digits: int
    seconds: float
    iterations: int


@dataclass(frozen=True)
class MaxInstance:
    complexity: str
    budget_seconds: float
    value: int | None
    display: str


def is_prime(n: int) -> bool:
    """Trial division up to ``sqrt(n)``, as in the statement."""
    if n < 2:
        return False
    for divisor in range(2, math.isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True


def prime_iterations(n: int) -> int:
    """Number of loop iterations performed by :func:`is_prime`."""
    if n < 2:
        return 0
    return math.isqrt(n) - 1


def measure_prime(numbers: tuple[int, ...] | list[int], repeats: int = 1) -> list[PrimeMeasurement]:
    """Time :func:`is_prime` on each number and record the number of digits."""
    measurements: list[PrimeMeasurement] = []
    for number in numbers:
        best = math.inf
        for _ in range(repeats):
            start = time.perf_counter()
            is_prime(number)
            best = min(best, time.perf_counter() - start)
        measurements.append(
            PrimeMeasurement(
                number=number,
                digits=len(str(number)),
                seconds=best,
                iterations=prime_iterations(number),
            )
        )
    return measurements


def format_duration(seconds: float) -> str:
    """Format a duration with a readable unit."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.1f} ns"
    if seconds < 1e-3:
        return f"{seconds * 1e6:.1f} us"
    if seconds < 1:
        return f"{seconds * 1e3:.1f} ms"
    if seconds < 60:
        return f"{seconds:.2f} s"
    if seconds < HOUR:
        return f"{seconds / MINUTE:.2f} min"
    if seconds < DAY:
        return f"{seconds / HOUR:.2f} h"
    if seconds < YEAR:
        return f"{seconds / DAY:.2f} days"
    years = seconds / YEAR
    if years < 1e6:
        return f"{years:.2f} years"
    return f"{years:.2e} years"


def _format_log10(log10_value: float) -> str:
    return f"10^{log10_value:.1f}"


def theoretical_times(n: int = 10**6, operation_seconds: float = 1e-6) -> dict[str, str]:
    """Times needed by the four algorithms of exercise 3, question 1."""
    results: dict[str, str] = {}
    results["log n"] = format_duration(math.log2(n) * operation_seconds)
    results["n"] = format_duration(n * operation_seconds)
    results["n^2"] = format_duration(n * n * operation_seconds)
    # 2^n overflows every float: work with logarithms.
    log10_seconds = n * math.log10(2) + math.log10(operation_seconds)
    seconds = 10**log10_seconds if log10_seconds < 308 else math.inf
    if math.isfinite(seconds):
        results["2^n"] = format_duration(seconds)
    else:
        log10_years = log10_seconds - math.log10(YEAR)
        results["2^n"] = f"about {_format_log10(log10_years)} years"
    return results


def _solve_n_log_n(seconds: float) -> int:
    """Largest n such that ``n * log2(n) <= seconds``."""
    if seconds < 1:
        return 1
    low, high = 1.0, max(2.0, seconds)
    for _ in range(100):
        middle = (low + high) / 2
        if middle * math.log2(middle) <= seconds:
            low = middle
        else:
            high = middle
    return int(low)


def _inverse_factorial(seconds: float) -> int:
    """Largest n such that ``n! <= seconds``."""
    n = 1
    factorial = 1
    while math.factorial(n + 1) <= seconds:
        n += 1
        factorial = math.factorial(n)
        if n > 1000:  # pragma: no cover - unreachable with realistic budgets
            break
    return n if factorial <= seconds else n - 1


def _format_size(value: int | None, fallback: str) -> str:
    if value is None:
        return fallback
    if value < 10**6:
        return f"{value:,}"
    return f"{value:.3e}"


def max_instance_sizes(seconds: float, operation_seconds: float = 1e-6) -> list[MaxInstance]:
    """Largest instance solvable in ``seconds`` for each complexity.

    ``operation_seconds`` is the duration of one elementary operation
    (one microsecond by default), so the number of available operations is
    ``seconds / operation_seconds``.
    """
    operations = seconds / operation_seconds
    sizes: list[MaxInstance] = []

    log_exponent = operations  # n = 2^operations
    log_value = 2**int(log_exponent) if log_exponent <= 10000 else None
    sizes.append(
        MaxInstance(
            "lg n",
            seconds,
            log_value,
            f"2^{log_exponent:,.0f}" if log_value is None else _format_size(log_value, ""),
        )
    )

    root = int(math.isqrt(int(operations)))
    sizes.append(MaxInstance("sqrt(n)", seconds, root, _format_size(root, "")))

    linear = int(round(operations))
    sizes.append(MaxInstance("n", seconds, linear, _format_size(linear, "")))

    n_log_n = _solve_n_log_n(operations)
    sizes.append(MaxInstance("n lg n", seconds, n_log_n, _format_size(n_log_n, "")))

    square = int(math.isqrt(int(operations)))
    sizes.append(MaxInstance("n^2", seconds, square, _format_size(square, "")))

    cube = int(round(operations ** (1 / 3)))
    while (cube + 1) ** 3 <= operations:
        cube += 1
    while cube**3 > operations:
        cube -= 1
    sizes.append(MaxInstance("n^3", seconds, cube, _format_size(cube, "")))

    exponential = int(math.floor(math.log2(operations))) if operations >= 1 else 0
    sizes.append(MaxInstance("2^n", seconds, exponential, _format_size(exponential, "")))

    factorial = _inverse_factorial(operations)
    sizes.append(MaxInstance("n!", seconds, factorial, _format_size(factorial, "")))

    return sizes


def complexity_table(budgets: dict[str, float] | None = None) -> list[list[str]]:
    """Build the table of exercise 3, question 2 as rows of strings."""
    budgets = budgets or BUDGETS
    header = ["Complexity", *budgets.keys()]
    rows = [header]
    labels = ("lg n", "sqrt(n)", "n", "n lg n", "n^2", "n^3", "2^n", "n!")
    for label in labels:
        row = [label]
        for seconds in budgets.values():
            instance = next(item for item in max_instance_sizes(seconds) if item.complexity == label)
            row.append(instance.display)
        rows.append(row)
    return rows
