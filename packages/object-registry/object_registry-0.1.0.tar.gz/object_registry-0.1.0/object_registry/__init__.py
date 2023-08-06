from __future__ import annotations

import weakref


_registries: dict[type, dict[int, weakref.ReferenceType[ObjectRegistry]]] = {}


class ObjectRegistry:
    """
    Objects of the inheriting class are tracked in a registry.

    The registry stores weak references to objects,
    allowing objects to be garbage collected when
    they are no longer referenced elsewhere in the code.
    If an object is deleted or its reference becomes invalid,
    it is automatically unregistered from the registry.
    """

    def __init_subclass__(cls) -> None:
        """
        Add class to registry to track its instantiated objects.
        """
        _registries[cls] = {}
    
    def __new__(cls, *args, **kwargs) -> ObjectRegistry:
        """
        Register object upon creation.
        """
        obj = super().__new__(cls, *args, **kwargs)
        _registries[cls][id(obj)] = weakref.ref(obj)
        return obj

    def __del__(self) -> None:
        """
        Unregister object upon deletion.
        """
        try:
            del _registries[type(self)][id(self)]
        except KeyError:
            pass


    @classmethod
    def from_id(cls, object_id: int, /) -> ObjectRegistry:
        """
        Get object by ID.
        """
        
        obj = None

        if object_id in _registries[cls]:
            # Attempt to follow the weak reference.
            obj = _registries[cls][object_id]()

            if obj is None:
                # If the reference has been invalidated,
                # delete and unregister the stray object.
                del _registries[cls][object_id]

        if obj is None:
            raise KeyError(f'No object by ID {object_id}.')

        return obj
