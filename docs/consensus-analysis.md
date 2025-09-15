# Unified Consensus Analysis

Pantheon Legends provides **automatic consensus calculation** that eliminates manual orchestration and provides seamless multi-engine analysis with reliability weighting.

## 🎯 Key Benefits

- **No Manual Orchestration**: Single method call runs engines and calculates consensus
- **Automatic Reliability Weighting**: Engines weighted by reliability and confidence  
- **Real Engine Results**: Uses actual `LegendEnvelope` data, not simulations
- **Flexible Filtering**: Filter by reliability, engine type, or specific engines
- **Robust Error Handling**: Consensus works even if some engines fail
- **One-Call Analysis**: Returns both individual results AND consensus

## 🚀 Quick Start

### Basic Unified Analysis
```python
import asyncio
from datetime import datetime
from legends import Pantheon, LegendRequest

async def basic_consensus():
    pantheon = Pantheon.create_default()
    
    # Single call - engines + consensus automatically
    result = await pantheon.analyze_with_consensus(
        LegendRequest("AAPL", "1D", datetime.now())
    )
    
    # Individual engine results
    for engine_result in result.engine_results:
        print(f"{engine_result.legend}: {engine_result.facts}")
    
    # Automatic consensus
    if result.consensus:
        print(f"Consensus: {result.consensus.signal.value}")
        print(f"Confidence: {result.consensus.confidence:.1%}")

asyncio.run(basic_consensus())
```

### Convenience Functions
```python
from legends import quick_analysis, consensus_only

# All-in-one analysis (no setup required)
result = await quick_analysis("SPY", with_consensus=True)
print(f"SPY: {result.consensus.signal.value}")

# Consensus-only analysis
consensus = await consensus_only("BTCUSD") 
print(f"BTCUSD: {consensus.signal.value}")
```

## 📊 Consensus Signals

The consensus analyzer returns standardized signals:

| Signal | Description | Score Range |
|--------|-------------|-------------|
| `strong_bullish` | High confidence upward momentum | 0.7 to 1.0 |
| `bullish` | Positive bias with moderate confidence | 0.3 to 0.7 |
| `neutral` | No clear directional bias | -0.3 to 0.3 |
| `bearish` | Negative bias with moderate confidence | -0.7 to -0.3 |
| `strong_bearish` | High confidence downward momentum | -1.0 to -0.7 |
| `insufficient_data` | Not enough reliable engines | N/A |

## 🔧 Advanced Options

### Reliability Filtering
```python
# High reliability engines only
result = await pantheon.analyze_with_consensus(
    request,
    min_consensus_reliability=ReliabilityLevel.HIGH
)

# Medium or higher reliability
result = await pantheon.analyze_with_consensus(
    request, 
    min_consensus_reliability=ReliabilityLevel.MEDIUM
)
```

### Selective Engine Analysis
```python
# Traditional engines only
result = await pantheon.analyze_with_consensus(
    request,
    engine_names=["Dow Theory", "Wyckoff Method"]
)

# Specific engine combination
result = await pantheon.analyze_with_consensus(
    request,
    engine_names=["Wyckoff Method", "Volume Breakout Scanner"]
)
```

### Quick Consensus Options
```python
# Symbol-specific consensus
consensus = await pantheon.quick_consensus(
    symbol="NVDA",
    timeframe="4H", 
    min_reliability=ReliabilityLevel.PROVEN
)

# With timestamp
consensus = await pantheon.quick_consensus(
    symbol="TSLA",
    timestamp=specific_datetime,
    min_reliability=ReliabilityLevel.HIGH
)
```

## 📈 Consensus Quality Metrics

The consensus result includes quality assessment:

### Quality Levels
- **`high`**: 3+ engines, average reliability ≥ 0.7, confidence ≥ 0.7
- **`medium`**: 2+ engines, average reliability ≥ 0.5, confidence ≥ 0.5  
- **`low`**: Below medium thresholds
- **`insufficient`**: No valid engines for consensus

### Accessing Quality Metrics
```python
result = await pantheon.analyze_with_consensus(request)

if result.consensus:
    print(f"Quality: {result.consensus.consensus_quality}")
    print(f"Engines: {result.consensus.engines_analyzed}")
    print(f"Reliability: {result.consensus.reliability_average:.2f}")
    print(f"Confidence: {result.consensus.confidence:.1%}")
```

## ⚖️ Reliability Weighting

Engines are automatically weighted by reliability level:

