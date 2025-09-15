# Getting Started with Pantheon Legends

## What is Pantheon Legends?

Pantheon Legends is a Python framework for building financial market analysis "legend engines" - modular components that implement specific trading methodologies and signal detection algorithms.

## Quick Installation

```bash
pip install pantheon-legends
```

Test your installation:
```bash
python -c "import legends; legends.test_installation()"
```

## Core Concepts

### Legend Engines
A **Legend Engine** is a self-contained analysis module that:
- Implements a specific trading methodology (Dow Theory, Wyckoff, etc.)
- Takes market data as input
- Returns structured analysis results
- Reports progress and quality metrics

### The Pantheon Orchestrator
The **Pantheon** class manages multiple legend engines:
- Runs legends individually or concurrently
- Aggregates results from multiple methodologies
- Provides a unified interface for complex analysis

### Data Flow
```
Market Data → Legend Engine → Analysis Results → Pantheon → Trading Decisions
```

## Your First Legend

### Option 1: Convert Existing Scanner
If you have a market scanner, convert it easily:

```bash
python -m legends create
```

This will guide you through creating a legend template from your scanner.

### Option 2: Build from Scratch
```python
from legends.contracts import ILegendEngine, LegendRequest, LegendEnvelope, QualityMeta
from datetime import datetime
from typing import Optional

class MyFirstLegend:
    @property
    def name(self) -> str:
        return "MyFirst"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        # Your analysis logic here
        facts = {
            "signal": "bullish",
            "confidence": 0.85,
            "price_target": 150.00
        }
        
        quality = QualityMeta(
            sample_size=100.0,
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
```

## Using Your Legend

### Single Legend
```python
import asyncio
from datetime import datetime
from legends import LegendRequest

async def main():
    legend = MyFirstLegend()
    
    request = LegendRequest(
        symbol="BTC-USD",
        timeframe="1h",
        as_of=datetime.now()
    )
    
    result = await legend.run_async(request)
    print(f"Signal: {result.facts['signal']}")

asyncio.run(main())
```

### Multiple Legends with Pantheon
```python
from legends import Pantheon

async def main():
    pantheon = Pantheon()
    pantheon.register_engine(MyFirstLegend())
    
    request = LegendRequest("ETH-USD", "4h", datetime.now())
    
    # Unified analysis with automatic consensus
    result = await pantheon.analyze_with_consensus(request)
    
    # Individual engine results
    for engine_result in result.engine_results:
        print(f"{engine_result.legend}: {engine_result.facts}")
    
    # Automatic consensus (if multiple engines)
    if result.consensus:
        print(f"Consensus: {result.consensus.signal.value}")
        print(f"Confidence: {result.consensus.confidence:.1%}")

asyncio.run(main())
```

### Quick Analysis (No Setup Required)

For quick analysis without manual Pantheon setup:

```python
from legends import quick_analysis, consensus_only

# Complete analysis with consensus
result = await quick_analysis("BTC-USD", timeframe="1D")
print(f"Consensus: {result.consensus.signal.value}")

# Consensus-only analysis  
consensus = await consensus_only("SPY", min_reliability=ReliabilityLevel.HIGH)
print(f"High-reliability consensus: {consensus.signal.value}")
```

## Next Steps

1. **[Legend Development Guide](legend-development.md)** - Deep dive into building legends
2. **[API Reference](api-reference.md)** - Complete API documentation
3. **[Examples](examples.md)** - Real-world legend implementations
4. **[Contributing](../CONTRIBUTING.md)** - How to contribute to the project

## Need Help?

- 📚 **Documentation**: Browse the `/docs` folder
- 🐛 **Issues**: Report bugs on GitHub
- 💬 **Discussions**: Join the community discussions
- 📧 **Contact**: Reach out to the maintainers

Happy legend building! 🏛️
