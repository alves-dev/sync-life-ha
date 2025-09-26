# Integração 'sync life' com o Home Assistant

### configuration.yaml

```yaml
synclife:
  nutrition:
    supplement:
      values:
        - person: person.dev
          supplement: creatina
        - person: person.dev
          supplement: whey
        - person: person.segundo_junior
          supplement: remedio x
    liquid:
      values:
        - name: Água
          healthy: true
        - name: Café
          healthy: false
      goals:
        - name: 'Daily Healthy Liquid'
          person: person.dev
          value: 3000
  sleep_tracking:
    persons:
      - person.igor_moreira
```
### Chaves:
- `nutrition`:
  - `supplement`:
    - `values`: Pessoas x suplemento que vou gerar sensores para nutrição
  - `liquid`:
    - `values`: Liquidos disponiveis para ingestão e se são ou não saudaveis
    - `goals`: Metas, vira um sensor para a pessoa
- `sleep_tracking`:
  - `persons`: Pessoas onde vai gerar sensor para mapeamento de sono
