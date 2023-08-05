"""Contruct declarations for some COSEM types and structures."""
# pylint: disable=protected-access
from __future__ import annotations

import datetime
from decimal import Decimal
from typing import Any

import construct  # type: ignore

# See COSEM blue Book table 2 (Common data types) in section 4.1.5 Common data types
# NOTE: Not all types are defined here
CommonDataTypes = construct.Enum(
    construct.Int8ub,
    null_data=0,
    array=1,
    structure=2,
    double_long_unsigned=6,  # Unsigned32 [0...4 294 967 295]
    octet_string=9,  # An ordered sequence of octets (8 bit bytes)
    visible_string=10,  # An ordered sequence of ASCII characters
    integer=15,  # Integer8 [-128...127]
    long=16,  # Integer16 [-32 768...32 767]
    long_unsigned=18,  # Unsigned16 [0...65 535]
    enum=22,  # as CosemPhysicalUnits
)

# See COSEM blue Book table 4 (Enumerated values for physical units) in section 4.3.2 Register
# NOTE: Not all values are defined here
PhysicalUnits = construct.Enum(
    construct.Int8ub, W=27, var=29, Wh=30, varh=32, A=33, V=35
)

# Integer8 [-128...127]
Integer = construct.Int8sb

# Integer16 [-32 768...32 767]
Long = construct.Int16sb

# Unsigned16 [0...65 535]
LongUnsigned = construct.Int16ub

# Unsigned32 [0...4 294 967 295]
DoubleLongUnsigned = construct.Int32ub

VisibleString = construct.PascalString(construct.Int8ub, "ASCII")

OctedStringText = construct.FocusedSeq(
    "value",
    "length" / construct.Int8ub,
    "value" / construct.PaddedString(construct.this.length, "ASCII"),
)

ObisCode = construct.ExprAdapter(
    construct.Int8ub[6],
    decoder=lambda obj, ctx: ".".join(f"{b}" for b in obj),
    encoder=lambda obj, ctx: [int(part) for part in obj.split(".")],
)

OptionalDateTimeByte = construct.ExprAdapter(
    construct.Int8ub,
    decoder=lambda obj, ctx: obj if obj != 0xFF else None,
    encoder=lambda obj, ctx: obj if obj is not None else 0xFF,
)

# See COSEM blue Book section 4.1.6.1 Date and time formats
DateTime = construct.Struct(
    construct.Const(0x0C, construct.Int8ub),  # expect length 12
    "year" / construct.Int16ub,
    "month" / construct.Int8ub,
    "day_of_month" / construct.Int8ub,
    "day_of_week" / construct.Int8ub,
    "hour" / OptionalDateTimeByte,
    "minute" / OptionalDateTimeByte,
    "second" / OptionalDateTimeByte,
    "hundredths_of_second" / OptionalDateTimeByte,
    "deviation"
    / construct.ExprAdapter(
        construct.Int16sb,
        decoder=lambda obj, ctx: obj if obj != -0x8000 else None,
        encoder=lambda obj, ctx: obj if obj is not None else -0x8000,
    )
    * ("Range -720...+720 in minutes of local time to UTC. 0x8000 = not specified"),
    "clock_status_byte" / construct.Peek(OptionalDateTimeByte),
    "clock_status"
    / construct.If(
        construct.this.clock_status_byte != 0xFF,
        construct.BitStruct(
            "invalid_value"
            / construct.BitsInteger(1)
            * (
                "Time could not be recovered after an incident. Detailed conditions are "
                "manufacturer specific (for example after the power to the clock has been "
                "interrupted). For a valid status, bit 0 shall not be set if bit 1 is set."
            ),
            "doubtful_value"
            / construct.BitsInteger(1)
            * (
                "Time could be recovered after an incident but the value cannot be guaranteed. "
                "Detailed conditions are manufacturer specific. For a valid status, bit 1 shall "
                "not be set if bit 0 is set."
            ),
            "different_clock_base"
            / construct.BitsInteger(1)
            * (
                "Bit is set if the basic timing information for the clock at the actual moment "
                "is taken from a timing source different from the source specified in clock_base."
            ),
            "invalid_clock_status"
            / construct.BitsInteger(1)
            * (
                "This bit indicates that at least one bit of the clock status is invalid. "
                "Some bits may be correct. The exact meaning shall be explained in the "
                "manufacturer's documentation."
            ),
            construct.BitsInteger(3),
            "daylight_saving_active"
            / construct.BitsInteger(1)
            * "Flag set to true: the transmitted time contains the daylight saving deviation (summer time).",
        ),
    ),
    construct.If(construct.this.clock_status_byte == 0xFF, construct.Int8ub),
    "datetime"
    / construct.Computed(
        lambda ctx: datetime.datetime(
            ctx.year,
            ctx.month,
            ctx.day_of_month,
            ctx.hour,
            ctx.minute,
            ctx.second,
            ctx.hundredths_of_second * 10000
            if ctx.hundredths_of_second is not None
            else 0,
            datetime.timezone(datetime.timedelta(minutes=ctx.deviation * -1))
            if ctx.deviation is not None
            else None,
        )
    ),
)

