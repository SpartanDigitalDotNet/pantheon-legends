#!/usr/bin/env python3
"""Simple test without pandas dependency"""

import legends
from legends import LegendType, ReliabilityLevel

print('✅ Testing Enhanced Type System')
print('Legend Types:', [t.value for t in LegendType])
print('Reliability Levels:', [r.value for r in ReliabilityLevel])

print('\n✅ Creating Pantheon')
pantheon = legends.Pantheon.create_default()

print('\n✅ Available Engines:')
for name, info in pantheon.available_engines.items():
    print(f'  {name}: {info["type"]} ({info["reliability"]})')

print('\n✅ Testing Filtering')
traditional = pantheon.get_engines_by_type(LegendType.TRADITIONAL)
scanner = pantheon.get_engines_by_type(LegendType.SCANNER)
print(f'Traditional Engines: {len(traditional)}')
print(f'Scanner Engines: {len(scanner)}')

high_rel = pantheon.get_engines_by_reliability(ReliabilityLevel.HIGH)
print(f'High Reliability Engines: {len(high_rel)}')

print('\n🎉 All tests passed!')
