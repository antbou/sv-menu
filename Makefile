.PHONY: run requirements build shiv ci clean

run:
	poetry run sv-menu

run-args:
	poetry run sv-menu $(ARGS)

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

shiv:
	shiv -c sv-menu -o sv-menu.pyz -r requirements.txt .

ci:
	act -j build -e .github/workflows/push-tag.json

clean:
	rm -f sv-menu.pyz requirements.txt
