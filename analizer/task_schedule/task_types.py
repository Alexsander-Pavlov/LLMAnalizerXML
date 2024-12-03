from typing import Any, Callable, TypeVar, TypeAlias


TD = TypeVar('TD', bound=dict[str, Any])
TemplateFunc: TypeAlias = Callable[[str, str, str, str],
                                   list[dict[str, str]]]
