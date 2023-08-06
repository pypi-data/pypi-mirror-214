from unittest.mock import patch, MagicMock

import contextlib
import io
import unittest

from gfxinfo import SUPPORTED_GPU_DBS, PCIDevice, DeviceTreeGPU

from .amdgpu import AMDGPU, AmdGpuDeviceDB
from .intel import IntelGPU, IntelI915GpuDeviceDB
from .virt import VirtGPU


class DatabaseTests(unittest.TestCase):
    def test_check_db(self):
        for gpu_db in SUPPORTED_GPU_DBS:
            with self.subTest(GPU_DB=type(gpu_db).__name__):
                self.assertTrue(gpu_db.check_db())


class PCIDeviceTests(unittest.TestCase):
    def test_hash(self):
        self.assertEqual(hash(PCIDevice(0x1234, 0x5678, 0x9a)), 0x123456789a)

    def test_str(self):
        self.assertEqual(str(PCIDevice(0x1234, 0x5678, 0x9a)), "0x1234:0x5678:0x9a")

    def test_from_str(self):
        self.assertEqual(PCIDevice.from_str("1234:5678:9a"), PCIDevice(0x1234, 0x5678, 0x9a))
        self.assertEqual(PCIDevice.from_str("0x1234:0x5678:0x9a"), PCIDevice(0x1234, 0x5678, 0x9a))

        self.assertEqual(PCIDevice.from_str("0x1234:5678"), PCIDevice(0x1234, 0x5678, 0x0))

        with self.assertRaises(ValueError):
            self.assertEqual(PCIDevice.from_str("0x1234:5678:0x12:045"), PCIDevice(0x1234, 0x5678, 0x0))


class DeviceTreeGPUTests(unittest.TestCase):
    def setUp(self):
        self.gpu = DeviceTreeGPU.from_compatible_str("brcm,bcm2711-vc5\0brcm,bcm2835-vc4\0")

    def test_base_name(self):
        self.assertEqual(self.gpu.base_name, "brcm-bcm2711-vc5")

    def test_pciid(self):
        self.assertIsNone(self.gpu.pciid)

    def test_pci_device(self):
        self.assertIsNone(self.gpu.pci_device)

    def test_tags(self):
        self.assertEqual(self.gpu.tags, {"dt_gpu:vendor:brcm", "dt_gpu:model:bcm2711-vc5"})

    def test_structured_tags(self):
        self.assertEqual(self.gpu.structured_tags,
                         {"type": "devicetree",
                          "vendor": "brcm",
                          "model": "bcm2711-vc5"})

    def test_str(self):
        self.assertEqual(str(self.gpu), "<DeviceTreeGPU: brcm/bcm2711-vc5>")

    def test_from_compatible_str(self):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertIsNone(DeviceTreeGPU.from_compatible_str("brcm,bcm2711-vc5,extra"))

        self.assertEqual(f.getvalue(), ("ERROR: The compatible 'brcm,bcm2711-vc5,extra' is not "
                                        "following the expected format 'vendor,model'\n"))

    def test_unknown_fields(self):
        self.assertEqual(self.gpu.unknown_fields, set())


class AMDGPUTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x1002, product_id=0x163F, revision=0xAE)
        self.gpu = AMDGPU(pci_device=self.pci_device, asic_type="GFX10_3_3",
                          is_APU=True, marketing_name="AMD Custom GPU 0405 / Steam Deck")

    def test_pciid(self):
        assert self.gpu.pciid == str(self.pci_device)

    def test_some_devices(self):
        self.assertEqual(self.gpu.codename, "VANGOGH")
        self.assertIsNone(self.gpu.family)
        self.assertEqual(self.gpu.architecture, "RDNA2")
        self.assertEqual(self.gpu.base_name, "gfx10-vangogh")
        self.assertTrue(self.gpu.is_APU)
        self.assertEqual(self.gpu.unknown_fields, set())
        self.assertEqual(self.gpu.tags, {'amdgpu:generation:10', 'amdgpu:architecture:RDNA2',
                                         'amdgpu:codename:VANGOGH', 'amdgpu:pciid:0x1002:0x163f:0xae',
                                         'amdgpu:integrated'})
        self.assertEqual(self.gpu.structured_tags, {
            'APU': True,
            'architecture': 'RDNA2',
            'codename': 'VANGOGH',
            'family': None,
            'generation': 10,
            'gfxversion': 'gfx10',
            'integrated': True,
            'marketing_name': "AMD Custom GPU 0405 / Steam Deck",
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu'
        })

        renoir = AMDGPU(pci_device=self.pci_device, asic_type="GFX9_0_C", is_APU=True, marketing_name="Marketing name")
        self.assertEqual(renoir.codename, "RENOIR")
        self.assertEqual(renoir.family, "AI")
        self.assertEqual(renoir.architecture, "GCN5.1")
        self.assertEqual(renoir.base_name, "gfx9-renoir")
        self.assertTrue(renoir.is_APU)
        self.assertEqual(renoir.unknown_fields, set())
        self.assertEqual(renoir.tags, {'amdgpu:generation:9', 'amdgpu:architecture:GCN5.1',
                                       'amdgpu:codename:RENOIR', 'amdgpu:pciid:0x1002:0x163f:0xae',
                                       'amdgpu:integrated', 'amdgpu:family:AI'})
        self.assertEqual(renoir.structured_tags, {
            'APU': True,
            'architecture': 'GCN5.1',
            'codename': 'RENOIR',
            'family': "AI",
            'generation': 9,
            'gfxversion': 'gfx9',
            'integrated': True,
            'marketing_name': 'Marketing name',
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu'
        })
        self.assertEqual(str(renoir), "<AMDGPU: PCIID 0x1002:0x163f:0xae - RENOIR - AI - GCN5.1 - gfx9>")

        navi31 = AMDGPU(pci_device=self.pci_device, asic_type="GFX11_0_0", is_APU=False,
                        marketing_name="AMD Radeon RX 7900 XTX")
        self.assertEqual(navi31.codename, "NAVI31")
        self.assertEqual(navi31.family, None)
        self.assertEqual(navi31.architecture, "RDNA3")
        self.assertEqual(navi31.base_name, "gfx11-navi31")
        self.assertFalse(navi31.is_APU)
        self.assertEqual(navi31.unknown_fields, set())
        self.assertEqual(navi31.tags, {'amdgpu:generation:11', 'amdgpu:architecture:RDNA3',
                                       'amdgpu:codename:NAVI31', 'amdgpu:discrete',
                                       'amdgpu:pciid:0x1002:0x163f:0xae'})
        self.assertEqual(navi31.structured_tags, {
            'APU': False,
            'architecture': 'RDNA3',
            'codename': 'NAVI31',
            'generation': 11,
            'gfxversion': 'gfx11',
            'integrated': False,
            'marketing_name': 'AMD Radeon RX 7900 XTX',
            'pciid': '0x1002:0x163f:0xae',
            'type': 'amdgpu',
            'family': None,
        })
        self.assertEqual(str(navi31), "<AMDGPU: PCIID 0x1002:0x163f:0xae - NAVI31 - None - RDNA3 - gfx11>")


class AmdGpuDeviceDBTests(unittest.TestCase):
    @patch('builtins.open')
    def test_db_missing(self, open_mock):
        def side_effect(*args, **kwargs):
            if len(args) > 1 and args[1] == 'r':
                raise FileNotFoundError()
            else:
                return MagicMock()
        open_mock.side_effect = side_effect

        # DB missing, but download works
        db = AmdGpuDeviceDB()
        self.assertGreater(len(db.devices), 1)
        self.assertTrue(db.check_db())

        # DB missing, and URL failed
        with patch('valve_gfx_ci.gfxinfo.gpudb.requests.get', side_effect=ValueError()):
            db = AmdGpuDeviceDB()
            self.assertEqual(len(db.devices), 1)
            self.assertFalse(db.check_db())

    def test_update(self):
        db = AmdGpuDeviceDB()
        db.cache_db = MagicMock()

        # Check that the DB is marked as not up to date by default
        self.assertFalse(db.is_up_to_date)

        # Check that calling update() calls cache_db() and marks the DB as up to date
        self.assertTrue(db.update())
        db.cache_db.assert_called_once_with()
        self.assertTrue(db.is_up_to_date)

        # Check that further update() calls don't lead to more calls to cache_db()
        self.assertTrue(db.update())
        db.cache_db.assert_called_once_with()

    def test_check_db(self):
        db = AmdGpuDeviceDB()

        # Check that the DB is complete by default
        self.assertTrue(db.check_db())

        # Add an incomplete GPU
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0x0001, revision=0x42)
        db.devices[pci_device] = AMDGPU(pci_device=pci_device, asic_type="GFX10_3_42",
                                        is_APU=True, marketing_name="GPU with non-existant architecture")

        self.assertFalse(db.check_db())

    def test_db_name(self):
        self.assertEqual(AmdGpuDeviceDB().db_name, "AmdGpuDeviceDB")


