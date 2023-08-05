#include "algorithms/simulation/circuit_to_truthtable.hpp"

#include "dd/Simulation.hpp"

namespace syrec {

    auto buildTruthTable(const qc::QuantumComputation& qc, TruthTable& tt) -> void {
        const auto nBits = qc.getNqubits();

        tt.setConstants(qc.getAncillary());
        tt.setGarbage(qc.getGarbage());

        assert(nBits < 65U);

        auto dd = std::make_unique<dd::Package<>>(nBits);

        const auto totalInputs = 1U << nBits;

        std::uint64_t n = 0U;

        while (n < totalInputs) {
            const auto inCube = TruthTable::Cube::fromInteger(n, nBits);
            ++n;

            const auto boolCube  = inCube.toBoolVec();
            bool       nextInput = false;

            for (auto i = 0U; i < nBits; i++) {
                if (tt.isConstant(i) && (boolCube[i])) {
                    nextInput = true;
                    break;
                }
            }

            if (nextInput) {
                continue;
            }

            auto const inEdge    = dd->makeBasisState(static_cast<dd::QubitCount>(nBits), boolCube);
            const auto out       = dd::simulate(&qc, inEdge, dd, 1);
            const auto outString = out.begin()->first;

            tt.try_emplace(inCube, TruthTable::Cube::fromString(outString));
        }
    }

} // namespace syrec
