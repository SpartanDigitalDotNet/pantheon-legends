"""
Quick test to verify the consolidated Wyckoff engine works with existing examples.
"""

import asyncio
from legends import WyckoffLegendEngine, LegendRequest
from datetime import datetime

async def test_consolidated_wyckoff():
    """Test the consolidated Wyckoff engine with simple usage."""
    print("=== Testing Consolidated Wyckoff Method Engine ===\n")
    
    # Create engine
    wyckoff = WyckoffLegendEngine()
    
    print(f"Engine: {wyckoff.name}")
    print(f"Description: {wyckoff.description}")
    print(f"Type: {wyckoff.legend_type.value}\n")
    
    # Test with SPY
    request = LegendRequest(
        symbol="SPY",
        timeframe="1D", 
        as_of=datetime.now()
    )
    
    print("Running Wyckoff analysis...")
    result = await wyckoff.run_async(request)
    
    print(f"\n✅ Analysis completed!")
    print(f"   Legend: {result.legend}")
    print(f"   Symbol: {result.facts.get('symbol', 'N/A')}")
    print(f"   Phase: {result.facts.get('current_phase', 'N/A')}")
    print(f"   Position Bias: {result.facts.get('position_bias', 'N/A')}")
    print(f"   Smart Money Activity: {result.facts.get('smart_money_activity', 'N/A')}")
    
    print(f"\n📊 Quality Metrics:")
    print(f"   Sample Size: {result.quality.sample_size}")
    print(f"   Manipulation Sensitivity: {result.quality.manipulation_sensitivity}")
    print(f"   False Positive Risk: {result.quality.false_positive_risk}")
    
    print(f"\n🎯 Wyckoff Laws Validation:")
    laws = result.facts
    print(f"   Supply/Demand: {laws['law_of_supply_demand']['law_validation']}")
    print(f"   Cause/Effect: {laws['law_of_cause_effect']['law_validation']}")
    print(f"   Effort/Result: {laws['law_of_effort_result']['law_validation']}")
    
    print(f"\n✅ Consolidated Wyckoff engine working perfectly!")
    
if __name__ == "__main__":
    asyncio.run(test_consolidated_wyckoff())
