# Examples Collection

Real-world examples and patterns for building effective legends.

## Basic Examples

### Simple Moving Average Crossover

```python
from legends import ILegendEngine, LegendRequest, LegendEnvelope, QualityMeta, LegendProgress
from typing import Optional, Dict, Any, List
from datetime import datetime

class MovingAverageCrossover:
    """Simple moving average crossover strategy"""
    
    @property
    def name(self) -> str:
        return "SMA_Crossover"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="fetching_data", percent=20.0
            ))
        
        # Simulate fetching price data
        prices = await self._fetch_prices(request.symbol, request.timeframe)
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="calculating_sma", percent=60.0
            ))
        
        # Calculate moving averages
        sma_short = self._sma(prices, 10)  # 10-period SMA
        sma_long = self._sma(prices, 20)   # 20-period SMA
        
        # Generate signal
        signal = "hold"
        strength = 0.0
        
        if len(sma_short) >= 2 and len(sma_long) >= 2:
            current_short = sma_short[-1]
            current_long = sma_long[-1]
            prev_short = sma_short[-2]
            prev_long = sma_long[-2]
            
            # Bullish crossover: short SMA crosses above long SMA
            if prev_short <= prev_long and current_short > current_long:
                signal = "buy"
                strength = 0.8
            # Bearish crossover: short SMA crosses below long SMA
            elif prev_short >= prev_long and current_short < current_long:
                signal = "sell"
                strength = 0.8
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="complete", percent=100.0
            ))
        
        facts = {
            "primary_signal": signal,
            "signal_strength": strength,
            "signal_type": "crossover",
            "sma_short": sma_short[-1] if sma_short else 0,
            "sma_long": sma_long[-1] if sma_long else 0,
            "price": prices[-1] if prices else 0
        }
        
        quality = QualityMeta(
            sample_size=float(len(prices)),
            freshness_sec=60.0,  # Assume 1-minute old data
            data_completeness=1.0 if len(prices) >= 20 else len(prices) / 20
        )
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
    
    def _sma(self, prices: List[float], period: int) -> List[float]:
        """Calculate simple moving average"""
        if len(prices) < period:
            return []
        
        sma_values = []
        for i in range(period - 1, len(prices)):
            avg = sum(prices[i - period + 1:i + 1]) / period
            sma_values.append(avg)
        
        return sma_values
    
    async def _fetch_prices(self, symbol: str, timeframe: str) -> List[float]:
        """Simulate fetching price data"""
        # In real implementation, fetch from your data source
        import random
        base_price = 50000 if "BTC" in symbol else 3000
        return [base_price + random.uniform(-1000, 1000) for _ in range(50)]
```

### RSI Momentum Strategy

```python
class RSIMomentum:
    """RSI-based momentum strategy"""
    
    @property
    def name(self) -> str:
        return "RSI_Momentum"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        # Fetch price data
        prices = await self._fetch_prices(request.symbol, request.timeframe)
        
        if len(prices) < 15:  # Need at least 15 periods for RSI calculation
            return self._insufficient_data_result(request)
        
        # Calculate RSI
        rsi = self._calculate_rsi(prices, period=14)
        current_rsi = rsi[-1] if rsi else 50
        
        # Generate signals based on RSI levels
        signal = "hold"
        strength = 0.0
        signal_type = "neutral"
        
        if current_rsi < 30:
            signal = "buy"
            strength = (30 - current_rsi) / 30  # Stronger signal when more oversold
            signal_type = "reversal"
        elif current_rsi > 70:
            signal = "sell"
            strength = (current_rsi - 70) / 30  # Stronger signal when more overbought
            signal_type = "reversal"
        
        facts = {
            "primary_signal": signal,
            "signal_strength": min(strength, 1.0),
            "signal_type": signal_type,
            "rsi": current_rsi,
            "rsi_oversold": current_rsi < 30,
            "rsi_overbought": current_rsi > 70,
            "price": prices[-1]
        }
        
        quality = QualityMeta(
            sample_size=float(len(prices)),
            freshness_sec=60.0,
            data_completeness=1.0
        )
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return []
        
        gains = []
        losses = []
        
        # Calculate price changes
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))
        
        rsi_values = []
        
        # Calculate RSI for each period
        for i in range(period - 1, len(gains)):
            avg_gain = sum(gains[i - period + 1:i + 1]) / period
            avg_loss = sum(losses[i - period + 1:i + 1]) / period
            
            if avg_loss == 0:
                rsi = 100
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            rsi_values.append(rsi)
        
        return rsi_values
    
    def _insufficient_data_result(self, request: LegendRequest) -> LegendEnvelope:
        """Return neutral result when insufficient data"""
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts={
                "primary_signal": "hold",
                "signal_strength": 0.0,
                "error": "Insufficient data for RSI calculation"
            },
            quality=QualityMeta(0.0, 0.0, 0.0)
        )
    
    async def _fetch_prices(self, symbol: str, timeframe: str) -> List[float]:
        """Simulate fetching price data"""
        import random
        base_price = 50000 if "BTC" in symbol else 3000
        prices = [base_price]
        
        for _ in range(49):  # Generate 50 prices total
            change = random.uniform(-0.05, 0.05)  # ±5% change
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        return prices
```

