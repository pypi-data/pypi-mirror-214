
/******************************************************************************
 *                                                                            *
 * This file is part of the simulation tool PROPOSAL.                         *
 *                                                                            *
 * Copyright (C) 2017 TU Dortmund University, Department of Physics,          *
 *                    Chair Experimental Physics 5b                           *
 *                                                                            *
 * This software may be modified and distributed under the terms of a         *
 * modified GNU Lesser General Public Licence version 3 (LGPL),               *
 * copied verbatim in the file "LICENSE".                                     *
 *                                                                            *
 * Modifcations to the LGPL License:                                          *
 *                                                                            *
 *      1. The user shall acknowledge the use of PROPOSAL by citing the       *
 *         following reference:                                               *
 *                                                                            *
 *         J.H. Koehne et al.  Comput.Phys.Commun. 184 (2013) 2070-2090 DOI:  *
 *         10.1016/j.cpc.2013.04.001                                          *
 *                                                                            *
 *      2. The user should report any bugs/errors or improvments to the       *
 *         current maintainer of PROPOSAL or open an issue on the             *
 *         GitHub webpage                                                     *
 *                                                                            *
 *         "https://github.com/tudo-astroparticlephysics/PROPOSAL"            *
 *                                                                            *
 ******************************************************************************/

#pragma once

#include "PROPOSAL/crosssection/parametrization/Photonuclear.h"
#include <memory>
#include <unordered_map>

#define PHOTO_PARAM_REAL_DEC(param)                                            \
    class Photo##param : public PhotoRealPhotonAssumption {                    \
    public:                                                                    \
        Photo##param(bool hard_component);                                     \
        using base_param_t = Photonuclear;                                     \
                                                                               \
        std::unique_ptr<Parametrization<Component>> clone() const override;    \
                                                                               \
    };                                                                         \
                                                                               \
    template <> struct ParametrizationName<Photo##param> {                     \
        static constexpr auto value = #param;                                  \
    };                                                                         \
                                                                               \
    template <> struct ParametrizationId<Photo##param> {                       \
        static constexpr size_t value = 1000000005;                            \
    };

namespace PROPOSAL {
namespace crosssection {
    class Photoproduction;
    class PhotoRealPhotonAssumption : public Photonuclear {
        using realphoton_ptr = std::shared_ptr<RealPhoton>;

    protected:
        bool hard_component_;
        std::shared_ptr<crosssection::Photoproduction> photon_param_;
        std::unordered_map<size_t, realphoton_ptr> hard_component_map;

    public:
        PhotoRealPhotonAssumption(bool hard_component, std::shared_ptr<crosssection::Photoproduction> photon_param);
        virtual ~PhotoRealPhotonAssumption() = default;

        virtual double DifferentialCrossSection(const ParticleDef&,
            const Component&, double energy, double v) const;

        double CalculateParametrization(const Component&, double) const;
    };

    PHOTO_PARAM_REAL_DEC(Zeus)
    PHOTO_PARAM_REAL_DEC(BezrukovBugaev)
    PHOTO_PARAM_REAL_DEC(Kokoulin)
    PHOTO_PARAM_REAL_DEC(Rhode)

} // namespace crosssection
} // namespace PROPOSAL

#undef PHOTO_PARAM_REAL_DEC
