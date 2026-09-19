// bypass-blacklist
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
  "autorules-geosite-youtube": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/youtube.mrs",
    "path": "./ruleset/autorules-geosite-youtube.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-openai": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/openai.mrs",
    "path": "./ruleset/autorules-geosite-openai.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-openai-extra": {
    "type": "http",
    "behavior": "classical",
    "format": "text",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/openai-extra.txt",
    "path": "./ruleset/autorules-geosite-openai-extra.txt",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-discord": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/discord.mrs",
    "path": "./ruleset/autorules-geosite-discord.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-telegram": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/telegram.mrs",
    "path": "./ruleset/autorules-geosite-telegram.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-meta": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/meta.mrs",
    "path": "./ruleset/autorules-geosite-meta.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-twitter": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/twitter.mrs",
    "path": "./ruleset/autorules-geosite-twitter.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-cloudflare": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/cloudflare.mrs",
    "path": "./ruleset/autorules-geoip-cloudflare.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-cloudfront": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/cloudfront.mrs",
    "path": "./ruleset/autorules-geoip-cloudfront.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-fastly": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/fastly.mrs",
    "path": "./ruleset/autorules-geoip-fastly.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-facebook": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/facebook.mrs",
    "path": "./ruleset/autorules-geoip-facebook.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-telegram": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/telegram.mrs",
    "path": "./ruleset/autorules-geoip-telegram.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-twitter": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/twitter.mrs",
    "path": "./ruleset/autorules-geoip-twitter.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geosite-ru-blocked": {
    "type": "http",
    "behavior": "domain",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/ru-blocked.mrs",
    "path": "./ruleset/autorules-geosite-ru-blocked.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-ru-blocked": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/ru-blocked.mrs",
    "path": "./ruleset/autorules-geoip-ru-blocked.mrs",
    "interval": 3600,
    "proxy": "PROXY"
  },
  "autorules-geoip-re-filter": {
    "type": "http",
    "behavior": "ipcidr",
    "format": "mrs",
    "url": "https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geoip/re-filter.mrs",
    "path": "./ruleset/autorules-geoip-re-filter.mrs",
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
  "RULE-SET,autorules-geosite-youtube,PROXY",
  "RULE-SET,autorules-geosite-openai,PROXY",
  "RULE-SET,autorules-geosite-openai-extra,PROXY",
  "RULE-SET,autorules-geosite-discord,PROXY",
  "RULE-SET,autorules-geosite-telegram,PROXY",
  "RULE-SET,autorules-geosite-meta,PROXY",
  "RULE-SET,autorules-geosite-twitter,PROXY",
  "RULE-SET,autorules-geoip-cloudflare,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-cloudfront,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-fastly,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-facebook,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-telegram,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-twitter,PROXY,no-resolve",
  "RULE-SET,autorules-geosite-ru-blocked,PROXY",
  "RULE-SET,autorules-geoip-ru-blocked,PROXY,no-resolve",
  "RULE-SET,autorules-geoip-re-filter,PROXY,no-resolve",
  "MATCH,DIRECT"
];
  return config;
}
