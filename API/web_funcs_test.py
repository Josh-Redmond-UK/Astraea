from src.utils import *

ee.Initialize()



def test_coord_parse():
    testApiString = '-0.115177,51.521916,-0.141263,51.504393,-0.102477,51.490283,-0.05288,51.504393,-0.037262,51.523732,-0.115177,51.521916'
    test_geom_random = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.eq('ADM2_NAME', 'Greater London')).first().geometry()
    assert type(coordsToROI(testApiString)) == type(test_geom_random)


def test_coord_parse_2():
    testApiString = '-0.115177,51.521916,-0.141263,51.504393,-0.102477,51.490283,-0.05288,51.504393,-0.037262,51.523732,-0.115177,51.521916'
    test_geom_random = ee.FeatureCollection('FAO/GAUL/2015/level2').filter(ee.Filter.eq('ADM2_NAME', 'Greater London')).first().geometry()
    coordsToROI(testApiString).getInfo()


def test_geocode():
    assert type(reverse_geocode_area(-21, 11)) == type("string")