## Advanced Examples

### Multi-Timeframe Analysis

```python
class MultiTimeframeAnalysis:
    """Analyze multiple timeframes for comprehensive view"""
    
    @property
    def name(self) -> str:
        return "Multi_Timeframe"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        # Define timeframes to analyze
        timeframes = ["1h", "4h", "1d"]
        analyses = {}
        
        for i, tf in enumerate(timeframes):
            if progress_callback:
                await progress_callback(LegendProgress(
                    legend=self.name,
                    stage=f"analyzing_{tf}",
                    percent=(i + 1) * 30.0,
                    note=f"Analyzing {tf} timeframe"
                ))
            
            # Analyze each timeframe
            analysis = await self._analyze_timeframe(request.symbol, tf)
            analyses[tf] = analysis
        
        # Combine insights from all timeframes
        combined_signal = self._combine_signals(analyses)
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="complete", percent=100.0
            ))
        
        facts = {
            "primary_signal": combined_signal["signal"],
            "signal_strength": combined_signal["strength"],
            "signal_type": "multi_timeframe",
            **{f"{tf}_trend": analysis["trend"] for tf, analysis in analyses.items()},
            **{f"{tf}_strength": analysis["strength"] for tf, analysis in analyses.items()}
        }
        
        # Quality based on worst timeframe
        min_quality = min(analysis["quality"] for analysis in analyses.values())
        quality = QualityMeta(
            sample_size=min_quality,
            freshness_sec=60.0,
            data_completeness=1.0
        )
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
    
    async def _analyze_timeframe(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Analyze a single timeframe"""
        prices = await self._fetch_prices(symbol, timeframe)
        
        if len(prices) < 20:
            return {"trend": "neutral", "strength": 0.0, "quality": 0.0}
        
        # Simple trend analysis using moving averages
        sma_short = sum(prices[-10:]) / 10
        sma_long = sum(prices[-20:]) / 20
        current_price = prices[-1]
        
        # Determine trend
        if current_price > sma_short > sma_long:
            trend = "bullish"
            strength = min((current_price - sma_long) / sma_long, 0.1) * 10
        elif current_price < sma_short < sma_long:
            trend = "bearish" 
            strength = min((sma_long - current_price) / sma_long, 0.1) * 10
        else:
            trend = "neutral"
            strength = 0.0
        
        return {
            "trend": trend,
            "strength": strength,
            "quality": float(len(prices))
        }
    
    def _combine_signals(self, analyses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Combine signals from multiple timeframes"""
        
        # Weight timeframes (longer timeframes have more weight)
        weights = {"1h": 0.2, "4h": 0.3, "1d": 0.5}
        
        bullish_score = 0.0
        bearish_score = 0.0
        
        for tf, analysis in analyses.items():
            weight = weights.get(tf, 0.33)
            strength = analysis["strength"]
            
            if analysis["trend"] == "bullish":
                bullish_score += strength * weight
            elif analysis["trend"] == "bearish":
                bearish_score += strength * weight
        
        # Determine combined signal
        if bullish_score > bearish_score and bullish_score > 0.3:
            return {"signal": "buy", "strength": bullish_score}
        elif bearish_score > bullish_score and bearish_score > 0.3:
            return {"signal": "sell", "strength": bearish_score}
        else:
            return {"signal": "hold", "strength": 0.0}
    
    async def _fetch_prices(self, symbol: str, timeframe: str) -> List[float]:
        """Simulate fetching timeframe-specific data"""
        import random
        
        # Different volatility for different timeframes
        volatility = {"1h": 0.02, "4h": 0.05, "1d": 0.1}.get(timeframe, 0.03)
        
        base_price = 50000 if "BTC" in symbol else 3000
        prices = [base_price]
        
        for _ in range(49):
            change = random.uniform(-volatility, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
        
        return prices
```

