from dataclasses import dataclass
from typing import List, Optional, Union
from iqrfpy.enums.sensor_types import SensorDataSize, SensorTypes, SensorFrcCommands
from iqrfpy.utils.common import Common


@dataclass
class SensorData:
    sensor_type: SensorTypes
    index: int
    name: str
    short_name: str
    unit: str
    decimal_places: int
    frc_commands: List[int]
    value: Optional[Union[int, float, List[int]]]

    def __init__(self, sensor_type: SensorTypes, index: int, name: str, short_name: str, unit: str, decimal_places: int,
                 frc_commands: List[int], value: Optional[Union[int, float, List[int]]] = None):
        self.sensor_type = sensor_type
        self.index = index
        self.name = name
        self.short_name = short_name
        self.unit = unit
        self.decimal_places = decimal_places
        self.frc_commands = frc_commands
        self.value = value


@dataclass
class Temperature:
    type = SensorTypes.TEMPERATURE
    name = 'Temperature'
    short_name = 't'
    unit = '˚C'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class CarbonDioxide:
    type = SensorTypes.CARBON_DIOXIDE
    name = 'Carbon dioxide'
    short_name = 'CO2'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


@dataclass
class VolatileOrganicCompound:
    type = SensorTypes.VOLATILE_ORGANIC_COMPOUND
    name = 'Volatile organic compound'
    short_name = 'VOC'
    unit = 'ppm'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE,
        SensorFrcCommands.FRC_2BYTES
    ]


class ExtraLowVoltage:
    type = SensorTypes.EXTRA_LOW_VOLTAGE
    name = 'Extra-low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class EarthsMagneticField:
    type = SensorTypes.EARTHS_MAGNETIC_FIELD
    name = "Earth's magnetic field"
    short_name = 'B'
    unit = 'T'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class LowVoltage:
    type = SensorTypes.LOW_VOLTAGE
    name = 'Low voltage'
    short_name = 'U'
    unit = 'V'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Current:
    type = SensorTypes.CURRENT
    name = 'Current'
    short_name = 'I'
    unit = 'A'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Power:
    type = SensorTypes.POWER
    name = 'Power'
    short_name = 'E'
    unit = 'W'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class MainsFrequency:
    type = SensorTypes.MAINS_FREQUENCY
    name = 'Mains frequency'
    short_name = 'f'
    unit = 'Hz'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class TimeSpan:
    type = SensorTypes.TIME_SPAN
    name = 'Timespan',
    short_name = 't'
    unit = 's'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Illuminance:
    type = SensorTypes.ILLUMINANCE
    name = 'Illuminance'
    short_name = 'Ev'
    unit = 'lx'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class NitrogenDioxide:
    type = SensorTypes.NITROGEN_DIOXIDE
    name = 'Nitrogen dioxide'
    short_name = 'NO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class SulfurDioxide:
    type = SensorTypes.SULFUR_DIOXIDE
    name = 'Sulfur dioxide'
    short_name = 'SO2'
    unit = 'ppm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class CarbonMonoxide:
    type = SensorTypes.CARBON_MONOXIDE
    name = 'Carbon monoxide'
    short_name = 'CO'
    unit = 'ppm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Ozone:
    type = SensorTypes.OZONE
    name = 'Ozone'
    short_name = 'O3'
    unit = 'ppm'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class AtmosphericPressure:
    type = SensorTypes.ATMOSPHERIC_PRESSURE
    name = 'Atmospheric pressure'
    short_name = 'p'
    unit = 'hPa'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ColorTemperature:
    type = SensorTypes.COLOR_TEMPERATURE
    name = 'Color temperature'
    short_name = 'Tc'
    unit = 'K'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM25:
    type = SensorTypes.PARTICULATES_PM2_5
    name = 'Particulates PM2.5'
    short_name = 'PM2.5'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class SoundPressureLevel:
    type = SensorTypes.SOUND_PRESSURE_LEVEL
    name = 'Sound pressure level'
    short_name = 'Lp'
    unit = 'dB'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Altitude:
    type = SensorTypes.ALTITUDE
    name = 'Altitude'
    short_name = 'h'
    unit = 'm'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Acceleration:
    types = SensorTypes.ACCELERATION
    name = 'Acceleration'
    short_name = 'a'
    unit = 'm/s2'
    decimal_places = 8
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Ammonia:
    types = SensorTypes.AMMONIA
    name = 'Ammonia'
    short_name = 'NH3'
    unit = 'ppm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class Methane:
    type = SensorTypes.METHANE
    name = 'Methane'
    short_name = 'CH4'
    unit = '%'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ShortLength:
    type = SensorTypes.SHORT_LENGTH
    name = 'Short length'
    short_length = 'l'
    unit = 'm'
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM1:
    type = SensorTypes.PARTICULATES_PM1
    name = 'Particulates PM1'
    short_name = 'PM1'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM4:
    type = SensorTypes.PARTICULATES_PM4
    name = 'Particulates PM4'
    short_name = 'PM4'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class ParticulatesPM10:
    type = SensorTypes.PARTICULATES_PM10
    name = 'Particulates PM10'
    short_name = 'PM10'
    unit = 'µg/m3'
    decimal_places = 2
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class TotalVolatileOrganicCompound:
    type = SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND
    name = 'Total volatile organic compound'
    short_name = 'TVOC'
    unit = 'µg/m3'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class NitrogenOxides:
    type = SensorTypes.NITROGEN_OXIDES
    name = 'Nitrogen oxides'
    short_name = 'NOX'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES
    ]


