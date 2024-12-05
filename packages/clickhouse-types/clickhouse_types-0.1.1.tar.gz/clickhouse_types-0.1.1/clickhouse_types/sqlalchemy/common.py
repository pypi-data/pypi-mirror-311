from typing import Type, Union

import sqlalchemy as sa
import sqlalchemy.ext.compiler
from sqlalchemy.sql.functions import Function
from sqlalchemy.sql.type_api import to_instance


class ClickHouseTypeEngine(sa.types.TypeEngine):
    def compile(self, dialect=None):
        from clickhouse_sqlalchemy.drivers.base import clickhouse_dialect

        return super(ClickHouseTypeEngine, self).compile(
            dialect=clickhouse_dialect
        )


class Indexable(ClickHouseTypeEngine, sa.types.Indexable):
    pass


class String(sa.types.String, ClickHouseTypeEngine):
    pass


class Int(sa.types.Integer, ClickHouseTypeEngine):
    pass


class Float(sa.types.Float, ClickHouseTypeEngine):
    pass


class Boolean(sa.types.Boolean, ClickHouseTypeEngine):
    pass


class Array(Indexable, ClickHouseTypeEngine):
    __visit_name__ = 'array'

    hashable = False

    def __init__(self, item_type):
        self.item_type = item_type
        self.item_type_impl = to_instance(item_type)
        super(Array, self).__init__()

    def __repr__(self):
        nested_type_str = f'{self.item_type_impl.__module__}.{self.item_type_impl!r}'
        return f'Array({nested_type_str})'

    @property
    def python_type(self):
        return list

    def literal_processor(self, dialect):
        item_processor = self.item_type_impl.literal_processor(dialect)

        def process(value):
            processed_value = []
            for x in value:
                if item_processor:
                    x = item_processor(x)
                processed_value.append(x)
            return '[' + ', '.join(processed_value) + ']'

        return process


class Nullable(ClickHouseTypeEngine):
    __visit_name__ = 'nullable'

    def __init__(self, nested_type):
        self.nested_type = to_instance(nested_type)
        super(Nullable, self).__init__()


class UUID(String):
    __visit_name__ = 'uuid'


class LowCardinality(ClickHouseTypeEngine):
    __visit_name__ = 'lowcardinality'

    def __init__(self, nested_type):
        self.nested_type = to_instance(nested_type)
        super(LowCardinality, self).__init__()

    def __repr__(self):
        nested_type_str = f'{self.nested_type.__module__}.{self.nested_type!r}'
        return f'LowCardinality({nested_type_str})'


class Int8(Int):
    __visit_name__ = 'int8'


class UInt8(Int):
    __visit_name__ = 'uint8'


class Int16(Int):
    __visit_name__ = 'int16'


class UInt16(Int):
    __visit_name__ = 'uint16'


class Int32(Int):
    __visit_name__ = 'int32'


class UInt32(Int):
    __visit_name__ = 'uint32'


class Int64(Int):
    __visit_name__ = 'int64'


class UInt64(Int):
    __visit_name__ = 'uint64'


class Int128(Int):
    __visit_name__ = 'int128'


class UInt128(Int):
    __visit_name__ = 'uint128'


class Int256(Int):
    __visit_name__ = 'int256'


class UInt256(Int):
    __visit_name__ = 'uint256'


class Float32(Float):
    __visit_name__ = 'float32'


class Float64(Float):
    __visit_name__ = 'float64'


class Date(sa.types.Date, ClickHouseTypeEngine):
    __visit_name__ = 'date'


class Date32(sa.types.Date, ClickHouseTypeEngine):
    __visit_name__ = 'date32'


class DateTime(sa.types.DateTime, ClickHouseTypeEngine):
    __visit_name__ = 'datetime'

    def __init__(self, timezone=None):
        super(DateTime, self).__init__()
        self.timezone = timezone


class DateTime64(DateTime, ClickHouseTypeEngine):
    __visit_name__ = 'datetime64'

    def __init__(self, precision=3, timezone=None):
        self.precision = precision
        super(DateTime64, self).__init__(timezone=timezone)


