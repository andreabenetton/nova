# SPDX-License-Identifier: Apache-2.0
import json
import tempfile
import unittest
from pathlib import Path

from nova_contract.cli import canonical_bytes, lint_interface, load_yaml, validate_document


class ContractToolTests(unittest.TestCase):
    def test_canonical_bytes_are_key_order_independent(self):
        left = canonical_bytes({"b": 2, "a": 1})
        right = canonical_bytes({"a": 1, "b": 2})
        self.assertEqual(left, right)
        self.assertEqual(json.loads(left), {"a": 1, "b": 2})

    def test_invalid_interface_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema = Path(__file__).resolve().parents[3] / "contracts" / "schemas" / "nidl" / "0.1" / "interface.schema.json"
            contract = root / "interface.yaml"
            contract.write_text(
                f'$schema: "{schema}"\n'
                'nidl: "0.1"\n'
                'interface:\n'
                '  id: "bad"\n'
                '  name: "Bad"\n'
                '  kind: "stratum-interface"\n'
                '  version: "0.1.0"\n'
                '  status: "experimental"\n'
                'roles:\n'
                '  provider: "A"\n'
                '  consumer: "B"\n',
                encoding="utf-8",
            )
            self.assertTrue(validate_document(contract))


    def test_strict_type_references_are_enforced(self):
        document = {
            "interface": {"id": "NOVA-IF-TEST", "version": "0.1.0"},
            "compatibility": {"type_references": "strict"},
            "types": {},
            "operations": [
                {
                    "id": 1,
                    "name": "missing",
                    "caller": "consumer",
                    "input": "MissingRequest",
                }
            ],
        }
        errors = lint_interface(Path("interface.yaml"), document)
        self.assertTrue(any("undeclared type MissingRequest" in error for error in errors))

    def test_repository_contract_loads(self):
        root = Path(__file__).resolve().parents[3]
        contract = root / "contracts" / "interfaces" / "p-r" / "0.1.0" / "interface.yaml"
        data = load_yaml(contract)
        self.assertEqual(data["interface"]["id"], "NOVA-IF-P-R")


if __name__ == "__main__":
    unittest.main()
