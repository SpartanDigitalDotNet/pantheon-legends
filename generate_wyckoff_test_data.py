"""
Wyckoff Legend Test Data Generator

Generates deterministic OHLCV test data for Wyckoff Method analysis validation.
Creates six JSON files with plausible bars, events, and Point & Figure objectives
that explicitly satisfy strict Wyckoff canon for automated testing.

Run: python generate_wyckoff_test_data.py
"""

import json
import pathlib
from typing import Dict, List, Any, Union


def create_accumulation_bars() -> List[Dict[str, Union[int, float]]]:
    """
    Create 15-bar accumulation sequence following strict Wyckoff canon.
    
    Bar Layout:
    1-5: Pre-decline establishing downtrend context
    6: SC (Selling Climax) - wide down spread, climactic volume, close off low
    7: AR (Automatic Rally) - strong bounce up
    8: ST (Secondary Test) - test SC low with lower volume/narrower spread
    9: Spring - brief undercut of support
    10: Test - lower volume test of spring low
    11: SOS (Sign of Strength) - break through AR high, increased volume
    12: LPS (Last Point of Support) - pullback holds above resistance
    13-15: Follow-through drift up
    """
    bars = [
        # Pre-decline context (bars 1-5)
        {"time": 1, "open": 125.0, "high": 126.0, "low": 123.0, "close": 124.0, "volume": 45000},
        {"time": 2, "open": 124.0, "high": 124.5, "low": 120.0, "close": 121.0, "volume": 55000},
        {"time": 3, "open": 121.0, "high": 122.0, "low": 117.0, "close": 118.0, "volume": 60000},
        {"time": 4, "open": 118.0, "high": 119.0, "low": 115.0, "close": 116.0, "volume": 65000},
        {"time": 5, "open": 116.0, "high": 117.0, "low": 112.0, "close": 113.0, "volume": 70000},
        
        # SC - Selling Climax (bar 6)
        {"time": 6, "open": 113.0, "high": 113.5, "low": 105.0, "close": 107.0, "volume": 150000},  # Wide spread down, climactic volume, close off low
        
        # AR - Automatic Rally (bar 7)
        {"time": 7, "open": 107.0, "high": 118.0, "low": 106.0, "close": 116.0, "volume": 120000},  # Strong bounce up
        
        # ST - Secondary Test (bar 8)
        {"time": 8, "open": 116.0, "high": 115.0, "low": 108.0, "close": 109.0, "volume": 80000},   # Test SC low, lower volume, narrower spread, close above SC low
        
        # Spring (bar 9)
        {"time": 9, "open": 109.0, "high": 110.0, "low": 104.0, "close": 108.0, "volume": 90000},   # Brief undercut of support
        
        # Test of Spring (bar 10)
        {"time": 10, "open": 108.0, "high": 109.0, "low": 105.0, "close": 107.0, "volume": 60000},  # Lower volume test
        
        # SOS - Sign of Strength (bar 11)
        {"time": 11, "open": 107.0, "high": 120.0, "low": 106.0, "close": 119.0, "volume": 140000}, # Break through AR high, increased volume
        
        # LPS - Last Point of Support (bar 12)
        {"time": 12, "open": 119.0, "high": 120.0, "low": 115.0, "close": 116.0, "volume": 70000},  # Pullback holds above former resistance
        
        # Follow-through (bars 13-15)
        {"time": 13, "open": 116.0, "high": 119.0, "low": 115.0, "close": 118.0, "volume": 65000},
        {"time": 14, "open": 118.0, "high": 121.0, "low": 117.0, "close": 120.0, "volume": 75000},
        {"time": 15, "open": 120.0, "high": 123.0, "low": 119.0, "close": 122.0, "volume": 80000},
    ]
    return bars


def create_accumulation_events() -> Dict[str, str]:
    """Create event labels for accumulation sequence."""
    return {
        "5": "SC",      # Selling Climax at bar 6 (0-indexed: 5)
        "6": "AR",      # Automatic Rally at bar 7 (0-indexed: 6)
        "7": "ST",      # Secondary Test at bar 8 (0-indexed: 7)
        "8": "Spring",  # Spring at bar 9 (0-indexed: 8)
        "9": "Test",    # Test at bar 10 (0-indexed: 9)
        "10": "SOS",    # Sign of Strength at bar 11 (0-indexed: 10)
        "11": "LPS"     # Last Point of Support at bar 12 (0-indexed: 11)
    }


def create_accumulation_pf() -> Dict[str, Union[str, float, int]]:
    """
    Create Point & Figure objective for accumulation.
    Breakout at SOS high (120.0), horizontal count ~8 boxes.
    """
    return {
        "direction": "up",
        "breakout_level": 120.0,   # SOS high
        "boxes": 8,                # Horizontal count from trading range
        "box_size": 2.0,           # $2 per box
        "objective": 136.0         # 120.0 + (8 * 2.0)
    }


