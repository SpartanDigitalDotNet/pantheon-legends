#!/usr/bin/env python3
"""
Examples demonstrating the new unified consensus analysis functionality.

This shows how the enhanced pantheon-legends framework eliminates manual
orchestration and provides automatic consensus calculation.
"""

import asyncio
from datetime import datetime
from legends import (
    Pantheon, AnalysisResult, ConsensusResult,
    LegendRequest, ReliabilityLevel,
    quick_analysis, consensus_only
)


async def example_unified_analysis():
    """Example: One-call analysis with automatic consensus"""
    print("🎯 Example: Unified Analysis with Automatic Consensus")
    print("=" * 55)
    
    # Create Pantheon instance
    pantheon = Pantheon.create_default()
    
    # Single method call - runs engines AND calculates consensus
    result = await pantheon.analyze_with_consensus(
        request=LegendRequest(
            symbol="AAPL",
            timeframe="1D",
            as_of=datetime.now()
        ),
        enable_consensus=True
    )
    
    print(f"✅ Analysis complete in {result.execution_time_ms:.1f}ms")
    print(f"📊 Engines: {result.successful_engines}/{result.total_engines}")
    
    # Individual results
    print(f"\n🔧 Individual Engine Results:")
    for engine_result in result.engine_results:
        signal = engine_result.facts.get('primary_trend', 
                 engine_result.facts.get('position_bias', 'N/A'))
        print(f"  • {engine_result.legend}: {signal}")
    
    # Automatic consensus
    if result.consensus:
        print(f"\n🎯 Automatic Consensus:")
        print(f"  Signal: {result.consensus.signal.value}")
        print(f"  Confidence: {result.consensus.confidence:.1%}")
        print(f"  Quality: {result.consensus.consensus_quality}")
        
        print(f"\n⚖️ Engine Contributions:")
        for name, contrib in result.consensus.engine_contributions.items():
            print(f"  • {name}: {contrib['signal']} (weight: {contrib['weight_contribution']:.2f})")


async def example_convenience_functions():
    """Example: Using convenience functions for quick analysis"""
    print("\n\n⚡ Example: Convenience Functions")
    print("=" * 35)
    
    # Quick analysis - no Pantheon setup required
    print("🚀 Quick analysis (all-in-one)...")
    result = await quick_analysis(
        symbol="SPY",
        timeframe="4H",
        with_consensus=True
    )
    
    print(f"Result: {result.consensus.signal.value if result.consensus else 'No consensus'}")
    
    # Consensus only - minimal overhead
    print("\n🎯 Consensus-only analysis...")
    consensus = await consensus_only(
        symbol="TSLA",
        min_reliability=ReliabilityLevel.MEDIUM
    )
    
    print(f"TSLA consensus: {consensus.signal.value} ({consensus.confidence:.1%})")


async def example_reliability_filtering():
    """Example: Filtering engines by reliability for consensus"""
    print("\n\n🔍 Example: Reliability-Filtered Consensus")
    print("=" * 45)
    
    pantheon = Pantheon.create_default()
    request = LegendRequest(symbol="BTCUSD", timeframe="1H", as_of=datetime.now())
    
    # High reliability consensus
    high_rel_result = await pantheon.analyze_with_consensus(
        request=request,
        min_consensus_reliability=ReliabilityLevel.HIGH
    )
    
    if high_rel_result.consensus:
        print(f"🏆 High-reliability consensus:")
        print(f"  Signal: {high_rel_result.consensus.signal.value}")
        print(f"  Engines: {high_rel_result.consensus.engines_analyzed}")
        print(f"  Avg reliability: {high_rel_result.consensus.reliability_average:.2f}")
    
    # Medium reliability consensus  
    med_rel_result = await pantheon.analyze_with_consensus(
        request=request,
        min_consensus_reliability=ReliabilityLevel.MEDIUM
    )
    
    if med_rel_result.consensus:
        print(f"\n📊 Medium-reliability consensus:")
        print(f"  Signal: {med_rel_result.consensus.signal.value}")
        print(f"  Engines: {med_rel_result.consensus.engines_analyzed}")