class RelativeHumidity:
    type = SensorTypes.RELATIVE_HUMIDITY
    name = 'Relative humidity'
    short_name = 'RH'
    unit = '%'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class BinaryData7:
    type = SensorTypes.BINARY_DATA7
    name = 'Binary data7'
    short_name = 'bin7'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class PowerFactor:
    type = SensorTypes.POWER_FACTOR
    name = 'Power factor'
    short_name = 'cos θ'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class UVIndex:
    type = SensorTypes.UV_INDEX
    name = 'UV index'
    short_name = 'UV'
    unit = ''
    decimal_places = 3
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class PH:
    type = SensorTypes.PH
    name = 'pH'
    short_name = 'pH'
    unit = ''
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class RSSI:
    type = SensorTypes.RSSI
    name = 'RSSI'
    short_name = 'RSSI'
    unit = 'dBm'
    decimal_places = 1
    frc_commands = [
        SensorFrcCommands.FRC_1BYTE
    ]


class BinaryData30:
    type = SensorTypes.BINARY_DATA30
    name = 'Binary data30'
    short_name = 'bin30'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_2BYTES,
        SensorFrcCommands.FRC_4BYTES
    ]


class Consumption:
    type = SensorTypes.CONSUMPTION
    name = 'Consumption'
    short_name = 'E'
    unit = 'Wh'
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Datetime:
    type = SensorTypes.DATETIME
    name = 'DateTime'
    short_name = 'DateTime'
    unit = ''
    decimal_places = 0
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class TimeSpanLong:
    type = SensorTypes.TIME_SPAN_LONG
    name = 'Timespan long'
    short_name = 't'
    unit = 's'
    decimal_places = 4
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Latitude:
    type = SensorTypes.LATITUDE
    name = 'Latitude'
    short_name = 'LAT'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class Longitude:
    type = SensorTypes.LONGITUDE
    name = 'Longitude'
    short_name = 'LONG'
    unit = '°'
    decimal_places = 7
    frc_commands = [
        SensorFrcCommands.FRC_4BYTES
    ]


class DataBlock:
    type = SensorTypes.DATA_BLOCK
    name = 'Data block'
    short_name = 'datablock'
    unit = ''
    decimal_places = 0
    frc_commands = []


