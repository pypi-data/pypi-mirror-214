<!--
Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
SPDX-License-Identifier: MIT
-->

NEWS
======


## 0.1.0 - 2023-06-18 <a id='0.1.0'></a>

### Added

- `FrozenMappie`: add `__copy__` and `__deepcopy__`
- Add official support for Python 3.12.

### Changed

- **Drop support for Python 3.7**
- **`FrozenMappie`: require `data` to be a positional arg**
- `FactoryFrozenMappie.__new__`: rename `self` arg to `cls`

## 0.0.2 - 2023-06-15 <a id='0.0.2'></a>

### Added

- Add py.typed file as per [PEP 561][PEP 561].

[PEP 561]: https://peps.python.org/pep-0561/

## 0.0.1 - 2023-06-13 <a id='0.0.1'></a>

Initial release