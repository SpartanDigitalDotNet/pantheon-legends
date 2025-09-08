#!/usr/bin/env python3
"""Quick test of enhanced type system"""

import legends
from legends import LegendType, ReliabilityLevel

def test_type_system():
    # Show available types
    print('Legend Types:', [t.value for t in LegendType])
    print('Reliability Levels:', [r.value for r in ReliabilityLevel])

    # Create pantheon and show engines
    pantheon = legends.Pantheon.create_default()
    print('\nAvailable Engines:')
    for name, info in pantheon.available_engines.items():
        print(f'  {name}: {info["type"]} ({info["reliability"]})')

    # Test filtering
    traditional = pantheon.get_engines_by_type(LegendType.TRADITIONAL)
    scanner = pantheon.get_engines_by_type(LegendType.SCANNER)
    
    print(f'\nFiltering Results:')
    print(f'  Traditional Engines: {len(traditional)}')
    print(f'  Scanner Engines: {len(scanner)}')
    
    high_rel = pantheon.get_engines_by_reliability(ReliabilityLevel.HIGH)
    print(f'  High Reliability Engines: {len(high_rel)}')

if __name__ == '__main__':
    test_type_system()
