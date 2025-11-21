# ru-it-audit-notebook

## English

Open-source interactive IT audit report template for Russian contexts. Jupyter notebooks and YAML checklists render into HTML/PDF reports for executives and engineers. Includes scoring profiles, inventory mapping, and safe AI-generated executive summaries.

---

## Русский

`ru-it-audit-notebook` — интерактивный шаблон ИТ-аудита, адаптированный под российские реалии (1С, ПДн/152-ФЗ, резервирование, базовые вопросы КИИ и онлайн-касс). Jupyter + YAML/Markdown превращают ответы и инвентаризацию в готовый HTML/PDF отчёт: краткое executive summary для директора и детализированный чек-лист для технарей.

### Как работает
- YAML-чек-листы и инвентаризация → ноутбуки считают баллы и формируют контекст.
- Jinja2-шаблоны рендерят markdown для руководства и технического приложения.
- nbconvert/papermill собирают HTML/PDF отчёт и артефакты.

### Кому полезно
- Внутренним DevSecOps/ИБ-командам, аудиторам и интеграторам.
- Тем, кому нужны регулярные отчёты по ПДн/152-ФЗ, резервированию, КИИ и ИТ-ландшафту.

### Быстрый старт
```bash
pip install -e .[dev]
ru-it-audit run-notebooks \
  --inventory examples/inventory/sample_inventory.csv \
  --answers-dir examples/inputs \
  --out-dir .artifacts/notebooks
ru-it-audit build-report \
  --artifacts-dir .artifacts/notebooks \
  --out-html report.html \
  --out-pdf report.pdf
```

### Профессиональные услуги – run-as-daemon.ru

Проект развивается инженером DevOps/DevSecOps с сайта [run-as-daemon.ru](https://run-as-daemon.ru).

Если вам нужно:
- провести ИТ-аудит инфраструктуры (1С, сервера, облака, резервирование);
- оценить риски по ПДн/152-ФЗ и базовым требованиям по КИИ;
- быстро и регулярно выпускать отчёты для руководства и технарей,

вы можете заказать консалтинг, аудит и сопровождение.

### Дисклеймер
Инструмент не является юридическим заключением и не заменяет формальные проверки регуляторов. Проверяйте выводы с юристами и ответственными за ИБ.
