Python API client for ssa.fai.kz
================================

Install
-------

.. code:: bash

   pip install ssakz

Usage
-----

.. code:: python

   from ssakz import Client
   client = Client("<your API key>")

The API key is available upon registering at ssa.fai.kz

.. code:: python

   # Query near-miss events, starting from 2023-06-19,
   # where the minimal predicted distance between objects is less than 30 km
   nme = client.get_nme(rhigh=30, since='2023-06-19')

.. code:: python

   # Query space weather data (neutron flux)
   # starting one day ago
   nf = client.get_sw_neutrons(since='-1d')

Module functions
~~~~~~~~~~~~~~~~

-  ``get_nme`` - query data on near-miss events forecasts
-  ``get_sw_solar`` - query data on solar flux
-  ``get_sw_neutrons`` - query data on cosmic neutrons flux
-  ``get_sw_geomag`` - query data on geomagnetic field
-  ``get_sw_geomag_?``, with ``?`` being either ``x``, ``y`` or ``z`` -
   query data on geomagnetic field components
-  ``get_sw_k_index`` - query data on perturbation k-index

Dependency
----------

-  ``pyzmq`` (installed automatically with ``pip``)
