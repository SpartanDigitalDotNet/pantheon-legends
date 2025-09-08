# Troubleshooting Guide

Common issues and solutions when working with Pantheon Legends.

## Installation Issues

### Package Not Found
```bash
pip install pantheon-legends
# Error: Could not find a version that satisfies the requirement pantheon-legends
```

**Solutions:**
1. Check package name spelling
2. Update pip: `pip install --upgrade pip`
3. Try with specific index: `pip install -i https://pypi.org/simple/ pantheon-legends`
4. Verify Python version (requires 3.8+)

### Import Errors
```python
from legends import LegendRequest
# ImportError: No module named 'legends'
```

**Solutions:**
1. Verify installation: `pip list | grep pantheon`
2. Check virtual environment activation
3. Test installation: `python -c "from legends import test_installation; print(test_installation())"`

### Version Conflicts
```bash
pip install pantheon-legends
# ERROR: pip's dependency resolver does not currently take into account all the packages
```

**Solutions:**
1. Create fresh virtual environment:
   ```bash
   python -m venv legend_env
   legend_env\Scripts\activate  # Windows
   pip install pantheon-legends
   ```
2. Use pip's legacy resolver: `pip install --use-deprecated=legacy-resolver pantheon-legends`

## Development Issues

### Async/Await Problems

**Problem: Legend not executing**
```python
class MyLegend:
    async def run_async(self, request, progress_callback=None):
        return result

# Not working
result = legend.run_async(request)  # Returns coroutine, not result
```

**Solution:**
```python
import asyncio

# Correct usage
result = await legend.run_async(request)

# Or in non-async context
result = asyncio.run(legend.run_async(request))
```

**Problem: Blocking operations in async code**
```python
async def run_async(self, request, progress_callback=None):
    time.sleep(5)  # Blocks event loop!
    return result
```

**Solution:**
```python
async def run_async(self, request, progress_callback=None):
    await asyncio.sleep(5)  # Non-blocking
    return result

# For CPU-intensive work
import asyncio
import concurrent.futures

async def run_async(self, request, progress_callback=None):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, cpu_intensive_function, data)
    return result
```

### Progress Callback Issues

**Problem: Progress callback not working**
```python
async def run_async(self, request, progress_callback=None):
    if progress_callback:
        progress_callback(LegendProgress(...))  # Missing await!
```

**Solution:**
```python
async def run_async(self, request, progress_callback=None):
    if progress_callback:
        await progress_callback(LegendProgress(...))
```

**Problem: Progress percentages don't make sense**
```python
# Bad progress reporting
await progress_callback(LegendProgress(legend=self.name, stage="start", percent=50))
await progress_callback(LegendProgress(legend=self.name, stage="middle", percent=25))
```

**Solution:**
```python
# Good progress reporting
await progress_callback(LegendProgress(legend=self.name, stage="start", percent=0))
await progress_callback(LegendProgress(legend=self.name, stage="middle", percent=50))
await progress_callback(LegendProgress(legend=self.name, stage="complete", percent=100))
```

### Data Quality Issues

**Problem: Quality metrics always zero**
```python
quality = QualityMeta(0.0, 0.0, 0.0)  # Not helpful
```

**Solution:**
```python
def _calculate_quality(self, market_data):
    sample_size = len(market_data.get('prices', []))
    
    # Calculate data freshness
    last_update = market_data.get('timestamp', datetime.now())
    freshness_sec = (datetime.now() - last_update).total_seconds()
    
    # Calculate completeness
    expected_samples = 100  # Expected number of data points
    completeness = min(1.0, sample_size / expected_samples)
    
    return QualityMeta(
        sample_size=float(sample_size),
        freshness_sec=freshness_sec,
        data_completeness=completeness
    )
```

## Runtime Errors

### Memory Issues

**Problem: Legend consumes too much memory**
```python
class MemoryHungryLegend:
    def __init__(self):
        self.historical_data = []  # Keeps growing!
    
    async def run_async(self, request, progress_callback=None):
        data = await self._fetch_large_dataset()
        self.historical_data.append(data)  # Memory leak
```

**Solution:**
```python
class EfficientLegend:
    def __init__(self):
        self._cache = {}
        self._max_cache_size = 100
    
    async def run_async(self, request, progress_callback=None):
        # Process data without storing everything
        data = await self._fetch_data()
        result = self._process_data(data)
        
        # Limited caching
        if len(self._cache) >= self._max_cache_size:
            # Remove oldest entries
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        return result
```

### Timeout Issues

