# Locaya

> Simple i18n system written in pure Python

```python
from locaya import Locaya


locaya = Locaya()
locaya.loader()

localization = locaya.get("localization")
localized_string = localization("key")
```