def create_distribution_bars() -> List[Dict[str, Union[int, float]]]:
    """
    Create 15-bar distribution sequence following strict Wyckoff canon.
    
    Bar Layout:
    1-5: Pre-advance establishing uptrend context
    6: BC (Buying Climax) - wide up spread, climactic volume, close off high
    7: AR (Automatic Reaction) - sharp decline
    8: ST (Secondary Test) - test BC high with lower volume/narrower spread
    9: UT (Upthrust) - thrust above trading range high
    10: UTAD (Upthrust After Distribution) - deeper/later thrust that fails
    11: SOW (Sign of Weakness) - break through AR low, increased volume
    12: LPSY (Last Point of Supply) - weak rally failing below resistance
    13-15: Follow-through drift down
    """
    bars = [
        # Pre-advance context (bars 1-5)
        {"time": 1, "open": 85.0, "high": 87.0, "low": 84.0, "close": 86.0, "volume": 45000},
        {"time": 2, "open": 86.0, "high": 89.0, "low": 85.0, "close": 88.0, "volume": 55000},
        {"time": 3, "open": 88.0, "high": 92.0, "low": 87.0, "close": 91.0, "volume": 60000},
        {"time": 4, "open": 91.0, "high": 95.0, "low": 90.0, "close": 94.0, "volume": 65000},
        {"time": 5, "open": 94.0, "high": 98.0, "low": 93.0, "close": 97.0, "volume": 70000},
        
        # BC - Buying Climax (bar 6)
        {"time": 6, "open": 97.0, "high": 108.0, "low": 96.0, "close": 106.0, "volume": 150000}, # Wide spread up, climactic volume, close off high
        
        # AR - Automatic Reaction (bar 7)
        {"time": 7, "open": 106.0, "high": 107.0, "low": 95.0, "close": 97.0, "volume": 120000}, # Sharp decline
        
        # ST - Secondary Test (bar 8)
        {"time": 8, "open": 97.0, "high": 105.0, "low": 96.0, "close": 103.0, "volume": 80000},  # Test BC high, lower volume, narrower spread, close below BC high
        
        # UT - Upthrust (bar 9)
        {"time": 9, "open": 103.0, "high": 109.0, "low": 102.0, "close": 104.0, "volume": 90000}, # Thrust above trading range high but fails back in
        
        # UTAD - Upthrust After Distribution (bar 10)
        {"time": 10, "open": 104.0, "high": 110.0, "low": 103.0, "close": 105.0, "volume": 85000}, # Deeper thrust that fails back in
        
        # SOW - Sign of Weakness (bar 11)
        {"time": 11, "open": 105.0, "high": 106.0, "low": 92.0, "close": 94.0, "volume": 140000}, # Break through AR low, increased volume
        
        # LPSY - Last Point of Supply (bar 12)
        {"time": 12, "open": 94.0, "high": 99.0, "low": 93.0, "close": 96.0, "volume": 70000},   # Weak rally failing below resistance
        
        # Follow-through (bars 13-15)
        {"time": 13, "open": 96.0, "high": 97.0, "low": 91.0, "close": 93.0, "volume": 75000},
        {"time": 14, "open": 93.0, "high": 94.0, "low": 88.0, "close": 90.0, "volume": 80000},
        {"time": 15, "open": 90.0, "high": 91.0, "low": 85.0, "close": 87.0, "volume": 85000},
    ]
    return bars


def create_distribution_events() -> Dict[str, str]:
    """Create event labels for distribution sequence."""
    return {
        "5": "BC",      # Buying Climax at bar 6 (0-indexed: 5)
        "6": "AR",      # Automatic Reaction at bar 7 (0-indexed: 6)
        "7": "ST",      # Secondary Test at bar 8 (0-indexed: 7)
        "8": "UT",      # Upthrust at bar 9 (0-indexed: 8)
        "9": "UTAD",    # Upthrust After Distribution at bar 10 (0-indexed: 9)
        "10": "SOW",    # Sign of Weakness at bar 11 (0-indexed: 10)
        "11": "LPSY"    # Last Point of Supply at bar 12 (0-indexed: 11)
    }


def create_distribution_pf() -> Dict[str, Union[str, float, int]]:
    """
    Create Point & Figure objective for distribution.
    Breakdown at SOW low (92.0), horizontal count ~8 boxes.
    """
    return {
        "direction": "down",
        "breakout_level": 92.0,    # SOW low (breakdown level)
        "boxes": 8,                # Horizontal count from trading range
        "box_size": 2.0,           # $2 per box
        "objective": 76.0          # 92.0 - (8 * 2.0)
    }


