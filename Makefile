.default: build
build:
	rm -rf dist
	mkdir dist
	cp index.html index.js index.py pyscript.toml dist/
	@if [ -z "${API_KEY}" ]; then exit 1; fi
	python -c "import sys; lines = sys.stdin.read(); print(lines.replace('os.environ[\"API_KEY\"]','\"${API_KEY}\"'))" <dist/index.py >dist/tmpindex.py
	mv dist/tmpindex.py dist/index.py
	poetry build --format wheel
	ls dist/geodecoder-0-py3-none-any.whl

.PHONY: watch
watch:
	watchfiles make --ignore-paths dist