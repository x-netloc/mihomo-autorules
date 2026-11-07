// freedom-no-ru
// Generated from autorules. Do not edit by hand.

function main(config) {
  const groups = config["proxy-groups"] || [];
  const proxies = config.proxies || [];
  const hasProxyPolicy = [...groups, ...proxies].some(
    (item) => item && item.name === "PROXY",
  );
  if (!hasProxyPolicy) {
    const fallbackGroups = groups
      .map((group) => group && group.name)
      .filter((name) => name && name !== "DIRECT" && name !== "REJECT");
    config["proxy-groups"] = [
      {
        name: "PROXY",
        type: "select",
        "include-all": true,
        proxies: [...fallbackGroups, "DIRECT"],
      },
      ...groups,
    ];
  }

  const providers = {
  "autorules-geosite-private": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/private.mrs",
    "path": "./ruleset/autorules-geosite-private.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-private-extra": {
    "type": "http",
    "behavior": "classical",
    "format": "text",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/private-extra.txt",
    "path": "./ruleset/autorules-geosite-private-extra.txt",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-private": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/private.mrs",
    "path": "./ruleset/autorules-geoip-private.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-apple": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/apple.mrs",
    "path": "./ruleset/autorules-geosite-apple.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-icloud": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/icloud.mrs",
    "path": "./ruleset/autorules-geosite-icloud.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-category-ru": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/category-ru.mrs",
    "path": "./ruleset/autorules-geosite-category-ru.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-ru-available-only-inside": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/ru-available-only-inside.mrs",
    "path": "./ruleset/autorules-geosite-ru-available-only-inside.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-ru": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/ru.mrs",
    "path": "./ruleset/autorules-geoip-ru.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  }
};
  config["rule-providers"] = Object.assign(
    config["rule-providers"] || {},
    providers,
  );
  config.rules = [
  "RULE-SET,autorules-geosite-private,DIRECT",
  "RULE-SET,autorules-geosite-private-extra,DIRECT",
  "RULE-SET,autorules-geoip-private,DIRECT,no-resolve",
  "RULE-SET,autorules-geosite-apple,DIRECT",
  "RULE-SET,autorules-geosite-icloud,DIRECT",
  "DOMAIN-SUFFIX,ru,DIRECT",
  "DOMAIN-SUFFIX,su,DIRECT",
  "DOMAIN-SUFFIX,xn--p1ai,DIRECT",
  "DOMAIN-SUFFIX,2gis.com,DIRECT",
  "DOMAIN-SUFFIX,vk.com,DIRECT",
  "DOMAIN-SUFFIX,vk.me,DIRECT",
  "DOMAIN-SUFFIX,userapi.com,DIRECT",
  "RULE-SET,autorules-geosite-category-ru,DIRECT",
  "RULE-SET,autorules-geosite-ru-available-only-inside,DIRECT",
  "RULE-SET,autorules-geoip-ru,DIRECT,no-resolve",
  "MATCH,PROXY"
];
  return config;
}
