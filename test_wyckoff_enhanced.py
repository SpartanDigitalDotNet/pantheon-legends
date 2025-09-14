"""
Test script for the enhanced Wyckoff Method engine.

This script validates the WyckoffMethodEnhanced implementation and demonstrates
the comprehensive analysis capabilities including the three Wyckoff Laws,
market phase detection, event analysis, and smart money activity.
"""

import asyncio
from datetime import datetime
from legends import WyckoffLegendEngine, LegendRequest, LegendProgress

async def progress_callback(progress: LegendProgress):
    """Progress callback to monitor analysis stages."""
    print(f"[{progress.legend}] {progress.stage}: {progress.percent:.1f}% - {progress.note}")

async def test_wyckoff_enhanced():
    """Test the enhanced Wyckoff Method engine."""
    print("=== Enhanced Wyckoff Method Engine Test ===\n")
    
    # Create the enhanced engine
    engine = WyckoffLegendEngine()
    
    print(f"Engine: {engine.name}")
    print(f"Description: {engine.description}")
    print(f"Type: {engine.legend_type.value}\n")
    
    # Create test request
    request = LegendRequest(
        symbol="SPY",
        timeframe="1D",
        as_of=datetime.now()
    )
    
    print(f"Analyzing {request.symbol} on {request.timeframe} timeframe...")
    print("=" * 60)
    
    # Run the analysis
    result = await engine.run_async(request, progress_callback)
    
    print("\n" + "=" * 60)
    print("ENHANCED WYCKOFF ANALYSIS RESULTS")
    print("=" * 60)
    
    # Display fundamental laws
    print("\n🔍 WYCKOFF FUNDAMENTAL LAWS:")
    laws = result.facts
    
    print(f"\n  📊 Law of Supply & Demand:")
    supply_demand = laws["law_of_supply_demand"]
    print(f"    Market Balance: {supply_demand['market_balance']}")
    print(f"    Supply Pressure: {supply_demand['supply_pressure']:.2f}")
    print(f"    Demand Strength: {supply_demand['demand_strength']:.2f}")
    print(f"    Validation: {supply_demand['law_validation']}")
    
    print(f"\n  🎯 Law of Cause & Effect:")
    cause_effect = laws["law_of_cause_effect"]
    print(f"    Accumulation Period: {cause_effect['accumulation_period']}")
    print(f"    Cause Magnitude: {cause_effect['cause_magnitude']:.2f}")
    print(f"    Expected Effect: {cause_effect['expected_effect']}")
    print(f"    Price Objective: ${cause_effect['price_objective']:.2f}")
    print(f"    Validation: {cause_effect['law_validation']}")
    
    print(f"\n  ⚡ Law of Effort & Result:")
    effort_result = laws["law_of_effort_result"]
    print(f"    Effort Level: {effort_result['effort_level']:.2f}")
    print(f"    Result Achieved: {effort_result['result_achieved']:.2f}")
    print(f"    Harmony: {effort_result['effort_result_harmony']}")
    print(f"    Divergence: {effort_result['divergence_type']}")
    print(f"    Validation: {effort_result['law_validation']}")
    
    # Display market phase
    print(f"\n📈 MARKET PHASE ANALYSIS:")
    print(f"    Current Phase: {laws['current_phase']}")
    print(f"    Confidence: {laws['phase_confidence']:.2f}")
    print(f"    Progression: {laws['phase_progression']:.2f}")
    
    # Display Wyckoff events
    print(f"\n🎪 WYCKOFF EVENTS DETECTED:")
    events = laws["detected_events"]
    confidence_scores = laws["event_confidence_scores"]
    for event in events:
        confidence = confidence_scores.get(event, 0.0)
        star = "⭐" if event in laws["significant_events"] else "  "
        print(f"    {star} {event}: {confidence:.2f}")
    
    # Display smart money analysis
    print(f"\n💰 SMART MONEY ANALYSIS:")
    smart_money = laws["smart_money_activity"]
    composite_man = laws["composite_man_behavior"]
    print(f"    Activity Level: {smart_money:.2f}")
    print(f"    Composite Man Behavior: {composite_man['behavior']}")
    print(f"    Behavior Confidence: {composite_man['confidence']:.2f}")
    
    # Display volume spread analysis
    print(f"\n📊 VOLUME SPREAD ANALYSIS:")
    vs_analysis = laws["volume_spread_analysis"]
    print(f"    Volume Quality: {vs_analysis['volume_quality']}")
    print(f"    Spread Analysis: {vs_analysis['spread_analysis']}")
    print(f"    Relationship Health: {vs_analysis['relationship_health']}")
    
    # Display trading guidance
    print(f"\n💡 TRADING GUIDANCE:")
    risk_reward = laws["risk_reward_assessment"]
    entry_exit = laws["entry_exit_guidance"]
    print(f"    Position Bias: {laws['position_bias']}")
    print(f"    Risk/Reward Ratio: {risk_reward['risk_reward_ratio']:.1f}")
    print(f"    Success Probability: {risk_reward['probability_success']:.2f}")
    print(f"    Entry Strategy: {entry_exit['entry_strategy']}")
    print(f"    Entry Zone: ${entry_exit['optimal_entry_zone']['low']:.2f} - ${entry_exit['optimal_entry_zone']['high']:.2f}")
    print(f"    Stop Loss: ${entry_exit['stop_loss_level']:.2f}")
    
    # Display supply/demand zones
    print(f"\n🔴 SUPPLY ZONES:")
    for zone in laws["supply_zones"]:
        print(f"    ${zone['level']:.2f} (Strength: {zone['strength']:.2f})")
    
    print(f"\n🟢 DEMAND ZONES:")
    for zone in laws["demand_zones"]:
        print(f"    ${zone['level']:.2f} (Strength: {zone['strength']:.2f})")
    
    # Display quality metadata
    print(f"\n📋 ANALYSIS QUALITY:")
    quality = result.quality
    print(f"    Sample Size: {quality.sample_size}")
    print(f"    Freshness: {quality.freshness_sec}s")
    print(f"    Data Completeness: {quality.data_completeness:.2f}")
    print(f"    Validation Years: {quality.validation_period_years}")
    print(f"    False Positive Risk: {quality.false_positive_risk:.2f}")
    print(f"    Manipulation Sensitivity: {quality.manipulation_sensitivity:.2f}")
    
    print(f"\n✅ Enhanced Wyckoff analysis completed successfully!")
    print(f"    Legend: {result.legend}")
    print(f"    Timeframe: {result.tf}")
    print(f"    Analysis Time: {result.at}")
    
    return result

