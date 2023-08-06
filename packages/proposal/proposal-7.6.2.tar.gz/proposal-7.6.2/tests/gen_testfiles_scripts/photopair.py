import os
import proposal as pp
import numpy as np

particle_defs = [
    pp.particle.GammaDef(),
]

mediums = [
    pp.medium.Air(),
    pp.medium.Ice(),
    pp.medium.Uranium()
]

multiplier = 1.

params = [
    pp.parametrization.photopair.Tsai,
    pp.parametrization.photopair.KochMotz
]

lpms = [0, 1]

density_corrections = [1., 2.]

energies = np.logspace(1, 13, num=13)


def create_tables(dir_name, **kwargs):

    pp.RandomGenerator.get().set_seed(1234)

    buf = {}

    for key in kwargs:
        if key == "dNdx" and kwargs[key] is True:
            f_dNdx = open(dir_name + "PhotoPair_dNdx.txt", "w")
            buf["dNdx"] = [f_dNdx, [""]]

    for particle in particle_defs:
        for medium in mediums:
            for param in params:
                for lpm in lpms:
                    for density_correction in density_corrections:
                        args = {
                            "parametrization": param(lpm, particle, medium, density_correction),
                            "particle_def": particle,
                            "target": medium,
                            "cuts": None,
                            "interpolate": False
                        }

                        xsection = pp.crosssection.make_crosssection(**args)

                        for key in buf:
                            buf[key][1] = [""]

                            for energy in energies:
                                if key == "dNdx":
                                    result = [str(xsection.calculate_dNdx(energy))]

                                buf[key][1].append(particle.name)
                                buf[key][1].append(medium.name)
                                buf[key][1].append(str(multiplier))
                                buf[key][1].append(str(lpm))
                                buf[key][1].append(str(density_correction))
                                buf[key][1].append(str(energy))
                                buf[key][1].append(xsection.param_name)
                                buf[key][1].extend(result)
                                buf[key][1].append("\n")

                            buf[key][0].write("\t".join(buf[key][1]))


def main(dir_name):
    create_tables(dir_name, dNdx=True, stoch=True)

if __name__ == "__main__":

    dir_name = "TestFiles/"

    if os.path.isdir(dir_name):
        print("Directory {} already exists".format(dir_name))
    else:
        os.makedirs(dir_name)
        print("Directory {} created".format(dir_name))

    main(dir_name)
