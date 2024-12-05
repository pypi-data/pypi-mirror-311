from typing import Callable, TypeVar

__T = TypeVar("__T", bound=Callable[..., ...])


# noinspection PyUnusedLocal
def native(func: __T, onlyFunc: bool = False, /) -> __T:
    """
    Compile this function to native code, bypassing Pylang's default behavior.

    ### Parameters:
    - `onlyFunc` (`bool`, optional):
      - `True`: Only compile this function into native code.
      - `False` (default): Allow Pylang to decide whether to compile the entire module.

    ### Notes:
    - Native compilation can improve performance but may alter Python's behavior.
    - If compilation fails, Pylang will fall back to interpreting the function.

    ### Example:
    ```python
    @native
    def compute(x, y):
        return x ** y

    @native(True)
    def isolated_func(a, b):
        return a + b
    ```
    """
    return func


def pure(func: __T, /) -> __T:
    """
    Mark this function as a pure function, allowing Pylang to precompute its result.

    A pure function is one that always returns the same output for the same input and does not depend on
    or modify external state. By using the `@pure` decorator, Pylang can optimize the function by potentially
    precomputing its result at compile time, eliminating the need to call it at runtime.

    **Note**:
    - Pylang **may** precompute the result of a pure function, but this is not guaranteed. In some cases,
      Pylang may still retain the function call.
    - Make sure that the function truly adheres to the definition of a pure function, i.e., no side effects
      and consistent return values for the same inputs.
    - Using `@pure` on functions that are not pure may lead to incorrect optimizations.

    Example:
        @pure
        def add(a, b):
            return a + b
    """
    return func
