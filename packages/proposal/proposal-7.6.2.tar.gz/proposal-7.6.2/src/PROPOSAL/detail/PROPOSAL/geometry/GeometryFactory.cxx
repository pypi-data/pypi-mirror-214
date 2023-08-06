
#include <algorithm>
#include <memory>
#include <stdexcept>

#include "PROPOSAL/Logging.h"
#include "PROPOSAL/geometry/Geometry.h"
#include "PROPOSAL/geometry/GeometryFactory.h"
#include <nlohmann/json.hpp>

/* namespace PROPOSAL { */
/* std::shared_ptr<Geometry> CreateGeometry(Geometry_Type type) */
/* { */
/*     auto searched_geometry = Geometry_Map.find(type); */
/*     if (searched_geometry != Geometry_Map.end()) { */
/*         return searched_geometry->second; */
/*     } */
/*     throw std::invalid_argument("Geometry not found."); */
/* } */
/* } // namespace PROPOSAL */

/* namespace PROPOSAL { */
/* std::shared_ptr<Geometry> CreateGeometry(std::string name) */
/* { */
/*     std::transform(name.begin(), name.end(), name.begin(), */
/*         [](unsigned char c) { return std::tolower(c); }); */

/*     for (size_t id = 0; id < Geometry_Name.size(); ++id) { */
/*         if (name == Geometry_Name[id]) { */
/*             return CreateGeometry(static_cast<Geometry_Type>(id)); */
/*         } */
/*     } */
/*     throw std::invalid_argument("Geometry not found."); */
/* } */
/* } // namespace PROPOSAL */

namespace PROPOSAL{
std::shared_ptr<Geometry> CreateGeometry(const nlohmann::json& config){
    if (config.contains("shape")){
        std::string shape = config["shape"];
        std::transform(shape.begin(), shape.end(), shape.begin(), ::tolower);
        if (shape == "sphere") {
            return std::make_shared<Sphere>(config);
        } else if (shape == "box") {
            return std::make_shared<Box>(config);
        } else if (shape == "cylinder") {
            return std::make_shared<Cylinder>(config);
        } else {
            throw std::invalid_argument("Unknown parameter 'shape' in geometry.");
        }
    }
    else{
        throw std::invalid_argument("Geometry config file must contain a paremeter called 'shape'.");
    }
}
} //namespace PROPOSAL
