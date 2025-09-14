"""
Simple Wyckoff test data visualizer for debugging and validation.

This script provides a text-based visualization of the generated test data
to help validate the Wyckoff patterns and events.
"""

import json
import argparse
import pathlib
from typing import Dict, List, Any


def load_json_file(filepath: str) -> Any:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def visualize_bars(bars: List[Dict], events: Dict[str, str], title: str) -> None:
    """Create a text-based visualization of OHLCV bars with events."""
    print(f"\n{title}")
    print("=" * len(title))
    
    # Find price range for scaling
    all_prices = []
    for bar in bars:
        all_prices.extend([bar["high"], bar["low"], bar["open"], bar["close"]])
    
    min_price = min(all_prices)
    max_price = max(all_prices)
    price_range = max_price - min_price
    
    print(f"Price Range: ${min_price:.1f} - ${max_price:.1f}")
    print(f"Volume Range: {min(b['volume'] for b in bars):,} - {max(b['volume'] for b in bars):,}")
    print()
    
    # Header
    print("Bar# | Event | Open   | High   | Low    | Close  | Volume   | Spread | Notes")
    print("-" * 80)
    
    for i, bar in enumerate(bars):
        bar_num = i + 1
        event = events.get(str(i), "")
        
        # Calculate spread and volume characteristics
        spread = bar["high"] - bar["low"]
        vol = bar["volume"]
        
        # Determine bar characteristics
        notes = []
        if vol > 120000:
            notes.append("High Vol")
        if spread > 8:
            notes.append("Wide Spread")
        if bar["close"] < bar["open"]:
            notes.append("Red")
        else:
            notes.append("Green")
        
        # Special event analysis
        if event == "SC":
            close_pos = (bar["close"] - bar["low"]) / spread
            notes.append(f"Close@{close_pos:.1%}")
        elif event == "SOS":
            notes.append("Breakout")
        elif event == "Spring":
            notes.append("Undercut")
        
        event_str = f"{event:6}" if event else "      "
        notes_str = ", ".join(notes)
        
        print(f"{bar_num:3d}  | {event_str} | {bar['open']:6.1f} | {bar['high']:6.1f} | "
              f"{bar['low']:6.1f} | {bar['close']:6.1f} | {vol:8,} | {spread:6.1f} | {notes_str}")


def visualize_pf(pf: Dict, title: str) -> None:
    """Visualize Point & Figure objective."""
    print(f"\n{title} - Point & Figure Analysis")
    print("-" * 40)
    print(f"Direction: {pf['direction'].upper()}")
    print(f"Breakout Level: ${pf['breakout_level']:.1f}")
    print(f"Horizontal Count: {pf['boxes']} boxes")
    print(f"Box Size: ${pf['box_size']:.1f}")
    print(f"Price Objective: ${pf['objective']:.1f}")
    
    move_size = pf['objective'] - pf['breakout_level']
    print(f"Expected Move: ${abs(move_size):.1f} ({'+' if move_size > 0 else ''}{move_size:.1f})")


def analyze_wyckoff_sequence(bars: List[Dict], events: Dict[str, str], sequence_type: str) -> None:
    """Analyze the Wyckoff sequence for canonical relationships."""
    print(f"\n{sequence_type.title()} Sequence Analysis")
    print("-" * 35)
    
    # Find key events
    event_bars = {event: bars[int(idx)] for idx, event in events.items()}
    
    if sequence_type == "accumulation":
        # Accumulation analysis
        if "SC" in event_bars and "ST" in event_bars:
            sc = event_bars["SC"]
            st = event_bars["ST"]
            sc_spread = sc["high"] - sc["low"]
            st_spread = st["high"] - st["low"]
            
            print(f"SC Spread: {sc_spread:.1f}, Volume: {sc['volume']:,}")
            print(f"ST Spread: {st_spread:.1f}, Volume: {st['volume']:,}")
            print(f"ST/SC Volume Ratio: {st['volume']/sc['volume']:.2f}")
            print(f"ST/SC Spread Ratio: {st_spread/sc_spread:.2f}")
        
        if "AR" in event_bars and "SOS" in event_bars:
            ar = event_bars["AR"]
            sos = event_bars["SOS"]
            print(f"AR High: ${ar['high']:.1f}")
            print(f"SOS High: ${sos['high']:.1f}")
            print(f"SOS breaks AR: {sos['high'] > ar['high']}")
    
    elif sequence_type == "distribution":
        # Distribution analysis
        if "BC" in event_bars and "ST" in event_bars:
            bc = event_bars["BC"]
            st = event_bars["ST"]
            bc_spread = bc["high"] - bc["low"]
            st_spread = st["high"] - st["low"]
            
            print(f"BC Spread: {bc_spread:.1f}, Volume: {bc['volume']:,}")
            print(f"ST Spread: {st_spread:.1f}, Volume: {st['volume']:,}")
            print(f"ST/BC Volume Ratio: {st['volume']/bc['volume']:.2f}")
            print(f"ST/BC Spread Ratio: {st_spread/bc_spread:.2f}")
        
        if "AR" in event_bars and "SOW" in event_bars:
            ar = event_bars["AR"]
            sow = event_bars["SOW"]
            print(f"AR Low: ${ar['low']:.1f}")
            print(f"SOW Low: ${sow['low']:.1f}")
            print(f"SOW breaks AR: {sow['low'] < ar['low']}")


def main():
    """Main visualization function."""
    parser = argparse.ArgumentParser(description="Visualize Wyckoff test data")
    parser.add_argument("--bars", required=True, help="Path to bars JSON file")
    parser.add_argument("--ann", required=True, help="Path to events JSON file")
    parser.add_argument("--pf", required=True, help="Path to P&F JSON file")
    parser.add_argument("--title", default="Wyckoff Analysis", help="Chart title")
    
    args = parser.parse_args()
    
    # Load data
    bars = load_json_file(args.bars)
    events = load_json_file(args.ann)
    pf = load_json_file(args.pf)
    
    # Determine sequence type
    sequence_type = "accumulation" if "accumulation" in args.bars else "distribution"
    
    # Visualize
    visualize_bars(bars, events, args.title)
    visualize_pf(pf, args.title)
    analyze_wyckoff_sequence(bars, events, sequence_type)
    
    print(f"\n{'='*60}")
    print(f"✅ Visualization complete for {len(bars)} bars with {len(events)} events")


if __name__ == "__main__":
    main()
