# Integração 'sync life' com o Home Assistant

### configuration.yaml

```yaml
synclife:
  nutrition:
    values:
      - person: person.dev
        supplement: creatina
      - person: person.dev
        supplement: whey
      - person: person.segundo_junior
        supplement: remedio x
  sleep_tracking:
    persons:
      - person.igor_moreira
```

- `synclife.nutrition.values`: Pessoas x suplemento que vou gerar sensores para nutrição
- `synclife.sleep_tracking.persons`: Pessoas que var gerar sensor para mapeamento de sono