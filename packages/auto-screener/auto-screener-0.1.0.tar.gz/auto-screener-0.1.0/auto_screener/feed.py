# feed.py

import threading
import asyncio
import time
import warnings
from functools import partial
import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any,
    Union, Callable, List, Type
)

import pandas as pd

from represent import Modifiers, BaseModel

from cryptofeed import FeedHandler
from cryptofeed.feed import Feed
from cryptofeed.types import OrderBook
from cryptofeed.defines import L2_BOOK

from auto_screener.dataset import (
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME
)
from auto_screener.symbols import Separator, adjust_symbol
from auto_screener.screener import (
    BaseScreener, BaseMultiScreener, create_market_dataframe
)
from auto_screener.hints import Number
from auto_screener.exchanges import EXCHANGES
from auto_screener.collect import (
    find_name, validate_exchange, validate_symbol
)

__all__ = [
    "MarketRecorder",
    "MarketHandler",
    "MarketScreener",
    "add_feeds",
    "create_market",
    "market_screener",
    "market_recorder",
    "create_orderbook_dataframe"
]

Market = Dict[str, Dict[str, pd.DataFrame]]
RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

def create_orderbook_dataframe() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_market_dataframe(
        columns=MarketRecorder.COLUMNS
    )
# end create_orderbook_dataframe

def create_market(data: Dict[str, Iterable[str]]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol: create_orderbook_dataframe()
            for symbol in data[exchange]
        } for exchange in data
    }
# end create_market