async def example_selective_engines():
    """Example: Running consensus with specific engines"""
    print("\n\n🎛️ Example: Selective Engine Consensus")
    print("=" * 40)
    
    pantheon = Pantheon.create_default()
    request = LegendRequest(symbol="NVDA", timeframe="1D", as_of=datetime.now())
    
    # Traditional engines only
    traditional_result = await pantheon.analyze_with_consensus(
        request=request,
        engine_names=["Dow Theory", "Wyckoff Method"],
        enable_consensus=True
    )
    
    if traditional_result.consensus:
        print(f"🏛️ Traditional engines consensus:")
        print(f"  Signal: {traditional_result.consensus.signal.value}")
        print(f"  Confidence: {traditional_result.consensus.confidence:.1%}")
    
    # All engines
    all_result = await pantheon.analyze_with_consensus(
        request=request,
        enable_consensus=True
    )
    
    if all_result.consensus:
        print(f"\n🌐 All engines consensus:")
        print(f"  Signal: {all_result.consensus.signal.value}")
        print(f"  Confidence: {all_result.consensus.confidence:.1%}")


async def example_comparison_old_vs_new():
    """Example: Comparing old manual vs new automatic approach"""
    print("\n\n🔄 Example: Old vs New Approach")
    print("=" * 35)
    
    pantheon = Pantheon.create_default()
    request = LegendRequest(symbol="MSFT", timeframe="1D", as_of=datetime.now())
    
    print("❌ OLD APPROACH (Manual Orchestration):")
    print("   1. results = await pantheon.run_all_legends_async(request)")
    print("   2. signals = extract_signals_from_results(results)")
    print("   3. consensus = calculate_manual_consensus(signals)")
    print("   → Multiple steps, error-prone, manual aggregation")
    
    print("\n✅ NEW APPROACH (Automatic Consensus):")
    print("   result = await pantheon.analyze_with_consensus(request)")
    print("   → One call, automatic consensus, no manual orchestration")
    
    # Demonstrate new approach
    result = await pantheon.analyze_with_consensus(request)
    
    print(f"\n📊 Result:")
    print(f"  Individual results: {len(result.engine_results)}")
    print(f"  Consensus: {result.consensus.signal.value if result.consensus else 'None'}")
    print(f"  Quality: {result.consensus.consensus_quality if result.consensus else 'N/A'}")


async def example_error_handling():
    """Example: Robust error handling in unified analysis"""
    print("\n\n🛡️ Example: Error Handling")
    print("=" * 28)
    
    pantheon = Pantheon.create_default()
    
    # Even if some engines fail, consensus can still work
    try:
        result = await pantheon.analyze_with_consensus(
            request=LegendRequest(
                symbol="ERROR_TEST",
                timeframe="1D", 
                as_of=datetime.now()
            )
        )
        
        print(f"✅ Analysis completed despite potential errors")
        print(f"  Successful engines: {result.successful_engines}")
        print(f"  Consensus available: {result.consensus is not None}")
        
        if result.consensus:
            print(f"  Consensus quality: {result.consensus.consensus_quality}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


async def main():
    """Run all unified consensus examples"""
    print("🏛️ Pantheon Legends - Unified Consensus Examples")
    print("🎯 Automatic consensus with NO manual orchestration")
    print("=" * 60)
    
    try:
        await example_unified_analysis()
        await example_convenience_functions()
        await example_reliability_filtering()
        await example_selective_engines()
        await example_comparison_old_vs_new()
        await example_error_handling()
        
        print("\n\n🎉 All examples completed successfully!")
        print("\n📋 Key Benefits Demonstrated:")
        print("  ✅ No manual orchestration required")
        print("  ✅ Automatic consensus from real engine results")
        print("  ✅ Reliability-weighted scoring")
        print("  ✅ One-call unified analysis")
        print("  ✅ Flexible filtering and selection")
        print("  ✅ Robust error handling")
        print("  ✅ Convenience functions for common use cases")
        
        print("\n🚀 Ready for production use!")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
