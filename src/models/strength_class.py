"""
Модели данных для классов прочности стали
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ChemicalElement:
    """Химический элемент с диапазоном значений"""
    symbol: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: str = "%"
    
    def __str__(self) -> str:
        if self.min_value is not None and self.max_value is not None:
            return f"{self.symbol}: {self.min_value}-{self.max_value} {self.unit}"
        elif self.max_value is not None:
            return f"{self.symbol}: ≤ {self.max_value} {self.unit}"
        elif self.min_value is not None:
            return f"{self.symbol}: ≥ {self.min_value} {self.unit}"
        return f"{self.symbol}"


@dataclass
class MechanicalProperty:
    """Механическое свойство с значением и единицами измерения"""
    name: str
    value: float
    unit: str
    temperature: Optional[float] = None
    
    def __str__(self) -> str:
        temp_str = f" при {self.temperature}°C" if self.temperature else ""
        return f"{self.name}: {self.value} {self.unit}{temp_str}"


@dataclass
class StrengthClass:
    """Класс прочности стали"""
    name: str
    gost_standard: str
    chemical_composition: List[ChemicalElement] = field(default_factory=list)
    mechanical_properties: List[MechanicalProperty] = field(default_factory=list)
    deviations: Dict[str, str] = field(default_factory=dict)
    test_requirements: Dict[str, str] = field(default_factory=dict)
    related_standards: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Преобразование в словарь"""
        return {
            'name': self.name,
            'gost_standard': self.gost_standard,
            'chemical_composition': [
                {
                    'symbol': elem.symbol,
                    'min_value': elem.min_value,
                    'max_value': elem.max_value,
                    'unit': elem.unit
                }
                for elem in self.chemical_composition
            ],
            'mechanical_properties': [
                {
                    'name': prop.name,
                    'value': prop.value,
                    'unit': prop.unit,
                    'temperature': prop.temperature
                }
                for prop in self.mechanical_properties
            ],
            'deviations': self.deviations,
            'test_requirements': self.test_requirements,
            'related_standards': self.related_standards,
            'notes': self.notes
        }
