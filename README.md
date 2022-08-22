# QCCS

## Explanation

Following the programming exercises in the textbook
"Quantum Computing for Computer Scientists" by N. S.
Yanofsky and M. A. Mannucci.

## Contributing (note to self)

Install all requirements:

``` sh
pip install -r requirements.txt
```

Install pre-commit:

``` sh
pre-commit install
```

Format with

``` sh
python -m black --target-version py310 --preview * --force-exclude *.md *.txt
```

Run all tests with

``` sh
coverage run tests/test_runner.py
```

Create html report with

``` sh
coverage html
```
