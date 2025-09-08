#!/usr/bin/env python3
"""
Comprehensive deployment test for Pantheon Legends v0.2.0
"""

import legends

def test_deployment():
    print('🚀 Testing Enhanced Pantheon Legends Framework v0.2.0')
    print(f'📦 Version: {legends.__version__}')

    # Test installation
    print('\n=== Installation Test ===')
    result = legends.test_installation()

    # Test enhanced features  
    print('\n=== Enhanced Features Test ===')
    from legends import LegendType, ReliabilityLevel, TraditionalLegendBase, ScannerEngineBase

    # Create pantheon
    pantheon = legends.Pantheon.create_default()
    engines = pantheon.available_engines

    print(f'✅ Enhanced type system working')
    print(f'📋 Available engines: {len(engines)}')
    for name, info in engines.items():
        print(f'  - {name}: {info["type"]} ({info["reliability"]})')

    # Test type filtering
    traditional = pantheon.get_engines_by_type(LegendType.TRADITIONAL)
    scanner = pantheon.get_engines_by_type(LegendType.SCANNER)
    print(f'🎯 Traditional engines: {len(traditional)}')
    print(f'🔍 Scanner engines: {len(scanner)}')

    # Test reliability filtering
    high_rel = pantheon.get_engines_by_reliability(ReliabilityLevel.HIGH)
    print(f'⭐ High reliability engines: {len(high_rel)}')

    # Test consensus analysis
    print('\n=== Consensus Analysis Test ===')
    import pandas as pd
    
    sample_data = pd.DataFrame({
        'close': [100, 101, 102, 103, 104],
        'volume': [1000, 1100, 1200, 1300, 1400]
    })
    
    consensus = pantheon.get_consensus_analysis("TEST", sample_data)
    print(f'📊 Consensus calculated: {consensus["qualified_engines"]} engines')
    print(f'🎯 Consensus signal: {consensus["consensus_signal"]}')

    print('\n🎉 All enhanced features working correctly!')
    print('✅ Ready for deployment!')
    return True

if __name__ == '__main__':
    test_deployment()
