.PHONY: test run

test:
	uv run python -m pytest -v

dev:
	uv run python -m fastapi dev

run:
	uv run python -m fastapi run
