A Range is an object resembling a set but optimised for contiguous
ranges of int members.

*Latest release 20230619*:
* Span: sanity check .start and .end.
* Range.issubset: efficient comparison with another Range, also .issuperset.

## Function `overlap(span1, span2)`

Return a list `[start,end]` denoting the overlap of two spans.

Example:

    >>> overlap([1,9], [5,13])
    [5, 9]

## Class `Range`

A collection of `int`s that collates adjacent ints.

The interface is as for a `set` with additional methods:
* `spans()`: return an iterable of `Span`s, with `.start`
  included in each `Span` and `.end` just beyond

Additionally, the update/remove/etc methods have a secondary
calling signature: `(start,end)`, which is the same as passing
in `Range(start,end)` but much more efficient.

*Method `Range.__init__(self, start=None, end=None, debug=None)`*:
Initialise the Range.

Called with `start` and `end`, these specify the initial
`Span` of the `Range`.
If called with just one argument that argument instead be an iterable
of integer values comprising the values in the `Range`.

*Method `Range.__and__(self, other)`*:
Return a new `Range` containing elements in both `self` and `other`.

*Method `Range.__contains__(self, x)`*:
Test `x` to see if it is wholly contained in this Range.

`x` may be another `Range`, a `Span`, or a single `int` or an iterable
yielding a pair of `int`s.

Example:

    >>> R = Range(4,7)
    >>> R.add(11,15)
    >>> (3,7) in R
    False
    >>> (4,7) in R
    True
    >>> (4,8) in R
    False

*Method `Range.__ge__(self, other)`*:
Test that `self` is a superset of `other`.

*Method `Range.__iter__(self)`*:
Yield all the elements.

*Method `Range.__le__(self, other)`*:
Test that `self` is a subset of `other`.

*Method `Range.__or__(self, other)`*:
Return a new `Range` containing the elements of `self` and `other`.

*Method `Range.__sub__(self, start, end=None)`*:
Subtract `start`, or `start:end`, from the `Range`.

*Method `Range.__xor__(self, other)`*:
Return a new `Range` with elements in `self` or `other` but not both.

*Method `Range.add(self, start, end=None)`*:
Like `set.add` but with an extended signature.

*Method `Range.add_span(self, start, end)`*:
Update self with [start,end].

*Method `Range.as_list(self)`*:
This `Range` as a `list` of 2-element per-`Span` `list`s.

>>> R = Range(4, 8)
>>> R.as_list()
[[4, 8]]
>>> R.add(11, 14)
>>> R.as_list()
[[4, 8], [11, 14]]
>>> R.remove(12)
>>> R.as_list()
[[4, 8], [11, 12], [13, 14]]

*Method `Range.clear(self)`*:
Clear the `Range`: remove all elements.

*Method `Range.copy(self)`*:
Return a copy of this Range.

*Method `Range.difference(self, start, end=None)`*:
Subtract `start`, or `start:end`, from the `Range`.

*Method `Range.difference_update(self, start, end=None)`*:
Like `set.discard` but with an extended signature.

*Method `Range.discard(self, start, end=None)`*:
Like `set.discard` but with an extended signature.

*Method `Range.discard_span(self, start, end, remove_mode=False)`*:
Remove [start,end] from Range if present.

*Method `Range.dual(self, start=None, end=None)`*:
Return an iterable of the gaps (spans not in this Range).
If `start` is omitted, start at the minimum of 0 and the
lowest span in the Range.
If `end` is omitted, use the maximum span in the Range.

*Property `Range.end`*:
Return the end offset of the `Range`,
the maximum `Span` .end or `0` if the `Range` is empty.

*Method `Range.intersection(self, other)`*:
Return a new `Range` containing elements in both `self` and `other`.

*Method `Range.intersection_update(self, other)`*:
Update the `Range`, keeping only elements
found in both `self` and `other`.

*Method `Range.isempty(self)`*:
Test if the Range is empty.

*Method `Range.issubset(self, other)`*:
Test that `self` is a subset of `other`.

*Method `Range.issuperset(self, other)`*:
Test that `self` is a superset of `other`.

*Method `Range.pop(self)`*:
Remove and return an arbitrary element.
Raise `KeyError` if the `Range` is empty.

*Method `Range.remove(self, start, end=None)`*:
Like `set.remove` but with an extended signature.

*Method `Range.slices(self, start=None, end=None)`*:
Return an iterable of (inside, Span) covering the gaps and spans in this Range.
If `start` is omitted, start at the minimum of 0 and the
lowest span in the Range.
If `end` is omitted, use the maximum span in the Range.
`inside` is true for spans and false for gaps.
TODO: make this efficient if `start` isn't near the start of the _spans.

*Property `Range.span0`*:
Return the first `Span`; raises `IndexError` if there are no spans.

*Method `Range.span_position(self, start, end)`*:
Somewhat like `bisect_left`, return indices `(i,j)`
such that all spans with indices < `i`
strictly preceed `start` amd all spans with indices > `j`
strictly follow `end`.

*Method `Range.spans(self)`*:
Return an iterable of `Spans` covering the `Range`.

*Property `Range.start`*:
Return the start offset of the `Range`,
the minimum `Span` .start or `0` if the `Range` is empty.

*Method `Range.symmetric_difference(self, other)`*:
Return a new `Range` with elements in `self` or `other` but not both.

*Method `Range.symmetric_difference_update(self, other)`*:
Update the `Range`, keeping only elements found in `self` or `other`,
but not in both.

*Method `Range.union(self, other)`*:
Return a new `Range` containing the elements of `self` and `other`.

*Method `Range.update(self, iterable)`*:
Update the `Range` to include the values from `iterable`.

## Class `Span(Span, builtins.tuple)`

A namedtuple with `.start` and `.end` attributes.

*Method `Span.as_list(self)`*:
This `Span` as a 2 element `list`.

*Property `Span.size`*:
The `.size` of a `Span` is its length: `end - start`.

## Function `spans(items)`

Return an iterable of `Spans` for all contiguous sequences in
`items`.

Example:

    >>> list(spans([1,2,3,7,8,11,5]))
    [1:4, 7:9, 11:12, 5:6]

# Release Log



*Release 20230619*:
* Span: sanity check .start and .end.
* Range.issubset: efficient comparison with another Range, also .issuperset.

*Release 20230518*:
Span,Range: new as_list() methods.

*Release 20190102*:
Span: provide __len__.

*Release 20171231*:
* Add Range.span0, returning the first Span.
* Implement __bool__ and__nonzero__.
* Accept a Span in __contains__.
* Some small bugfixes.

*Release 20160828*:
* Add Range.start like existing Range.end.
* Use "install_requires" instead of "requires" in DISTINFO.
* Small bugfix.

*Release 20150116*:
First PyPI release.
