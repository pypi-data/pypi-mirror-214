#include "StochasticNoiseSimulator.hpp"

#include <gtest/gtest.h>
#include <memory>

/**
 * These tests may have to be adjusted if something about the random-number generation changes.
 */
using namespace qc::literals;

std::unique_ptr<qc::QuantumComputation> stochGetAdder4Circuit() {
    // circuit taken from https://github.com/pnnl/qasmbench
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(4);
    quantumComputation->x(0);
    quantumComputation->x(1);
    quantumComputation->h(3);
    quantumComputation->x(3, 2_pc);
    quantumComputation->t(0);
    quantumComputation->t(1);
    quantumComputation->t(2);
    quantumComputation->tdag(3);
    quantumComputation->x(1, 0_pc);
    quantumComputation->x(3, 2_pc);
    quantumComputation->x(0, 3_pc);
    quantumComputation->x(2, 1_pc);
    quantumComputation->x(1, 0_pc);
    quantumComputation->x(3, 2_pc);
    quantumComputation->tdag(0);
    quantumComputation->tdag(1);
    quantumComputation->tdag(2);
    quantumComputation->t(3);
    quantumComputation->x(1, 0_pc);
    quantumComputation->x(3, 2_pc);
    quantumComputation->s(3);
    quantumComputation->x(0, 3_pc);
    quantumComputation->h(3);
    return quantumComputation;
}

TEST(StochNoiseSimTest, SingleOneQubitGateOnTwoQubitCircuit) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->x(0);
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ASSERT_EQ(ddsim.getNumberOfOps(), 1);

    ddsim.simulate(1);

    auto m = ddsim.measureAll(false);

    ASSERT_EQ("01", m);
}

TEST(StochNoiseSimTest, ClassicControlledOp) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->x(0);
    quantumComputation->measure(0, 0);
    std::unique_ptr<qc::Operation> op(new qc::StandardOperation(2, 1, qc::X));
    auto                           classicalRegister = std::pair<std::size_t, std::size_t>(0, 1);
    quantumComputation->emplace_back<qc::ClassicControlledOperation>(op, classicalRegister, 1);

    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);

    auto m = ddsim.measureAll(false);

    ASSERT_EQ("11", m);
}

TEST(StochNoiseSimTest, DestructiveMeasurementAll) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->h(0);
    quantumComputation->h(1);
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);

    const std::vector<dd::ComplexValue> vBefore = ddsim.getVector();
    ASSERT_EQ(vBefore[0], vBefore[1]);
    ASSERT_EQ(vBefore[0], vBefore[2]);
    ASSERT_EQ(vBefore[0], vBefore[3]);

    const std::string                   m      = ddsim.measureAll(true);
    const std::vector<dd::ComplexValue> vAfter = ddsim.getVector();
    const std::size_t                   i      = std::stoul(m, nullptr, 2);

    ASSERT_EQ(vAfter[i].r, 1.0);
    ASSERT_EQ(vAfter[i].i, 0.0);
}

TEST(StochNoiseSimTest, DestructiveMeasurementOne) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->h(0);
    quantumComputation->h(1);
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);

    const char                          m      = ddsim.measureOneCollapsing(0);
    const std::vector<dd::ComplexValue> vAfter = ddsim.getVector();

    if (m == '0') {
        ASSERT_EQ(vAfter[0], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[2], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[1], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[3], (dd::ComplexValue{0, 0}));
    } else if (m == '1') {
        ASSERT_EQ(vAfter[0], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[2], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[1], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[3], dd::complex_SQRT2_2);
    } else {
        FAIL() << "Measurement result not in {0,1}!";
    }
}

TEST(StochNoiseSimTest, DestructiveMeasurementOneArbitraryNormalization) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->h(0);
    quantumComputation->h(1);
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);

    std::mt19937_64 gen{}; // NOLINT(cert-msc51-cpp)

    char const m = ddsim.dd->measureOneCollapsing(ddsim.rootEdge, 0, false, gen);

    const std::vector<dd::ComplexValue> vAfter = ddsim.getVector();

    for (auto const& e: vAfter) {
        std::cout << e << " ";
    }
    std::cout << "\n";

    if (m == '0') {
        ASSERT_EQ(vAfter[0], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[2], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[1], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[3], (dd::ComplexValue{0, 0}));
    } else if (m == '1') {
        ASSERT_EQ(vAfter[0], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[2], (dd::ComplexValue{0, 0}));
        ASSERT_EQ(vAfter[1], dd::complex_SQRT2_2);
        ASSERT_EQ(vAfter[3], dd::complex_SQRT2_2);
    } else {
        FAIL() << "Measurement result not in {0,1}!";
    }
}

