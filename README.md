# Installation et Execution

## 1. Créer un environnement virtuel
> python -m venv venv

## 2. Activer l'environnement
> venv\Scripts\activate.bat

## 3. Installer les dépendances
> pip install -r requirements.txt

## 4. Executer allure-pytest
> py.test --alluredir=results .\main.py --browser-type=chrome

## 5. Lancer un serveur allure pour voir les résultats
> allure serve results

# Quelques fonctionnalités de pytest
## Fixture scope
Spécifier module en tant que scope dans le décorateur de fixture permet de faire
un équivalent au tearDownClass de unittest.
> @pytest.fixture(scope='module')

## Markers
### Passer des paramètres à une fonction fixture
Ici, je spécifie les paramètres à passer à la fixture connect en les mettant dans un dictionnaire. 
```python
@pytest.mark.parametrize('connect', [{'email': 'CRM@gmail.com', 'psw': 'password'}], indirect=True)
def test_function(connect) -> None:
    ...
```

On peut ainsi les récupérer à l'intérieur de la fixture connect avec `request.param[...]`
```python
@pytest.fixture()
def connect(request) -> None:
    print(request.param['email'])
    print(request.param['psw'])
```

### Pytest Configuration
Le décorateur `@pytest.mark` nous permet également de taguer nos tests.  

`@pytest.mark.regression`

```
// fichier pytest.ini
[pytest]
markers =
    regression: Tests de regression
```
Avec l'option -m de pytest, on peut choisir d'exécuter seulement les tests taguer avec les markers de notre choix.  
> py.test --alluredir=results .\main.py --browser-type=chrome -m regression

## Hooks
En utilisant un hook, on peut récupérer le résultat de chacun de nos tests.  
Ici, on récupère notre driver puis on crée un screenshot que l'on attache à allure.  
```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        if 'browser' in item.fixturenames:
            web_driver = item.funcargs['browser']
        else:
            print('Failed to find web driver')
            return

        # Attach a screenshot if a test failed
        allure.attach(
            web_driver.get_screenshot_as_png(),
            name='screenshot',
            attachment_type=allure.attachment_type.PNG
        )
```
