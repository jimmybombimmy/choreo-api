hw:
	@echo "Hello Choreo World!"

seed-db:
	uv run -m app.seed.seed

test:
	uv run pytest test/

test-unit:
	uv run pytest test/unit --cov=app --cov-report=term-missing

test-int:
	uv run -m app.seed.seed
	uv run pytest -m integration