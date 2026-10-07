hw:
	@echo "Hello Choreo World!"

seed-db:
	uv run -m app.scripts.seed.seed

test-unit:
	uv run pytest test/unit --cov=app --cov-report=term-missing

test-int:
	uv run -m app.scripts.seed.seed
	uv run pytest -m integration