### Volume-Price Analysis

```python
class VolumePriceAnalysis:
    """Analyze price movements with volume confirmation"""
    
    @property
    def name(self) -> str:
        return "Volume_Price_Analysis"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="fetching_data", percent=25.0
            ))
        
        # Fetch price and volume data
        market_data = await self._fetch_market_data(request.symbol, request.timeframe)
        prices = market_data["prices"]
        volumes = market_data["volumes"]
        
        if len(prices) < 20 or len(volumes) < 20:
            return self._insufficient_data_result(request)
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="analyzing_volume", percent=70.0
            ))
        
        # Analyze volume patterns
        volume_analysis = self._analyze_volume_patterns(prices, volumes)
        
        # Analyze price patterns
        price_analysis = self._analyze_price_patterns(prices)
        
        # Combine volume and price analysis
        combined_signal = self._combine_analysis(volume_analysis, price_analysis)
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="complete", percent=100.0
            ))
        
        facts = {
            "primary_signal": combined_signal["signal"],
            "signal_strength": combined_signal["strength"],
            "signal_type": combined_signal["type"],
            "volume_trend": volume_analysis["trend"],
            "volume_spike": volume_analysis["spike"],
            "price_momentum": price_analysis["momentum"],
            "breakout_confirmed": combined_signal.get("breakout_confirmed", False),
            "current_price": prices[-1],
            "current_volume": volumes[-1],
            "avg_volume": sum(volumes[-20:]) / 20
        }
        
        quality = QualityMeta(
            sample_size=float(len(prices)),
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
    
    def _analyze_volume_patterns(self, prices: List[float], volumes: List[float]) -> Dict[str, Any]:
        """Analyze volume patterns and trends"""
        current_volume = volumes[-1]
        avg_volume = sum(volumes[-20:]) / 20
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        
        # Check for volume spike
        volume_spike = volume_ratio > 1.5
        
        # Volume trend (increasing/decreasing)
        recent_avg = sum(volumes[-5:]) / 5
        older_avg = sum(volumes[-15:-5]) / 10
        
        if recent_avg > older_avg * 1.2:
            volume_trend = "increasing"
        elif recent_avg < older_avg * 0.8:
            volume_trend = "decreasing"
        else:
            volume_trend = "stable"
        
        return {
            "trend": volume_trend,
            "spike": volume_spike,
            "ratio": volume_ratio
        }
    
    def _analyze_price_patterns(self, prices: List[float]) -> Dict[str, Any]:
        """Analyze price momentum and patterns"""
        current_price = prices[-1]
        prev_price = prices[-2] if len(prices) > 1 else current_price
        
        # Calculate momentum
        price_change = (current_price - prev_price) / prev_price if prev_price != 0 else 0
        
        # Price momentum over last 5 periods
        if len(prices) >= 5:
            momentum_5 = (prices[-1] - prices[-5]) / prices[-5]
        else:
            momentum_5 = 0
        
        # Determine momentum strength
        if abs(momentum_5) > 0.05:  # 5% change
            momentum = "strong"
        elif abs(momentum_5) > 0.02:  # 2% change
            momentum = "moderate"
        else:
            momentum = "weak"
        
        return {
            "momentum": momentum,
            "change_percent": price_change * 100,
            "momentum_5_percent": momentum_5 * 100
        }
    
    def _combine_analysis(self, volume_analysis: Dict, price_analysis: Dict) -> Dict[str, Any]:
        """Combine volume and price analysis for signals"""
        
        signal = "hold"
        strength = 0.0
        signal_type = "neutral"
        breakout_confirmed = False
        
        # Strong bullish signal: price up + volume spike
        if (price_analysis["change_percent"] > 2 and 
            volume_analysis["spike"] and 
            volume_analysis["trend"] == "increasing"):
            signal = "buy"
            strength = 0.9
            signal_type = "breakout"
            breakout_confirmed = True
        
        # Strong bearish signal: price down + volume spike
        elif (price_analysis["change_percent"] < -2 and 
              volume_analysis["spike"] and 
              volume_analysis["trend"] == "increasing"):
            signal = "sell"
            strength = 0.9
            signal_type = "breakdown"
            breakout_confirmed = True
        
        # Moderate bullish: good momentum + volume support
        elif (price_analysis["momentum"] in ["moderate", "strong"] and 
              price_analysis["momentum_5_percent"] > 0 and
              volume_analysis["trend"] != "decreasing"):
            signal = "buy"
            strength = 0.6
            signal_type = "momentum"
        
        # Moderate bearish: negative momentum + volume support
        elif (price_analysis["momentum"] in ["moderate", "strong"] and 
              price_analysis["momentum_5_percent"] < 0 and
              volume_analysis["trend"] != "decreasing"):
            signal = "sell"
            strength = 0.6
            signal_type = "momentum"
        
        return {
            "signal": signal,
            "strength": strength,
            "type": signal_type,
            "breakout_confirmed": breakout_confirmed
        }
    
    async def _fetch_market_data(self, symbol: str, timeframe: str) -> Dict[str, List[float]]:
        """Simulate fetching price and volume data"""
        import random
        
        base_price = 50000 if "BTC" in symbol else 3000
        base_volume = 1000000
        
        prices = [base_price]
        volumes = [base_volume]
        
        for i in range(49):
            # Generate correlated price and volume
            price_change = random.uniform(-0.03, 0.03)
            new_price = prices[-1] * (1 + price_change)
            
            # Volume tends to be higher during price movements
            volume_multiplier = 1 + abs(price_change) * 2 + random.uniform(-0.3, 0.3)
            new_volume = volumes[-1] * max(0.5, volume_multiplier)
            
            prices.append(new_price)
            volumes.append(new_volume)
        
        return {"prices": prices, "volumes": volumes}
    
    def _insufficient_data_result(self, request: LegendRequest) -> LegendEnvelope:
        """Return neutral result when insufficient data"""
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts={
                "primary_signal": "hold",
                "signal_strength": 0.0,
                "error": "Insufficient price or volume data"
            },
            quality=QualityMeta(0.0, 0.0, 0.0)
        )
```

