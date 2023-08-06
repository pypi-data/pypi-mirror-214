
#include "gtest/gtest.h"
#include <cmath>

#include "PROPOSAL/Constants.h"
#include "PROPOSAL/particle/Particle.h"
#include "PROPOSAL/math/Cartesian3D.h"
#include "PROPOSAL/math/Spherical3D.h"

using namespace PROPOSAL;

Cartesian3D position(1., 1., 1.);
Spherical3D direction(0., 0., 0.);

TEST(Comparison, Comparison_equal)
{
    direction.SetCoordinates({1, 20 * PI / 180., 20 * PI / 180.});

    ParticleState A;
    ParticleState B;
    EXPECT_TRUE(A == B);

    ParticleState* C = new ParticleState();
    C->position = position;
    C->direction = direction;
    ParticleState* D = new ParticleState();
    D->position = position;
    D->direction = direction;

    C->energy = 1e6;
    D->energy = 1e6;
    EXPECT_TRUE(*C == *D);

    position    = Cartesian3D();
    direction   = Cartesian3D();
    ParticleState* E = new ParticleState();
    E->position = position;
    E->direction = direction;
    EXPECT_TRUE(A == *E);
}

TEST(Comparison, Comparison_not_equal)
{
    direction.SetCoordinates({1, 20 * PI / 180., 20 * PI / 180.});

    ParticleState A;
    ParticleState B;
    A.SetType(ParticleType::EMinus);
    B.SetType(ParticleType::MuMinus);
    EXPECT_TRUE(A != B);

    ParticleState* C = new ParticleState();
    C->position = position;
    C->direction = direction;
    ParticleState* D = new ParticleState();

    D->position = position;
    D->direction = direction;
    D->energy = 1e6;
    EXPECT_TRUE(*C != *D);
}

TEST(Assignment, Copyconstructor)
{
    ParticleState A;
    ParticleState B = A;

    EXPECT_TRUE(A == B);
}

TEST(Assignment, Copyconstructor2)
{
    direction.SetCoordinates({1, 20 * PI / 180., 20 * PI / 180.});
    ParticleState A;
    A.SetType(ParticleType::TauMinus);
    A.position = position;
    A.direction = direction;
    ParticleState B(A);

    EXPECT_TRUE(A == B);
}

TEST(ParticleState, MomentumCalculation)
{
     MuMinusDef p_def;
     double energy = 1e3;
     ParticleState state;
     state.type = p_def.particle_type;
     state.energy = energy;

    EXPECT_NEAR(state.GetMomentum(),
                std::sqrt(energy * energy - p_def.mass * p_def.mass),
                COMPUTER_PRECISION);

    // check that momentum is calculated correctly for custom particle
    auto p_def_custom = ParticleDef::Builder().SetParticleDef(p_def).SetParticleType(99).SetMass(200).build();
    ParticleState state_custom;
    state_custom.type = p_def_custom.particle_type;
    state_custom.energy = energy;

    EXPECT_NEAR(state_custom.GetMomentum(),
                std::sqrt(energy * energy - p_def_custom.mass * p_def_custom.mass),
                COMPUTER_PRECISION);


}

int main(int argc, char** argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
