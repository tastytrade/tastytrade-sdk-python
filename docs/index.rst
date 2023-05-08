tastytrade-sdk
==========================================

Getting Started
***************

Install
"""""""

.. code-block:: bash

    pip install tastytrade-sdk


Use It
""""""

.. code-block:: python

    from tastytrade_sdk import Tastytrade

    tastytrade = Tastytrade()

    tastytrade.login(
        username='jane.doe@email..com',
        password='password'
    )

    tastytrade.instruments.get_active_equities()




.. toctree::
    :hidden:
    :caption: API Reference

    tastytrade
    instruments
    market-metrics
    watchlists
