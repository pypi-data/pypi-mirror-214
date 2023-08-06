from typing import Any, Tuple

from arranges.utils import as_type, inf, is_intlike, is_iterable, is_rangelike, to_int


class Range:
    """
    A range of numbers, similar to Python slice notation, but with no step or
    negative/relative ranges.
    """

    start: int = 0
    stop: int = inf

    def __init__(self, value: Any, stop: int = None):
        """
        Construct a range from either a value:

        If `value` is a string, it'll use `Range.from_str` and expect a string
        in slice notation.

        If `value` is an iterable, it'll use `Range.from_iterable` and expect
        a sequence of consecutive integers.

        If `value` is an object with `start`, `stop` and `step` value, it'll
        use the start and stop values from that, though the `step` value must
        be 1.

        If `value` is an integer, it'll use that as the stop value, just like a
        Python range or slice.

        If a `value` and `stop` are provided then `value` is the start like in
        a range or slice.
        """
        start_and_stop = value is not None and stop is not None

        if start_and_stop:
            self.start = value
            self.stop = stop

        else:
            if is_rangelike(value):
                if value.step not in (None, 1):
                    raise ValueError("Step values are not supported")

                self.start = 0 if value.start is None else value.start
                self.stop = inf if value.stop is None else value.stop
            elif isinstance(value, str):
                other = self.from_str(value)
                self.start = other.start
                self.stop = other.stop
            elif is_iterable(value):
                other = self.from_iterable(value)
                self.start = other.start
                self.stop = other.stop
            else:
                self.start = 0
                self.stop = value

        # Convert to integers
        self.start = int(self.start)
        if self.stop is not inf:
            self.stop = int(self.stop)

        self.step = 1

        if self.start < 0 or self.stop < 0:
            raise ValueError("Start and stop must be positive")

        if self.start > self.stop:
            raise ValueError("Stop can't be before start")

        if self.start == self.stop:
            self.start = self.stop = 0

        super().__init__()

    @classmethod
    def from_str(cls, value: str) -> "Range":
        """
        Construct Range from a string, Python slice notation. e.g. "100:" or
        "1:10".

        Hex, octal and binary numbers are supported, using Python syntax, e.g.
        "0x10:0x20" or "0o10:0o20" or "0b100:0b110".

        Special values "start", "inf" and "end" can be used, which are considered
        to be 0 and `inf` respectively.

        An empty string is treated to be an empty range, and ":" is the full range.
        """
        vals = [v.strip() for v in str(value).split(":")]

        if len(vals) > 2:
            raise ValueError("Too many values, Only start and stop are allowed")

        if len(vals) == 1:
            if not vals[0]:
                # Empty range
                start = stop = 0
            else:
                # single value
                start = to_int(vals[0], 0)
                stop = start + 1
        else:
            # start:stop
            start = to_int(vals[0], 0)
            stop = to_int(vals[1], inf)

        return cls(start, stop)

    @classmethod
    def from_iterable(cls, values: Any) -> "Range":
        """
        Construct Range from an iterable
        """
        values = list(set(values))
        values.sort()

        if not values or len(values) == 1:
            return Range(0, 0)

        start = int(values[0])
        stop = start

        for value in values:
            if not is_intlike(value) or value < 0:
                raise ValueError("Only positive integers are allowed")

            if value > stop:
                raise ValueError("Continuous ranges only")

            if value == stop:
                stop += 1

        return Range(start, stop)

    @staticmethod
    def sort_key(value: "Range") -> Tuple[int]:
        """
        Sort key function for sorting ranges
        """
        return value.start, value.stop

    def __repr__(self):
        """
        Python representation
        """
        name = self.__class__.__name__
        if not self:
            return f"{name}(0, 0)"
        if not self.start and self.stop is inf:
            return f"{name}(0, inf)"
        if self.start == 0:
            return f"{name}({self.stop})"

        return f"{name}({self.start}, {self.stop})"

    def __str__(self):
        """
        Convert to a string
        """
        if not self:
            return ""
        if not self.start and self.stop == inf:
            return ":"
        if not self.start:
            return f":{self.stop}"
        if self.stop == inf:
            return f"{self.start}:"
        if self.stop == self.start + 1:
            return str(self.start)

        return f"{self.start}:{self.stop}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        """
        Compare two ranges
        """
        if is_intlike(other):
            return self.start == other and self.stop == other + 1
        if isinstance(other, str):
            return self == self.from_str(other)
        if not self and not other:
            return True

        try:
            other = as_type(Range, other)
        except (TypeError, ValueError):
            return False

        return self.start == other.start and self.stop == other.stop

    def isdisjoint(self, other: Any) -> bool:
        """
        Return True if this range is disjoint from the other range
        """
        other = as_type(Range, other)
        return not self.intersects(other)

    def issubset(self, other: Any) -> bool:
        """
        Return True if this range is a subset of the other range
        """
        other = as_type(Range, other)
        return self in other

    def __le__(self, other: Any) -> bool:
        """
        Return True if this range is a subset of the other range
        """
        other = as_type(Range, other)
        return self in other

    def __lt__(self, other: Any) -> bool:
        """
        Return True if this range is a proper subset of the other range
        """
        other = as_type(Range, other)
        return self in other and self != other

    def issuperset(self, other: Any) -> bool:
        """
        Return True if this range is a superset of the other range
        """
        other = as_type(Range, other)
        return other in self

    def __ge__(self, other: Any) -> bool:
        """
        Return True if this range is a superset of the other range
        """
        other = as_type(Range, other)
        return other in self

    def __gt__(self, other: Any) -> bool:
        """
        Return True if this range is a proper superset of the other range
        """
        other = as_type(Range, other)
        return other in self and self != other

    def union(self, *others) -> "Range":
        """
        Return the union of this range and the other ranges
        """
        ret = self
        for other in others:
            ret = ret | other
        return ret

    def __invert__(self) -> "Range":
        """
        Return the inverse of this range (compliment)
        """
        if not self:
            return Range(0, inf)

        if self.start == 0:
            return Range(self.stop, inf)

        if self.stop == inf:
            return Range(0, self.start)

        raise ValueError("Inverting this range will cause a discontinuity")

    def __or__(self, other: Any) -> "Range":
        """
        Return the union of this range and the other range
        """
        if not other:
            return self
        if not self:
            return other

        if not self.isconnected(other):
            raise ValueError(f"{self} and {other} aren't touching")

        start = min(self.start, other.start)
        stop = max(self.stop, other.stop)

        return Range(start, stop)

    def intersection(self, *others: "Range") -> "Range":
        """
        Return the intersection of this range and the other ranges
        """
        ret: Range = self

        for other in others:
            if not ret.intersects(other):
                return Range(0, 0)

            start = max(ret.start, other.start)
            stop = min(ret.stop, other.stop)
            if start >= stop:
                return Range(0, 0)

            ret = Range(start, stop)

        return ret

    def __and__(self, other: "Range") -> "Range":
        """
        Return the intersection of this range and the other range
        """
        return self.intersection(other)

    def __sub__(self, other: "Range") -> "Range":
        """
        Return the difference between this range and the other
        """
        if not self.intersects(other):
            return Range(self)

    # def difference(self, *others):
    #     """
    #     Remove the other ranges from this one
    #     """
    #

    # def symmetric_difference(self, other: "Range") -> "Range":
    #     """
    #     Return the symmetric difference of two ranges
    #     """

    # def __xor__(self, other: "Range") -> "Range":
    #     """
    #     Return the symmetric difference of two ranges
    #     """

    def __contains__(self, other: Any) -> bool:
        """
        Membership test. Supports integers, strings, ranges and iterables.
        """
        if is_intlike(other):
            return self.start <= other <= self.last

        if not self:  # nothing fits in an empty range
            return False

        if is_rangelike(other):
            if not other:
                return True  # the empty set is a subset of all other sets

            inf_stop = other.stop or inf
            start_inside = not self.start or other.start in self
            last_inside = self.stop is None or (inf_stop - 1) in self

            return start_inside and last_inside

        if isinstance(other, str):
            return self.from_str(other) in self

        if is_iterable(other):
            for o in other:
                if o not in self:
                    return False
            return True

        raise TypeError(f"Unsupported type {type(other)}")

    def __iter__(self):
        """
        Iterate over the values in this range
        """
        i = self.start
        while i < self.stop:
            yield i
            i += 1

    def __len__(self) -> int:
        """
        Get the length of this range
        """
        if self.start == self.stop:
            return 0

        if self.stop == inf:
            return inf.__index__()

        return self.stop - self.start

    def __bool__(self) -> bool:
        """
        True if this range has a length
        """
        return len(self) > 0

    @property
    def last(self) -> int:
        """
        Gets the last value in this range. Will return inf if the range
        has no end, and -1 if it has no contents,
        """
        if not self:
            return -1
        return self.stop - 1

    def intersects(self, other: "Range") -> bool:
        """
        True if this range intersects the other range.
        """
        if self in other or other in self:
            return True

        if self.start in other or other.start in self:
            return True

        return False

    def isadjacent(self, other: "Range") -> bool:
        """
        True if this range is adjacent to the other range
        """
        if self.stop == other.start or other.stop == self.start:
            return True

        return False

    def isconnected(self, other: "Range") -> bool:
        """
        True if this range is adjacent to or overlaps the other range, and so they
        can be joined together.
        """
        return self.isadjacent(other) or self.intersects(other)

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            return cls.from_str(value)

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
