"""Unittests for the os2webscanner.

These will pass when you run "manage.py test os2webscanner".
"""

import os
import pep8

from django.test import TestCase
from django.conf import settings

from os2webscanner.models import Domain, Organization, Scanner, Scan
from validate import validate_domain

install_directory = os.path.abspath(os.path.join(settings.BASE_DIR, '..'))


class ScannerTest(TestCase):

    """Test running a scan and domain validation."""

    @classmethod
    def setUpClass(cls):
        """Setup some data to test with."""
        # Don't change the order of these, because Magenta needs pk = 2 to pass
        # the validation test
        cls.google = Organization(name="Google")
        cls.google.save()
        cls.magenta = Organization(name="Magenta", pk=2)
        cls.magenta.save()

    def test_validate_domain(self):
        """Test validating domains."""
        # Make sure Google does not validate in any of the possible methods
        all_methods = [Domain.ROBOTSTXT, Domain.WEBSCANFILE, Domain.METAFIELD]
        # Make sure Magenta's website validates using all possible methods
        for validation_method in all_methods:
            domain = Domain(url="http://www.magenta.dk/",
                            validation_method=validation_method,
                            organization=self.magenta
                            pk=1)
            domain.save()
            self.assertTrue(validate_domain(domain))

        for validation_method in all_methods:
            domain = Domain(url="http://www.google.com/",
                            validation_method=validation_method,
                            organization=self.google
                            pk=2)
            domain.save()
            self.assertFalse(validate_domain(domain))

    def test_run_scan(self):
        """Test running a scan."""
        domain = Domain(url="http://www.magenta.dk/",
                        organization=self.magenta,
                        validation_method=Domain.ROBOTSTXT)
        scanner = Scanner(organization=self.magenta, schedule="")
        scanner.save()
        self.assertTrue(isinstance(scanner.run(test_only=True), Scan))
        self.assertFalse(scanner.run(test_only=True))


def pep8_test(filepath):
    """Run a pep8 test on the filepath."""
    def do_test(self):
        # print "PATH:", filepath
        arglist = ['--exclude=lib', filepath]
        pep8.process_options(arglist)
        pep8.input_dir(filepath)
        output = pep8.get_statistics()
        # print "PEP8 OUTPUT: " + str(output)
        self.assertEqual(len(output), 0)

    return do_test


class Pep8Test(TestCase):

    """Test that django app and scrapy webscanner are PEP8-compliant."""

    j = lambda dir: os.path.join(install_directory, dir)

    test_os2webscanner = pep8_test(j('django-os2webscanner'))
    test_scrapywebscanner = pep8_test(j('scrapy-webscanner'))
