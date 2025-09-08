# Legend Development Guide

## Building Effective Legend Engines

This guide covers best practices for developing robust, performant legend engines.

## Legend Engine Architecture

### Core Interface
Every legend must implement the `ILegendEngine` protocol:

```python
class ILegendEngine(Protocol):
    @property
    def name(self) -> str: ...
    
    async def run_async(
        self, 
        request: LegendRequest, 
        progress_callback: Optional[ProgressCallback] = None
    ) -> LegendEnvelope: ...
```

### Essential Components

#### 1. Name Property
```python
@property
def name(self) -> str:
    return "MyLegend"  # Unique identifier for your legend
```

#### 2. Async Execution
```python
async def run_async(self, request, progress_callback=None):
    # Your analysis logic here
    pass
```

#### 3. Progress Reporting
```python
if progress_callback:
    await progress_callback(LegendProgress(
        legend=self.name,
        stage="analyzing",
        percent=50.0,
        note="Processing market data"
    ))
```

## Data Processing Patterns

### Market Data Access
```python
async def _fetch_market_data(self, symbol: str, timeframe: str) -> Dict[str, Any]:
    """
    Connect to your data source:
    - REST APIs (Binance, Coinbase, Alpha Vantage)
    - WebSocket feeds
    - Local databases
    - CSV files
    """
    # Example: REST API call
    async with aiohttp.ClientSession() as session:
        url = f"https://api.exchange.com/klines?symbol={symbol}&interval={timeframe}"
        async with session.get(url) as response:
            return await response.json()
```

