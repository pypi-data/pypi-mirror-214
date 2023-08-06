
#pragma once

#include "PROPOSAL/secondaries/parametrization/ionization/Ionization.h"

namespace PROPOSAL {
namespace secondaries {
    struct NaivIonization : public secondaries::Ionization,
                            public DefaultSecondaries<NaivIonization> {
        int primary_particle_type;
        double primary_particle_mass;

        static constexpr int n_rnd = 1;

        NaivIonization(const ParticleDef& p, const Medium&)
            : primary_particle_type(p.particle_type),
              primary_particle_mass(p.mass)
        {
        }

        std::tuple<Cartesian3D, Cartesian3D> CalculateDirections(
            const Vector3D&, double, double, double) final;
        std::tuple<double, double> CalculateEnergy(double, double) final;

        size_t RequiredRandomNumbers() const noexcept final { return n_rnd; }
        std::vector<ParticleState> CalculateSecondaries(
            StochasticLoss, const Component&, std::vector<double>&) final;
    };
} // namespace secondaries
} // namespace PROPOSAL
