# mihomo-autorules

Автоматически обновляемые rule-providers для Mihomo и готовые JavaScript
overrides для Mihomo Party / Clash Party.

Категории и профили маршрутизации берутся из единого репозитория
[`autorules`](https://github.com/x-netloc/autorules). Этот репозиторий отвечает
только за преобразование в формат Mihomo и не хранит собственную копию списков.

## Готовые профили

В Mihomo Party откройте `Overrides`, импортируйте URL скрипта, затем назначьте
его нужной подписке.

| Профиль | Маршрутизация | URL override |
| --- | --- | --- |
| `bypass-blacklist` | Заблокированное и выбранные зарубежные сервисы через `PROXY`, остальное напрямую | `https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/profiles/bypass-blacklist.js` |
| `freedom-no-ru` | Российские и локальные ресурсы напрямую, остальное через `PROXY` | `https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/profiles/freedom-no-ru.js` |
| `freedom-no-ru-no-ads` | То же самое с блокировкой рекламы | `https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/profiles/freedom-no-ru-no-ads.js` |

Override сохраняет прокси, proxy-providers, группы и остальные настройки
подписки, но заменяет `rules` выбранным профилем. Если группы `PROXY` нет, она
создаётся автоматически и включает существующие группы и доступные узлы.

## Что публикуется

Ветка [`dist`](https://github.com/x-netloc/mihomo-autorules/tree/dist)
содержит:

```text
geosite/<category>.mrs          доменные правила
geosite/<category>-extra.txt    DOMAIN-KEYWORD / DOMAIN-REGEX, если они есть
geoip/<category>.mrs            IPv4 и IPv6 сети
profiles/<profile>.js           готовые overrides
INDEX.md                        категории и количество правил
```

Домены и CIDR компилируются официальным CLI Mihomo в нативный MRS. Правила,
которые MRS выразить не может, не отбрасываются: `keyword:` и `regexp:`
публикуются отдельным provider с `behavior: classical`.

## Подключение отдельной категории

Пример доменного provider:

```yaml
rule-providers:
  ru-blocked:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/x-netloc/mihomo-autorules/dist/geosite/ru-blocked.mrs
    path: ./ruleset/autorules-geosite-ru-blocked.mrs
    interval: 3600
    proxy: PROXY

rules:
  - RULE-SET,ru-blocked,PROXY
```

Если у категории в `INDEX.md` есть classical extras, подключите также файл
`geosite/<category>-extra.txt` с `behavior: classical` и `format: text`.

## Обновления

GitHub Actions каждый час проверяет upstream, commit `autorules`, версию Mihomo
и код адаптера. При изменении любого источника ветка `dist` пересобирается, а
новые категории и профили появляются автоматически.

Форматы providers соответствуют официальной
[документации Mihomo](https://wiki.metacubex.one/en/config/rule-providers/).
