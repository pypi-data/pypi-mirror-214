import os
import proposal as pp
import numpy as np

parametrizations = [
    pp.parametrization.compton.KleinNishina(),
]

mediums = [
    pp.medium.Ice(),
    pp.medium.Hydrogen(),
    pp.medium.Uranium()
]

particle = pp.particle.GammaDef()

cuts = [
    pp.EnergyCutSettings(np.inf, 1),
    pp.EnergyCutSettings(500, 1),
    pp.EnergyCutSettings(np.inf, 0.05),
    pp.EnergyCutSettings(500, 0.05)
]

multiplier = 1.

energies = np.logspace(4, 13, num=10)


def create_tables(dir_name, **kwargs):

    pp.RandomGenerator.get().set_seed(1234)

    buf = {}

    for key in kwargs:
        if key == "dEdx" and kwargs[key] is True:
            f_dNdx = open(dir_name + "Compton_dEdx.txt", "w")
            buf["dEdx"] = [f_dNdx, [""]]
        if key == "dNdx" and kwargs[key] is True:
            f_dNdx = open(dir_name + "Compton_dNdx.txt", "w")
            buf["dNdx"] = [f_dNdx, [""]]
        if key == "stoch" and kwargs[key] is True:
            f_stoch = open(dir_name + "Compton_e.txt", "w")
            buf["stoch"] = [f_stoch, [""]]

    for medium in mediums:
        for cut in cuts:
            for parametrization in parametrizations:
                args = {
                    "parametrization": parametrization,
                    "particle_def": particle,
                    "target": medium,
                    "cuts": cut,
                    "interpolate": False
                }

                xsection = pp.crosssection.make_crosssection(**args)

                for key in buf:
                    buf[key][1] = [""]

                    for energy in energies:
                        if key == "dEdx":
                            result = [str(xsection.calculate_dEdx(energy))]
                        if key == "dNdx":
                            result = [str(xsection.calculate_dNdx(energy))]
                        if key == "stoch":
                            rnd1 = pp.RandomGenerator.get().random_double()
                            rnd2 = pp.RandomGenerator.get().random_double()

                            components = medium.components
                            comp = components[int(rnd2*len(components))]
                            dNdx_for_comp = xsection.calculate_dNdx(energy, comp.hash);

                            if np.isfinite(cut.ecut) or cut.vcut < 1:
                                result = xsection.calculate_stochastic_loss(
                                    comp.hash, energy, rnd1*dNdx_for_comp)
                            else:
                                result = 0
                            result = [str(rnd1), str(rnd2), str(result)]


                        buf[key][1].append(medium.name)
                        buf[key][1].append(str(cut.ecut))
                        buf[key][1].append(str(cut.vcut))
                        buf[key][1].append(str(multiplier))
                        buf[key][1].append(str(energy))
                        buf[key][1].extend(result)
                        buf[key][1].append(xsection.param_name)
                        buf[key][1].append("\n")

                    buf[key][0].write("\t".join(buf[key][1]))


def main(dir_name):
    create_tables(dir_name, dEdx=True, dNdx=True, stoch=True)

if __name__ == "__main__":

    dir_name = "TestFiles/"

    if os.path.isdir(dir_name):
        print("Directory {} already exists".format(dir_name))
    else:
        os.makedirs(dir_name)
        print("Directory {} created".format(dir_name))

    main(dir_name)
