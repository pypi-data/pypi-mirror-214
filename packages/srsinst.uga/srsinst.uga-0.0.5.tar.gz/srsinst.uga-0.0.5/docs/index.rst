.. SRS UGA documentation master file, created by
   sphinx-quickstart on Sun May  9 14:07:21 2023.

.. _overview:

``srsinst.uga`` documentation
===================================
``srsinst.uga`` is a `Python package <package_>`_ to control and acquire data with
`Stanford Research Systems (SRS) Universal Gas Analyzer (UGA) <uga100_>`_
using `srsgui`_  as a base instrument driver and a graphic user interface (GUI).

    ..  image:: _static/image/UGA100_composition_analysis_screenshot.png
        :width: 500pt
        :target: `overview`_   
 
**SRS UGA** is a `residual gas analyzer <rga_>`_ packaged with a vacuum system. 
Any measurement instruments running in vacuum require great attention
to operate without damaging them or the pumping system. It is important to familiar yourself
to **SRS UGA** before using ``srsinst.uga`` for control and data acquisition. If you are new to
**SRS UGA**, refer to the  `user's manual <manual_>`_ for details.


.. toctree::
   :maxdepth: 4

   installation
   connection
   basic_operation
   scan_operation
   
   srsinst.uga
   troubleshooting
   changelog   

Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _srsgui: https://thinksrs.github.io/srsgui/
.. _package: https://docs.python.org/3/tutorial/modules.html#packages
.. _uga100: https://thinksrs.com/products/uga.html
.. _rga: https://en.wikipedia.org/wiki/Residual_gas_analyzer
.. _manual: https://thinksrs.com/downloads/pdfs/manuals/UGAm.pdf