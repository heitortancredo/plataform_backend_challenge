# DC PLATFORM BACKEND CHALLENGE


## PART - 1 - Rate limiter

### Instalação

- Dependências: Python 3.x
- [Redis](https://redis.io/topics/quickstart) 

```bash
pip install -r requirements.txt
```

### Executando o servidor

 - Passos:
* Configure o Redis editando o arquivo "part-1/src/app/config.py" (padrao localhost)
- Excecute o servidor: 

		```bash
python run.py
```



### Testes

```bash
 pytest -vv --disable-warnings
 or
 sh run_tests.sh
```


## PART - 2 - URL Aggregator 

### Instalação

- Dependências: Python 3.5+

```bash
pip install -r requirements.txt
```

### Executando o applicativo

```bash
python app.py -i <input_dump_file> -o <output_dump_file>
```

### Testes

```bash
 pytest -vv
 or
 sh run_tests.sh
```