**Problem: Legend times out**
```python
async def run_async(self, request, progress_callback=None):
    # Long-running operation without timeout handling
    data = await self._fetch_massive_dataset()  # Takes 5 minutes
```

**Solution:**
```python
import asyncio

async def run_async(self, request, progress_callback=None):
    try:
        # Set reasonable timeout
        data = await asyncio.wait_for(
            self._fetch_data(), 
            timeout=30.0  # 30 seconds
        )
    except asyncio.TimeoutError:
        # Return neutral result on timeout
        return self._create_timeout_result(request)
    
    return await self._analyze_data(data)

def _create_timeout_result(self, request):
    return LegendEnvelope(
        legend=self.name,
        at=request.as_of,
        tf=request.timeframe,
        facts={
            "primary_signal": "hold",
            "signal_strength": 0.0,
            "error": "Analysis timeout"
        },
        quality=QualityMeta(0.0, 0.0, 0.0)
    )
```

### Network/API Issues

**Problem: API rate limiting**
```python
async def _fetch_data(self, symbol):
    # Makes too many requests
    data = []
    for i in range(100):
        response = await self._api_call(symbol, i)  # Rate limited!
        data.append(response)
```

**Solution:**
```python
import asyncio
import aiohttp
from asyncio import Semaphore

class RateLimitedLegend:
    def __init__(self):
        self._rate_limiter = Semaphore(5)  # Max 5 concurrent requests
        self._session = None
    
    async def _get_session(self):
        if self._session is None:
            connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            self._session = aiohttp.ClientSession(connector=connector)
        return self._session
    
    async def _fetch_data_with_rate_limit(self, symbol):
        async with self._rate_limiter:
            session = await self._get_session()
            try:
                async with session.get(f"https://api.example.com/{symbol}") as response:
                    return await response.json()
            except aiohttp.ClientError as e:
                # Handle network errors
                return {"error": str(e), "prices": []}
    
    async def _batch_fetch(self, symbols):
        # Fetch with rate limiting
        tasks = [self._fetch_data_with_rate_limit(symbol) for symbol in symbols]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

## Data Issues

### Missing or Invalid Data

**Problem: Legend crashes on missing data**
```python
async def run_async(self, request, progress_callback=None):
    data = await self._fetch_data(request.symbol)
    prices = data['prices']  # KeyError if 'prices' doesn't exist
    return self._analyze(prices[0])  # IndexError if prices is empty
```

**Solution:**
```python
async def run_async(self, request, progress_callback=None):
    try:
        data = await self._fetch_data(request.symbol)
        
        # Validate data structure
        if not isinstance(data, dict):
            return self._create_error_result(request, "Invalid data format")
        
        prices = data.get('prices', [])
        if not prices or len(prices) < 10:
            return self._create_insufficient_data_result(request)
        
        # Validate price data
        valid_prices = [p for p in prices if isinstance(p, (int, float)) and p > 0]
        if len(valid_prices) < len(prices) * 0.8:  # 80% of data should be valid
            return self._create_error_result(request, "Too many invalid price points")
        
        return await self._analyze(valid_prices)
        
    except Exception as e:
        return self._create_error_result(request, f"Analysis failed: {str(e)}")

def _create_insufficient_data_result(self, request):
    return LegendEnvelope(
        legend=self.name,
        at=request.as_of,
        tf=request.timeframe,
        facts={
            "primary_signal": "hold",
            "signal_strength": 0.0,
            "error": "Insufficient data for analysis"
        },
        quality=QualityMeta(0.0, 0.0, 0.0)
    )
```

### Data Type Issues

**Problem: Type errors in calculations**
```python
def _calculate_sma(self, prices, period):
    return sum(prices[-period:]) / period  # TypeError if prices contains strings
```

**Solution:**
```python
def _calculate_sma(self, prices, period):
    try:
        # Ensure all prices are numeric
        numeric_prices = []
        for price in prices:
            if isinstance(price, (int, float)):
                numeric_prices.append(float(price))
            elif isinstance(price, str):
                try:
                    numeric_prices.append(float(price))
                except ValueError:
                    continue  # Skip invalid price
        
        if len(numeric_prices) < period:
            return 0.0
        
        return sum(numeric_prices[-period:]) / period
        
    except Exception as e:
        self.logger.error(f"SMA calculation error: {e}")
        return 0.0
```

## Pantheon Integration Issues

### Registration Problems

**Problem: Legend not found in Pantheon**
```python
pantheon = Pantheon()
pantheon.register_engine(MyLegend())

