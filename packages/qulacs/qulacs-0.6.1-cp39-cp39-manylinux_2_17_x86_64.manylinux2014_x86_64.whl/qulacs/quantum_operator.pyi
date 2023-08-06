from typing import Tuple

import qulacs_core

def create_quantum_operator_from_openfermion_file(
    arg0: str,
) -> qulacs_core.GeneralQuantumOperator: ...
def create_quantum_operator_from_openfermion_text(
    arg0: str,
) -> qulacs_core.GeneralQuantumOperator: ...
def create_split_quantum_operator(
    arg0: str,
) -> Tuple[qulacs_core.GeneralQuantumOperator, qulacs_core.GeneralQuantumOperator]: ...
def from_json(json: str) -> qulacs_core.GeneralQuantumOperator: ...
