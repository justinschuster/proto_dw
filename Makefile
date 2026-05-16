.PHONY: sync
sync:
	uv sync --all-extras --all-packages --group dev

.PHONY: format
format: 
	uv run ruff format
	uv run ruff check --fix

.PHONY: format-check
format-check:
	uv run ruff format --check

.PHONY: lint
lint: 
	uv run ruff check

.PHONY: mypy
mypy: 
	uv run mypy . --exclude site

.PHONY: pyright
pyright:
	uv run pyright --project pyrightconfig.json

.PHONY: typecheck
typecheck:
	@set -eu; \
	mypy_pid=''; \
	pyright_pid=''; \
	trap 'test -n "$$mypy_pid" && kill $$mypy_pid 2>/dev/null || true; test -n "$$pyright_pid" && kill $$pyright_pid 2>/dev/null || true' EXIT INT TERM; \
	echo "Running make mypy and make pyright in parallel..."; \
	$(MAKE) mypy & mypy_pid=$$!; \
	$(MAKE) pyright & pyright_pid=$$!; \
	wait $$mypy_pid; \
	wait $$pyright_pid; \
	trap - EXIT

.PHONY: tests
tests:
	uv run pytest --cov --verbose

.PHONY: snapshots-fix
snapshots-fix: 
	uv run pytest --inline-snapshot=fix 

.PHONY: snapshots-create 
snapshots-create: 
	uv run pytest --inline-snapshot=create 

.PHONY: check
check: format-check lint typecheck tests

.PHONY: terraform-fmt
terraform-fmt:
	terraform -chdir=infra fmt -recursive

.PHONY: terraform-init
terraform-init:
	terraform -chdir=infra init

.PHONY: terraform-validate
terraform-validate:
	terraform -chdir=infra validate

.PHONY: terraform-check
terraform-check: terraform-fmt terraform-init terraform-validate
