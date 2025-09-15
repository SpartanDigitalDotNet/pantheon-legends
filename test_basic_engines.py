#!/usr/bin/env python3
"""
Simple test to check engine execution
"""

import asyncio
from datetime import datetime
from legends import Pantheon, LegendRequest


async def test_basic_engines():
    print("Testing basic engine execution...")
    
    pantheon = Pantheon.create_default()
    request = LegendRequest(
        symbol="TEST",
        timeframe="1D", 
        as_of=datetime.now()
    )
    
    print(f"Registered engines: {list(pantheon._engines.keys())}")
    
    # Test individual engines
    for engine_name in pantheon._engines.keys():
        try:
            result = await pantheon.run_legend_async(engine_name, request)
            print(f"✅ {engine_name}: {bool(result.facts)} facts")
            if result.facts:
                print(f"   Sample facts: {list(result.facts.keys())[:3]}")
        except Exception as e:
            print(f"❌ {engine_name}: {e}")
    
    # Test all engines together
    print(f"\nTesting all engines together...")
    results = await pantheon.run_all_legends_async(request)
    print(f"Total results: {len(results)}")
    
    for result in results:
        print(f"  {result.legend}: {len(result.facts)} facts")


if __name__ == "__main__":
    asyncio.run(test_basic_engines())
