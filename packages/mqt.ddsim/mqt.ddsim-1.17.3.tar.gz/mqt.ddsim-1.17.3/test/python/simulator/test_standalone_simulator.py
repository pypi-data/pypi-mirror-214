import pathlib
import unittest

from qiskit import QuantumCircuit

from mqt import ddsim


class MQTStandaloneSimulatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.nonzero_states_ghz = 2

    def test_truly_standalone(self):
        filename = str(pathlib.Path(__file__).with_name("ghz_03.qasm").absolute())
        sim = ddsim.CircuitSimulator(filename)
        result = sim.simulate(1000)
        print(result)
        assert len(result.keys()) == self.nonzero_states_ghz
        assert "000" in result
        assert "111" in result

    def test_standalone(self):
        circ = QuantumCircuit(3)
        circ.h(0)
        circ.cx(0, 1)
        circ.cx(0, 2)

        sim = ddsim.CircuitSimulator(circ)
        result = sim.simulate(1000)
        assert len(result.keys()) == self.nonzero_states_ghz
        assert "000" in result
        assert "111" in result

    def test_standalone_with_seed(self):
        circ = QuantumCircuit(3)
        circ.h(0)
        circ.cx(0, 1)
        circ.cx(0, 2)

        sim = ddsim.CircuitSimulator(circ, seed=1337)
        result = sim.simulate(1000)
        assert len(result.keys()) == self.nonzero_states_ghz
        assert "000" in result
        assert "111" in result

    def test_standalone_simple_approximation(self):
        import numpy as np

        # creates a state with <2% probability of measuring |1x>
        circ = QuantumCircuit(2)
        circ.h(0)
        circ.cry(np.pi / 8, 0, 1)
        circ.i(0)
        circ.i(0)

        # create a simulator that approximates once and by at most 2%
        sim = ddsim.CircuitSimulator(circ, approximation_step_fidelity=0.98, approximation_steps=1)
        result = sim.simulate(4096)

        # the result should always be 0
        assert len(result.keys()) == self.nonzero_states_ghz
        assert "00" in result
        assert "01" in result

    @staticmethod
    def test_native_two_qubit_gates():
        from qiskit.circuit.library import XXMinusYYGate, XXPlusYYGate

        qc = QuantumCircuit(2)
        qc.dcx(0, 1)
        qc.ecr(0, 1)
        qc.rxx(0.5, 0, 1)
        qc.rzz(0.5, 0, 1)
        qc.ryy(0.5, 0, 1)
        qc.rzx(0.5, 0, 1)
        qc.append(XXMinusYYGate(0.5, 0.25), [0, 1])
        qc.append(XXPlusYYGate(0.5, 0.25), [0, 1])
        print(qc)
        print(qc.global_phase)
        sim = ddsim.CircuitSimulator(qc)
        result = sim.simulate(1000)
        print(result)

    @staticmethod
    def test_expectation_value_local_operators():
        import numpy as np

        max_qubits = 3
        for qubits in range(1, max_qubits + 1):
            qc = QuantumCircuit(qubits)
            sim = ddsim.CircuitSimulator(qc)
            for i in range(qubits):
                x_observable = QuantumCircuit(qubits)
                x_observable.x(i)
                assert sim.expectation_value(x_observable) == 0
                z_observable = QuantumCircuit(qubits)
                z_observable.z(i)
                assert sim.expectation_value(z_observable) == 1
                h_observable = QuantumCircuit(qubits)
                h_observable.h(i)
                assert np.allclose(sim.expectation_value(h_observable), 1 / np.sqrt(2))

    @staticmethod
    def test_expectation_value_global_operators():
        import numpy as np

        max_qubits = 3
        for qubits in range(1, max_qubits + 1):
            qc = QuantumCircuit(qubits)
            sim = ddsim.CircuitSimulator(qc)
            x_observable = QuantumCircuit(qubits)
            z_observable = QuantumCircuit(qubits)
            h_observable = QuantumCircuit(qubits)
            for i in range(qubits):
                x_observable.x(i)
                z_observable.z(i)
                h_observable.h(i)
            assert sim.expectation_value(x_observable) == 0
            assert sim.expectation_value(z_observable) == 1
            assert np.allclose(sim.expectation_value(h_observable), (1 / np.sqrt(2)) ** qubits)
