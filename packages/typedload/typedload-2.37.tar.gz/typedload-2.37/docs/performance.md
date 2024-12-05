Performance
===========

Negative values mean that the library failed the test.

The tests are done on my PC. The following libraries are tested:

* `typedload`, the 3 most recent versions. It shines with tagged unions, which is what I mostly use.
* `pydantic2` years of work to rewrite it in Rust, [implemented detection of tagged unions years after I did it](https://github.com/pydantic/pydantic/issues/5163#issuecomment-1619203179), still managing to lose some benchmarks 😅
* `apischema` is slower where there are unions, faster otherwise

Using Python 3.13
-----------------

![performance chart](3.13_tagged_union_of_objects.svg "Load tagged union of objects")
![performance chart](3.13_dump_objects.svg "Dump objects")
![performance chart](3.13_load_list_of_floats_and_ints.svg "Load list of floats and ints")
![performance chart](3.13_load_list_of_lists.svg "Load list of lists")
![performance chart](3.13_load_list_of_NamedTuple_objects.svg "Load list of NamedTuple")
![performance chart](3.13_load_big_dictionary.svg "Load big dictionary")
![performance chart](3.13_load_list_of_ints.svg "Load list of ints")


Using Pypy 7.3.17
-----------------

![performance chart](3.10_tagged_union_of_objects.svg "Load tagged union of objects")
![performance chart](3.10_dump_objects.svg "Dump objects")
![performance chart](3.10_load_list_of_floats_and_ints.svg "Load list of floats and ints")
![performance chart](3.10_load_list_of_lists.svg "Load list of lists")
![performance chart](3.10_load_list_of_NamedTuple_objects.svg "Load list of NamedTuple")
![performance chart](3.10_load_big_dictionary.svg "Load big dictionary")
![performance chart](3.10_load_list_of_ints.svg "Load list of ints")


Run the tests
-------------

Generate the performance chart locally.

```bash
python3 -m venv perfvenv
. perfvenv/bin/activate
pip install apischema pydantic attrs
export PYTHONPATH=$(pwd)
make gnuplot
```
