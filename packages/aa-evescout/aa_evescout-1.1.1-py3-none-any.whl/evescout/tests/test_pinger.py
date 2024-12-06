from django.test import TestCase
from eveuniverse.models import EveSolarSystem

from evescout.models import SignaturePinger, SignatureSystem
from evescout.tests.testdata.load_eveuniverse import load_eveuniverse


class TestPinger(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_create(self):
        SignaturePinger.create(1273234292821987391)
        self.assertTrue(True)

    def test_pingers_in_range(self):
        hasmijaala = EveSolarSystem.objects.get(id=30002806)
        hasmijaala_sig = SignatureSystem.create(
            00, hasmijaala, SignatureSystem.SignatureOrigin.THERA
        )

        sujarento = EveSolarSystem.objects.get(name="Sujarento")
        pinger_suj = SignaturePinger.create(000, sujarento)
        pinger_suj.min_ping_distance_jump = 1  # won't ping for hasmijaala
        pinger_suj.save()

        nagamanen = EveSolarSystem.objects.get(name="Nagamanen")
        pinger_nag = SignaturePinger.create(000, nagamanen)
        pinger_nag.min_ping_distance_jump = 2  # will ping for hasmijaala
        pinger_nag.save()

        tannolen = EveSolarSystem.objects.get(name="Tannolen")
        pinger_tan = SignaturePinger.create(000, tannolen)
        pinger_tan.always_ping = True
        pinger_tan.save()

        pingers_in_range = hasmijaala_sig.pingers_in_range()

        self.assertIn(pinger_nag, pingers_in_range)
        self.assertNotIn(pinger_suj, pingers_in_range)
        self.assertIn(pinger_tan, pingers_in_range)

    def test_uninitialized_pinger_in_range(self):
        """
        Unitialized pingers (with system still at None) were causing a crash when calling `pingers_in_range()`
        """
        oto = EveSolarSystem.objects.get(name="Oto")

        SignaturePinger.create(1)

        signature = SignatureSystem.create(
            1, oto, SignatureSystem.SignatureOrigin.THERA
        )

        pingers = signature.pingers_in_range()

        self.assertEqual(0, len(pingers))

    def test_in_range(self):
        nagamanen = EveSolarSystem.objects.get(id=30002807)
        pinger = SignaturePinger.create(00, nagamanen)
        pinger.min_ping_distance_ly = 10
        pinger.min_ping_distance_ly = 10
        pinger.save()

        hasmijaala = EveSolarSystem.objects.get(id=30002806)
        sig = SignatureSystem.create(
            00, hasmijaala, SignatureSystem.SignatureOrigin.THERA
        )

        self.assertTrue(sig.is_pinger_in_range(pinger))

    def test_name(self):
        pinger = SignaturePinger.create(1)

        self.assertEqual("Unlinked pinger 1", str(pinger))

    def test_wh_never_in_range(self):
        tama = EveSolarSystem.objects.get(name="Tama")
        pinger = SignaturePinger.create(1)
        pinger.always_ping = True
        pinger.system = tama
        pinger.save()

        wh_system = EveSolarSystem.objects.get(id=31001805)
        signature = SignatureSystem.create(
            00, wh_system, SignatureSystem.SignatureOrigin.THERA
        )

        pingers_in_range = signature.pingers_in_range()

        self.assertEqual(0, len(pingers_in_range))