## Integration Examples

### Using Multiple Legends with Pantheon

```python
import asyncio
from datetime import datetime
from legends import Pantheon, LegendRequest

async def comprehensive_analysis_example():
    """Example of running multiple legends together"""
    
    # Create pantheon and register legends
    pantheon = Pantheon()
    pantheon.register_engine(MovingAverageCrossover())
    pantheon.register_engine(RSIMomentum())
    pantheon.register_engine(MultiTimeframeAnalysis())
    pantheon.register_engine(VolumePriceAnalysis())
    
    # Create analysis request
    request = LegendRequest(
        symbol="BTC-USD",
        timeframe="1h",
        as_of=datetime.now()
    )
    
    # Progress tracking
    progress_log = []
    async def progress_handler(progress):
        progress_log.append(f"{progress.legend}: {progress.stage} ({progress.percent:.1f}%)")
        print(progress_log[-1])
    
    # Run all legends
    print("Running comprehensive analysis...")
    results = await pantheon.run_all_legends_async(request, progress_handler)
    
    # Analyze results
    signals = {}
    for result in results:
        signals[result.legend] = {
            "signal": result.facts.get("primary_signal"),
            "strength": result.facts.get("signal_strength", 0),
            "quality": result.quality.sample_size
        }
    
    # Create consensus signal
    consensus = create_consensus_signal(signals)
    
    print(f"\n--- Analysis Results for {request.symbol} ---")
    for legend, signal_data in signals.items():
        print(f"{legend}: {signal_data['signal']} (strength: {signal_data['strength']:.2f})")
    
    print(f"\nConsensus Signal: {consensus['signal']} (confidence: {consensus['confidence']:.2f})")
    
    return results, consensus

def create_consensus_signal(signals: Dict[str, Dict]) -> Dict[str, Any]:
    """Create consensus signal from multiple legend results"""
    
    # Weight signals by quality and strength
    buy_score = 0.0
    sell_score = 0.0
    total_weight = 0.0
    
    for legend, data in signals.items():
        signal = data["signal"]
        strength = data["strength"]
        quality_weight = min(data["quality"] / 100.0, 1.0)  # Normalize quality
        
        weight = strength * quality_weight
        total_weight += weight
        
        if signal == "buy":
            buy_score += weight
        elif signal == "sell":
            sell_score += weight
    
    if total_weight == 0:
        return {"signal": "hold", "confidence": 0.0}
    
    # Normalize scores
    buy_score /= total_weight
    sell_score /= total_weight
    
    # Determine consensus
    if buy_score > sell_score and buy_score > 0.3:
        return {"signal": "buy", "confidence": buy_score}
    elif sell_score > buy_score and sell_score > 0.3:
        return {"signal": "sell", "confidence": sell_score}
    else:
        return {"signal": "hold", "confidence": max(buy_score, sell_score)}

# Run the example
if __name__ == "__main__":
    asyncio.run(comprehensive_analysis_example())
```

