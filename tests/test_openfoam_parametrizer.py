from src.openfoam_parametrizer import dictionary

dictionary['cylinder_names'] = ['cylinder0', 'outerCylinder']
dictionary['cylinders_intersecting_propeller'] = ['cylinder0']


def test_searchable_surface_list():
    dictionary["cylinder_names"] = [
        "cylinder0",
        "cylinder1",
        "cylinder2",
        "outerCylinder",
    ]

    assert dictionary['searchable_surface_list'] == """    cylinder0
    {
        type        triSurfaceMesh;
        file        "cylinder0.obj";
        regions
        {
            cylinder0
            {
                 name       cylinder0;
            }
        }
    }
    cylinder1
    {
        type        triSurfaceMesh;
        file        "cylinder1.obj";
        regions
        {
            cylinder1
            {
                 name       cylinder1;
            }
        }
    }
    cylinder2
    {
        type        triSurfaceMesh;
        file        "cylinder2.obj";
        regions
        {
            cylinder2
            {
                 name       cylinder2;
            }
        }
    }"""
