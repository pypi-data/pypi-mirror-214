IDSPy_Dictionaries
==================

IMAS Data Dictionaries converted to Python Dataclass used in the  IDSPy suite.

Prerequisites
=============

To use this script, you need to have Python **3.10** or later installed. You can download Python from https://www.python.org/downloads/.

Installation
============

To install the necessary packages, run the following command:

.. code-block:: console

   python -m pip install idspy_dictionaries

Usage
=====

To load the desired IDS :

.. code-block:: python

   from idspy_dictionaries import ids_gyrokinetics # or any other available IDS
   new_ids = ids_gyrokinetics.Gyrokinetics()

FAQ
===

**Q:** What is the minimum required version of Python to run this script?
  **A:** The minimum required version of Python is 3.10.

**Q:** Can I add new members to the dataclasses?
  **A:** By default it's not possible to be sure that the dataclasses follow the IMAS conventions. 


**Q:** I would really like to use python <3.10 is it really impossible? 
  **A:** IDSPy_dictionaries used mainly python dataclasses and the slot property which had been added in python 3.10 only. The main reason to use __slots__ is to avoid addition of members in the IDS and remains fully compliant with IMAS.

**Q:** Can I load all the dictionaries at once?  
  **A:** For performances reasons, it's not possible right now.


