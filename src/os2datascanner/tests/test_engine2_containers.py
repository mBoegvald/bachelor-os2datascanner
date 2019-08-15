#!/usr/bin/env python
import unittest

from os2datascanner.engine2.model.core import Source, SourceManager
from os2datascanner.engine2.model.data import DataSource
import os.path

here_path = os.path.dirname(__file__)
test_data_path = os.path.join(here_path, "data", "engine2")


class Engine2ContainerTest(unittest.TestCase):
    def setUp(self) -> None:
        with open(os.path.join(test_data_path, "test-vector"), "rt") as fp:
            self.correct_content = fp.read()

    def test(self):
        with SourceManager() as sm:

            def process(source, depth=0):
                for handle in source.handles(sm):
                    print("{0}{1}".format("  " * depth, handle))
                    derived_source = Source.from_handle(handle)
                    if derived_source:
                        process(derived_source, depth + 1)
                    elif handle.get_name() == "url":
                        with handle.follow(sm).make_stream() as fp:
                            url = fp.read().decode("utf-8")
                        process(Source.from_url(url), depth + 1)
                    elif handle.get_name() == "test-vector" or isinstance(
                            source, DataSource):
                        r = handle.follow(sm)
                        reported_size = r.get_size()
                        with r.make_stream() as fp:
                            stream_raw = fp.read()
                            stream_size = len(stream_raw)
                            stream_content = stream_raw.decode("utf-8")
                        with r.make_path() as p:
                            with open(p, "rb") as fp:
                                file_raw = fp.read()
                                file_size = len(file_raw)
                                file_content = file_raw.decode("utf-8")
                        self.assertEqual(
                                stream_size,
                                reported_size,
                                "{0}: model stream length invalid".format(
                                        handle))
                        self.assertEqual(
                                file_size,
                                reported_size,
                                "{0}: model stream length invalid".format(
                                        handle))
                        self.assertEqual(
                                file_raw,
                                stream_raw,
                                "{0}: model file and stream not equal".format(
                                        handle))
                        self.assertEqual(
                                stream_content,
                                self.correct_content,
                                "{0}: model stream invalid".format(handle)                        )
                        self.assertEqual(
                                file_content,
                                self.correct_content,
                                "{0}: model file invalid".format(handle))

            process(Source.from_url("file://" + test_data_path))


if __name__ == "__main__":
    main()