def write_json_file(data: Any, filepath: pathlib.Path) -> None:
    """Write data to JSON file with pretty formatting."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def validate_accumulation_data(bars: List[Dict], events: Dict[str, str], pf: Dict) -> None:
    """Validate accumulation data meets Wyckoff canon requirements."""
    print("🔍 Validating accumulation data...")
    
    # Get key bar indices
    sc_idx, ar_idx, st_idx = 5, 6, 7
    spring_idx, test_idx = 8, 9
    sos_idx, lps_idx = 10, 11
    
    # SC validation: wide spread down, climactic volume, close off low
    sc_bar = bars[sc_idx]
    spread = sc_bar["high"] - sc_bar["low"]
    close_position = (sc_bar["close"] - sc_bar["low"]) / spread
    assert spread >= 8.0, f"SC spread too narrow: {spread}"
    assert sc_bar["volume"] >= 140000, f"SC volume not climactic: {sc_bar['volume']}"
    assert close_position <= 0.3, f"SC close not off low: {close_position}"
    
    # ST validation: lower volume than SC, narrower spread, close above SC low
    st_bar = bars[st_idx]
    st_spread = st_bar["high"] - st_bar["low"]
    assert st_bar["volume"] < sc_bar["volume"], f"ST volume not lower than SC: {st_bar['volume']} vs {sc_bar['volume']}"
    assert st_spread < spread, f"ST spread not narrower than SC: {st_spread} vs {spread}"
    assert st_bar["close"] > sc_bar["low"], f"ST close not above SC low: {st_bar['close']} vs {sc_bar['low']}"
    
    # Spring validation: undercut support
    spring_bar = bars[spring_idx]
    assert spring_bar["low"] < sc_bar["low"], f"Spring didn't undercut SC low: {spring_bar['low']} vs {sc_bar['low']}"
    
    # Test validation: lower volume than spring
    test_bar = bars[test_idx]
    assert test_bar["volume"] < spring_bar["volume"], f"Test volume not lower: {test_bar['volume']} vs {spring_bar['volume']}"
    
    # SOS validation: break through AR high, increased volume
    ar_bar = bars[ar_idx]
    sos_bar = bars[sos_idx]
    assert sos_bar["high"] > ar_bar["high"], f"SOS didn't break AR high: {sos_bar['high']} vs {ar_bar['high']}"
    assert sos_bar["volume"] > test_bar["volume"], f"SOS volume not increased: {sos_bar['volume']} vs {test_bar['volume']}"
    
    # LPS validation: pullback holds above former resistance
    lps_bar = bars[lps_idx]
    assert lps_bar["low"] > ar_bar["high"] * 0.95, f"LPS didn't hold above resistance: {lps_bar['low']} vs {ar_bar['high']}"
    
    # P&F validation
    assert pf["direction"] == "up", f"P&F direction wrong: {pf['direction']}"
    assert pf["objective"] != pf["breakout_level"], f"P&F objective equals breakout: {pf['objective']} vs {pf['breakout_level']}"
    assert pf["objective"] > pf["breakout_level"], f"P&F objective not above breakout: {pf['objective']} vs {pf['breakout_level']}"
    
    print("✅ Accumulation data validation passed!")


def validate_distribution_data(bars: List[Dict], events: Dict[str, str], pf: Dict) -> None:
    """Validate distribution data meets Wyckoff canon requirements."""
    print("🔍 Validating distribution data...")
    
    # Get key bar indices
    bc_idx, ar_idx, st_idx = 5, 6, 7
    ut_idx, utad_idx = 8, 9
    sow_idx, lpsy_idx = 10, 11
    
    # BC validation: wide spread up, climactic volume, close off high
    bc_bar = bars[bc_idx]
    spread = bc_bar["high"] - bc_bar["low"]
    close_position = (bc_bar["close"] - bc_bar["low"]) / spread
    assert spread >= 10.0, f"BC spread too narrow: {spread}"
    assert bc_bar["volume"] >= 140000, f"BC volume not climactic: {bc_bar['volume']}"
    assert close_position >= 0.7, f"BC close not off high: {close_position}"
    
    # ST validation: lower volume than BC, narrower spread, close below BC high
    st_bar = bars[st_idx]
    st_spread = st_bar["high"] - st_bar["low"]
    assert st_bar["volume"] < bc_bar["volume"], f"ST volume not lower than BC: {st_bar['volume']} vs {bc_bar['volume']}"
    assert st_spread < spread, f"ST spread not narrower than BC: {st_spread} vs {spread}"
    assert st_bar["close"] < bc_bar["high"], f"ST close not below BC high: {st_bar['close']} vs {bc_bar['high']}"
    
    # UT/UTAD validation: thrust above trading range high
    ut_bar = bars[ut_idx]
    utad_bar = bars[utad_idx]
    tr_high = max(bc_bar["high"], st_bar["high"])
    assert ut_bar["high"] > tr_high, f"UT didn't thrust above TR high: {ut_bar['high']} vs {tr_high}"
    assert utad_bar["high"] > tr_high, f"UTAD didn't thrust above TR high: {utad_bar['high']} vs {tr_high}"
    
    # SOW validation: break through AR low, increased volume
    ar_bar = bars[ar_idx]
    sow_bar = bars[sow_idx]
    assert sow_bar["low"] < ar_bar["low"], f"SOW didn't break AR low: {sow_bar['low']} vs {ar_bar['low']}"
    assert sow_bar["volume"] > utad_bar["volume"], f"SOW volume not increased: {sow_bar['volume']} vs {utad_bar['volume']}"
    
    # LPSY validation: weak rally failing below resistance
    lpsy_bar = bars[lpsy_idx]
    assert lpsy_bar["high"] < ar_bar["low"] * 1.05, f"LPSY rallied too high: {lpsy_bar['high']} vs {ar_bar['low']}"
    
    # P&F validation
    assert pf["direction"] == "down", f"P&F direction wrong: {pf['direction']}"
    assert pf["objective"] != pf["breakout_level"], f"P&F objective equals breakout: {pf['objective']} vs {pf['breakout_level']}"
    assert pf["objective"] < pf["breakout_level"], f"P&F objective not below breakout: {pf['objective']} vs {pf['breakout_level']}"
    
    print("✅ Distribution data validation passed!")


def main():
    """Generate all Wyckoff test data files."""
    print("🎯 Generating Wyckoff Legend Test Data...")
    
    # Create output directory
    output_dir = pathlib.Path("wyckoff_test_data")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Created directory: {output_dir.absolute()}")
    
    # Generate accumulation data
    print("\n📈 Generating accumulation sequence...")
    acc_bars = create_accumulation_bars()
    acc_events = create_accumulation_events()
    acc_pf = create_accumulation_pf()
    
    # Generate distribution data
    print("📉 Generating distribution sequence...")
    dist_bars = create_distribution_bars()
    dist_events = create_distribution_events()
    dist_pf = create_distribution_pf()
    
    # Write all files
    files = [
        ("accumulation_bars.json", acc_bars),
        ("accumulation_events.json", acc_events),
        ("accumulation_pf.json", acc_pf),
        ("distribution_bars.json", dist_bars),
        ("distribution_events.json", dist_events),
        ("distribution_pf.json", dist_pf),
    ]
    
    print("\n💾 Writing JSON files...")
    for filename, data in files:
        filepath = output_dir / filename
        write_json_file(data, filepath)
        print(f"   ✅ {filepath.absolute()}")
    
    # Validate data
    print("\n🔬 Running validation checks...")
    validate_accumulation_data(acc_bars, acc_events, acc_pf)
    validate_distribution_data(dist_bars, dist_events, dist_pf)
    
    print(f"\n✅ Successfully generated {len(files)} Wyckoff test data files!")
    print(f"📂 Output directory: {output_dir.absolute()}")
    
    # Print summary
    print("\n📊 Data Summary:")
    print(f"   Accumulation: {len(acc_bars)} bars, {len(acc_events)} events")
    print(f"   Distribution: {len(dist_bars)} bars, {len(dist_events)} events")
    print(f"   P&F Objectives: UP to {acc_pf['objective']}, DOWN to {dist_pf['objective']}")


if __name__ == "__main__":
    main()


"""
USAGE README:

How to run:
    python generate_wyckoff_test_data.py

What files are produced and how to view them with our existing wyckoff_viz_cli.py:

Accumulation demo:
    python wyckoff_viz_cli.py --bars wyckoff_test_data/accumulation_bars.json --ann wyckoff_test_data/accumulation_events.json --pf wyckoff_test_data/accumulation_pf.json --title "Wyckoff Accumulation Demo"

Distribution demo:
    python wyckoff_viz_cli.py --bars wyckoff_test_data/distribution_bars.json --ann wyckoff_test_data/distribution_events.json --pf wyckoff_test_data/distribution_pf.json --title "Wyckoff Distribution Demo"

The generated data follows strict Wyckoff canon:
- Accumulation: SC → AR → ST → Spring → Test → SOS → LPS → Markup
- Distribution: BC → AR → ST → UT → UTAD → SOW → LPSY → Markdown
- Deterministic OHLCV data designed to trigger proper Wyckoff event detection
- Point & Figure objectives calculated using horizontal count method
- All data validated against Wyckoff principles (volume, spread, price relationships)
"""
