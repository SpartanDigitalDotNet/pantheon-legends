#!/usr/bin/env python3
"""
Test script for the enhanced Pantheon Legends framework.
Tests the new type system and filtering capabilities.
"""

import legends

def test_enhanced_framework():
    print('=== Testing Enhanced Pantheon Legends Framework ===')
    
    # Test imports
    from legends import LegendType, ReliabilityLevel, TraditionalLegendBase, ScannerEngineBase
    print('✅ Type system imports successful')
    
    # Create pantheon with all engines
    pantheon = legends.Pantheon.create_default()
    print('✅ Pantheon created with default engines')
    
    # Test type-aware methods
    engines = pantheon.available_engines
    print(f'📋 Available engines ({len(engines)}):')
    for name, info in engines.items():
        print(f'  - {name}: {info["type"]} ({info["reliability"]})')
    
    # Test filtering by type
    traditional = pantheon.get_engines_by_type(LegendType.TRADITIONAL)
    scanner = pantheon.get_engines_by_type(LegendType.SCANNER)
    print(f'🎯 Traditional engines: {len(traditional)}')
    print(f'🔍 Scanner engines: {len(scanner)}')
    
    # Test filtering by reliability
    high_rel = pantheon.get_engines_by_reliability(ReliabilityLevel.HIGH)
    medium_rel = pantheon.get_engines_by_reliability(ReliabilityLevel.MEDIUM)
    print(f'⭐ High reliability engines: {len(high_rel)}')
    print(f'📊 Medium+ reliability engines: {len(medium_rel)}')
    
    # Test engine properties
    print('\n🔍 Engine Details:')
    for name, engine in pantheon._engines.items():
        print(f'  {name}:')
        print(f'    Type: {engine.legend_type.value}')
        print(f'    Reliability: {engine.reliability_level.value}')
        print(f'    Description: {engine.description}')
    
    print('\n🎉 All tests passed!')
    return True

if __name__ == '__main__':
    test_enhanced_framework()