async def test_contract_compatibility():
    """Test that the enhanced engine maintains contract compatibility."""
    print("\n" + "=" * 60)
    print("CONTRACT COMPATIBILITY TEST")
    print("=" * 60)
    
    engine = WyckoffLegendEngine()
    request = LegendRequest(
        symbol="TEST",
        timeframe="1H",
        as_of=datetime.now()
    )
    
    result = await engine.run_async(request)
    
    # Verify LegendEnvelope structure
    assert hasattr(result, 'legend'), "Missing legend field"
    assert hasattr(result, 'at'), "Missing at field"
    assert hasattr(result, 'tf'), "Missing tf field"
    assert hasattr(result, 'facts'), "Missing facts field"
    assert hasattr(result, 'quality'), "Missing quality field"
    
    # Verify facts is a dictionary
    assert isinstance(result.facts, dict), "Facts must be a dictionary"
    
    # Verify required Wyckoff analysis components
    required_keys = [
        "law_of_supply_demand",
        "law_of_cause_effect", 
        "law_of_effort_result",
        "current_phase",
        "detected_events",
        "smart_money_activity"
    ]
    
    for key in required_keys:
        assert key in result.facts, f"Missing required key: {key}"
    
    print("✅ Contract compatibility verified!")
    print("✅ LegendEnvelope structure intact")
    print("✅ All required Wyckoff components present")
    print("✅ Facts dictionary properly structured")

if __name__ == "__main__":
    async def main():
        await test_wyckoff_enhanced()
        await test_contract_compatibility()
    
    asyncio.run(main())
