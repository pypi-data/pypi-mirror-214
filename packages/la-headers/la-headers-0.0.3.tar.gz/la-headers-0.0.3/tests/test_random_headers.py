import json
from unittest import TestCase, main

from la_headers import generate_random_headers


class TestSystem(TestCase):
    def test_base(self) -> None:
        # TODO: Change test to check all possible paths,
        # instead of generate many.
        for _ in range(1_000):
            print(json.dumps(generate_random_headers(), indent=2))


if __name__ == "__main__":
    main()
