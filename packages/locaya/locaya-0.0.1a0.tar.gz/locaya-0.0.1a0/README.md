# Locaya

> Simple YAML-based localization system

```python
from locaya import Locaya


locaya = Locaya(strict=False)
locaya.load_file("./localization.yml")
locaya.load_directory("./localizations")

localization = locaya.get("localization")
localized_string = localization("key")
```