# Later...
result = await pantheon.run_single_legend_async("MyLegend", request)
# KeyError: Legend 'MyLegend' not found
```

**Solution:**
```python
# Check legend name property
class MyLegend:
    @property
    def name(self) -> str:
        return "MyLegend"  # Must match exactly

# Verify registration
pantheon = Pantheon()
pantheon.register_engine(MyLegend())

registered = pantheon.get_registered_engines()
print(f"Registered engines: {registered}")

# Use exact name from registration
if "MyLegend" in registered:
    result = await pantheon.run_single_legend_async("MyLegend", request)
```

### Concurrent Execution Issues

**Problem: Legends interfering with each other**
```python
class StatefulLegend:
    def __init__(self):
        self.shared_data = {}  # Shared between concurrent runs!
    
    async def run_async(self, request, progress_callback=None):
        self.shared_data[request.symbol] = "processing"  # Race condition
```

**Solution:**
```python
class StatelessLegend:
    async def run_async(self, request, progress_callback=None):
        # Use local variables for request-specific data
        local_data = {}
        
        # Or use request ID for isolation
        request_id = f"{request.symbol}_{request.timeframe}_{request.as_of.timestamp()}"
        
        # Process without shared state
        return await self._analyze(request, local_data)
```

## Performance Issues

### Slow Legend Execution

**Problem: Legend takes too long**
```python
async def run_async(self, request, progress_callback=None):
    # Inefficient data processing
    results = []
    for i in range(10000):
        result = complex_calculation(i)  # Blocking CPU work
        results.append(result)
```

**Solution:**
```python
import asyncio
import concurrent.futures

async def run_async(self, request, progress_callback=None):
    # Use thread pool for CPU-intensive work
    loop = asyncio.get_event_loop()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Batch process data
        batches = [data[i:i+1000] for i in range(0, len(data), 1000)]
        
        tasks = []
        for batch in batches:
            task = loop.run_in_executor(executor, self._process_batch, batch)
            tasks.append(task)
        
        # Process batches concurrently
        batch_results = await asyncio.gather(*tasks)
        
        # Combine results
        results = []
        for batch_result in batch_results:
            results.extend(batch_result)
    
    return self._create_result(results)

def _process_batch(self, batch):
    """CPU-intensive processing in thread pool"""
    return [complex_calculation(item) for item in batch]
```

### Memory Leaks

**Problem: Memory usage keeps growing**
```python
class LeakyLegend:
    def __init__(self):
        self.all_results = []  # Grows forever
    
    async def run_async(self, request, progress_callback=None):
        result = await self._analyze(request)
        self.all_results.append(result)  # Memory leak
        return result
```

**Solution:**
```python
from collections import deque
import weakref

class EfficientLegend:
    def __init__(self):
        # Use bounded cache
        self.recent_results = deque(maxlen=100)
        
        # Or use weak references
        self._result_cache = weakref.WeakValueDictionary()
    
    async def run_async(self, request, progress_callback=None):
        # Check cache first
        cache_key = f"{request.symbol}_{request.timeframe}"
        
        if cache_key in self._result_cache:
            return self._result_cache[cache_key]
        
        result = await self._analyze(request)
        
        # Store with automatic cleanup
        self._result_cache[cache_key] = result
        self.recent_results.append(result)
        
        return result
```

## Testing Issues

### Test Failures

**Problem: Tests fail with async errors**
```python
def test_legend():
    legend = MyLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    result = legend.run_async(request)  # Wrong! Returns coroutine
    assert result.legend == "MyLegend"  # AttributeError
```

**Solution:**
```python
import pytest

@pytest.mark.asyncio
async def test_legend():
    legend = MyLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    result = await legend.run_async(request)  # Correct
    assert result.legend == "MyLegend"

# Alternative for non-async test runner
def test_legend_sync():
    import asyncio
    
    legend = MyLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    result = asyncio.run(legend.run_async(request))
    assert result.legend == "MyLegend"
```

**Problem: Tests are unreliable due to external dependencies**
```python
async def test_legend():
    legend = RealDataLegend()  # Depends on external API
    result = await legend.run_async(request)  # Fails when API is down
```

**Solution:**
```python
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_legend_with_mock():
    legend = RealDataLegend()
    
    # Mock external dependencies
    mock_data = {"prices": [100, 101, 102], "volumes": [1000, 1100, 1200]}
    
    with patch.object(legend, '_fetch_data', new=AsyncMock(return_value=mock_data)):
        result = await legend.run_async(request)
        assert result.facts["primary_signal"] in ["buy", "sell", "hold"]
