import math


# Each factor converts the unit to its family's base unit.
# For example, 1 kV = 1000 V.
UNITS = {
    "mV": ("voltage", 0.001),
    "V": ("voltage", 1.0),
    "kV": ("voltage", 1000.0),
    "mA": ("current", 0.001),
    "A": ("current", 1.0),
    "ohm": ("resistance", 1.0),
    "kohm": ("resistance", 1_000.0),
    "Mohm": ("resistance", 1_000_000.0),
    "mW": ("power", 0.001),
    "W": ("power", 1.0),
    "kW": ("power", 1000.0),
    "mm": ("length", 0.001),
    "cm": ("length", 0.01),
    "m": ("length", 1.0),
    "km": ("length", 1000.0),
    "in": ("length", 0.0254),
}


def convert_units(value, from_unit, to_unit):
    """Convert between units in the same measurement family."""
    if from_unit not in UNITS or to_unit not in UNITS:
        return {"error": "One or both units are unsupported."}

    from_family, from_factor = UNITS[from_unit]
    to_family, to_factor = UNITS[to_unit]

    if from_family != to_family:
        return {"error": f"Cannot convert {from_unit} to {to_unit}."}

    if not math.isfinite(value):
        return {"error": "Enter a finite number."}

    converted = value * (from_factor / to_factor)

    if not math.isfinite(converted):
        return {"error": "The converted value is outside the supported range."}

    if converted > value:
        direction = "up"
    elif converted < value:
        direction = "down"
    else:
        direction = "unchanged"

    return {
        "original_value": value,
        "original_unit": from_unit,
        "converted_value": converted,
        "converted_unit": to_unit,
        "numeric_direction": direction,
    }


def calculate_dc_power(voltage_v, current_a):
    """Calculate DC power in watts using P = V × I."""
    if not math.isfinite(voltage_v) or not math.isfinite(current_a):
        return {"error": "Voltage and current must be finite numbers."}

    power_w = voltage_v * current_a

    if not math.isfinite(power_w):
        return {"error": "The calculated power is outside the supported range."}

    return {
        "formula": "P = V × I",
        "voltage_v": voltage_v,
        "current_a": current_a,
        "power_w": power_w,
    }


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "convert_units",
        "description": "Convert a value between compatible engineering units.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {"type": "number"},
                "from_unit": {"type": "string", "enum": list(UNITS)},
                "to_unit": {"type": "string", "enum": list(UNITS)},
            },
            "required": ["value", "from_unit", "to_unit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "calculate_dc_power",
        "description": "Calculate DC power in watts from volts and amps.",
        "parameters": {
            "type": "object",
            "properties": {
                "voltage_v": {"type": "number"},
                "current_a": {"type": "number"},
            },
            "required": ["voltage_v", "current_a"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]