### Custom Progress Reporting

```python
import asyncio
from datetime import datetime

class ProgressTracker:
    """Enhanced progress tracking with timing and logging"""
    
    def __init__(self):
        self.start_time = None
        self.legend_progress = {}
        self.completed_legends = set()
    
    async def __call__(self, progress):
        """Progress callback function"""
        if self.start_time is None:
            self.start_time = datetime.now()
        
        legend = progress.legend
        self.legend_progress[legend] = progress
        
        # Calculate elapsed time
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Display progress
        print(f"[{elapsed:6.1f}s] {legend:20} | {progress.stage:15} | {progress.percent:6.1f}%")
        
        if progress.note:
            print(f"{'':30} Note: {progress.note}")
        
        # Track completed legends
        if progress.percent >= 100.0:
            self.completed_legends.add(legend)
    
    def get_summary(self):
        """Get progress summary"""
        total_legends = len(self.legend_progress)
        completed_count = len(self.completed_legends)
        
        if total_legends == 0:
            return "No legends executed"
        
        completion_rate = completed_count / total_legends * 100
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        return f"Completed {completed_count}/{total_legends} legends ({completion_rate:.1f}%) in {elapsed:.1f}s"

async def progress_tracking_example():
    """Example with enhanced progress tracking"""
    
    pantheon = Pantheon()
    pantheon.register_engine(MovingAverageCrossover())
    pantheon.register_engine(RSIMomentum())
    
    request = LegendRequest("ETH-USD", "4h", datetime.now())
    
    # Use custom progress tracker
    tracker = ProgressTracker()
    
    print("Starting analysis with progress tracking...")
    print("-" * 70)
    
    results = await pantheon.run_all_legends_async(request, tracker)
    
    print("-" * 70)
    print(tracker.get_summary())
    
    return results

# Run progress tracking example
if __name__ == "__main__":
    asyncio.run(progress_tracking_example())
```

## Testing Examples

### Comprehensive Test Suite

