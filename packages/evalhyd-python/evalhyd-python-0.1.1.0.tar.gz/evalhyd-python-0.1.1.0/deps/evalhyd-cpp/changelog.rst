.. default-role:: obj

..
   latest
   ------

   Yet to be versioned and released. Only available from *dev* branch until then.


v0.1.1
------

Released on 2023-06-16.

.. rubric:: Scope changes

* remove `"WSS"` and `"AWI"` as probabilistic evaluation metric because of the
  arbitrary nature of using the sample climatology as reference/benchmark
  (`CPP#7 <https://gitlab.irstea.fr/HYCAR-Hydro/evalhyd/evalhyd-cpp/-/issues/7>`_)

.. rubric:: Bug fixes

* fix irrelevant rank check failure when passing arrays (and not tensors)
  (`CPP#6 <https://gitlab.irstea.fr/HYCAR-Hydro/evalhyd/evalhyd-cpp/-/issues/6>`_,
  `R#4 <https://gitlab.irstea.fr/HYCAR-Hydro/evalhyd/evalhyd-r/-/issues/4>`_)
* fix crashing conditional masking functionality at runtime with certain
  compilers on Windows (in particular when building with Rtools for R>4.1.3) due
  to the presence of square brackets in the regular expressions that do not seem
  supported
  (`R#6 <https://gitlab.irstea.fr/HYCAR-Hydro/evalhyd/evalhyd-r/-/issues/6>`_)
* fix bug when using calendar year as block for the bootstrapping functionality
  (`CPP#8 <https://gitlab.irstea.fr/HYCAR-Hydro/evalhyd/evalhyd-cpp/-/issues/8>`_)

v0.1.0
------

Released on 2023-05-03.

* first release
