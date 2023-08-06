# Python package template

Template for Python packages for qurix Technology.

## Structure

A normal Python package will start with the namespace `qurix` as in this sample package. A sample structure is as follows:

```text
.
├── LICENCE
├── Makefile
├── README.md
├── qurix
│   └── <domain>
│       └── <module-organization-level>
│           ├── __init__.py
│           ├── __version__.py
│           └── <module>
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    └── test_client.py
```

## Versioning

According to [semantic versioning](https://semver.org/lang/en).

## Deployment

Using Github Actions. See `.github/worfklows/`