# The contents of this file are subject to the Mozilla Public License
# Version 2.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
#    http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# OS2Webscanner was developed by Magenta in collaboration with OS2 the
# Danish community of open source municipalities (http://www.os2web.dk/).
#
# The code is currently governed by OS2 the Danish community of open
# source municipalities ( http://www.os2web.dk/ )
"""Processors."""
import random
import subprocess

from os2webscanner.models import ConversionQueueItem
from django.db import transaction, IntegrityError, DatabaseError
from django import db
from django.utils import timezone
import time
import os
import mimetypes
import sys
import magic
from django.conf import settings


# Minimum width and height an image must have to be scanned
MIN_OCR_DIMENSION_BOTH = 7

# Minimum width or height (at least one dimension) an image must have to be
# scanned
MIN_OCR_DIMENSION_EITHER = 64


def get_image_dimensions(file_path):
    """Return an image's dimensions as a tuple containing width and height.

    Uses the "identify" command from ImageMagick to retrieve the information.
    """
    dimensions = subprocess.check_output(["identify", "-format", "%wx%h",
                                     file_path])
    return tuple(int(dim.strip()) for dim in dimensions.split("x"))


class Processor(object):

    """Represents a Processor which can process spider and queue items.

    Provides methods to process queue items for the current processor type.
    Provides a central place to register processors and contains utility
    methods for other processors.
    """

    mime_magic = magic.Magic(mime=True)

    processors_by_type = {}
    processor_instances = {}

    documents_to_process = 10
    pid = None

    @classmethod
    def processor_by_type(cls, processor_type):
        """Return a Processor instance registered for the given type.

        The instance returned is always the same instance.
        """
        processor = cls.processor_instances.get(processor_type, None)
        if processor is None:
            processor_class = cls.processors_by_type.get(processor_type, None)
            if processor_class is None:
                return None
            processor = processor_class()
            cls.processor_instances[processor_type] = processor
        return processor

    @classmethod
    def var_dir(self):
        """Return the base data directory.

        Temporary files, as well as configuration files needed by
        processors should go somewhere under this directory.
        """
        return settings.VAR_DIR

    def handle_spider_item(self, data, url_object):
        """Process an item from a spider. Must be overridden.

        :type url_object: Url
        :param data: The textual or binary data to process.
        :param url_object: The Url object that the data was found at.
        """
        raise NotImplemented

    def handle_queue_item(self, item):
        """Process an item from a queue. Must be overridden.

        :type item: ConversionQueueItem
        :param item: The ConversionQueueItem to process.
        """
        raise NotImplemented

    def add_to_queue(self, data, url_object):
        """Add an item to the conversion queue.

        The data will be saved to a temporary file and added to the
        conversion queue for later processing.
        """
        # Write data to a temporary file
        # Get temporary directory
        tmp_dir = url_object.tmp_dir
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        file_name = os.path.basename(url_object.url)
        if file_name == '':
            file_name = url_object.pk + ".data"
        tmp_file_path = os.path.join(tmp_dir, file_name)
        f = open(tmp_file_path, 'w')
        f.write(data)
        f.close()

        # Create a conversion queue item
        new_item = ConversionQueueItem(
            file=tmp_file_path,
            type=self.mimetype_to_processor_type(url_object.mime_type),
            url=url_object,
            status=ConversionQueueItem.NEW,
        )
        new_item.save()
        return True

    def process_file(self, file_path, url):
        """Open the file associated with the item and process the file data.

        Calls self.process.
        """
        try:
            f = open(file_path, "r")
            self.process(f.read(), url)
            f.close()
        except IOError, e:
            print repr(e)
            return False
        return True

    def setup_queue_processing(self, pid, *args):
        """Setup the queue processor with additional arguments."""
        self.pid = pid

    def process_queue(self):
        """Process items in the queue in an infinite loop.

        If there are no items to process, waits 1 second before trying
        to get the next queue item.
        """
        print "Starting processing queue items of type %s, pid %s" % (
            self.item_type, self.pid
        )
        sys.stdout.flush()
        executions = 0

        while executions < self.documents_to_process:
            # Prevent memory leak in standalone scripts
            db.reset_queries()
            item = self.get_next_queue_item()
            if item is None:
                time.sleep(1)
            else:
                result = self.handle_queue_item(item)
                executions = executions + 1
                if not result:
                    item.status = ConversionQueueItem.FAILED
                    item.save()
                else:
                    item.delete()
                print "%s (%s): %s" % (
                    item.file_path,
                    item.url.url,
                    "success" if result else "fail"
                )
                sys.stdout.flush()

    @transaction.atomic
    def get_next_queue_item(self):
        """Get the next item in the queue.

        Returns None if there is nothing in the queue.
        """
        result = None

        while result is None:
            try:
                with transaction.atomic():
                    new_items_queryset = ConversionQueueItem.objects.filter(
                        type=self.item_type,
                        status=ConversionQueueItem.NEW
                    )

                    # Get scans with pending items of the wanted type
                    scans = new_items_queryset.values('url__scan').distinct()

                    # Pick a random scan
                    random_scan_pk = random.choice(scans)['url__scan']

                    # Get the first unprocessed item of the wanted type and
                    # from a random scan
                    result = new_items_queryset.filter(
                        url__scan=random_scan_pk).select_for_update(
                        nowait=True)[0]

                    # Change status of the found item
                    ltime = timezone.localtime(timezone.now())
                    result.status = ConversionQueueItem.PROCESSING
                    result.process_id = self.pid
                    result.process_start_time = ltime
                    result.save()
            except (DatabaseError, IntegrityError) as e:
                # Database transaction failed, we just try again
                print "".join([
                    "Transaction failed while getting queue item of type ",
                    "'" + self.item_type + "'"
                ])
                result = None
            except IndexError:
                # Nothing in the queue, return None
                result = None
                break
        return result

    def convert_queue_item(self, item):
        """Convert a queue item and add converted files to the queue.

        Creates a temporary directory for the queue item and calls
        self.convert to run the actual conversion. After converting,
        adds all files produced in the conversion directory to the queue.
        """
        tmp_dir = item.tmp_dir
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        result = self.convert(item, tmp_dir)
        if os.path.exists(item.file_path):
            os.remove(item.file_path)

        self.add_processed_files(item, tmp_dir)
        return result

    def convert(self, item, tmp_dir):
        """Convert the item and output converted files in the temp dir.

        Must be implemented by classes which call convert_queue_item.
        It is expected that the conversion outputs converted files in the
        temporary directory.
        """
        raise NotImplemented

    def add_processed_files(self, item, tmp_dir):
        """Recursively add all files in the temp dir to the queue."""
        ignored_ocr_count = 0
        for root, dirnames, filenames in os.walk(tmp_dir):
            for fname in filenames:
                # TODO: How do we decide which types are supported?
                try:
                    # Guess the mime type from the file name
                    mime_type, encoding = mimetypes.guess_type(fname)
                    file_path = os.path.join(root, fname)
                    if mime_type is None:
                        # Guess the mime type from the file contents
                        mime_type = self.mime_magic.from_file(file_path)
                    processor_type = Processor.mimetype_to_processor_type(
                        mime_type)

                    # Disable OCR if requested
                    if (processor_type == 'ocr' and
                        not item.url.scan.do_ocr):
                        processor_type = None

                    # Ignore and delete images which are smaller than
                    # the minimum dimensions
                    if processor_type == 'ocr':
                        (w, h) = get_image_dimensions(file_path)
                        if not ((w >= MIN_OCR_DIMENSION_BOTH and
                                 h >= MIN_OCR_DIMENSION_BOTH)
                                and (w >= MIN_OCR_DIMENSION_EITHER or
                                     h >= MIN_OCR_DIMENSION_EITHER)):
                            ignored_ocr_count += 1
                            processor_type = None

                    if processor_type is not None:
                        new_item = ConversionQueueItem(
                            file=file_path,
                            type=processor_type,
                            url=item.url,
                            status=ConversionQueueItem.NEW,
                        )
                        new_item.save()
                    else:
                        os.remove(file_path)

                except ValueError:
                    continue
        if ignored_ocr_count > 0:
            print "Ignored %d extracted images because the dimensions were" \
                  "small (width AND height must be >= %d) AND (width OR " \
                  "height must be >= %d))" % (ignored_ocr_count,
                                               MIN_OCR_DIMENSION_BOTH,
                                               MIN_OCR_DIMENSION_EITHER)

    @classmethod
    def register_processor(cls, processor_type, processor):
        """Register the processor class as processor for the given type."""
        cls.processors_by_type[processor_type] = processor

    opendocument = 'application/vnd.oasis.opendocument'
    officedocument = 'application/vnd.openxmlformats-officedocument'

    mimetypes_to_processors = {
        'text': 'text',
        'image': 'ocr',

        'text/html': 'html',
        'text/xml': 'html',
        'application/xhtml+xml': 'html',
        'application/xml': 'html',
        'application/vnd.google-earth.kml+xml': 'html',

        'application/javascript': 'text',
        'application/json': 'text',
        'application/csv': 'text',

        'application/zip': 'zip',

        'application/pdf': 'pdf',

        'application/rtf': 'libreoffice',
        'application/msword': 'libreoffice',
        opendocument + '.chart': 'libreoffice',
        opendocument + '.database': 'libreoffice',
        opendocument + '.formula': 'libreoffice',
        opendocument + '.graphics': 'libreoffice',
        opendocument + '.graphics-template': 'libreoffice',
        opendocument + '.image': 'libreoffice',
        opendocument + '.presentation': 'libreoffice',
        opendocument + '.presentation-template': 'libreoffice',
        opendocument + '.spreadsheet': 'libreoffice',
        opendocument + '.spreadsheet-template': 'libreoffice',
        opendocument + '.text': 'libreoffice',
        opendocument + '.text-master': 'libreoffice',
        opendocument + '.text-template': 'libreoffice',
        opendocument + '.text-web': 'libreoffice',
        officedocument + '.presentationml.presentation': 'libreoffice',
        officedocument + '.presentationml.slide': 'libreoffice',
        officedocument + '.presentationml.slideshow': 'libreoffice',
        officedocument + '.presentationml.template': 'libreoffice',
        officedocument + '.spreadsheetml.sheet': 'libreoffice',
        officedocument + '.spreadsheetml.template': 'libreoffice',
        officedocument + '.wordprocessingml.document': 'libreoffice',
        officedocument + '.wordprocessingml.template': 'libreoffice',
        'application/vnd.ms-excel': 'libreoffice',
        'application/vnd.ms-powerpoint': 'libreoffice',

        'application/vnd.lotus-1-2-3': 'libreoffice',
        'application/lotus123': 'libreoffice',
        'application/wk3': 'libreoffice'
    }

    @classmethod
    def mimetype_to_processor_type(cls, mime_type):
        """Get the type name of the processor which handles the mime-type."""
        if mime_type is None:
            return None
        processor = cls.mimetypes_to_processors.get(mime_type, None)
        if processor is None:
            processor = cls.mimetypes_to_processors.get(
                mime_type.split("/")[0], None
            )
        return processor
