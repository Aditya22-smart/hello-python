from pycaret.classification import *
from pycaret.datasets import get_data
iris = get_data('iris')
exp = setup(iris, target='species', session_id=42, silent=True, html=False)
model = compare_models()
final = finalize_model(model)
save_model(final, 'iris_model')
