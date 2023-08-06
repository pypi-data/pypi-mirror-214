from unittest import TestCase, main

from la_headers.gen.system import generate_system


class TestSystem(TestCase):
    def test_linux(self) -> None:
        print(generate_system("linux", "22.04", "chrome"))

    def test_android(self) -> None:
        print(generate_system("android", "16", "chrome"))

    def test_windows(self) -> None:
        print(generate_system("windows", "10", "chrome"))

    def test_mac(self) -> None:
        print(generate_system("mac", "19", "chrome"))


if __name__ == "__main__":
    main()