```

## CLI Tool Issues

### Scaffold Tool Problems

**Problem: Scaffold tool not found**
```bash
python -m legends create
# No module named legends.__main__
```

**Solution:**
1. Verify installation: `pip show pantheon-legends`
2. Check Python path: `python -c "import legends; print(legends.__file__)"`
3. Try alternative: `python -c "from legends.scaffold import main; main()"`

**Problem: Scaffold generates invalid code**
```python
# Generated code has syntax errors or import issues
```

**Solution:**
1. Update to latest version: `pip install --upgrade pantheon-legends`
2. Report issue with details of generated code
3. Manually fix generated template:
   ```python
   # Add missing imports
   from typing import Optional, Dict, Any
   from datetime import datetime
   ```

## Environment Issues

### Virtual Environment Problems

**Problem: Package not found in virtual environment**
```bash
source venv/bin/activate  # Linux/Mac
pip install pantheon-legends
python -c "import legends"  # ModuleNotFoundError
```

**Solution:**
1. Verify virtual environment is activated:
   ```bash
   which python  # Should point to venv
   pip list | grep pantheon  # Should show package
   ```

2. Recreate virtual environment if corrupted:
   ```bash
   deactivate
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install pantheon-legends
   ```

### Python Version Issues

**Problem: Package requires newer Python**
```bash
pip install pantheon-legends
# ERROR: Package requires Python '>=3.8' but current Python is 3.7
```

**Solution:**
1. Check Python version: `python --version`
2. Install Python 3.8+: Download from python.org
3. Use specific Python version:
   ```bash
   python3.8 -m venv venv
   source venv/bin/activate
   pip install pantheon-legends
   ```

## Debugging Tips

### Enable Debug Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("legends")

class DebuggableLegend:
    def __init__(self):
        self.logger = logging.getLogger(f"legends.{self.name}")
    
    async def run_async(self, request, progress_callback=None):
        self.logger.debug(f"Starting analysis for {request.symbol}")
        
        try:
            result = await self._analyze(request)
            self.logger.debug(f"Analysis complete: {result.facts}")
            return result
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}", exc_info=True)
            raise
```

### Use Interactive Debugging

```python
import asyncio
from legends import LegendRequest
from datetime import datetime

async def debug_legend():
    legend = MyLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    
    # Set breakpoint for debugging
    import pdb; pdb.set_trace()
    
    result = await legend.run_async(request)
    return result

# Run in IPython or Jupyter for better debugging
if __name__ == "__main__":
    result = asyncio.run(debug_legend())
```

### Profile Performance

```python
import cProfile
import asyncio
import time

async def profile_legend():
    legend = MyLegend()
    request = LegendRequest("BTC-USD", "1h", datetime.now())
    
    start_time = time.time()
    result = await legend.run_async(request)
    end_time = time.time()
    
    print(f"Execution time: {end_time - start_time:.3f} seconds")
    return result

# Profile with cProfile
if __name__ == "__main__":
    cProfile.run("asyncio.run(profile_legend())")
```

## Getting Help

### Community Support
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check [getting-started.md](getting-started.md) and [api-reference.md](api-reference.md)

### Common Resources
- **Examples**: See [examples.md](examples.md) for working code
- **Best Practices**: Review [legend-development.md](legend-development.md)
- **Community Guidelines**: Follow [community-guidelines.md](community-guidelines.md)

### Reporting Issues
When reporting issues, include:

1. **Environment details**:
   ```bash
   python --version
   pip show pantheon-legends
   pip list | grep -E "(pandas|numpy|aiohttp)"
   ```

2. **Minimal reproduction code**:
   ```python
   from legends import LegendRequest
   from datetime import datetime
   
   # Your minimal failing example here
   ```

3. **Error messages** (full traceback)
4. **Expected vs actual behavior**

### Performance Optimization Checklist

When legends are running slowly:

- [ ] Use `await` for all async operations
- [ ] Implement data caching for repeated requests
- [ ] Use connection pooling for HTTP requests
- [ ] Batch API calls where possible
- [ ] Move CPU-intensive work to thread pools
- [ ] Limit memory usage with bounded caches
- [ ] Add timeout handling for long operations
- [ ] Profile code to identify bottlenecks
- [ ] Use efficient data structures (numpy arrays, etc.)
- [ ] Minimize data copying and transformation

Remember: Most issues can be resolved by carefully reading error messages and following async/await patterns correctly!