TEST(StochNoiseSimTest, ApproximateByFidelity) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(3);
    quantumComputation->h(0);
    quantumComputation->h(1);
    quantumComputation->x(2, {0_pc, 1_pc});
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1, 54);

    ddsim.simulate(1);

    ASSERT_EQ(ddsim.getActiveNodeCount(), 6);

    double const resultingFidelity = ddsim.approximateByFidelity(0.3, false, true);

    ASSERT_EQ(ddsim.getActiveNodeCount(), 3);
    ASSERT_DOUBLE_EQ(resultingFidelity, 0.5); //equal up to 4 ULP
}

TEST(StochNoiseSimTest, ApproximateBySampling) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(3);
    quantumComputation->h(0);
    quantumComputation->h(1);
    quantumComputation->x(2, {0_pc, 1_pc});
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);

    ASSERT_EQ(ddsim.getActiveNodeCount(), 6);

    double const resultingFidelity = ddsim.approximateBySampling(1, 0, true);

    ASSERT_EQ(ddsim.getActiveNodeCount(), 3);
    ASSERT_LE(resultingFidelity, 0.75); // the least contributing path has .25
}

TEST(StochNoiseSimTest, Reordering) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(3);
    quantumComputation->h(0);
    quantumComputation->h(1);
    quantumComputation->barrier({0, 1, 2});
    quantumComputation->x(2, {0_pc, 1_pc});

    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);
}

TEST(StochNoiseSimTest, SimulateClassicControlledOpWithError) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->x(0);
    quantumComputation->measure(0, 0);
    quantumComputation->h(0);
    std::unique_ptr<qc::Operation> op(new qc::StandardOperation(2, 1, qc::X));
    auto                           classicalRegister = std::pair<std::size_t, std::size_t>(0, 1);
    quantumComputation->emplace_back<qc::ClassicControlledOperation>(op, classicalRegister, 1);

    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.02, std::optional<double>{}, 2, 1000, std::string("0-3"), false, 1, 1);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.1;
    EXPECT_NEAR(m.find("00")->second, 0.496431, tolerance);
    EXPECT_NEAR(m.find("01")->second, 0.0224184, tolerance);
    EXPECT_NEAR(m.find("10")->second, 0.460269, tolerance);
    EXPECT_NEAR(m.find("11")->second, 0.0208816, tolerance);
}

TEST(StochNoiseSimTest, SimulateAdder4WithoutNoise) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), 1, 1);

    ddsim.simulate(1);
    auto m = ddsim.measureAll(false);
    ASSERT_EQ("1001", m);
}

TEST(StochNoiseSimTest, SimulateAdder4WithDecoherenceAndGateError) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.1, std::optional<double>{}, 2, 1000, std::string("0-16"), false, 1, 1);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.25574412296741467, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.177720207953642, tolerance);
    EXPECT_NEAR(m.find("0010")->second, 0.06386485600556026, tolerance);
    EXPECT_NEAR(m.find("0011")->second, 0.04438060064535747, tolerance);
    EXPECT_NEAR(m.find("0100")->second, 0.0898482618504159, tolerance);
    EXPECT_NEAR(m.find("0101")->second, 0.062436925904517736, tolerance);
    EXPECT_NEAR(m.find("0110")->second, 0.022981537137908348, tolerance);
    EXPECT_NEAR(m.find("0111")->second, 0.015970195341710985, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.08799481366902726, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.061149120043750206, tolerance);
    EXPECT_NEAR(m.find("1010")->second, 0.02480081309590326, tolerance);
    EXPECT_NEAR(m.find("1011")->second, 0.017234499727102268, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.03505400112419414, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.024359601507422463, tolerance);
}

TEST(StochNoiseSimTest, SimulateAdder4WithDecoherenceAndGateErrorSelectedProperties) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.1, std::optional<double>{}, 2, 1000, std::string("4,8-15"), false, 1, 1);

    auto         m         = ddsim.stochSimulate();
    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0100")->second, 0.0898482618504159, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.08799481366902726, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.061149120043750206, tolerance);
    EXPECT_NEAR(m.find("1010")->second, 0.02480081309590326, tolerance);
    EXPECT_NEAR(m.find("1011")->second, 0.017234499727102268, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.03505400112419414, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.024359601507422463, tolerance);
}

