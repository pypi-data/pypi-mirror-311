from __future__ import annotations

import ast

from typing import Any, Iterable, Iterator, Optional, overload, SupportsIndex, Union

from tree_sitter import Node

from .base import Item, JsonStream
from .style import JsonStyle


# TODO haven't figured out whether None can be subclassed
class Null(Item):
    def __init__(
        self,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ):
        super().__init__(original, stream, annealed)

    @classmethod
    def from_json(self, node: Node, stream: JsonStream) -> "Null":
        return self(original=node, stream=stream, annealed=False)

    def to_string(self) -> str:
        return "~"

    def __hash__(self) -> int:
        return hash(None)

    def __eq__(self, other: object) -> bool:
        return other is None or isinstance(other, Null)


class Boolean(Item):
    def __init__(
        self,
        value: bool,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> None:
        super().__init__(original, stream, annealed)
        self.value = value

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Boolean":
        assert node.text is not None
        t = node.text.decode("utf-8")
        return cls(
            value=ast.literal_eval(t.capitalize()),
            original=node,
            stream=stream,
            annealed=False,
        )

    def to_string(self) -> str:
        return str(self).lower()

    def __bool__(self) -> bool:
        return self.value

    def __nonzero__(self) -> bool:
        return self.value

    def __int__(self) -> int:
        return 1 if self else 0

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, bool):
            return other == self.value
        elif isinstance(other, int):
            return other == int(self)
        elif isinstance(other, Boolean):
            return other.value == self.value
        return NotImplemented

    def __repr__(self) -> str:
        return repr(self.value)