class IntelGpuTests(unittest.TestCase):
    def test_raw_codenames(self):
        pci_device = PCIDevice(vendor_id=0x1002, product_id=0x0001, revision=0x42)

        unsupported_format = IntelGPU(pci_device=pci_device, raw_codename="_IDONTEXIST")
        self.assertEqual(unsupported_format.short_architecture, "_IDONTEXIST")
        self.assertIsNone(unsupported_format.variant)
        self.assertIsNone(unsupported_format.gt)
        self.assertIsNone(unsupported_format.human_name)
        self.assertTrue(unsupported_format.is_integrated)
        self.assertEqual(unsupported_format.unknown_fields, {"gen_version", "architecture"})
        self.assertEqual(unsupported_format.base_name, 'intel-unk-_idontexist')
        self.assertEqual(unsupported_format.tags, {'intelgpu:pciid:0x1002:0x1:0x42',
                                                   'intelgpu:raw_codename:_IDONTEXIST'})
        self.assertEqual(unsupported_format.structured_tags, {'pciid': '0x1002:0x1:0x42', 'raw_codename': '_IDONTEXIST',
                                                              'type': 'intelgpu'})

        ats_m75 = IntelGPU(pci_device=pci_device, raw_codename="ATS_M75")
        self.assertEqual(ats_m75.short_architecture, "ATS")
        self.assertEqual(ats_m75.variant, "M75")
        self.assertIsNone(ats_m75.gt)
        self.assertEqual(ats_m75.human_name, "Arctic Sound M75")
        self.assertEqual(ats_m75.architecture, "ARCTICSOUND")
        self.assertFalse(ats_m75.is_integrated)
        self.assertEqual(ats_m75.base_name, 'intel-gen12-ats-m75')
        self.assertEqual(ats_m75.tags, {'intelgpu:pciid:0x1002:0x1:0x42', 'intelgpu:gen:12',
                                        'intelgpu:codename:ATS-M75', 'intelgpu:discrete',
                                        'intelgpu:architecture:ARCTICSOUND'})

        adlp = IntelGPU(pci_device=pci_device, raw_codename="ADLP")
        self.assertEqual(adlp.short_architecture, "ADL")
        self.assertEqual(adlp.variant, "P")
        self.assertIsNone(adlp.gt)
        self.assertEqual(adlp.human_name, "Alder Lake P")
        self.assertEqual(adlp.architecture, "ALDERLAKE")
        self.assertTrue(adlp.is_integrated)
        self.assertEqual(adlp.base_name, 'intel-gen12-adl-p')
        self.assertEqual(adlp.structured_tags, {'architecture': 'ALDERLAKE', 'codename': 'ADL-P', 'generation': 12,
                                                'integrated': True, 'marketing_name': 'Alder Lake P',
                                                'pciid': '0x1002:0x1:0x42', 'type': 'intelgpu'})

        whl_u_gt2 = IntelGPU(pci_device=pci_device, raw_codename="WHL_U_GT2")
        self.assertEqual(whl_u_gt2.short_architecture, "WHL")
        self.assertEqual(whl_u_gt2.variant, "U")
        self.assertEqual(whl_u_gt2.gt, 2)
        self.assertEqual(whl_u_gt2.human_name, "Whisky Lake U GT2")
        self.assertEqual(whl_u_gt2.architecture, "WHISKYLAKE")
        self.assertTrue(whl_u_gt2.is_integrated)
        self.assertEqual(whl_u_gt2.base_name, 'intel-gen9-whl-u-gt2')
        self.assertEqual(str(whl_u_gt2), "<IntelGPU: PCIID 0x1002:0x1:0x42 - gen9 - Whisky Lake U GT2>")

        bdw_gt1 = IntelGPU(pci_device=pci_device, raw_codename="BDW_GT1")
        self.assertEqual(bdw_gt1.short_architecture, "BDW")
        self.assertIsNone(bdw_gt1.variant)
        self.assertEqual(bdw_gt1.gt, 1)
        self.assertEqual(bdw_gt1.human_name, "Broadwell GT1")
        self.assertEqual(bdw_gt1.architecture, "BROADWELL")
        self.assertTrue(bdw_gt1.is_integrated)
        self.assertEqual(bdw_gt1.base_name, 'intel-gen8-bdw-gt1')
        self.assertEqual(bdw_gt1.tags, {'intelgpu:pciid:0x1002:0x1:0x42', 'intelgpu:gen:8',
                                        'intelgpu:codename:BDW-GT1', 'intelgpu:integrated',
                                        'intelgpu:architecture:BROADWELL', 'intelgpu:GT:1'})

        vlv = IntelGPU(pci_device=pci_device, raw_codename="VLV")
        self.assertEqual(vlv.short_architecture, "VLV")
        self.assertIsNone(vlv.variant)
        self.assertIsNone(vlv.gt)
        self.assertEqual(vlv.human_name, "Valley View")
        self.assertEqual(vlv.architecture, "VALLEYVIEW")
        self.assertTrue(vlv.is_integrated)
        self.assertEqual(vlv.base_name, 'intel-gen7-vlv')
        self.assertEqual(str(vlv), "<IntelGPU: PCIID 0x1002:0x1:0x42 - gen7 - Valley View>")


