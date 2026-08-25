load:
	python src/etl/loader.py

validate:
	python src/etl/validator.py

clean:
	del nifty100.db