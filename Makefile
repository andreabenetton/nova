PYTHON ?= python3

.PHONY: setup contracts normalize lint matrix context boundaries contract-tests agent-instructions rust test check tree

setup:
	$(PYTHON) -m pip install --no-build-isolation -e tools/nova-contract

contracts:
	nova-contract validate contracts

normalize:
	nova-contract normalize contracts --check

lint:
	nova-contract lint contracts

matrix:
	nova-contract matrix contracts --check

context:
	nova-contract context .

boundaries:
	nova-contract boundaries canon/dependency-policy.yaml implementations/rust

contract-tests:
	$(PYTHON) -m unittest discover -s tools/nova-contract/tests

agent-instructions:
	$(PYTHON) tools/check_agent_instructions.py

rust:
	cargo fmt --all -- --check
	cargo check --workspace
	cargo clippy --workspace --all-targets

test:
	cargo test --workspace

check: contracts normalize lint matrix context boundaries contract-tests agent-instructions rust test

tree:
	find . -path './.git' -prune -o -print | sort
