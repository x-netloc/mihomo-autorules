#!/usr/bin/env python3
"""Build Mihomo rule-provider sources and Mihomo Party overrides."""

from __future__ import annotations

import argparse
import ipaddress
import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Iterable


ACTION_NAMES = {
    "direct": "DIRECT",
    "proxy": "PROXY",
    "reject": "REJECT",
}
SELECTORS = {"geosite", "geoip", "domains", "cidrs"}


class BuildError(Exception):
    pass


def load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise BuildError(f"cannot read {path}: {exc}") from exc


def unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def source_lines(path: Path) -> Iterable[str]:
    if not path.is_file():
        raise BuildError(f"missing upstream category: {path}")
    with path.open(encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if " @" in line:
                line = line.split(" @", 1)[0].strip()
            elif not line.startswith("regexp:") and "@" in line:
                line = line.split("@", 1)[0].strip()
            if line:
                yield line


def convert_geosite(path: Path) -> tuple[list[str], list[str]]:
    domains: list[str] = []
    extras: list[str] = []
    for line in source_lines(path):
        if line.startswith("domain:"):
            domains.append(f"+.{line[7:]}")
        elif line.startswith("full:"):
            domains.append(line[5:])
        elif line.startswith("keyword:"):
            extras.append(f"DOMAIN-KEYWORD,{line[8:]}")
        elif line.startswith("regexp:"):
            extras.append(f"DOMAIN-REGEX,{line[7:]}")
        else:
            domains.append(f"+.{line}")
    return unique(domains), unique(extras)


def convert_geoip(path: Path) -> list[str]:
    networks: list[str] = []
    for line in source_lines(path):
        try:
            network = ipaddress.ip_network(line, strict=False)
        except ValueError as exc:
            raise BuildError(f"invalid CIDR in {path}: {line}") from exc
        networks.append(str(network))
    return unique(networks)


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def provider_name(kind: str, category: str, extra: bool = False) -> str:
    suffix = "-extra" if extra else ""
    return f"autorules-{kind}-{category}{suffix}"


def provider_definition(
    kind: str,
    category: str,
    repository: str,
    dist_ref: str,
    extra: bool = False,
) -> dict[str, Any]:
    name = provider_name(kind, category, extra)
    if extra:
        relative_path = f"geosite/{category}-extra.txt"
        behavior = "classical"
        file_format = "text"
    else:
        relative_path = f"{kind}/{category}.mrs"
        behavior = "domain" if kind == "geosite" else "ipcidr"
        file_format = "mrs"
    local_extension = "txt" if extra else "mrs"
    return {
        "type": "http",
        "behavior": behavior,
        "format": file_format,
        "url": (
            f"https://raw.githubusercontent.com/{repository}/{dist_ref}/"
            f"{relative_path}"
        ),
        "path": f"./ruleset/{name}.{local_extension}",
        "interval": 3600,
        "proxy": "PROXY",
    }


def inline_domain_rule(value: str, action: str) -> str:
    try:
        prefix, pattern = value.split(":", 1)
    except ValueError as exc:
        raise BuildError(f"invalid domain rule: {value}") from exc
    rule_types = {
        "domain": "DOMAIN-SUFFIX",
        "full": "DOMAIN",
        "keyword": "DOMAIN-KEYWORD",
        "regexp": "DOMAIN-REGEX",
    }
    try:
        rule_type = rule_types[prefix]
    except KeyError as exc:
        raise BuildError(f"unsupported domain rule: {value}") from exc
    return f"{rule_type},{pattern},{action}"


def inline_cidr_rule(value: str, action: str) -> str:
    try:
        version = ipaddress.ip_network(value, strict=False).version
    except ValueError as exc:
        raise BuildError(f"invalid CIDR rule: {value}") from exc
    rule_type = "IP-CIDR6" if version == 6 else "IP-CIDR"
    return f"{rule_type},{value},{action},no-resolve"


def render_override(
    profile: dict[str, Any],
    stats: dict[str, dict[str, dict[str, int]]],
    repository: str,
    dist_ref: str,
) -> str:
    profile_id = profile["id"]
    providers: dict[str, dict[str, Any]] = {}
    rules: list[str] = []

    for rule in profile["rules"]:
        try:
            action = ACTION_NAMES[rule["action"]]
        except KeyError as exc:
            raise BuildError(f"unsupported action in profile {profile_id}") from exc
        selectors = SELECTORS & rule.keys()
        if len(selectors) != 1:
            raise BuildError(f"invalid selector in profile {profile_id}")
        selector = selectors.pop()

        if selector in {"geosite", "geoip"}:
            for category in rule[selector]:
                category_stats = stats[selector][category]
                primary_count = category_stats["domain" if selector == "geosite" else "cidr"]
                if primary_count:
                    name = provider_name(selector, category)
                    providers[name] = provider_definition(
                        selector,
                        category,
                        repository,
                        dist_ref,
                    )
                    no_resolve = ",no-resolve" if selector == "geoip" else ""
                    rules.append(f"RULE-SET,{name},{action}{no_resolve}")
                if selector == "geosite" and category_stats["extra"]:
                    name = provider_name(selector, category, extra=True)
                    providers[name] = provider_definition(
                        selector,
                        category,
                        repository,
                        dist_ref,
                        extra=True,
                    )
                    rules.append(f"RULE-SET,{name},{action}")
        elif selector == "domains":
            rules.extend(inline_domain_rule(value, action) for value in rule[selector])
        else:
            rules.extend(inline_cidr_rule(value, action) for value in rule[selector])

    try:
        default_action = ACTION_NAMES[profile["default"]]
    except KeyError as exc:
        raise BuildError(f"unsupported default action in profile {profile_id}") from exc
    rules.append(f"MATCH,{default_action}")

    providers_json = json.dumps(providers, ensure_ascii=False, indent=2)
    rules_json = json.dumps(rules, ensure_ascii=False, indent=2)
    return f"""// {profile_id}
// Generated from autorules. Do not edit by hand.

function main(config) {{
  const groups = config["proxy-groups"] || [];
  const proxies = config.proxies || [];
  const hasProxyPolicy = [...groups, ...proxies].some(
    (item) => item && item.name === "PROXY",
  );
  if (!hasProxyPolicy) {{
    const fallbackGroups = groups
      .map((group) => group && group.name)
      .filter((name) => name && name !== "DIRECT" && name !== "REJECT");
    config["proxy-groups"] = [
      {{
        name: "PROXY",
        type: "select",
        "include-all": true,
        proxies: [...fallbackGroups, "DIRECT"],
      }},
      ...groups,
    ];
  }}

  const providers = {providers_json};
  config["rule-providers"] = Object.assign(
    config["rule-providers"] || {{}},
    providers,
  );
  config.rules = {rules_json};
  return config;
}}
"""


def build(args: argparse.Namespace) -> None:
    catalog = load_toml(args.catalog)
    categories = catalog["categories"]
    profile_ids = catalog["profiles"]["ids"]
    upstream = catalog["upstream"]
    source_name = f"{upstream['repository']}@{upstream['ref']}"

    stats: dict[str, dict[str, dict[str, int]]] = {
        "geosite": {},
        "geoip": {},
    }
    for category in categories["geosite"]:
        domains, extras = convert_geosite(
            args.geosite_in / f"geosite_{category}.txt"
        )
        if domains:
            write_lines(args.out / "staging/geosite" / f"{category}.txt", domains)
        if extras:
            write_lines(args.out / "geosite" / f"{category}-extra.txt", extras)
        stats["geosite"][category] = {
            "domain": len(domains),
            "extra": len(extras),
        }

    for category in categories["geoip"]:
        cidrs = convert_geoip(args.geoip_in / f"geoip_{category}.txt")
        if cidrs:
            write_lines(args.out / "staging/geoip" / f"{category}.txt", cidrs)
        stats["geoip"][category] = {"cidr": len(cidrs)}

    profiles_dir = args.out / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    for profile_id in profile_ids:
        profile_path = args.profiles / f"{profile_id}.toml"
        profile = load_toml(profile_path)
        if profile.get("id") != profile_id:
            raise BuildError(f"profile id mismatch: {profile_path}")
        override = render_override(profile, stats, args.repository, args.dist_ref)
        (profiles_dir / f"{profile_id}.js").write_text(override, encoding="utf-8")

    index = [
        "# Mihomo rule-provider index",
        f"# Source: {source_name}",
        "# Catalog: autorules",
        "",
        "| Kind | Category | MRS rules | Classical extras |",
        "| --- | --- | ---: | ---: |",
    ]
    for category in categories["geosite"]:
        category_stats = stats["geosite"][category]
        index.append(
            f"| geosite | {category} | {category_stats['domain']} | "
            f"{category_stats['extra']} |"
        )
    for category in categories["geoip"]:
        index.append(
            f"| geoip | {category} | {stats['geoip'][category]['cidr']} | 0 |"
        )
    (args.out / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    (args.out / ".build-manifest.json").write_text(
        json.dumps(
            {
                "source": source_name,
                "profiles": profile_ids,
                "categories": stats,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"Prepared {len(categories['geosite'])} geosite categories, "
        f"{len(categories['geoip'])} geoip categories and "
        f"{len(profile_ids)} overrides in {args.out}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--profiles", required=True, type=Path)
    parser.add_argument("--geosite-in", required=True, type=Path)
    parser.add_argument("--geoip-in", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--repository", default="x-netloc/mihomo-autorules")
    parser.add_argument("--dist-ref", default="dist")
    return parser.parse_args()


def main() -> int:
    try:
        build(parse_args())
    except (BuildError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
