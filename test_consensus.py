#!/usr/bin/env python3
"""
Test consensus analysis functionality.
"""

import pandas as pd
from datetime import datetime
import legends

def test_consensus_analysis():
    print('=== Testing Consensus Analysis ===')
    
    # Create pantheon with all engines
    pantheon = legends.Pantheon.create_default()
    
    # Create sample data (would normally be real market data)
    data = pd.DataFrame({
        'open': [100, 101, 102, 103, 104],
        'high': [101, 102, 103, 104, 105], 
        'low': [99, 100, 101, 102, 103],
        'close': [100.5, 101.5, 102.5, 103.5, 104.5],
        'volume': [1000, 1200, 800, 1500, 900]
    })
    
    try:
        # Test consensus analysis
        consensus = pantheon.get_consensus_analysis(
            symbol="TEST",
            data=data,
            min_reliability=legends.ReliabilityLevel.MEDIUM,
            include_scanner_engines=True
        )
        
        print(f"✅ Consensus analysis completed")
        print(f"📊 Consensus signal: {consensus['consensus_signal']}")
        print(f"🎯 Confidence: {consensus['confidence']:.2f}")
        print(f"⚖️ Consensus score: {consensus['consensus_score']:.2f}")
        print(f"🔧 Qualified engines: {consensus['qualified_engines']}")
        print(f"📈 Total weight: {consensus['total_weight']}")
        
        print("\n🔍 Engine Results:")
        for name, result in consensus['engine_results'].items():
            if 'error' in result:
                print(f"  ❌ {name}: {result['error']}")
            else:
                print(f"  ✅ {name}: weight={result['weight']}, type={result['type']}")
        
        # Test filtering - traditional only
        traditional_consensus = pantheon.get_consensus_analysis(
            symbol="TEST", 
            data=data,
            include_scanner_engines=False
        )
        
        print(f"\n📚 Traditional-only consensus:")
        print(f"  Qualified engines: {traditional_consensus['qualified_engines']}")
        print(f"  Signal: {traditional_consensus['consensus_signal']}")
        
        print("\n🎉 Consensus analysis tests passed!")
        
    except Exception as e:
        print(f"❌ Consensus analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_consensus_analysis()
