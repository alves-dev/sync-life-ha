# Integração 'sync life' com o Home Assistant

### configuration.yaml

```yaml
synclife:
  nutrition:
    persons:
      - person.dev
      - person.igor_moreira
  sleep_tracking:
    persons:
      - person.igor_moreira
```

- `synclife.nutrition.persons`: Pessoas que vou gerar sensores para nutrição
- `synclife.sleep_tracking.persons`: Pessoas que var gerar sensor para mapeamento de sono