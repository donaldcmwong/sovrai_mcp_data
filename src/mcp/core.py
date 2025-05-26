"""
Market Data MCP Server Implementation using FastAPI-MCP
Implements the Model Context Protocol (MCP) for providing market data context to LLMs.
"""

from fastapi import FastAPI, Depends, HTTPException
#from fastapi_mcp import FastApiMCP, MCPTool
from pydantic import BaseModel, Field
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
from typing import List, Dict, Union, Optional
import numpy as np
from enum import Enum
from fastmcp import FastMCP

mcp = FastMCP(title='blah',
              version="1.0.0")

# Models for request/response
class Interval(str, Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"

class MarketDataRequest(BaseModel):
    symbols: Union[str, List[str]]
    start_date: Optional[str] = Field(None, description="Start date in YYYY-MM-DD format")
    end_date: Optional[str] = Field(None, description="End date in YYYY-MM-DD format")
    interval: Optional[Interval] = Field(Interval.ONE_DAY, description="Data interval")

class PriceData(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: datetime

class MarketSummary(BaseModel):
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    open: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None

# # Create FastAPI app
# app = FastAPI(
#     title="Market Data MCP Server",
#     description="MCP server providing market data through yfinance",
#     version="1.0.0"
# )


# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy"}

# @app.post("/market-data", response_model=Dict[str, List[PriceData]])
@mcp.tool("market_data")
async def get_market_data(request: MarketDataRequest):
    """
    Fetch historical market data for given symbols.
    """
    if isinstance(request.symbols, str):
        symbols = [request.symbols]
    else:
        symbols = request.symbols
        
    if not request.start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        start_date = request.start_date
        
    if not request.end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = request.end_date
        
    result = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(
                start=start_date,
                end=end_date,
                interval=request.interval.value
            )
            
            # Convert to list of PriceData
            price_data = []
            for index, row in data.iterrows():
                price_data.append(PriceData(
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume'],
                    timestamp=index
                ))
                
            result[symbol] = price_data
            logger.info(f"Successfully fetched data for {symbol}")
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching data for {symbol}: {str(e)}")
                
    return result

# @app.post("/current-price", response_model=Dict[str, float])
@mcp.tool("current_price")
async def get_current_price(symbols: Union[str, List[str]]):
    """
    Get the current market price for given symbols.
    """
    if isinstance(symbols, str):
        symbols = [symbols]
            
    result = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            current_price = ticker.info.get('regularMarketPrice')
            if current_price is None:
                raise ValueError(f"No price data available for {symbol}")
            result[symbol] = current_price
            logger.info(f"Current price for {symbol}: {current_price}")
        except Exception as e:
            logger.error(f"Error fetching current price for {symbol}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching price for {symbol}: {str(e)}")
                
    return result

# @app.post("/market-summary", response_model=Dict[str, MarketSummary])
@mcp.tool("market_summary")
async def get_market_summary(symbols: List[str]):
    """
    Get a summary of market data including price, volume, and basic metrics.
    """
    summary = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            summary[symbol] = MarketSummary(
                current_price=info.get('regularMarketPrice'),
                previous_close=info.get('previousClose'),
                open=info.get('regularMarketOpen'),
                day_high=info.get('dayHigh'),
                day_low=info.get('dayLow'),
                volume=info.get('volume'),
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('forwardPE'),
                week_52_high=info.get('fiftyTwoWeekHigh'),
                week_52_low=info.get('fiftyTwoWeekLow')
            )
            logger.info(f"Generated market summary for {symbol}")
        except Exception as e:
            logger.error(f"Error generating market summary for {symbol}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error fetching summary for {symbol}: {str(e)}")
                
    return summary


if __name__ == "__main__":
    mcp.run()