```python
import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch
from legends import LegendRequest, Pantheon

class TestMovingAverageCrossover:
    """Comprehensive test suite for MovingAverageCrossover legend"""
    
    @pytest.fixture
    def legend(self):
        return MovingAverageCrossover()
    
    @pytest.fixture
    def sample_request(self):
        return LegendRequest("BTC-USD", "1h", datetime.now())
    
    @pytest.mark.asyncio
    async def test_basic_functionality(self, legend, sample_request):
        """Test basic legend execution"""
        result = await legend.run_async(sample_request)
        
        assert result.legend == "SMA_Crossover"
        assert result.tf == "1h"
        assert "primary_signal" in result.facts
        assert result.facts["primary_signal"] in ["buy", "sell", "hold"]
        assert 0.0 <= result.facts["signal_strength"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_progress_reporting(self, legend, sample_request):
        """Test progress callback functionality"""
        progress_updates = []
        
        async def progress_handler(progress):
            progress_updates.append(progress)
        
        await legend.run_async(sample_request, progress_handler)
        
        assert len(progress_updates) >= 2  # At least start and end
        assert progress_updates[0].percent == 20.0  # First progress
        assert progress_updates[-1].percent == 100.0  # Final progress
    
    @pytest.mark.asyncio
    async def test_with_mock_data(self, legend, sample_request):
        """Test with controlled market data"""
        # Mock data that should trigger buy signal
        bullish_prices = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109] * 5
        
        with patch.object(legend, '_fetch_prices', return_value=bullish_prices):
            result = await legend.run_async(sample_request)
            
            # Should generate buy signal due to uptrend
            assert result.facts["primary_signal"] in ["buy", "hold"]
            assert result.facts["sma_short"] > result.facts["sma_long"]
    
    def test_sma_calculation(self, legend):
        """Test SMA calculation logic"""
        prices = [10, 12, 14, 16, 18, 20]
        
        # Test 3-period SMA
        sma_3 = legend._sma(prices, 3)
        expected = [12.0, 14.0, 16.0, 18.0]  # (10+12+14)/3, (12+14+16)/3, etc.
        
        assert len(sma_3) == 4
        assert sma_3 == expected
    
    def test_insufficient_data(self, legend):
        """Test behavior with insufficient data"""
        short_prices = [100, 101]
        
        sma_10 = legend._sma(short_prices, 10)
        assert sma_10 == []  # Should return empty list

@pytest.mark.asyncio
async def test_pantheon_integration():
    """Test legends working with Pantheon orchestrator"""
    pantheon = Pantheon()
    pantheon.register_engine(MovingAverageCrossover())
    pantheon.register_engine(RSIMomentum())
    
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    
    # Test running all legends
    results = await pantheon.run_all_legends_async(request)
    
    assert len(results) == 2
    legend_names = [result.legend for result in results]
    assert "SMA_Crossover" in legend_names
    assert "RSI_Momentum" in legend_names
    
    # Test running specific legend
    sma_result = await pantheon.run_single_legend_async("SMA_Crossover", request)
    assert sma_result.legend == "SMA_Crossover"

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in legends"""
    
    class ErrorLegend:
        @property
        def name(self):
            return "ErrorLegend"
        
        async def run_async(self, request, progress_callback=None):
            raise ValueError("Test error")
    
    pantheon = Pantheon()
    pantheon.register_engine(ErrorLegend())
    
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    
    # Should handle errors gracefully
    with pytest.raises(ValueError):
        await pantheon.run_single_legend_async("ErrorLegend", request)

def test_data_quality_assessment():
    """Test quality metric calculations"""
    legend = MovingAverageCrossover()
    
    # Test with good data
    good_prices = list(range(100))
    # In real implementation, quality would be calculated in run_async
    
    # Test with limited data
    limited_prices = list(range(10))
    # Quality should reflect data limitations
```

## Performance Examples

### Optimized Legend with Caching

