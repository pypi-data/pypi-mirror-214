# authit

`authit` is the simple and light weight *Identity platform*

## Installation

Install directly from PIP registry

```
pip install authit
```

## Usage

Import package and initialize

```python
import authit
auth = authit.connect()
```

To create user

```python
auth.createUser(
    userName="user",
    password="password"
)
```

To authenticate user

```python
validUser = auth.authenticate(
    userName="user",
    password="password"
)