TEST(StochNoiseSimTest, SimulateRunWithBadParameters) {
    EXPECT_THROW(const StochasticNoiseSimulator ddsim(stochGetAdder4Circuit(), std::string("AP"), 0.3, std::optional<double>{}, 2, 1000, std::string("0-1000"), false, 1, 1), std::runtime_error);
    EXPECT_THROW(const StochasticNoiseSimulator ddsim(stochGetAdder4Circuit(), std::string("APK"), 0.01, std::optional<double>{}, 2, 1000, std::string("0-1000"), false, 1, 1), std::runtime_error);
}

TEST(StochNoiseSimTest, SimulateAdder4WithDecoherenceError) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("AP"), 0.01, std::optional<double>{}, 2, 1000, std::string("0-1000"), false, 1, 1);

    auto         m         = ddsim.stochSimulate();
    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.08441970960811902, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.0791112059351237, tolerance);
    EXPECT_NEAR(m.find("0100")->second, 0.016558289691361448, tolerance);
    EXPECT_NEAR(m.find("0101")->second, 0.016171421345261474, tolerance);
    EXPECT_NEAR(m.find("0110")->second, 0.02212697987399219, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.17460882977464234, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.5375349142994105, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.014249759740682603, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.01403353315543664, tolerance);
    EXPECT_NEAR(m.find("1110")->second, 0.01885716876841646, tolerance);
}

TEST(StochNoiseSimTest, SimulateAdder4WithDepolarizationError) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("D"), 0.01, std::optional<double>{}, 2, 1000, std::string("0-1000"), false, 1, 1);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.03323287049319544, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.03284348575778577, tolerance);
    EXPECT_NEAR(m.find("0010")->second, 0.01296430657356062, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.06839382801894367, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.7370101351171158, tolerance);
    EXPECT_NEAR(m.find("1010")->second, 0.010781280290814215, tolerance);
    EXPECT_NEAR(m.find("1011")->second, 0.02750867476569656, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.011706168989804651, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.01863469254111994, tolerance);
    EXPECT_NEAR(m.find("1110")->second, 0.016008233100915176, tolerance);
}

TEST(StochNoiseSimTest, SimulateAdder4WithNoiseAndApproximation) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.01, std::optional<double>{}, 2, 1000, std::string("-2-1000"), false, 1, 0.9);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.09693321927412533, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.09078880415385877, tolerance);
    EXPECT_NEAR(m.find("0010")->second, 0.01414096609854787, tolerance);
    EXPECT_NEAR(m.find("0100")->second, 0.02382034755245074, tolerance);
    EXPECT_NEAR(m.find("0101")->second, 0.023509799001774703, tolerance);
    EXPECT_NEAR(m.find("0110")->second, 0.02445760874001203, tolerance);
    EXPECT_NEAR(m.find("0111")->second, 0.011628281127642115, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.1731941264570172, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.41458550719988047, tolerance);
    EXPECT_NEAR(m.find("1010")->second, 0.013806211321349706, tolerance);
    EXPECT_NEAR(m.find("1011")->second, 0.01840334820660922, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.024245433691737584, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.026277984479993615, tolerance);
    EXPECT_NEAR(m.find("1110")->second, 0.023929692098939092, tolerance);
    EXPECT_NEAR(m.find("1111")->second, 0.011037316662706232, tolerance);

    EXPECT_GT(std::stoi(ddsim.additionalStatistics().at("approximation_runs")), 0);
}