class Enum(sa.types.Enum, ClickHouseTypeEngine):
    __visit_name__ = 'enum'
    native_enum = True

    def __init__(self, *enums, **kw):
        if not enums:
            enums = kw.get('_enums', ())  # passed as keyword

        super(Enum, self).__init__(*enums, **kw, convert_unicode=False)


class Enum8(Enum):
    __visit_name__ = 'enum8'


class Enum16(Enum):
    __visit_name__ = 'enum16'


class Decimal(sa.types.Numeric, ClickHouseTypeEngine):
    __visit_name__ = 'numeric'


class Tuple(Indexable, ClickHouseTypeEngine):
    __visit_name__ = 'tuple'

    def __init__(self, *nested_types):
        self.nested_types = nested_types
        super(Tuple, self).__init__()


class Map(Indexable, ClickHouseTypeEngine):
    __visit_name__ = 'map'

    def __init__(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type
        super(Map, self).__init__()


class AggregateFunction(ClickHouseTypeEngine):
    __visit_name__ = 'aggregatefunction'

    def __init__(
            self,
            agg_func: Union[Function, str],
            *nested_types: Union[Type[ClickHouseTypeEngine], ClickHouseTypeEngine],
    ):
        self.agg_func = agg_func
        self.nested_types = [to_instance(val) for val in nested_types]
        super(AggregateFunction, self).__init__()

    def __repr__(self) -> str:
        type_strs = [f'{val.__module__}.{val!r}' for val in self.nested_types]

        if isinstance(self.agg_func, str):
            agg_str = self.agg_func
        else:
            agg_str = f'sa.func.{self.agg_func}'

        return f"AggregateFunction({agg_str}, {', '.join(type_strs)})"


class SimpleAggregateFunction(ClickHouseTypeEngine):
    __visit_name__ = 'simpleaggregatefunction'

    def __init__(
            self,
            agg_func: Union[Function, str],
            *nested_types: Union[Type[ClickHouseTypeEngine], ClickHouseTypeEngine],
    ):
        self.agg_func = agg_func
        self.nested_types = [to_instance(val) for val in nested_types]
        super(SimpleAggregateFunction, self).__init__()

    def __repr__(self) -> str:
        type_strs = [f'{val.__module__}.{val!r}' for val in self.nested_types]

        if isinstance(self.agg_func, str):
            agg_str = self.agg_func
        else:
            agg_str = f'sa.func.{self.agg_func}'

        return f"SimpleAggregateFunction({agg_str}, {', '.join(type_strs)})"


class Nested(sa.types.TypeEngine):
    __visit_name__ = 'nested'

    def __init__(self, *columns):
        if not columns:
            raise ValueError('columns must be specified for nested type')
        self.columns = columns
        self._columns_dict = {col.name: col for col in columns}
        super(Nested, self).__init__()

    class Comparator(sa.types.UserDefinedType.Comparator):
        def __getattr__(self, key):
            str_key = key.rstrip("_")
            try:
                sub = self.type._columns_dict[str_key]
            except KeyError:
                raise AttributeError(key)
            else:
                original_type = sub.type
                try:
                    sub.type = Array(sub.type)
                    expr = NestedColumn(self.expr, sub)
                    return expr
                finally:
                    sub.type = original_type

    comparator_factory = Comparator


class NestedColumn(sa.ColumnClause):
    def __init__(self, parent, sub_column):
        self.parent = parent
        self.sub_column = sub_column
        if isinstance(self.parent, sa.Label):
            table = self.parent.element.table
        else:
            table = self.parent.table
        super(NestedColumn, self).__init__(
            sub_column.name,
            sub_column.type,
            _selectable=table
        )


@sa.ext.compiler.compiles(NestedColumn)
def _comp(element, compiler, **kw):
    from_labeled_label = False
    if isinstance(element.parent, sa.Label):
        from_labeled_label = True
    return "%s.%s" % (
        compiler.process(element.parent,
                         from_labeled_label=from_labeled_label,
                         within_label_clause=False,
                         within_columns_clause=True),
        compiler.visit_column(element, include_table=False),
    )


class BaseIPComparator(sa.UserDefinedType.Comparator):
    network_class = None

    def _wrap_to_ip(self, x):
        raise NotImplementedError()

    def _split_other(self, other):
        """
        Split values between addresses and networks
        This allows to generate complex filters with both addresses
        and networks in the same IN
        ie in_('10.0.0.0/24', '192.168.0.1')
        """
        addresses = []
        networks = []
        for sub in other:
            sub = self.network_class(sub)
            if sub.prefixlen == sub.max_prefixlen:
                # this is an address
                addresses.append(sub.network_address)
            else:
                networks.append(sub)
        return addresses, networks

    def in_(self, other):
        if isinstance(other, (list, tuple)):
            addresses, networks = self._split_other(other)
            addresses_clause = super(BaseIPComparator, self).in_(
                self._wrap_to_ip(x) for x in addresses
            ) if addresses else None
            networks_clause = sa.or_(*[
                sa.and_(
                    self >= self._wrap_to_ip(net[0]),
                    self <= self._wrap_to_ip(net[-1])
                )
                for net in networks
            ]) if networks else None
            if addresses_clause is not None and networks_clause is not None:
                return sa.or_(addresses_clause, networks_clause)
            elif addresses_clause is not None and networks_clause is None:
                return addresses_clause
            elif networks_clause is not None and addresses_clause is None:
                return networks_clause
            else:
                # other is an empty array
                return super(BaseIPComparator, self).in_(other)

        if not isinstance(other, self.network_class):
            other = self.network_class(other)

        return sa.and_(
            self >= self._wrap_to_ip(other[0]),
            self <= self._wrap_to_ip(other[-1])
        )

    def not_in(self, other):
        if isinstance(other, (list, tuple)):
            addresses, networks = self._split_other(other)
            addresses_clause = super(BaseIPComparator, self).notin_(
                self._wrap_to_ip(x) for x in addresses
            ) if addresses else None
            networks_clause = sa.and_(*[
                sa.or_(
                    self < self._wrap_to_ip(net[0]),
                    self > self._wrap_to_ip(net[-1])
                )
                for net in networks
            ]) if networks else None
            if addresses_clause is not None and networks_clause is not None:
                return sa.and_(addresses_clause, networks_clause)
            elif addresses_clause is not None and networks_clause is None:
                return addresses_clause
            elif networks_clause is not None and addresses_clause is None:
                return networks_clause
            else:
                # other is an empty array
                return super(BaseIPComparator, self).notin_(other)

        if not isinstance(other, self.network_class):
            other = self.network_class(other)

        return sa.or_(
            self < self._wrap_to_ip(other[0]),
            self > self._wrap_to_ip(other[-1])
        )


class IPv4(sa.types.UserDefinedType):
    __visit_name__ = "ipv4"

    cache_ok = True

    def bind_processor(self, dialect):
        def process(value):
            return str(value)

        return process

    def literal_processor(self, dialect):
        bp = self.bind_processor(dialect)

        def process(value):
            return "'%s'" % bp(value)

        return process

    def bind_expression(self, bindvalue):
        if isinstance(bindvalue.value, (list, tuple)):
            bindvalue.value = ([sa.func.toIPv4(x) for x in bindvalue.value])
            return bindvalue
        return sa.func.toIPv4(bindvalue)

    class comparator_factory(BaseIPComparator):
        network_class = sa.IPv4Network

        def _wrap_to_ip(self, x):
            return sa.func.toIPv4(str(x))


class IPv6(sa.types.UserDefinedType):
    __visit_name__ = "ipv6"

    cache_ok = True

    def bind_processor(self, dialect):
        def process(value):
            return str(value)

        return process

    def literal_processor(self, dialect):
        bp = self.bind_processor(dialect)

        def process(value):
            return "'%s'" % bp(value)

        return process

    def bind_expression(self, bindvalue):
        if isinstance(bindvalue.value, (list, tuple)):
            bindvalue.value = ([sa.func.toIPv6(x) for x in bindvalue.value])
            return bindvalue
        return sa.func.toIPv6(bindvalue)

    class comparator_factory(BaseIPComparator):
        network_class = sa.IPv6Network

        def _wrap_to_ip(self, x):
            return sa.func.toIPv6(str(x))
