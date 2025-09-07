"""
Example usage of the Pantheon Legends package.

This module demonstrates how to use the legend engines and Pantheon orchestrator.
"""

import asyncio
from datetime import datetime

from legends import (
    Pantheon,
    LegendRequest,
    LegendProgress,
    DowLegendEngine
)


async def progress_handler(progress: LegendProgress) -> None:
    """
    Example progress callback that prints progress updates.
    
    Args:
        progress: Progress update from a legend engine
    """
    print(f"[{progress.legend}] {progress.stage}: {progress.percent:.1f}% - {progress.note}")


async def single_engine_example():
    """Example of running a single legend engine."""
    print("=== Single Engine Example ===")
    
    # Create a Dow legend engine
    dow_engine = DowLegendEngine()
    
    # Create an analysis request
    request = LegendRequest(
        symbol="AAPL",
        timeframe="1d",
        as_of=datetime.now()
    )
    
    # Run the analysis with progress reporting
    print(f"Running {dow_engine.name} analysis for {request.symbol}...")
    result = await dow_engine.run_async(request, progress_handler)
    
    # Display results
    print(f"\nResults from {result.legend} engine:")
    print(f"  Symbol: {request.symbol}")
    print(f"  Timeframe: {result.tf}")
    print(f"  Analysis Time: {result.at}")
    print(f"  Data Quality: {result.quality.data_completeness:.1%} complete")
    print(f"  Data Freshness: {result.quality.freshness_sec}s old")
    
    print("\nKey Facts:")
    for key, value in result.facts.items():
        print(f"  {key}: {value}")


async def pantheon_orchestrator_example():
    """Example of using the Pantheon orchestrator with multiple engines."""
    print("\n=== Pantheon Orchestrator Example ===")
    
    # Create Pantheon with default engines
    pantheon = Pantheon.create_default()
    
    print(f"Available engines: {', '.join(pantheon.available_engines)}")
    
    # Create analysis request
    request = LegendRequest(
        symbol="MSFT",
        timeframe="4h",
        as_of=datetime.now()
    )
    
    # Run all engines concurrently
    print(f"\nRunning all engines for {request.symbol}...")
    results = await pantheon.run_all_legends_async(request, progress_handler)
    
    # Display aggregated results
    print(f"\nAggregated Results for {request.symbol}:")
    for result in results:
        print(f"\n--- {result.legend} Engine ---")
        print(f"  Confidence: {result.facts.get('confidence_score', 'N/A')}")
        print(f"  Primary Signal: {result.facts.get('primary_trend', result.facts.get('market_phase', 'N/A'))}")
        print(f"  Quality Score: {result.quality.data_completeness:.1%}")


async def custom_engine_example():
    """Example of creating and using a custom legend engine."""
    print("\n=== Custom Engine Example ===")
    
    class SimpleMovingAverageLegend:
        """Simple example of a custom legend engine."""
        
        @property
        def name(self) -> str:
            return "SMA"
        
        async def run_async(self, request, progress_callback=None):
            """Simple SMA analysis example."""
            from legends.contracts import LegendEnvelope, QualityMeta
            
            if progress_callback:
                await progress_callback(LegendProgress("SMA", "compute", 50.0, "Calculating moving averages"))
                await asyncio.sleep(0.1)
                await progress_callback(LegendProgress("SMA", "signal", 100.0, "Generating signals"))
            
            facts = {
                "sma_20": 165.50,
                "sma_50": 162.25,
                "sma_signal": "bullish_crossover",
                "trend_strength": 0.68
            }
            
            quality = QualityMeta(
                sample_size=50.0,
                freshness_sec=30.0,
                data_completeness=1.0
            )
            
            return LegendEnvelope(
                legend=self.name,
                at=request.as_of,
                tf=request.timeframe,
                facts=facts,
                quality=quality
            )
    
    # Create Pantheon and register custom engine
    pantheon = Pantheon()
    pantheon.register_engine(SimpleMovingAverageLegend())
    
    request = LegendRequest(
        symbol="TSLA",
        timeframe="1h",
        as_of=datetime.now()
    )
    
    print("Running custom SMA engine...")
    result = await pantheon.run_legend_async("SMA", request, progress_handler)
    
    print(f"\nCustom Engine Results:")
    print(f"  Engine: {result.legend}")
    print(f"  Signal: {result.facts['sma_signal']}")
    print(f"  Trend Strength: {result.facts['trend_strength']:.2f}")


async def main():
    """Run all examples."""
    await single_engine_example()
    await pantheon_orchestrator_example()
    await custom_engine_example()


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
