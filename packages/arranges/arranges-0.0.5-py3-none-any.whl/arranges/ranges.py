from typing import Any, List

from arranges.range import Range
from arranges.utils import is_intlike, is_iterable, is_rangelike


class Ranges:
    """
    An ordered set of ranges that are combined and sorted
    """

    ranges: list[Range]

    def __init__(self, value=""):
        self.ranges = []
        self.append(value)

        super().__init__()

    def append(self, value: Any) -> None:
        """
        Add to the list of ranges.

        This mutates the object.
        """
        # deal with non-range objects
        if not isinstance(value, Range):
            ranges = Ranges.flatten(value)
            ranges.sort(key=Range.sort_key)

            for r in ranges:
                self.append(r)
            return

        # absorb range objects
        self.ranges.append(value)
        self.ranges.sort(key=Range.sort_key)

        i = 1

        while i < len(self.ranges):
            current = self.ranges[i]
            last = self.ranges[i - 1]
            if last.isconnected(current):
                self.ranges[i - 1] = current.union(last)
                del self.ranges[i]
                i -= 1
            i += 1

    def __eq__(self, other: "Ranges") -> bool:
        """
        Compare the two lists based on their string representations
        """
        return str(self) == str(other)

    def __repr__(self) -> str:
        """
        Return a code representation of this bunch of ranges
        """
        return f'{self.__class__.__name__}("{str(self)}")'

    def __str__(self) -> str:
        """
        Return a string representation of this bunch of ranges
        """
        return ",".join(str(r) for r in self.ranges)

    def __add__(self, other: Any) -> "Ranges":
        """
        Combine this range with another range
        """
        new = Ranges(self)
        new.append(Ranges(other))
        return new

    def __contains__(self, other: Any) -> bool:
        """
        Are all of the other ranges in our ranges?
        """
        return str(self) == str(self + other)

    def __iter__(self):
        """
        Iterate over the values in our ranges.

        Note that this could be boundless.
        """
        for r in self.ranges:
            for i in r:
                yield i

    def intersects(self, other: Any) -> bool:
        """
        True if this range overlaps with the other range
        """
        other: Ranges = Ranges(other)
        for r in self.ranges:
            for o in other.ranges:
                if r.intersects(o):
                    return True

        return False

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        """
        For automatic validation in pydantic
        """
        yield cls.validate

    @staticmethod
    def flatten(obj: Any, _current=None) -> List["Range"]:
        """
        Coerce an object into a list of ranges.

        _current is used internally to keep track of the current
        """
        if _current is None:
            _current = []

        if is_rangelike(obj):
            _current.append(Range(obj))
        elif hasattr(obj, "ranges"):
            for r in obj.ranges:
                Ranges.flatten(r, _current=_current)
        elif isinstance(obj, str):
            for s in obj.split(","):
                _current.append(Range.from_str(s))
        elif is_intlike(obj):
            # todo: extend last range in case we're iterating over
            # a large sequence
            _current.append(Range(obj, obj + 1))
        elif is_iterable(obj):
            for item in obj:
                Ranges.flatten(item, _current=_current)
        else:
            raise TypeError(f"Unsupported type {type(obj)}")

        return _current
