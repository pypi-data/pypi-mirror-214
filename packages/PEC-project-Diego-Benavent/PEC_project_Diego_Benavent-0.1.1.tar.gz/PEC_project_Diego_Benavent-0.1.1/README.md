# PEC2

This package has a custom training function (train) that trains a model base
on the titanic dataset and returns the trained model.

## How to use

```python
import joblib
from model_pipeline_pypi.model_pipeline_pypi import train

titanic_csv_path = "your/path/to/titanic.csv"

clf = train(titanic_csv=titanic_csv_path)


# Save the trained model
joblib.dump(clf, "model.joblib")
```