class MarketRecorder(BaseModel):
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - market:
        The market structure of the data to store the fetched data in.
        This structure is a dictionary with exchange names as keys
        and dictionaries as values, where their keys are symbols,
        and their values are the dataframes to record the data.

    >>> from auto_screener.feed import market_recorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = market_recorder(data=market)

    """

    modifiers = Modifiers(**BaseModel.modifiers)
    modifiers.excluded.append("market")

    __slots__ = "market"

    COLUMNS = (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME)

    def __init__(self, market: Optional[Market] = None) -> None:
        """
        Defines the class attributes.

        :param market: The object to fill with the crypto feed record.
        """

        if market is None:
            market = {}
        # end if

        self.market: Market = market
    # end __init__

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols.keys())
            for exchange, symbols in self.market.items()
        }
    # end structure

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[L2_BOOK],
            callbacks={L2_BOOK: self.record},
            max_depth=2
        )
    # end parameters

    async def record(self, data: OrderBook, timestamp: float) -> None:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        exchange = find_name(
            name=data.exchange, names=self.market.keys()
        )
        symbol = find_name(
            name=adjust_symbol(
                symbol=data.symbol,
                separator=Separator.value
            ),
            names=exchange
        )

        dataset = (
            self.market.
            setdefault(exchange, {}).
            setdefault(symbol, create_orderbook_dataframe())
        )

        bids = data.book.bids.to_list()
        asks = data.book.asks.to_list()

        try:
            dataset.loc[dt.datetime.fromtimestamp(timestamp)] = {
                BIDS: float(bids[0][0]),
                ASKS: float(asks[0][0]),
                BIDS_VOLUME: float(bids[0][1]),
                ASKS_VOLUME: float(asks[0][1])
            }

        except IndexError:
            pass
        # end try
    # end record

    def data(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        exchange = find_name(name=exchange, names=self.market.keys())

        validate_exchange(
            exchange=exchange,
            exchanges=self.market.keys(),
            provider=self
        )

        validate_symbol(
            symbol=symbol,
            exchange=exchange,
            exchanges=self.market.keys(),
            symbols=self.market[exchange],
            provider=self
        )

        return self.market[exchange][symbol]
    # end data

    def screener(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> BaseScreener:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        """

        screener = BaseScreener(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel,
            market=self.data(exchange=exchange, symbol=symbol)
        )

        return screener
    # end screener

    def screeners(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> List[BaseScreener]:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        """

        base_screeners = []

        for exchange in self.market:
            for symbol in self.market[exchange]:
                base_screeners.append(
                    self.screener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel
                    )
                )
            # end for
        # end for

        return base_screeners
    # end create_screeners
# end MarketRecorder

class ExchangeFeed(Feed):
    """A class to represent an exchange feed object."""

    handler: Optional[FeedHandler] = None

    running: bool = False

    def stop(self) -> None:
        """Stops the process."""

        self.running = False

        Feed.stop(self)
    # end stop

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Create tasks for exchange interfaces and backends.

        :param loop: The event loop for the process.
        """

        self.running = True

        Feed.start(self, loop=loop)
    # end start
# end ExchangeFeed

def add_feeds(
        handler: FeedHandler,
        data: Dict[str, Iterable[str]],
        fixed: Optional[bool] = False,
        amount: Optional[int] = 5,
        separator: Optional[str] = Separator.value,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> None:
    """
    Adds the tickers to the handler for each exchange.

    :param handler: The handler object.
    :param data: The data of the exchanges and tickers to add.
    :param parameters: The parameters for the exchanges.
    :param fixed: The value for fixed parameters to all exchanges.
    :param separator: The separator of the assets.
    :param amount: The maximum amount of symbols for each feed.
    """

    base_parameters = None

    if not fixed:
        parameters = parameters or {}

    else:
        base_parameters = parameters or {}
        parameters = {}
    # end if

    for exchange, symbols in data.items():
        exchange = find_name(name=exchange, names=EXCHANGES.keys())

        symbols = [
            symbol.replace(separator, '-')
            for symbol in symbols
        ]

        if fixed:
            parameters.setdefault(exchange, base_parameters)
        # end if

        EXCHANGES[exchange]: Type[ExchangeFeed]

        packets = []

        for i in range(0, int(len(symbols) / amount) + len(symbols) % amount, amount):
            packets.append(symbols[i:])
        # end for

        for symbols_packet in packets:
            feed = EXCHANGES[exchange](
                symbols=symbols_packet,
                **(
                    parameters[exchange]
                    if (
                        (exchange in parameters) and
                        isinstance(parameters[exchange], dict) and
                        all(isinstance(key, str) for key in parameters)

                    ) else {}
                )
            )

            feed.start = partial(ExchangeFeed.start, feed)
            feed.stop = partial(ExchangeFeed.stop, feed)
            feed.handler = handler
            feed.running = False

            handler.add_feed(feed)
        # end for
    # end for
# end add_feeds

class MarketHandler(FeedHandler):
    """A class to handle the market data feed."""

    def __init__(self) -> None:
        """Defines the class attributes."""

        super().__init__(
            config={'uvloop': False, 'log': {'disabled': True}}
        )
    # end __init__
# end MarketHandler

class MarketScreener(BaseMultiScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.

    >>> from auto_screener.feed import market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = market_screener(data=structure)
    >>> screener.run()
    """

    modifiers = Modifiers(**BaseMultiScreener.modifiers)
    modifiers.excluded.extend(['update_process'])

    __slots__ = (
        "handler", "recorder", "updating",
        "update_process", "loop", "limited",
        "feeds_parameters", "screening_parameters"
    )

    DELAY = 10

    def __init__(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            recorder: Optional[MarketRecorder] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param handler: The handler object for the market data.
        :param recorder: The recorder object for recording the data.
        """

        super().__init__(
            location=location, cancel=cancel, delay=delay
        )

        self.handler = handler or MarketHandler()
        self.recorder = recorder or MarketRecorder()
        self.limited = limited or False

        self.screeners: List[BaseScreener] = self.create_screeners()

        self.updating = False

        self.update_process: Optional[threading.Thread] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None

        self.feeds_parameters: Optional[Dict[str, Any]] = None
        self.screening_parameters: Optional[Dict[str, Any]] = None
    # end __init__

    @property
    def market(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.market
    # end market

    def create_screener(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> BaseScreener:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        """

        return self.recorder.screener(
            symbol=symbol, exchange=exchange, location=location or self.location,
            cancel=cancel or self.cancel, delay=delay or self.delay
        )
    # end create_screener

    def create_screeners(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[Number, dt.timedelta]] = None,
            delay: Optional[Union[Number, dt.timedelta]] = None
    ) -> List[BaseScreener]:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        """

        return self.recorder.screeners(
            location=location or self.location,
            cancel=cancel or self.cancel, delay=delay or self.delay
        )
    # end create_screeners

    def add_feeds(
            self,
            data: Dict[str, Iterable[str]],
            fixed: Optional[bool] = True,
            separator: Optional[str] = Separator.value,
            parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
    ) -> None:
        """
        Adds the tickers to the handler for each exchange.

        :param data: The data of the exchanges and tickers to add.
        :param parameters: The parameters for the exchanges.
        :param fixed: The value for fixed parameters to all exchanges.
        :param separator: The separator of the assets.
        """

        self.feeds_parameters = dict(
            data=data, fixed=fixed, separator=separator, parameters=parameters
        )

        feed_params = self.recorder.parameters()
        feed_params.update(parameters or {})

        add_feeds(
            self.handler, data=data, fixed=fixed, separator=separator,
            parameters=feed_params
        )
    # end add_feeds

    def refresh(self) -> None:
        """Refreshes the feed objects."""

        if self.feeds_parameters is None:
            warnings.warn(
                "Cannot refresh feeds as there was "
                "no feeds initialization to repeat."
            )

            return
        # end if

        self.handler.feeds.clear()

        self.add_feeds(**self.feeds_parameters)
    # end refresh

    def rerun(self) -> None:
        """Refreshes the process."""

        if self.screening_parameters is None:
            warnings.warn(
                "Cannot rerun as there was "
                "no initial process to repeat."
            )

            return
        # end if

        self.terminate()
        self.refresh()
        self.run(**self.screening_parameters)
    # end rerun

    def data(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.data(exchange=exchange, symbol=symbol)
    # end data

    def run_loop(
            self,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()
        # end if

        self.loop = loop

        asyncio.set_event_loop(loop)

        self.running = True

        self.handler.run(
            start_loop=start and (not loop.is_running()),
            install_signal_handlers=False
        )
    # end run_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        for screener in self.screeners or self.create_screeners():
            screener.saving_process = threading.Thread(
                target=screener.saving_loop
            )
            screener.saving_process.start()
        # end for
    # end saving_loop

    def update_loop(self) -> None:
        """Updates the state of the screeners."""

        self.updating = True

        while self.updating:
            if self.running:
                self.update()
            # end if

            time.sleep(self.delay)
        # end while
    # end update_loop

    def save(self) -> None:
        """Runs the data handling loop."""

        for screener in self.screeners or self.create_screeners():
            threading.Thread(
                target=screener.save_dataset,
                kwargs=dict(location=self.location)
            ).start()
        # end for
    # end run

    def update(self) -> None:
        """Updates the state of the screeners."""

        for screener in self.screeners:
            for feed in self.handler.feeds:
                feed: ExchangeFeed

                if (
                    self.limited and
                    (screener.exchange.lower() == feed.id.lower()) and
                    (not feed.running)
                ):
                    screener.stop()
                # end if
            # end for
        # end for
    # end update

    def stop(self) -> None:
        """Stops the data handling loop."""

        super().stop()

        self.running = False

        if self.loop is None:
            return
        # end if

        if (
            self.updating and
            isinstance(self.update_process, threading.Thread) and
            self.update_process.is_alive()
        ):
            self.updating = False

            self.update_process = None
        # end if

        self.loop: asyncio.AbstractEventLoop

        async def stop() -> None:
            self.handler.stop(self.loop)
            self.handler.close(self.loop)
        # end stop

        self.loop.create_task(stop())

        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        # end for

        self.loop = None

        self.handler.running = False
    # end stop

    def run(
            self,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            wait: Optional[Union[bool, Number, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[Number, dt.timedelta, dt.datetime]] = None,
            update: Optional[bool] = True,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> threading.Thread:
        """
        Runs the program.

        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a timeout to the process.
        :param update: The value to update the screeners.
        :param start: The value to start the loop.
        :param loop: The event loop.

        :return: The timeout process.
        """

        if self.running:
            warnings.warn(f"Screener is already running.")

            return self.screening_process
        # end if

        self.running = True

        self.screening_parameters = dict(
            save=save, block=block, wait=wait, loop=loop,
            timeout=timeout, update=update, start=start
        )

        if save:
            self.saving_process = threading.Thread(
                target=self.saving_loop
            )

            self.saving_process.start()
        # end if

        if update:
            self.update_process = threading.Thread(
                target=self.update_loop
            )

            self.update_process.start()
        # end if

        if timeout:
            self.timeout(duration=timeout)
        # end if

        if not block:
            self.screening_process = threading.Thread(
                target=lambda: self.run_loop(loop=loop, start=start)
            )

            self.screening_process.start()

        else:
            self.run_loop(loop=loop, start=start)
        # end if

        if isinstance(wait, dt.datetime):
            wait = wait - dt.datetime.now()
        # end if

        if isinstance(wait, dt.timedelta):
            wait = wait.total_seconds()
        # end if

        if isinstance(wait, bool) and wait:
            self.wait_for_initialization()

        elif isinstance(wait, (int, float)):
            time.sleep(wait)
        # end if

        return self.screening_process
    # end run
# end MarketScreener

def market_recorder(data: Dict[str, Iterable[str]]) -> MarketRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.

    :return: The market recorder object.
    """

    return MarketRecorder(market=create_market(data=data))
# end market_recorder

def market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[Number, dt.timedelta]] = None,
        delay: Optional[Union[Number, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        market: Optional[Market] = None,
        recorder: Optional[MarketRecorder] = None,
        fixed: Optional[bool] = True,
        separator: Optional[str] = Separator.value,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> MarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param parameters: The parameters for the exchanges.
    :param market: The object to fill with the crypto feed record.
    :param fixed: The value for fixed parameters to all exchanges.
    :param separator: The separator of the assets.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.

    :return: The market screener object.
    """

    screener = MarketScreener(
        recorder=recorder or MarketRecorder(
            market=market or create_market(data=data)
        ),
        handler=handler, location=location,
        cancel=cancel, delay=delay, limited=limited
    )

    screener.add_feeds(
        data=screener.recorder.structure(), fixed=fixed,
        separator=separator, parameters=parameters
    )

    return screener
# end market_recorder