```python
import asyncio
from functools import lru_cache
from typing import Tuple, Dict, Any
import time

class OptimizedLegend:
    """Example of performance-optimized legend"""
    
    def __init__(self):
        self._cache = {}
        self._cache_ttl = 60  # 60 seconds
    
    @property
    def name(self) -> str:
        return "Optimized_Legend"
    
    async def run_async(self, request: LegendRequest, progress_callback=None) -> LegendEnvelope:
        start_time = time.time()
        
        # Use cached data if available
        cache_key = f"{request.symbol}_{request.timeframe}"
        cached_data = self._get_cached_data(cache_key)
        
        if cached_data:
            market_data = cached_data
            if progress_callback:
                await progress_callback(LegendProgress(
                    legend=self.name, stage="using_cache", percent=50.0
                ))
        else:
            if progress_callback:
                await progress_callback(LegendProgress(
                    legend=self.name, stage="fetching_data", percent=25.0
                ))
            
            market_data = await self._fetch_market_data(request.symbol, request.timeframe)
            self._cache_data(cache_key, market_data)
        
        # Use async processing for heavy calculations
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="calculating", percent=75.0
            ))
        
        # Run calculations in parallel
        indicators_task = asyncio.create_task(self._calculate_indicators(market_data))
        signals_task = asyncio.create_task(self._generate_signals(market_data))
        
        indicators, signals = await asyncio.gather(indicators_task, signals_task)
        
        # Combine results
        facts = {**indicators, **signals}
        facts["execution_time_ms"] = (time.time() - start_time) * 1000
        
        if progress_callback:
            await progress_callback(LegendProgress(
                legend=self.name, stage="complete", percent=100.0
            ))
        
        quality = QualityMeta(
            sample_size=float(len(market_data.get("prices", []))),
            freshness_sec=time.time() - market_data.get("timestamp", time.time()),
            data_completeness=1.0
        )
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
    
    def _get_cached_data(self, cache_key: str) -> Dict[str, Any]:
        """Get data from cache if not expired"""
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                return data
        return None
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]):
        """Cache data with timestamp"""
        data_with_timestamp = {**data, "timestamp": time.time()}
        self._cache[cache_key] = (data_with_timestamp, time.time())
    
    @lru_cache(maxsize=128)
    def _calculate_sma_cached(self, prices_tuple: Tuple[float, ...], period: int) -> float:
        """Cached SMA calculation for expensive operations"""
        prices = list(prices_tuple)
        if len(prices) < period:
            return 0.0
        return sum(prices[-period:]) / period
    
    async def _calculate_indicators(self, market_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate technical indicators asynchronously"""
        # Simulate CPU-intensive calculation
        await asyncio.sleep(0.1)  # Non-blocking wait
        
        prices = market_data.get("prices", [])
        if len(prices) < 20:
            return {"sma_20": 0.0, "sma_50": 0.0}
        
        # Use cached calculation for expensive operations
        prices_tuple = tuple(prices)
        sma_20 = self._calculate_sma_cached(prices_tuple, 20)
        sma_50 = self._calculate_sma_cached(prices_tuple, 50)
        
        return {"sma_20": sma_20, "sma_50": sma_50}
    
    async def _generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trading signals asynchronously"""
        # Simulate signal processing
        await asyncio.sleep(0.05)
        
        prices = market_data.get("prices", [])
        if len(prices) < 2:
            return {"primary_signal": "hold", "signal_strength": 0.0}
        
        # Simple momentum signal
        momentum = (prices[-1] - prices[-20]) / prices[-20] if len(prices) >= 20 else 0
        
        if momentum > 0.05:
            return {"primary_signal": "buy", "signal_strength": min(momentum * 10, 1.0)}
        elif momentum < -0.05:
            return {"primary_signal": "sell", "signal_strength": min(abs(momentum) * 10, 1.0)}
        else:
            return {"primary_signal": "hold", "signal_strength": 0.0}
    
    async def _fetch_market_data(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Simulate fetching market data with realistic delay"""
        # Simulate network delay
        await asyncio.sleep(0.2)
        
        import random
        base_price = 50000 if "BTC" in symbol else 3000
        
        prices = []
        for i in range(100):
            price = base_price * (1 + random.uniform(-0.1, 0.1))
            prices.append(price)
        
        return {
            "prices": prices,
            "volumes": [random.uniform(1000, 10000) for _ in range(100)],
            "timestamp": time.time()
        }

# Performance testing
async def performance_test():
    """Test legend performance"""
    legend = OptimizedLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    
    # Test multiple runs to see caching effect
    times = []
    
    for i in range(3):
        start = time.time()
        result = await legend.run_async(request)
        execution_time = time.time() - start
        times.append(execution_time)
        
        print(f"Run {i+1}: {execution_time:.3f}s (reported: {result.facts['execution_time_ms']:.1f}ms)")
    
    print(f"Average: {sum(times)/len(times):.3f}s")
    print(f"Cache benefit: {times[0]/times[1]:.1f}x faster on cached run")

if __name__ == "__main__":
    asyncio.run(performance_test())
```

These examples demonstrate various patterns and techniques for building effective legends. Use them as templates and inspiration for your own legend implementations.

Next: [Troubleshooting Guide](troubleshooting.md)