### Technical Indicators
```python
def _calculate_moving_average(self, prices: List[float], period: int) -> float:
    """Calculate simple moving average"""
    if len(prices) < period:
        return 0.0
    return sum(prices[-period:]) / period

def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

## Signal Generation

### Signal Types
```python
def _generate_signals(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate trading signals from market data"""
    
    signals = {
        "primary_signal": None,      # Main signal: "buy", "sell", "hold"
        "signal_strength": 0.0,      # Confidence: 0.0 to 1.0
        "signal_type": "neutral",    # Type: "breakout", "reversal", "continuation"
        "entry_price": None,         # Suggested entry price
        "stop_loss": None,          # Risk management level
        "take_profit": None,        # Profit target
        "timeframe_bias": "neutral", # "bullish", "bearish", "neutral"
    }
    
    # Your signal logic here
    if self._detect_breakout(market_data):
        signals["primary_signal"] = "buy"
        signals["signal_strength"] = 0.85
        signals["signal_type"] = "breakout"
    
    return signals
```

### Pattern Recognition
```python
def _detect_breakout(self, market_data: Dict[str, Any]) -> bool:
    """Detect price breakout patterns"""
    prices = market_data.get("prices", [])
    volumes = market_data.get("volumes", [])
    
    if len(prices) < 20 or len(volumes) < 20:
        return False
    
    # Check for price breakout above resistance
    resistance_level = max(prices[-20:-1])
    current_price = prices[-1]
    
    # Check for volume confirmation
    avg_volume = sum(volumes[-20:-1]) / 19
    current_volume = volumes[-1]
    
    price_breakout = current_price > resistance_level * 1.02  # 2% above resistance
    volume_confirmation = current_volume > avg_volume * 1.5   # 50% above average
    
    return price_breakout and volume_confirmation
```

## Quality Metrics

### Data Quality Assessment
```python
def _calculate_quality(self, market_data: Dict[str, Any]) -> QualityMeta:
    """Assess the quality of input data"""
    
    # Sample size - how much data we analyzed
    sample_size = len(market_data.get("prices", []))
    
    # Data freshness - how recent is the data
    last_timestamp = market_data.get("last_update", datetime.now())
    freshness_sec = (datetime.now() - last_timestamp).total_seconds()
    
    # Data completeness - percentage of expected data present
    expected_points = 100  # Expected number of data points
    actual_points = sample_size
    data_completeness = min(1.0, actual_points / expected_points)
    
    return QualityMeta(
        sample_size=float(sample_size),
        freshness_sec=freshness_sec,
        data_completeness=data_completeness
    )
```

## Performance Optimization

### Async Best Practices
```python
async def run_async(self, request, progress_callback=None):
    """Optimize for async performance"""
    
    # Use async for I/O operations
    market_data = await self._fetch_market_data(request.symbol, request.timeframe)
    
    # Use asyncio.gather for parallel operations
    indicators_task = asyncio.create_task(self._calculate_indicators(market_data))
    signals_task = asyncio.create_task(self._generate_signals(market_data))
    
    indicators, signals = await asyncio.gather(indicators_task, signals_task)
    
    # Combine results
    facts = {**indicators, **signals}
    
    return LegendEnvelope(...)
```

### Caching Strategies
```python
from functools import lru_cache
from typing import Tuple

class MyLegend:
    def __init__(self):
        self._cache = {}
    
    @lru_cache(maxsize=128)
    def _calculate_expensive_indicator(self, price_tuple: Tuple[float, ...]) -> float:
        """Cache expensive calculations"""
        # Convert tuple back to list for processing
        prices = list(price_tuple)
        # Expensive calculation here
        return result
    
    async def _get_cached_data(self, symbol: str, timeframe: str) -> Dict[str, Any]:
        """Cache market data for a short period"""
        cache_key = f"{symbol}_{timeframe}"
        cache_expiry = 60  # 60 seconds
        
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if (datetime.now() - timestamp).seconds < cache_expiry:
                return data
        
        # Fetch fresh data
        data = await self._fetch_market_data(symbol, timeframe)
        self._cache[cache_key] = (data, datetime.now())
        return data
```

## Error Handling

### Robust Error Management
```python
async def run_async(self, request, progress_callback=None):
    """Handle errors gracefully"""
    
    try:
        # Data fetching with timeout
        market_data = await asyncio.wait_for(
            self._fetch_market_data(request.symbol, request.timeframe),
            timeout=30.0
        )
        
        if not market_data or len(market_data.get("prices", [])) == 0:
            # Return neutral result for insufficient data
            return self._create_neutral_result(request, "Insufficient market data")
        
        # Analysis with fallback
        try:
            facts = await self._run_analysis(market_data)
        except Exception as e:
            # Log error but continue with basic analysis
            facts = self._basic_fallback_analysis(market_data)
        
        quality = self._calculate_quality(market_data)
        
        return LegendEnvelope(
            legend=self.name,
            at=request.as_of,
            tf=request.timeframe,
            facts=facts,
            quality=quality
        )
        
    except asyncio.TimeoutError:
        return self._create_neutral_result(request, "Data fetch timeout")
    except Exception as e:
        return self._create_error_result(request, str(e))

def _create_neutral_result(self, request: LegendRequest, reason: str) -> LegendEnvelope:
    """Create a neutral result when analysis cannot be performed"""
    return LegendEnvelope(
        legend=self.name,
        at=request.as_of,
        tf=request.timeframe,
        facts={
            "primary_signal": "hold",
            "signal_strength": 0.0,
            "error_reason": reason
        },
        quality=QualityMeta(0.0, 0.0, 0.0)
    )
```

## Testing Your Legend

### Unit Testing
```python
import pytest
from datetime import datetime
from legends import LegendRequest

class TestMyLegend:
    
    @pytest.fixture
    def legend(self):
        return MyLegend()
    
    @pytest.fixture 
    def sample_request(self):
        return LegendRequest(
            symbol="BTC-USD",
            timeframe="1h",
            as_of=datetime.now()
        )
    
    @pytest.mark.asyncio
    async def test_basic_functionality(self, legend, sample_request):
        """Test basic legend functionality"""
        result = await legend.run_async(sample_request)
        
        assert result.legend == legend.name
        assert result.tf == sample_request.timeframe
        assert isinstance(result.facts, dict)
        assert result.quality.sample_size >= 0
    
    @pytest.mark.asyncio
    async def test_progress_reporting(self, legend, sample_request):
        """Test progress callback functionality"""
        progress_updates = []
        
        async def progress_handler(progress):
            progress_updates.append(progress)
        
        await legend.run_async(sample_request, progress_handler)
        
        assert len(progress_updates) > 0
        assert all(0 <= p.percent <= 100 for p in progress_updates)
```

### Integration Testing
```python
@pytest.mark.asyncio
async def test_with_pantheon():
    """Test legend integration with Pantheon"""
    pantheon = Pantheon()
    pantheon.register_engine(MyLegend())
    
    request = LegendRequest("ETH-USD", "1h", datetime.now())
    results = await pantheon.run_all_legends_async(request)
    
    assert len(results) == 1
    assert results[0].legend == "MyLegend"
```

## Deployment Considerations

### Configuration
```python
import os
from dataclasses import dataclass

@dataclass
class LegendConfig:
    """Configuration for legend engine"""
    api_key: str = os.getenv("MARKET_API_KEY", "")
    base_url: str = os.getenv("MARKET_API_URL", "https://api.example.com")
    timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "60"))

class MyLegend:
    def __init__(self, config: LegendConfig = None):
        self.config = config or LegendConfig()
```

### Logging
```python
import logging

class MyLegend:
    def __init__(self):
        self.logger = logging.getLogger(f"legends.{self.name}")
    
    async def run_async(self, request, progress_callback=None):
        self.logger.info(f"Starting analysis for {request.symbol}")
        
        try:
            result = await self._analyze(request)
            self.logger.info(f"Analysis complete: {result.facts.get('primary_signal')}")
            return result
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise
```

## Best Practices Summary

1. **Always implement proper error handling**
2. **Use async/await for I/O operations** 
3. **Report progress for long-running operations**
4. **Cache expensive calculations when appropriate**
5. **Validate input data before processing**
6. **Return meaningful quality metrics**
7. **Test with real market data**
8. **Document your algorithm and parameters**
9. **Follow consistent naming conventions**
10. **Consider performance implications of your code**

Next: [API Reference](api-reference.md)
