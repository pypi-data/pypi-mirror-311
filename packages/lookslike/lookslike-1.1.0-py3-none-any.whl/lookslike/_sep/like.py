import random
import re


if hasattr(re, 'Pattern'):  # >Py3.6
    def is_regex_pattern(obj):
        return isinstance(obj, re.Pattern)
else:  # <=Py3.6
    def is_regex_pattern(obj):
        return 'SRE_Pattern' in str(type(obj))

NEVER_COMPARED = object()


class Like:
    """
    Compare an object with something which is similar (or equal) to it.

    :param args: One or multiple criteria that have to match.
                 For example: 42 == Like(42, int, re.compile('4.'), 
                                         lambda v: v == 42)
    :type args: type | Callable[[Any], bool] | re.Pattern | Any
    :param convert: Optional: A function to convert the comparison value 
                    before matching.
                    For example: [3, 2, 1] == Like([1, 2, 3], convert=sorted)
    :type convert: Callable[[Any], Any]

    Example:
        42 == Like(int)  # -> True

        'http://some.url' == Like(re.compile('http://.*')  # -> True

        10 == Like(lambda v: 9 < v < 11)  # -> True

        {'num': 42, 'alpha': 'abcd'} == {'num': Like(int), 
                                         'alpha': Like(str)} # -> True
    """

    def __init__(self, *args, convert=None):
        self._comparison_values = args
        self._convert = convert
        self._success = False
        self._uncompared = True

    def __eq__(self, other):
        self._uncompared = False
        for comparison_value in self._comparison_values:
            if not self._compare_single_value(comparison_value, other):
                self._success = False
                return False
        self._success = True
        return True

    def __ne__(self, other):
        return not other == self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        args = ', '.join([str(value) for value in self._comparison_values])
        prefix = '' if self._success else '!'
        prefix = '?' if self._uncompared else prefix
        return '{prefix}{cls}({args})'.format(cls=self.__class__.__name__,
                                              prefix=prefix,
                                              args=args)

    def _compare_single_value(self, comparison_value, other) -> bool:
        if self._convert is not None:
            other = self._convert(other)
        if isinstance(comparison_value, type):
            return isinstance(other, comparison_value)
        elif callable(comparison_value):
            return comparison_value(other)
        elif is_regex_pattern(comparison_value):
            if isinstance(other, (str, bytes)):
                stringified_value = other
            else:
                stringified_value = str(other)
            try:
                match = comparison_value.match(stringified_value)
            except TypeError:
                # This happens for b"ab" != Like(re.compile('ab')):
                # TypeError: cannot use a string pattern on a bytes-like object
                return False
            if match is None:
                return False
            return match.start() == 0 and match.end() == len(stringified_value)
        return type(other) == type(comparison_value) and other == comparison_value


class Similar(Like):
    """
    Compare an object with something which is similar (or equal) to it.

    Unlike the Like object, the Similar object will remember the value that it has been
    compared against the first time. It then assumes, that all further comparisons
    should have the exact same value.
    Furthermore, for successful comparisons, it will have the same string representation
    as the comparison value. This makes it easier when you display a diff of objects.

    The arguments have the same meaning as for the Like object and will be used
    during the first comparison.

    :param args: One or multiple criteria that have to match.
                 For example: 42 == Similar(42, int, re.compile('4.'),
                                           lambda v: v == 42)
    :type args: type | Callable[[Any], bool] | re.Pattern | Any
    :param convert: Optional: A function to convert the comparison value
                    before matching.
                    For example: [3, 2, 1] == Similar([1, 2, 3], convert=sorted)
    :type convert: Callable[[Any], Any]

    Example:

        identifier = Similar(int)
        assert [1, 1] == [identifier, identifier]  # True
        assert [1, 2] == [identifier, identifier]  # False, as 2nd value is not similar to 1st value
        assert [1, 1.0] == [identifier, identifier]  # False, als 2nd value is not int.

        identifier = Similar()
        assert [1, 1.0] == [identifier, identifier]  # True and Python defines 1 == 1.0 -> True
        assert ["1", 1] == [identifier, identifier]  # False as Python defines "1" == 1 -> False

        Examples with the same behaviour as the Like object:

        42 == Similar(int)  # -> True

        'http://some.url' == Similar(re.compile('http://.*')  # -> True

        10 == Similar(lambda v: 9 < v < 11)  # -> True

        {'num': 42, 'alpha': 'abcd'} == {'num': Similar(int),
                                         'alpha': Similar(str)} # -> True
    """
    def __init__(self, *args, convert=None, lock_to=NEVER_COMPARED):
        super(Similar, self).__init__(*args, convert=convert)
        self._identity_success = True
        self._locked_value = lock_to
        self._hash = random.getrandbits(128)

    def __hash__(self):
        assert self._locked_value is not NEVER_COMPARED, ('The lookslike.Similar object has not been compared to '
                                                          'anything yet, so the hash is not defined! You might want '
                                                          'to set the initial value using the lock_to keyword argument.')
        return hash(self._locked_value)

    def __eq__(self, other):
        if self._locked_value is NEVER_COMPARED:
            self._locked_value = other
            return super().__eq__(other)
        else:
            is_equal = other == self._locked_value
            super().__eq__(other)
            self._success = self._success and is_equal
            self._identity_success = self._identity_success and is_equal
            return self._success

    def __repr__(self):
        if self._locked_value is not NEVER_COMPARED:
            if self._success:
                return repr(self._locked_value)
            elif not self._identity_success:
                return '!Similar(locked_to={value})'.format(value=repr(self._locked_value))
        return super(Similar, self).__repr__()