class IntelI915GpuDeviceDBTests(unittest.TestCase):
    def test_db_name(self):
        self.assertEqual(IntelI915GpuDeviceDB().db_name, "IntelI915GpuDeviceDB")

    def test_cache_db(self):
        self.assertIsNotNone(IntelI915GpuDeviceDB().cache_db())

    def test_update(self):
        self.assertTrue(IntelI915GpuDeviceDB().update())

    def test_check_db(self):
        self.assertTrue(IntelI915GpuDeviceDB().check_db())

    def test_from_pciid(self):
        pci_device = PCIDevice(vendor_id=0x8086, product_id=0x3e9b, revision=0)
        dev = IntelI915GpuDeviceDB().from_pciid(pci_device)

        self.assertEqual(dev.codename, "CFL-H-GT2")

        # Make sure that in the presence of an unknown revision, we only use the vendor_id/product_id
        pci_device2 = PCIDevice(vendor_id=0x8086, product_id=0x3e9b, revision=42)
        self.assertEqual(dev, IntelI915GpuDeviceDB().from_pciid(pci_device2))


class VirtGPUTests(unittest.TestCase):
    def setUp(self):
        self.pci_device = PCIDevice(vendor_id=0x1af4, product_id=0x1050, revision=0)
        self.gpu = VirtGPU(pci_device=self.pci_device)

    def test_some_devices(self):
        self.assertEqual(self.gpu.base_name, "virtio")
        self.assertEqual(self.gpu.codename, "VIRTIO")
        self.assertEqual(self.gpu.tags, {'virtio:codename:VIRTIO', 'virtio:family:VIRTIO',
                                         'virtio:pciid:0x1af4:0x1050:0x0'})
        self.assertEqual(self.gpu.structured_tags, {
            'architecture': 'VIRTIO',
            'codename': 'VIRTIO',
            'generation': 1,
            'integrated': True,
            'marketing_name': "VirtIO",
            'pciid': '0x1af4:0x1050:0x0',
            'type': 'virtio'
        })
        self.assertEqual(str(self.gpu), "<VirtGPU: PCIID 0x1af4:0x1050:0x0>")
