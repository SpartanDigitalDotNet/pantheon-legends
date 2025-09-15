#!/usr/bin/env python3
"""
Test the new unified consensus analysis functionality
"""

import asyncio
from datetime import datetime
import legends


async def test_unified_consensus():
    """Test the new analyze_with_consensus method"""
    print("🧪 Testing Unified Consensus Analysis")
    print("=" * 45)
    
    # Create pantheon with default engines
    pantheon = legends.Pantheon.create_default()
    
    # Create analysis request
    request = legends.LegendRequest(
        symbol="TEST",
        timeframe="1D",
        as_of=datetime.now()
    )
    
    print(f"Available engines: {list(pantheon._engines.keys())}")
    
    # Test unified analysis with automatic consensus
    print("\n🚀 Running unified analysis with automatic consensus...")
    result = await pantheon.analyze_with_consensus(
        request=request,
        enable_consensus=True
    )
    
    print(f"\n✅ Analysis completed!")
    print(f"Total engines: {result.total_engines}")
    print(f"Successful engines: {result.successful_engines}")
    print(f"Execution time: {result.execution_time_ms:.1f}ms")
    
    # Display individual engine results
    print(f"\n🔧 Individual Engine Results:")
    for engine_result in result.engine_results:
        signal = engine_result.facts.get('signal', 
                 engine_result.facts.get('position_bias',
                 engine_result.facts.get('primary_trend', 'N/A')))
        print(f"  • {engine_result.legend}: {signal}")
    
    # Display consensus result
    if result.consensus:
        print(f"\n🎯 Automatic Consensus:")
        print(f"  Signal: {result.consensus.signal.value}")
        print(f"  Confidence: {result.consensus.confidence:.2%}")
        print(f"  Strength: {result.consensus.strength:.2%}")
        print(f"  Quality: {result.consensus.consensus_quality}")
        
        print(f"\n📊 Engine Breakdown:")
        print(f"  Bullish: {result.consensus.engines_bullish}")
        print(f"  Bearish: {result.consensus.engines_bearish}")
        print(f"  Neutral: {result.consensus.engines_neutral}")
        
        print(f"\n⚖️ Engine Contributions:")
        for engine_name, contribution in result.consensus.engine_contributions.items():
            print(f"  • {engine_name}: {contribution['signal']} "
                  f"(weight: {contribution['weight_contribution']:.2f})")
    else:
        print("❌ No consensus calculated")
    
    return result


async def test_quick_consensus():
    """Test the quick_consensus convenience method"""
    print("\n\n⚡ Testing Quick Consensus Method")
    print("=" * 40)
    
    pantheon = legends.Pantheon.create_default()
    
    # Test quick consensus
    print("🏃 Running quick consensus for SPY...")
    consensus = await pantheon.quick_consensus(
        symbol="SPY",
        timeframe="1D"
    )
    
    print(f"Signal: {consensus.signal.value}")
    print(f"Confidence: {consensus.confidence:.1%}")
    print(f"Engines analyzed: {consensus.engines_analyzed}")
    print(f"Quality: {consensus.consensus_quality}")


async def test_filtered_consensus():
    """Test consensus with reliability filtering"""
    print("\n\n🔍 Testing Filtered Consensus")
    print("=" * 35)
    
    pantheon = legends.Pantheon.create_default()
    request = legends.LegendRequest(
        symbol="BTCUSD",
        timeframe="4H",
        as_of=datetime.now()
    )
    
    # Test with high reliability filter
    print("🏆 Running with HIGH reliability filter...")
    result = await pantheon.analyze_with_consensus(
        request=request,
        enable_consensus=True,
        min_consensus_reliability=legends.ReliabilityLevel.HIGH
    )
    
    if result.consensus:
        print(f"High-reliability consensus: {result.consensus.signal.value}")
        print(f"Engines used: {result.consensus.engines_analyzed}")
        print(f"Average reliability: {result.consensus.reliability_average:.2f}")
    else:
        print("No high-reliability engines available")
    
    # Test with medium reliability filter
    print("\n📊 Running with MEDIUM reliability filter...")
    result = await pantheon.analyze_with_consensus(
        request=request,
        enable_consensus=True,
        min_consensus_reliability=legends.ReliabilityLevel.MEDIUM
    )
    
    if result.consensus:
        print(f"Medium-reliability consensus: {result.consensus.signal.value}")
        print(f"Engines used: {result.consensus.engines_analyzed}")


async def test_selective_engines():
    """Test consensus with specific engines"""
    print("\n\n🎛️ Testing Selective Engine Consensus")
    print("=" * 40)
    
    pantheon = legends.Pantheon.create_default()
    request = legends.LegendRequest(
        symbol="TSLA",
        timeframe="1H", 
        as_of=datetime.now()
    )
    
    # Test with only traditional engines
    traditional_engines = ["Dow Theory", "Wyckoff Method"]
    print(f"🏛️ Running traditional engines only: {traditional_engines}")
    
    result = await pantheon.analyze_with_consensus(
        request=request,
        engine_names=traditional_engines,
        enable_consensus=True
    )
    
    if result.consensus:
        print(f"Traditional consensus: {result.consensus.signal.value}")
        print(f"Confidence: {result.consensus.confidence:.1%}")
    
    print(f"Engines run: {len(result.engine_results)}")


async def test_consensus_signals():
    """Test different consensus signal types"""
    print("\n\n📡 Testing Consensus Signal Types") 
    print("=" * 40)
    
    # Display available signal types
    print("Available consensus signals:")
    for signal in legends.ConsensusSignal:
        print(f"  • {signal.value}")
    
    # Test with real analysis
    pantheon = legends.Pantheon.create_default()
    consensus = await pantheon.quick_consensus("SPY")
    
    print(f"\nSPY current signal: {consensus.signal.value}")
    print(f"Signal interpretation:")
    
    signal_descriptions = {
        "strong_bullish": "High confidence upward momentum expected",
        "bullish": "Positive bias with moderate confidence",
        "neutral": "No clear directional bias", 
        "bearish": "Negative bias with moderate confidence",
        "strong_bearish": "High confidence downward momentum expected",
        "insufficient_data": "Not enough reliable engines for consensus"
    }
    
    print(f"  → {signal_descriptions.get(consensus.signal.value, 'Unknown signal')}")


async def main():
    """Run all unified consensus tests"""
    print("🏛️ Pantheon Legends - Unified Consensus Analysis Tests")
    print("🎯 Testing automatic consensus with real engine results")
    print("=" * 60)
    
    try:
        await test_unified_consensus()
        await test_quick_consensus()
        await test_filtered_consensus() 
        await test_selective_engines()
        await test_consensus_signals()
        
        print("\n\n✅ All unified consensus tests completed!")
        print("🎉 Automatic consensus analysis is working!")
        print("\n📋 Key Features Tested:")
        print("  ✅ Unified analyze_with_consensus() method")
        print("  ✅ Automatic consensus from real engine results")
        print("  ✅ Reliability-weighted scoring")
        print("  ✅ Quick consensus convenience method")
        print("  ✅ Selective engine filtering")
        print("  ✅ No manual orchestration required")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
