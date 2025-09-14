# Wyckoff Test Data

This directory contains deterministic OHLCV test data for validating Wyckoff Method analysis engines.

## Files

### Accumulation Sequence
- `accumulation_bars.json` - 15 bars following strict Wyckoff accumulation canon
- `accumulation_events.json` - Event labels (SC, AR, ST, Spring, Test, SOS, LPS)
- `accumulation_pf.json` - Point & Figure upside objective

### Distribution Sequence  
- `distribution_bars.json` - 15 bars following strict Wyckoff distribution canon
- `distribution_events.json` - Event labels (BC, AR, ST, UT, UTAD, SOW, LPSY)
- `distribution_pf.json` - Point & Figure downside objective

## Wyckoff Canon Validation

### Accumulation Pattern
- **SC (Selling Climax)**: Wide down spread, climactic volume, close off low
- **AR (Automatic Rally)**: Strong bounce from SC low
- **ST (Secondary Test)**: Lower volume, narrower spread than SC, close above SC low
- **Spring**: Brief undercut of support level
- **Test**: Lower volume confirmation of spring low
- **SOS (Sign of Strength)**: Break through AR high with increased volume
- **LPS (Last Point of Support)**: Pullback holds above former resistance

### Distribution Pattern  
- **BC (Buying Climax)**: Wide up spread, climactic volume, close off high
- **AR (Automatic Reaction)**: Sharp decline from BC high
- **ST (Secondary Test)**: Lower volume, narrower spread than BC, close below BC high
- **UT (Upthrust)**: Thrust above trading range high that fails
- **UTAD (Upthrust After Distribution)**: Deeper thrust that also fails
- **SOW (Sign of Weakness)**: Break through AR low with increased volume
- **LPSY (Last Point of Supply)**: Weak rally failing below resistance

## Usage

### Generate Test Data
```bash
python generate_wyckoff_test_data.py
```

### Visualize Test Data
```bash
# Accumulation
python wyckoff_viz_cli.py --bars wyckoff_test_data/accumulation_bars.json --ann wyckoff_test_data/accumulation_events.json --pf wyckoff_test_data/accumulation_pf.json --title "Wyckoff Accumulation Demo"

# Distribution  
python wyckoff_viz_cli.py --bars wyckoff_test_data/distribution_bars.json --ann wyckoff_test_data/distribution_events.json --pf wyckoff_test_data/distribution_pf.json --title "Wyckoff Distribution Demo"
```

### Test with Wyckoff Engine
```python
from legends import WyckoffLegendEngine, LegendRequest
import json

# Load test data
with open("wyckoff_test_data/accumulation_bars.json") as f:
    bars = json.load(f)

# Test engine
engine = WyckoffLegendEngine()
request = LegendRequest(symbol="TEST", timeframe="1D")
result = await engine.run_async(request)

# Validate analysis
assert result.facts["position_bias"] == "bullish_bias"
assert "Accumulation" in result.facts["current_phase"]
```

## Validation Results

✅ **Data Quality**: All bars validated against Wyckoff canon  
✅ **Event Relationships**: SC/ST volume ratios, SOS/AR breakouts confirmed  
✅ **P&F Objectives**: Horizontal count method applied correctly  
✅ **Schema Compliance**: JSON structures match framework requirements  

The test data is designed to trigger proper Wyckoff event detection in compliant analysis engines.
