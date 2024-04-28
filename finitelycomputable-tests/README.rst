========================
FinitelyComputable-Tests
========================

This application provides a package the modules of which attempt to import the
actual test modules in finitelycomputable.tests, and ignores ImportErrors. The
reason for this is that finitelycomputable.tests is a namespace package,
support for which in pytest is new and does not appear to include the situation
where the test modules themselves are in a namespace package.

Note that using this shortcut means that if any of the tests themselves
generate an ImportError, those tests will be silently ignored.