| Reliability Level | Weight | Description |
|------------------|--------|-------------|
| `HIGH` | 1.0 | Proven, battle-tested engines |
| `MEDIUM` | 0.7 | Well-tested, stable engines |
| `VARIABLE` | 0.5 | Conditional reliability engines |
| `EXPERIMENTAL` | 0.3 | Research or prototype engines |

### Weight Calculation
```
final_weight = reliability_weight × confidence_score
weighted_score = Σ(signal × final_weight) / Σ(final_weight)
```

## 🔍 Engine Contributions

Access detailed breakdown of how each engine contributed:

```python
if result.consensus:
    print("Engine Contributions:")
    for name, contrib in result.consensus.engine_contributions.items():
        print(f"  • {name}:")
        print(f"    Signal: {contrib['signal']}")
        print(f"    Weight: {contrib['weight_contribution']:.2f}")
        print(f"    Reliability: {contrib['reliability_level']}")
```

## 🛡️ Error Handling

The consensus system is robust and handles various failure scenarios:

```python
# Consensus works even if some engines fail
result = await pantheon.analyze_with_consensus(request)

print(f"Total engines: {result.total_engines}")
print(f"Successful: {result.successful_engines}")

# Consensus calculated from successful engines only
if result.consensus:
    print(f"Consensus from {result.consensus.engines_analyzed} engines")
```

## 🔄 Migration from Manual Consensus

### Old Approach (Manual Orchestration)
```python
# ❌ Old way - multiple steps, error-prone
results = await pantheon.run_all_legends_async(request)
signals = extract_signals_manually(results)  # Manual work
consensus = calculate_consensus_manually(signals)  # More manual work
```

### New Approach (Automatic Consensus)
```python
# ✅ New way - one call, automatic
result = await pantheon.analyze_with_consensus(request)
# Individual results: result.engine_results
# Automatic consensus: result.consensus
```

## 📋 Complete Example

```python
import asyncio
from datetime import datetime
from legends import Pantheon, LegendRequest, ReliabilityLevel

async def comprehensive_consensus_example():
    """Complete example showing all consensus features"""
    
    # Setup
    pantheon = Pantheon.create_default()
    request = LegendRequest("MSFT", "1D", datetime.now())
    
    # Unified analysis
    result = await pantheon.analyze_with_consensus(
        request=request,
        enable_consensus=True,
        min_consensus_reliability=ReliabilityLevel.MEDIUM
    )
    
    print(f"⏱️ Analysis completed in {result.execution_time_ms:.1f}ms")
    print(f"🔧 Engines: {result.successful_engines}/{result.total_engines}")
    
    # Individual results
    print("\n📊 Individual Engine Results:")
    for engine_result in result.engine_results:
        signal = engine_result.facts.get('primary_trend', 'N/A')
        print(f"  • {engine_result.legend}: {signal}")
    
    # Consensus analysis
    if result.consensus:
        print(f"\n🎯 Consensus Analysis:")
        print(f"  Signal: {result.consensus.signal.value}")
        print(f"  Confidence: {result.consensus.confidence:.1%}")
        print(f"  Strength: {result.consensus.strength:.1%}")
        print(f"  Quality: {result.consensus.consensus_quality}")
        
        print(f"\n📈 Engine Breakdown:")
        print(f"  Bullish: {result.consensus.engines_bullish}")
        print(f"  Bearish: {result.consensus.engines_bearish}")
        print(f"  Neutral: {result.consensus.engines_neutral}")
        
        print(f"\n⚖️ Reliability Metrics:")
        print(f"  Average: {result.consensus.reliability_average:.2f}")
        print(f"  Weighted Score: {result.consensus.weighted_score:.3f}")
        
        print(f"\n🔧 Engine Contributions:")
        for name, contrib in result.consensus.engine_contributions.items():
            print(f"  • {name}: {contrib['signal']} "
                  f"(weight: {contrib['weight_contribution']:.2f})")
    else:
        print("❌ No consensus available")

# Run the example
asyncio.run(comprehensive_consensus_example())
```

## 🎉 Benefits Summary

| Feature | Manual Approach | Unified Consensus |
|---------|----------------|-------------------|
| **Orchestration** | Manual, multi-step | Automatic, one-call |
| **Error Handling** | Manual try/catch | Built-in robustness |
| **Reliability Weighting** | Manual calculation | Automatic weighting |
| **Signal Extraction** | Manual parsing | Automatic extraction |
| **Quality Assessment** | Manual evaluation | Automatic quality metrics |
| **Engine Filtering** | Manual filtering | Built-in filtering options |

The unified consensus analysis provides **production-ready consensus calculation** with **no manual orchestration required** – making multi-engine analysis seamless and robust.
