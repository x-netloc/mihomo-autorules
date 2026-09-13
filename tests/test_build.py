import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.build import (
    convert_geoip,
    convert_geosite,
    inline_cidr_rule,
    inline_domain_rule,
    build,
)


class ConversionTests(unittest.TestCase):
    def test_geosite_is_split_into_mrs_domains_and_classical_extras(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "geosite_test.txt"
            source.write_text(
                """domain:example.com
full:www.example.org
keyword:video
regexp:^api\\d+\\.example\\.net$
domain:example.com@attribute
# comment
""",
                encoding="utf-8",
            )

            domains, extras = convert_geosite(source)

            self.assertEqual(domains, ["+.example.com", "www.example.org"])
            self.assertEqual(
                extras,
                [
                    "DOMAIN-KEYWORD,video",
                    "DOMAIN-REGEX,^api\\d+\\.example\\.net$",
                ],
            )

    def test_geoip_is_validated_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "geoip_test.txt"
            source.write_text(
                "192.0.2.1/24\n2001:db8::/32\n192.0.2.0/24\n",
                encoding="utf-8",
            )

            self.assertEqual(
                convert_geoip(source),
                ["192.0.2.0/24", "2001:db8::/32"],
            )

    def test_inline_rules_preserve_all_canonical_domain_types(self) -> None:
        self.assertEqual(
            inline_domain_rule("domain:example.com", "DIRECT"),
            "DOMAIN-SUFFIX,example.com,DIRECT",
        )
        self.assertEqual(
            inline_domain_rule("regexp:^api", "PROXY"),
            "DOMAIN-REGEX,^api,PROXY",
        )
        self.assertEqual(
            inline_cidr_rule("2001:db8::/32", "DIRECT"),
            "IP-CIDR6,2001:db8::/32,DIRECT,no-resolve",
        )


class BuildTests(unittest.TestCase):
    def test_build_discovers_categories_and_profiles_from_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "profiles").mkdir()
            (root / "geosite").mkdir()
            (root / "geoip").mkdir()
            (root / "catalog.toml").write_text(
                """schema_version = 1

[upstream]
repository = "owner/upstream"
ref = "release"
geosite_asset = "geosite.dat"
geoip_asset = "geoip.dat"

[categories]
geosite = ["private"]
geoip = ["private"]

[profiles]
ids = ["example"]
""",
                encoding="utf-8",
            )
            (root / "profiles/example.toml").write_text(
                """schema_version = 1
id = "example"
description = "Example profile."
default = "proxy"

[[rules]]
action = "direct"
geosite = ["private"]

[[rules]]
action = "direct"
geoip = ["private"]
""",
                encoding="utf-8",
            )
            (root / "geosite/geosite_private.txt").write_text(
                "domain:example.com\nkeyword:private\n",
                encoding="utf-8",
            )
            (root / "geoip/geoip_private.txt").write_text(
                "192.0.2.0/24\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(
                catalog=root / "catalog.toml",
                profiles=root / "profiles",
                geosite_in=root / "geosite",
                geoip_in=root / "geoip",
                out=root / "out",
                repository="owner/repo",
                dist_ref="dist",
            )

            build(args)

            self.assertEqual(
                (root / "out/staging/geosite/private.txt").read_text(
                    encoding="utf-8"
                ),
                "+.example.com\n",
            )
            self.assertEqual(
                (root / "out/geosite/private-extra.txt").read_text(
                    encoding="utf-8"
                ),
                "DOMAIN-KEYWORD,private\n",
            )
            self.assertEqual(
                (root / "out/staging/geoip/private.txt").read_text(
                    encoding="utf-8"
                ),
                "192.0.2.0/24\n",
            )

            override = (root / "out/profiles/example.js").read_text(encoding="utf-8")
            self.assertIn("autorules-geosite-private", override)
            self.assertIn("autorules-geosite-private-extra", override)
            self.assertIn("autorules-geoip-private", override)
            self.assertIn("RULE-SET,autorules-geoip-private,DIRECT,no-resolve", override)
            self.assertIn("MATCH,PROXY", override)

            manifest = json.loads(
                (root / "out/.build-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["profiles"], ["example"])
            self.assertEqual(
                manifest["categories"]["geosite"]["private"],
                {"domain": 1, "extra": 1},
            )


if __name__ == "__main__":
    unittest.main()
