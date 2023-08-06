from snapshottest import TestCase
import unittest

from boringavatars import avatar


class AvatarTests(TestCase):
    def test_avatar_beam(self):
        out = avatar("foobar", variant="beam")
        self.assertMatchSnapshot(out)

    def test_avatar_marble(self):
        out = avatar("foobar", variant="marble")
        self.assertMatchSnapshot(out)

    def test_avatar_pixel(self):
        out = avatar("foobar", variant="pixel")
        self.assertMatchSnapshot(out)

    def test_avatar_sunset(self):
        out = avatar("foobar", variant="sunset")
        self.assertMatchSnapshot(out)

    def test_avatar_bauhaus(self):
        out = avatar("foobar", variant="bauhaus")
        self.assertMatchSnapshot(out)

    def test_avatar_ring(self):
        out = avatar("foobar", variant="ring")
        self.assertMatchSnapshot(out)


if __name__ == "__main__":
    unittest.main()