TEST(StochNoiseSimTest, SimulateAdder4WithDecoherenceAndGateErrorUnoptimizedSim) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.1, std::optional<double>{}, 2, 1000, std::string("0-16"), true, 1, 1);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.25574412296741467, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.177720207953642, tolerance);
    EXPECT_NEAR(m.find("0010")->second, 0.06386485600556026, tolerance);
    EXPECT_NEAR(m.find("0011")->second, 0.04438060064535747, tolerance);
    EXPECT_NEAR(m.find("0100")->second, 0.0898482618504159, tolerance);
    EXPECT_NEAR(m.find("0101")->second, 0.062436925904517736, tolerance);
    EXPECT_NEAR(m.find("0110")->second, 0.022981537137908348, tolerance);
    EXPECT_NEAR(m.find("0111")->second, 0.015970195341710985, tolerance);
    EXPECT_NEAR(m.find("1000")->second, 0.08799481366902726, tolerance);
    EXPECT_NEAR(m.find("1001")->second, 0.061149120043750206, tolerance);
    EXPECT_NEAR(m.find("1010")->second, 0.02480081309590326, tolerance);
    EXPECT_NEAR(m.find("1011")->second, 0.017234499727102268, tolerance);
    EXPECT_NEAR(m.find("1100")->second, 0.03505400112419414, tolerance);
    EXPECT_NEAR(m.find("1101")->second, 0.024359601507422463, tolerance);

    auto tmp0 = ddsim.getSeed();
    EXPECT_EQ(ddsim.getMaxMatrixNodeCount(), 0);
    EXPECT_EQ(ddsim.getMatrixActiveNodeCount(), 0);
    EXPECT_EQ(ddsim.countNodesFromRoot(), 0);
    auto statistics = ddsim.additionalStatistics();
    EXPECT_NEAR(m.find("1101")->second, 0.024359601507422463, tolerance);

    EXPECT_EQ(std::stoi(ddsim.additionalStatistics().at("approximation_runs")), 0);

    EXPECT_NE(statistics.find("step_fidelity"), statistics.end());
    EXPECT_NE(statistics.find("approximation_runs"), statistics.end());
    EXPECT_NE(statistics.find("perfect_run_time"), statistics.end());
    EXPECT_NE(statistics.find("mean_stoch_run_time"), statistics.end());
    EXPECT_NE(statistics.find("stoch_wall_time"), statistics.end());
    EXPECT_NE(statistics.find("parallel_instances"), statistics.end());
}

TEST(StochNoiseSimTest, ParseProperties) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.1, std::optional<double>{}, 2, 1000, std::string("0, 6, 1"), false, 1, 1);
    auto                     m = ddsim.stochSimulate();

    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("0000")->second, 0.25574412296741467, tolerance);
    EXPECT_NEAR(m.find("0110")->second, 0.022981537137908348, tolerance);
    EXPECT_NEAR(m.find("0001")->second, 0.177720207953642, tolerance);

    EXPECT_EQ(m.size(), 3);
}

TEST(StochNoiseSimTest, TestingBarrierGate) {
    auto quantumComputation = std::make_unique<qc::QuantumComputation>(2);
    quantumComputation->x(0);
    quantumComputation->h(1);
    quantumComputation->t(1);
    quantumComputation->barrier({0, 1});
    quantumComputation->h(1);
    quantumComputation->h(0);
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0.02, std::optional<double>{}, 2, 1000, std::string("0-3, 23, 444, 2"), false, 1, 1);

    auto m = ddsim.stochSimulate();

    double const tolerance = 0.01;
    EXPECT_NEAR(m.find("00")->second, 0.4168386766289282, tolerance);
    EXPECT_NEAR(m.find("01")->second, 0.102761323371072, tolerance);
    EXPECT_NEAR(m.find("10")->second, 0.3853912629956448, tolerance);
    EXPECT_NEAR(m.find("11")->second, 0.09500873700435522, tolerance);
}

TEST(StochNoiseSimTest, TestingWithErrorProbZero) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string("APD"), 0, std::optional<double>{}, 2, 1000, std::string("0-15"), false, 1, 1);

    auto         m         = ddsim.stochSimulate();
    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("1001")->second, 1, tolerance);
    EXPECT_EQ(m.size(), 3);
}

TEST(StochNoiseSimTest, TestingWithEmpthyNoiseTypes) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string(""), 0.1, std::optional<double>{}, 2, 1000, std::string("0-15"), false, 1, 1);

    auto         m         = ddsim.stochSimulate();
    double const tolerance = 0.1;

    EXPECT_NEAR(m.find("1001")->second, 1, tolerance);
    EXPECT_EQ(m.size(), 3);
}

TEST(StochNoiseSimTest, TestingSimulatorFunctionality) {
    auto                     quantumComputation = stochGetAdder4Circuit();
    StochasticNoiseSimulator ddsim(std::move(quantumComputation), std::string(""), 0.1, std::optional<double>{}, 2, 1000, std::string("0-15"), false, 1, 1);

    auto m = ddsim.stochSimulate();

    EXPECT_EQ(ddsim.getNumberOfQubits(), 4);
    EXPECT_EQ(ddsim.getActiveNodeCount(), 0);
    EXPECT_EQ(ddsim.getMaxNodeCount(), 0);
    EXPECT_EQ(ddsim.getMaxMatrixNodeCount(), 0);
    EXPECT_EQ(ddsim.getMatrixActiveNodeCount(), 0);
    EXPECT_EQ(ddsim.countNodesFromRoot(), 0);
    std::cout << ddsim.getName() << "\n";
}
