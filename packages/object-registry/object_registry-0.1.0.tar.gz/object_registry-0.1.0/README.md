# Object Registry

Keep track of all instantiated objects of a class.

## Installation

```shell
pip install object-registry
```

## Getting started

For any class whose objects you want to track, inherit from `ObjectRegistry` upon definition.

```python
from object_registry import ObjectRegistry

class MyClass(ObjectRegistry): ...
```

Instantiate objects of the derived class as usual. Each object will be automatically added to the registry.

```python
obj = MyClass()
```

Use `from_id` to retrieve an object by its Python object ID.

```python
object_id = id(obj)
retrieved_obj = MyClass.from_id(object_id)
```