class Integer(int, Item):
    def __new__(
        cls,
        value: int,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> Integer:
        return int.__new__(cls, value)

    def __init__(
        self,
        value: int,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> None:
        super().__init__(original, stream, annealed)

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Integer":
        assert node.text is not None
        t = node.text.decode("utf-8")
        return cls(
            value=ast.literal_eval(t), original=node, stream=stream, annealed=False
        )

    def to_string(self) -> str:
        return str(self)


class Float(float, Item):
    def __new__(
        cls,
        value: float,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> Float:
        return float.__new__(cls, value)

    def __init__(
        self,
        value: float,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> None:
        super().__init__(original, stream, annealed)

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> Float:
        assert node.text is not None
        t = node.text.decode("utf-8")
        # Special cases: [+-].inf .nan (case sensitive)
        if t.endswith("inf") or t.endswith("nan"):
            t = t.replace(".", "")
        return cls(value=float(t), original=node, stream=stream, annealed=False)

    def to_string(self) -> str:
        t = str(self)
        if t in ("nan", "inf"):
            return f".{t}"
        elif t == "-inf":
            return f"-.{t[1:]}"
        else:
            return t


class String(str, Item):
    # TODO qs=quoting style somehow
    # TODO decide if the original/stream/annealed default should go in item() instead
    def __new__(
        cls,
        value: str,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> "String":
        return super().__new__(cls, value)

    def __init__(
        self,
        value: str,
        original: Optional[Node] = None,
        stream: Optional[JsonStream] = None,
        annealed: bool = False,
    ) -> None:
        super().__init__(original, stream, annealed)

    @classmethod
    def from_json(
        cls,
        node: Node,
        stream: JsonStream,
    ) -> "String":
        assert node.text is not None
        text = node.text.decode("utf-8")
        value = ast.literal_eval(text)  # TODO
        return cls(value, node, stream, False)

    def to_string(self) -> str:
        return f'"{self}"'  # TODO escapes


class BlockItem(Item):
    _multiline: bool

    @property
    def start_byte(self) -> int:
        assert self._original is not None
        assert self._stream is not None
        if not self._multiline:
            return super().start_byte

        expected_indent = self._original.start_point.column
        leading_whitespace = self._stream._original_bytes[
            self._original.start_byte - expected_indent : self._original.start_byte
        ]
        p = self._original.start_byte - expected_indent
        assert p == 0 or self._stream._original_bytes[p - 1 : p] == b"\n"
        assert (
            leading_whitespace == b" " * expected_indent
        )  # can't handle same-line block like "- - a" yet
        return self._original.start_byte - expected_indent

    @property
    def end_byte(self) -> int:
        assert self._original is not None
        assert self._stream is not None
        if not self._multiline:
            return super().end_byte

        text = self._original.text
        assert isinstance(text, bytes)

        end_byte = self._original.end_byte
        trailing_newline_pos = self._stream._original_bytes.find(b"\n", end_byte)
        if trailing_newline_pos != -1:
            end_byte = trailing_newline_pos + 1
        return end_byte

    def children(self) -> Iterator[Item]:
        raise NotImplementedError

    def mod_style_for_children(self) -> JsonStyle:
        return self._style

    def cascade_style(self, style: JsonStyle) -> None:
        assert hasattr(self, "_style")
        self._style = style
        print("Set", type(self), style.base_indent)
        child_style = self.mod_style_for_children()
        for f in self.children():
            print("  ", type(f))
            if isinstance(f, BlockItem):
                f.cascade_style(child_style)


class Array(BlockItem, list[Item]):

    def __init__(
        self,
        value: list[ArrayItem],
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool,
        multiline: bool,
    ):
        super().__init__(original, stream, annealed)
        if value and not isinstance(value[0], ArrayItem):
            value = [
                ArrayItem(x, original=None, stream=None, annealed=True, multiline=True)
                for x in value
            ]
        list.__init__(self, value)
        self._multiline = multiline
        assert isinstance(value[-1], ArrayItem)
        # self._style is really my children's style
        if self._multiline:
            self._style = value[-1]._style
        else:
            self._style = JsonStyle()  # prevent inference

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Array":
        value = [
            ArrayItem(
                value=child,
                original=child,
                stream=stream,
                annealed=False,
                multiline=False,
            )
            # avoid []
            for child in node.children[1:-1]
            if child.type not in ("comment", "[", ",")
        ]
        return cls(value, original=node, stream=stream, annealed=False, multiline=False)

    def __hash__(self) -> int:  # type: ignore[override]
        return hash(tuple(self))

    def __eq__(self, other: Any) -> bool:
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

    def __iter__(self) -> Iterator[Item]:
        for f in list.__iter__(self):
            yield f.value  # type: ignore[attr-defined]

    def __repr__(self) -> str:
        return "[%s]" % (", ".join(repr(i) for i in self))

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> Item: ...
    @overload
    def __getitem__(self, index: slice, /) -> list[Item]: ...

    def __getitem__(
        self, index: Union[SupportsIndex, slice]
    ) -> Union[Item, list[Item]]:
        if isinstance(index, slice):
            return [v.value for v in list.__getitem__(self, index)]  # type: ignore[attr-defined]
        else:
            return list.__getitem__(self, index).value  # type: ignore[attr-defined,no-any-return]

    @overload
    def __setitem__(self, index: SupportsIndex, value: Item, /) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[Item], /) -> None: ...

    def __setitem__(self, index: Union[SupportsIndex, slice], value: Any) -> None:
        if isinstance(index, slice):
            self.anneal()
            new_value = [
                ArrayItem(
                    value=item(v),
                    original=None,
                    stream=None,
                    annealed=True,
                    multiline=self._multiline,
                    style=self._style,
                )
                for v in value
            ]
            list.__setitem__(self, index, new_value)
            self.cascade_style(self._style)
        else:
            seq_item: ArrayItem = list.__getitem__(self, index)  # type: ignore[assignment]
            seq_item.anneal()
            seq_item._value = item(value)
            seq_item.cascade_style(self._style)

    def __delitem__(self, index: Union[SupportsIndex, slice]) -> None:
        self.anneal()
        list.__delitem__(self, index)

    def append(self, value: Any) -> None:
        self.anneal()
        new_item = ArrayItem(
            value=item(value),
            original=None,
            stream=None,
            annealed=True,
            style=self._style,
        )
        new_item.cascade_style(self._style)
        list.append(self, new_item)

    def extend(self, other: Iterable[Any]) -> None:
        self.anneal()
        for x in other:
            self.append(x)

    def anneal(self, initial: bool = True) -> None:
        if self._annealed:
            return

        if initial and self._stream:
            self._stream.edit(self, self)

        # Apply recursively to all children.
        for x in self:
            if hasattr(x, "anneal"):
                x.anneal(initial=False)

        self._annealed = True

    def to_string(self) -> str:
        buf = []
        if not self._multiline:
            buf.append("[")
            for item in self:
                buf.append(item.to_string())
                buf.append(", ")
            buf.pop()
            buf.append("]")
        else:
            for item in list.__iter__(self):
                s = item.to_string()
                buf.append(s)
        if self._multiline and buf[-1][-1:] != "\n":
            buf.append("\n")
        return "".join(buf)

    def children(self) -> Iterator[Item]:
        for x in list.__iter__(self):
            yield x


class ArrayItem(BlockItem):
    def __init__(
        self,
        value: Union[Item, Node],
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool,
        *,
        multiline: bool = True,
        style: Optional[JsonStyle] = None,
    ):
        super().__init__(original, stream, annealed)
        self._value = value
        self._multiline = multiline
        if original and multiline:
            self._style = self._infer_style()
        else:
            self._style = style or JsonStyle()

    def _infer_style(self) -> JsonStyle:
        assert self._original is not None
        assert self._stream is not None
        # This is the amount of space to the left of "-" regardless of whether
        # it's all whitespace in the case of nested sequences like "- - x"
        expected_indent = self._original.start_point.column

        after_dash = self._stream._original_bytes[
            self._original.children[0].end_byte : self._original.children[1].start_byte
        ]
        if after_dash.startswith(b"\n"):
            after_dash = b" "
        return JsonStyle(
            base_indent=expected_indent,
            sequence_whitespace_after_dash=len(after_dash.decode("utf-8")),
        )

    @property
    def value(self) -> Item:
        if not isinstance(self._value, Item):
            self._value = item(self._value, self._stream)
        return self._value

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Item":
        raise NotImplementedError

    def anneal(self, initial: bool = True) -> None:
        if self._annealed:
            return

        if initial and self._stream:
            self._stream.edit(self, self)
        self.value.anneal(False)
        self._annealed = True

    def children(self) -> Iterator[Item]:
        yield self.value

    def to_string(self) -> str:
        buf = []
        v = self.value.to_string()
        buf.append(" " * self._style.base_indent)
        buf.append("-")
        if v.count("\n") > 1:
            # TODO this is only for block
            buf.append("\n")
        else:
            buf.append(" " * self._style.sequence_whitespace_after_dash)
        buf.append(v)
        if not v.endswith("\n"):
            buf.append("\n")
        return "".join(buf)


class Object(dict[Item, Item], BlockItem):
    # block_mapping > block_mapping_pair > key/value flow_node/block_node > $value

    def __new__(
        cls,
        value: dict[Item, ObjectPair],
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool,
        multiline: bool,
    ) -> "Object":
        return dict.__new__(cls, value)

    def __init__(
        self,
        value: dict[Item, ObjectPair],
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool,
        multiline: bool,
    ) -> None:
        BlockItem.__init__(self, original, stream, annealed)
        self._multiline = multiline
        if not original:
            if not value:
                raise NotImplementedError("Empty dict")
            if not isinstance(list(value.values())[-1], ObjectPair):
                value = {
                    item(k): ObjectPair(
                        item(k), item(v), original=None, stream=None, annealed=True
                    )
                    for k, v in value.items()
                }

        # Really my childrens' style
        # if self._multiline:
        #     self._style = list(value.values())[-1]._style
        # else:
        self._style = JsonStyle()  # prevent inference

        for k, v in value.items():
            dict.__setitem__(self, k, v)

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "Object":
        children = [
            ObjectPair.from_json(node=child, stream=stream)
            for child in node.children
            if child.type not in ("{", "}", ",", "comment")
        ]
        return cls(
            {child.key: child for child in children},
            original=node,
            stream=stream,
            annealed=False,
            multiline=True,
        )

    def children(self) -> Iterator[Item]:
        for v in self.values():
            yield v

    def anneal(self, initial: bool = True) -> None:
        if self._annealed:
            return

        if initial and self._stream:
            self._stream.edit(self, self)

        for item in self.values():
            item.anneal(initial=False)

        self._annealed = True

    def to_string(self) -> str:
        buf = []
        for k, pair in dict.items(self):
            buf.append(pair.to_string())
        if self._multiline and buf[-1][-1:] != "\n":
            buf.append("\n")
        return "".join(buf)

    # TODO other dict methods, like setdefault, get, etc

    def __contains__(self, key: Any) -> bool:
        return dict.__contains__(self, item(key))  # type: ignore[operator]

    def __getitem__(self, key: Any) -> Item:
        return dict.__getitem__(self, item(key)).value  # type: ignore[attr-defined, no-any-return]

    def __setitem__(self, key: Any, value: Any) -> None:
        key = item(key)
        pair: Optional[ObjectPair] = self.get(key, None)  # type: ignore[assignment]
        if pair is not None and self._stream and not self._annealed:
            pair.anneal()
            pair._value = item(value)
            pair.cascade_style(pair._style)
            return
        else:
            self.anneal()
            pair = ObjectPair(
                key,
                item(value),
                original=None,
                stream=self._stream,
                annealed=True,
            )
            pair.cascade_style(self._style)
            dict.__setitem__(self, key, pair)

    def __delitem__(self, key: Any) -> None:
        key = item(key)
        pair = self.get(key, None)
        if pair is not None and self._stream and not self._annealed:
            self._stream.edit(pair, None)
        else:
            self.anneal()

        dict.__delitem__(self, key)


class ObjectPair(BlockItem):
    def __init__(
        self,
        key: Item,
        value: Union[Item, Node],
        original: Optional[Node],
        stream: Optional[JsonStream],
        annealed: bool,
        style: Optional[JsonStyle] = None,
    ):
        super().__init__(original, stream, annealed)
        self._key = key
        self._value = value
        self._multiline = True
        # if original:
        #     self._style = self._infer_style()
        # else:
        self._style = style or JsonStyle()

    def _infer_style(self) -> JsonStyle:
        assert self._original is not None
        assert self._stream is not None
        expected_indent = self._original.start_point.column
        leading_whitespace = self._stream._original_bytes[
            self._original.start_byte - expected_indent : self._original.start_byte
        ]
        assert leading_whitespace == b" " * expected_indent, repr(leading_whitespace)
        before_colon = self._stream._original_bytes[
            self._original.children[0].end_byte : self._original.children[1].start_byte
        ]
        # 3 because key, ":", value
        if len(self._original.children) >= 3:
            tmp = self._stream._original_bytes[
                self._original.children[1]
                .end_byte : self._original.children[2]
                .start_byte
            ]
            after_colon = tmp.split(b"\n")[0]
            on_next_line = tmp[:-1].count(b"\n") > 0
            if on_next_line:
                next_line_indent = len(tmp.split(b"\n")[-1]) - expected_indent
            else:
                next_line_indent = 2  # leave default
        else:
            # implicit null
            after_colon = b""
            on_next_line = False
            next_line_indent = 2  # leave default

        return JsonStyle(
            base_indent=expected_indent,
            mapping_whitespace_before_colon=len(before_colon.decode("utf-8")),
            mapping_flow_space_after_colon=len(after_colon.decode("utf-8")),
            mapping_flow_on_next_line=on_next_line,
            mapping_next_line_indent=next_line_indent,
        )

    @classmethod
    def from_json(cls, node: Node, stream: JsonStream) -> "ObjectPair":
        value: Union[Item, Node]
        children = [
            child for child in node.children if child.type not in ("comment", ":")
        ]
        assert len(children) == 2
        key, value = children
        return cls(
            item(key, stream=stream),
            value,
            original=node,
            stream=stream,
            annealed=False,
        )

    @property
    def key(self) -> Item:
        return self._key

    @property
    def value(self) -> Item:
        if not isinstance(self._value, Item):
            self._value = item(self._value, self._stream)
        return self._value

    # TODO decide if initial makes sense here
    def anneal(self, initial: bool = True) -> None:
        if self._annealed:
            return

        if initial and self._stream:
            self._stream.edit(self, self)

        self.key.anneal(False)
        self.value.anneal(False)

        self._annealed = True

    def mod_style_for_children(self) -> JsonStyle:
        return self._style.indent()

    def children(self) -> Iterator[Item]:
        if isinstance(self.value, BlockItem):
            yield self.value

    def to_string(self) -> str:
        k = self.key.to_string()
        v = self.value.to_string()
        buf = []
        buf.append(" " * self._style.base_indent)
        buf.append(k)
        buf.append(" " * self._style.mapping_whitespace_before_colon)
        buf.append(":")
        if isinstance(self.value, BlockItem):
            buf.append("\n")
        elif self._style.mapping_flow_on_next_line:
            buf.append("\n")
            buf.append(" " * self._style.base_indent)
            buf.append(" " * self._style.mapping_next_line_indent)
        else:
            buf.append(" " * self._style.mapping_flow_space_after_colon)
        buf.append(v)
        if not buf[-1].endswith("\n"):
            buf.append("\n")
        return "".join(buf)


def item(node: Any, stream: Optional[JsonStream] = None) -> Item:
    t = node
    if isinstance(t, Item):
        return t
    elif isinstance(t, Node):
        assert stream is not None
        # if t.type == "flow_node" and t.children[0].type == "flow_sequence":
        #     return Array.from_json(t, stream)
        # elif t.type == "block_node" and t.children[0].type == "block_sequence":
        #     return Array.from_json(t, stream)
        # elif t.type == "block_node" and t.children[0].type == "block_mapping":
        #     return Object.from_json(t, stream)
        # elif (
        #     t.type == "flow_node"
        #     and t.children[0].type == "plain_scalar"
        #     and t.children[0].children[0].type == "string_scalar"
        # ):
        #     return String.from_json(t, stream, QuoteStyle.BARE)
        # elif t.type == "flow_node" and t.children[0].type == "single_quote_scalar":
        #     return String.from_json(t, stream, QuoteStyle.SINGLE)
        # elif t.type == "flow_node" and t.children[0].type == "double_quote_scalar":
        #     return String.from_json(t, stream, QuoteStyle.DOUBLE)
        # elif t.type == "block_node" and t.children[0].type == "block_scalar":
        #     return String.from_json(t, stream, QuoteStyle.BLOCK)
        # elif (
        #     t.type == "flow_node"
        #     and t.children[0].type == "plain_scalar"
        #     and t.children[0].children[0].type == "boolean_scalar"
        # ):
        #     return Boolean.from_json(t, stream)
        if t.type == "number":
            assert isinstance(t.text, bytes)
            if b"." in t.text:  # TODO more accurate float test
                return Float.from_json(t, stream)
            else:
                return Integer.from_json(t, stream)
        elif t.type == "string":
            return String.from_json(t, stream)
        elif t.type == "array":
            return Array.from_json(t, stream)
        elif t.type == "object":
            return Object.from_json(t, stream)
        elif (
            t.type == "flow_node"
            and t.children[0].type == "plain_scalar"
            and t.children[0].children[0].type == "null_scalar"
        ):
            return Null.from_json(t, stream)
        breakpoint()
        raise NotImplementedError(t)
    else:
        if t == None:  # noqa: E711
            return Null()
        elif isinstance(t, bool):
            return Boolean(t)
        elif isinstance(t, int):
            return Integer(t)
        elif isinstance(t, float):
            return Float(t)
        elif isinstance(t, str):
            return String(t)
        elif isinstance(t, dict):
            return Object(t, original=None, stream=None, annealed=True, multiline=True)
        elif isinstance(t, (list, tuple)):
            return Array(
                t, original=None, stream=None, annealed=True, multiline=True  # type: ignore[arg-type]
            )
        else:
            breakpoint()
            raise NotImplementedError(type(t))
