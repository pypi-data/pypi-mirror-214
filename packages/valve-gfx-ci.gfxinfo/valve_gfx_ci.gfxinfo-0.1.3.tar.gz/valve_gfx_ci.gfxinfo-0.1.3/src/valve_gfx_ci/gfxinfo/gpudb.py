import sys
import os

import requests

from .pcidevice import PCIDevice


class GpuDevice:
    @property
    def base_name(self):  # pragma: nocover
        raise NotImplementedError('Missing required property')

    @property
    def tags(self):  # pragma: nocover
        raise NotImplementedError('Missing required property')

    @property
    def structured_tags(self):  # pragma: nocover
        raise NotImplementedError('Missing required property')

    def __str__(self):  # pragma: nocover
        raise NotImplementedError('Missing required property')

    @property
    def pciid(self):
        if hasattr(self, "pci_device") and self.pci_device:
            return str(self.pci_device)

    @property
    def unknown_fields(self):
        return set()


class GpuDeviceDB:
    # Inherit from this class, and set DB_URL/DB_FILENAME as class parameters

    def __init__(self):
        self.is_up_to_date = False
        self.has_db = False
        self.devices = dict()

        if self._needs_db_file():
            try:
                db = open(self.db_cache_path, 'r').read()
                self.has_db = True
            except FileNotFoundError:
                try:
                    db = self.cache_db()
                    self.has_db = True
                except Exception as e:
                    print(f"ERROR: The pre-cached database is missing, and downloading it failed: {e}",
                          file=sys.stderr)
                    print(f"--> {self.db_name} GPUs won't be detected...")
                    db = ""

            self.parse_db(db)

        # Add all the static devices
        self.devices.update(self.static_devices)

    @property
    def static_devices(self):  # pragma: nocover
        return {}

    @classmethod
    def _needs_db_file(cls):
        return hasattr(cls, 'DB_URL') and hasattr(cls, 'DB_FILENAME')

    @property
    def db_name(self):
        return self.__class__.__name__

    @property
    def __db_cache_folder(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "dbs")

    @property
    def db_cache_path(self):
        return os.path.join(self.__db_cache_folder, self.DB_FILENAME)

    def cache_db(self):
        if not self._needs_db_file():  # pragma: nocover
            # Nothing to do
            return

        r = requests.get(self.DB_URL, timeout=5)
        r.raise_for_status()

        # Save the DB, for future use
        try:
            os.makedirs(self.__db_cache_folder, exist_ok=True)
            open(self.db_cache_path, "w").write(r.text)
        except Exception as e:  # pragma: nocover
            print(f"WARNING: could not cache the database file {self.DB_FILENAME}: {e}")

        return r.text

    def update(self):
        if not self._needs_db_file():  # pragma: nocover
            # Nothing to do
            return False

        if not self.is_up_to_date:
            self.cache_db()
            self.is_up_to_date = True

        return self.is_up_to_date

    def check_db(self):
        if not self._needs_db_file():
            return True

        if not self.has_db:
            print(f"ERROR: {self.db_name}'s GPU database is missing", file=sys.stderr)
            return False

        all_devices_complete = True
        for dev in self.devices.values():
            unknown_fields = dev.unknown_fields
            if len(unknown_fields) > 0:
                print(f"WARNING: The {self.db_name} device {dev.pci_device} ({dev.base_name}) has the following "
                      f"unknown fields: {unknown_fields}", file=sys.stderr)
                all_devices_complete = False

        return all_devices_complete

    def from_pciid(self, pci_device):
        if d := self.devices.get(pci_device):
            return d

        # We did not find a device with the exact PCIID, let's drop the revision and try again
        pci_device = PCIDevice(vendor_id=pci_device.vendor_id, product_id=pci_device.product_id,
                               revision=0)

        return self.devices.get(pci_device)

    def parse_db(self):  # pragma: nocover
        raise NotImplementedError()