class SensorParser:
    _type_classes = {
        SensorTypes.TEMPERATURE: Temperature,
        SensorTypes.CARBON_DIOXIDE: CarbonDioxide,
        SensorTypes.VOLATILE_ORGANIC_COMPOUND: VolatileOrganicCompound,
        SensorTypes.EXTRA_LOW_VOLTAGE: ExtraLowVoltage,
        SensorTypes.EARTHS_MAGNETIC_FIELD: EarthsMagneticField,
        SensorTypes.LOW_VOLTAGE: LowVoltage,
        SensorTypes.CURRENT: Current,
        SensorTypes.POWER: Power,
        SensorTypes.MAINS_FREQUENCY: MainsFrequency,
        SensorTypes.TIME_SPAN: TimeSpan,
        SensorTypes.ILLUMINANCE: Illuminance,
        SensorTypes.NITROGEN_DIOXIDE: NitrogenDioxide,
        SensorTypes.SULFUR_DIOXIDE: SulfurDioxide,
        SensorTypes.CARBON_MONOXIDE: CarbonMonoxide,
        SensorTypes.OZONE: Ozone,
        SensorTypes.ATMOSPHERIC_PRESSURE: AtmosphericPressure,
        SensorTypes.COLOR_TEMPERATURE: ColorTemperature,
        SensorTypes.PARTICULATES_PM2_5: ParticulatesPM25,
        SensorTypes.SOUND_PRESSURE_LEVEL: SoundPressureLevel,
        SensorTypes.ALTITUDE: Altitude,
        SensorTypes.ACCELERATION: Acceleration,
        SensorTypes.AMMONIA: Ammonia,
        SensorTypes.METHANE: Methane,
        SensorTypes.SHORT_LENGTH: ShortLength,
        SensorTypes.PARTICULATES_PM1: ParticulatesPM1,
        SensorTypes.PARTICULATES_PM4: ParticulatesPM4,
        SensorTypes.PARTICULATES_PM10: ParticulatesPM10,
        SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND: TotalVolatileOrganicCompound,
        SensorTypes.NITROGEN_OXIDES: NitrogenOxides,
        SensorTypes.RELATIVE_HUMIDITY: RelativeHumidity,
        SensorTypes.BINARY_DATA7: BinaryData7,
        SensorTypes.POWER_FACTOR: PowerFactor,
        SensorTypes.UV_INDEX: UVIndex,
        SensorTypes.PH: PH,
        SensorTypes.RSSI: RSSI,
        SensorTypes.BINARY_DATA30: BinaryData30,
        SensorTypes.CONSUMPTION: Consumption,
        SensorTypes.DATETIME: Datetime,
        SensorTypes.TIME_SPAN_LONG: TimeSpanLong,
        SensorTypes.LATITUDE: Latitude,
        SensorTypes.LONGITUDE: Longitude,
        SensorTypes.DATA_BLOCK: DataBlock,
    }

    @classmethod
    def get_sensor_class(cls, sensor_type: Union[SensorTypes, int]):
        if not SensorTypes.has_value(sensor_type):
            raise ValueError(f'Unknown or unsupported sensor type: {sensor_type}')
        if sensor_type not in cls._type_classes:
            raise ValueError(f'Data unavailable for sensor type: {sensor_type}')
        return cls._type_classes[sensor_type]

    @staticmethod
    def _data_len_from_type(sensor_type: int):
        if SensorDataSize.DATA_1BYTE_MIN <= sensor_type <= SensorDataSize.DATA_1BYTE_MAX:
            return 1
        elif SensorDataSize.DATA_2BYTES_MIN <= sensor_type <= SensorDataSize.DATA_2BYTES_MAX:
            return 2
        elif SensorDataSize.DATA_4BYTES_MIN <= sensor_type <= SensorDataSize.DATA_4BYTES_MAX:
            return 4

    @classmethod
    def enumerate_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(dpa)):
            sensor_type_value = dpa[i]
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def enumerate_from_json(cls, json: List[dict]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(json)):
            data = json[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def read_sensors_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        sensor_data = []
        index = 0
        while index < len(dpa):
            sensor_type_value = dpa[index]
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            if sensor_type == SensorTypes.DATA_BLOCK:
                data_length = dpa[index + 1]
                if (index + 1 + data_length) >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
                data = dpa[index + 2:index + 2 + data_length]
            else:
                data_length = cls._data_len_from_type(sensor_type)
                if (index + data_length) >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
                data = cls.convert(sensor_type, dpa[index + 1:index + 1 + data_length])
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data
                )
            )
            index += (data_length + 1)
        return sensor_data

    @classmethod
    def read_sensors_from_json(cls, json: List[dict]) -> List[SensorData]:
        sensor_data = []
        for i in range(len(json)):
            data = json[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise ValueError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = cls._type_classes[sensor_type]
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data['value']
                )
            )
        return sensor_data

    @staticmethod
    def convert(sensor_type: int, values: List[int]):
        match sensor_type:
            case SensorTypes.TEMPERATURE | SensorTypes.LOW_VOLTAGE:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 16.0) if sensor_value != 0x8000 else None
            case SensorTypes.ATMOSPHERIC_PRESSURE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 16.0) if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_DIOXIDE | SensorTypes.VOLATILE_ORGANIC_COMPOUND | SensorTypes.COLOR_TEMPERATURE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0x8000 else None
            case SensorTypes.TIME_SPAN | SensorTypes.ILLUMINANCE | SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND | \
                    SensorTypes.NITROGEN_OXIDES:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0xFFFF else None
            case SensorTypes.EXTRA_LOW_VOLTAGE | SensorTypes.CURRENT:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 1000.0) if sensor_value != 0x8000 else None
            case SensorTypes.MAINS_FREQUENCY | SensorTypes.NITROGEN_DIOXIDE | SensorTypes.SULFUR_DIOXIDE | \
                    SensorTypes.METHANE | SensorTypes.SHORT_LENGTH:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 1000.0) if sensor_value != 0xFFFF else None
            case SensorTypes.EARTHS_MAGNETIC_FIELD:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 10000000.0) if sensor_value != 0x8000 else None
            case SensorTypes.POWER:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0) if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_MONOXIDE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 100.0) if sensor_value != 0xFFFF else None
            case SensorTypes.OZONE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 10000.0) if sensor_value != 0xFFFF else None
            case SensorTypes.PARTICULATES_PM2_5 | SensorTypes.PARTICULATES_PM1 | SensorTypes.PARTICULATES_PM4 | \
                    SensorTypes.PARTICULATES_PM10:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0) if sensor_value != 0x8000 else None
            case SensorTypes.SOUND_PRESSURE_LEVEL:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 16.0) if sensor_value != 0x8000 else None
            case SensorTypes.ALTITUDE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0 - 1024) if sensor_value != 0xFFFF else None
            case SensorTypes.ACCELERATION:
                sensor_value = values[0] + (values[1] << 8)
                return (Common.word_complement(sensor_value) / 256.0) if sensor_value != 0x8000 else None
            case SensorTypes.AMMONIA:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 10.0) if sensor_value != 0xFFFF else None
            case SensorTypes.RELATIVE_HUMIDITY:
                return (values[0] / 2.0) if values[0] != 0xEE else None
            case SensorTypes.BINARY_DATA7:
                aux = values[0] & 0x80
                return values[0] if aux == 0 else None
            case SensorTypes.POWER_FACTOR:
                return (values[0] / 200.0) if values[0] != 0xEE else None
            case SensorTypes.UV_INDEX:
                return (values[0] / 8.0) if values[0] != 0xFF else None
            case SensorTypes.PH:
                return (values[0] / 16.0) if values[0] != 0xFF else None
            case SensorTypes.RSSI:
                return ((values[0] - 254) / 2.0) if values[0] != 0xFF else None
            case SensorTypes.BINARY_DATA30:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if (values[3] & 0x80) == 0 else None
            case SensorTypes.CONSUMPTION | SensorTypes.DATETIME:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.TIME_SPAN_LONG:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return (sensor_value / 16.0) if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.LATITUDE | SensorTypes.LONGITUDE:
                if values[0] == 0xFF or (values[2] & 0x40) == 0:
                    return None
                sensor_value = values[3] + ((values[2] & 0x3F) + (values[0] + (values[1] << 8)) / 10000) / 60
                if (values[2] & 0x80) != 0:
                    sensor_value = -sensor_value
                return sensor_value
            case SensorTypes.DATETIME:
                length = values[0]
                return values[1:1 + length]
            case _:
                return None