NullData: construct.Struct = construct.Struct(
    "_null_peek" / construct.Peek(CommonDataTypes),
    "value"
    / construct.If(
        CommonDataTypes.null_data == construct.this._null_peek,
        construct.GreedyRange(
            construct.Const(CommonDataTypes.null_data, CommonDataTypes)
        ),
    ),
)


# field types


def _type_code_to_type(
    type_code: construct.Enum,
) -> Any:
    """Map COSEM common data type codes to type."""
    return construct.Switch(
        type_code,
        {
            CommonDataTypes.null_data: NullData,
            CommonDataTypes.integer: Integer,
            CommonDataTypes.long: Long,
            CommonDataTypes.long_unsigned: LongUnsigned,
            CommonDataTypes.double_long_unsigned: DoubleLongUnsigned,
            CommonDataTypes.octet_string: construct.Select(DateTime, OctedStringText),
            CommonDataTypes.visible_string: VisibleString,
        },
        default=construct.Error,
    )


Field = construct.FocusedSeq(
    "value",
    "content_type" / CommonDataTypes,
    "value" / _type_code_to_type(construct.this.content_type),
)

ObisCodeOctedStringField = construct.FocusedSeq(
    "code",
    construct.Const(
        CommonDataTypes.octet_string, CommonDataTypes
    ),  # expect octet string (bytes)
    construct.Const(6, construct.Int8ub),  # expect length 6
    "code" / ObisCode,
)

VisibleStringField = construct.FocusedSeq(
    "value",
    construct.Const(
        CommonDataTypes.visible_string, CommonDataTypes
    ),  # An ordered sequence of ASCII characters
    "value" / VisibleString,
)

OctedStringTextField = construct.FocusedSeq(
    "value",
    construct.Const(
        CommonDataTypes.octet_string, CommonDataTypes
    ),  # expect octet string (bytes)
    "value" / OctedStringText,
)

IntegerField = construct.FocusedSeq(
    "value",
    construct.Const(CommonDataTypes.integer, CommonDataTypes),  # expect integer
    "value" / Integer,
)

DoubleLongUnsignedField = construct.FocusedSeq(
    "value",
    construct.Const(CommonDataTypes.double_long_unsigned, CommonDataTypes),
    "value" / DoubleLongUnsigned,
)

UnitField = construct.FocusedSeq(
    "value",
    construct.Const(CommonDataTypes.enum, CommonDataTypes),  # expect enum
    "value" / PhysicalUnits,
)

Scaler = construct.Struct(
    "exponent"
    / IntegerField,  # This is the exponent (to the base of 10) of the multiplication factor.
    "scale" / construct.Computed(lambda ctx: Decimal(10) ** ctx.exponent),
)

ScalerUnitField = construct.Struct(
    construct.Const(CommonDataTypes.structure, CommonDataTypes),  # expect structure
    construct.Const(2, construct.Int8ub),  # expect length 2
    "scaler" / Scaler,
    "unit" / UnitField,
)

DateTimeField = construct.FocusedSeq(
    "value",
    construct.Const(CommonDataTypes.octet_string, CommonDataTypes),
    "value" / DateTime,
)

OptionalDateTimeField = construct.FocusedSeq(
    "value",
    "content_type" / CommonDataTypes,
    construct.Check(
        lambda ctx: ctx.content_type
        in (CommonDataTypes.null_data, CommonDataTypes.octet_string)
    ),
    "value"
    / construct.If(construct.this.content_type != CommonDataTypes.null_data, DateTime),
)


LongInvokeIdAndPriority = construct.BitStruct(
    "invoke_id" / construct.BitsInteger(24),
    construct.Padding(4),
    "self_descriptive"
    / construct.Enum(construct.BitsInteger(1), NotSelfDescriptive=0, SelfDescriptive=1),
    "processing_option"
    / construct.Enum(construct.BitsInteger(1), ContinueOnError=0, BreakOnError=1),
    "service_class"
    / construct.Enum(construct.BitsInteger(1), Unconfirmed=0, Confirmed=1),
    "priority" / construct.Enum(construct.BitsInteger(1), Normal=0, High=1),
)

ApduTag = construct.Enum(construct.Int8ub, data_notification=0x0F)


def _get_apdu_struct(notification_body: construct.Struct) -> construct.Struct:
    return construct.Struct(
        "Tag" / ApduTag,
        "LongInvokeIdAndPriority" / LongInvokeIdAndPriority,
        "_datetimestartbyte" / construct.Peek(CommonDataTypes),
        "DateTime"
        / construct.Switch(
            construct.this._datetimestartbyte,
            {
                CommonDataTypes.null_data: construct.Byte,
                CommonDataTypes.octet_string: DateTimeField,
            },
            default=DateTime,
        ),
        "notification_body" / notification_body,
    )


def get_llc_pdu_struct(notification_body: construct.Struct) -> construct.Struct:
    """Get a LLC PDU struct wrapping supplied notification body."""
    return construct.Struct(
        "dsap" / construct.Int8ub,
        "ssap" / construct.Int8ub,
        "control" / construct.Int8ub,
        "information" / _get_apdu_struct(notification_body),
    )
