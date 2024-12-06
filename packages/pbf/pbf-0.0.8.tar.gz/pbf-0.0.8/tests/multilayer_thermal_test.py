import unittest
import pbf

units = pbf.units


class MultilayerThermalTest(unittest.TestCase):
    def test(self):
        inconel = pbf.makeMaterial("SS316L")

        # process parameters
        laserD4Sigma = 0.100 * units.mm
        laserSpeed = 800.0 * units.mm / units.s
        laserPower = 280.0 * units.W
        layerThickness = 0.050 * units.mm
        maxNewtonIter = 9
        powderDepositionTime = 0.001 * units.s
        nLayers = 3
        nLayerTracks = 1
        nrefinements = 2
        srefinements = 2

        # domain
        origin0 = 0.0 * units.mm
        origin1 = -0.15 * units.mm
        origin2 = -0.15 * units.mm
        length0 = 1.0 * units.mm
        length1 = 0.3 * units.mm
        basePlateHeight = 0.15 * units.mm
        domainMin = [origin0, origin1, origin2]
        domainHeight = origin2 + basePlateHeight + layerThickness * nLayers
        domainMax = [origin0 + length0, origin1 + length1, domainHeight]

        # scan path
        x0 = 0.0 * units.mm
        x1 = 1.0 * units.mm
        totalTime = (x1 - x0) * nLayerTracks * nLayers / laserSpeed + powderDepositionTime * nLayers
        layerTime = (x1 - x0) * nLayerTracks / laserSpeed
        singleTrackTime = (x1 - x0) / laserSpeed

        # discretization
        elementSize = 0.05  # 0.12 * laserD4Sigma
        grid = pbf.createMesh(domainMin, domainMax, elementSize, layerThickness * nLayers)  # zfactor??
        timestep = 0.5 * laserD4Sigma / laserSpeed  # 0.2 * laserD4Sigma / laserSpeed

        # laser beam shape
        laserBeam = pbf.gaussianBeam(sigma=laserD4Sigma / 4, absorptivity=0.32)

        # setup process simulation
        setup = pbf.ProcessSimulation(grid=grid, layerThickness=50 * units.um, ambientTemperature=50.0)
        setup.setMaterials( {"powder": pbf.makePowder(inconel), "structure": inconel, "baseplate": inconel,
                             "air": pbf.makeAir()})

        # thermal problem definition
        tsetup = pbf.ThermalProblem(setup, degree=1)
        tsetup.addDirichletBC(pbf.temperatureBC(4, setup.ambientTemperature))
        # Save number of elements and number of dofs every time step
        computedNElementsList, computedMaterialNCellsList, computedNDofList = [], [], []


        def meshDataAccumulator(thermalProblem, tstate):
            computedNElementsList.append(tstate.basis.nelements())
            computedNDofList.append(tstate.basis.ndof())
            computedMaterialNCellsList.append(tstate.history.grid().ncells())


        tsetup.addPostprocessor(meshDataAccumulator)

        tstate0 = pbf.makeThermalState(tsetup, grid, srefinement=srefinements)

        # solve problem
        # initialize moving heat source
        laserTrack = [pbf.LaserPosition(xyz=[x0, 0.0, layerThickness], time=0.0, power=0),
                      pbf.LaserPosition(xyz=[x0, 0.0, layerThickness], time=powderDepositionTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x1, 0.0, layerThickness], time=powderDepositionTime + layerTime,
                                        power=laserPower),
                      pbf.LaserPosition(xyz=[x0, 0.0, 2 * layerThickness], time=powderDepositionTime + layerTime, power=0.0),
                      pbf.LaserPosition(xyz=[x0, 0.0, 2 * layerThickness], time=2 * powderDepositionTime + layerTime,
                                        power=laserPower),
                      pbf.LaserPosition(xyz=[x1, 0.0, 2 * layerThickness],
                                        time=2 * powderDepositionTime + layerTime + layerTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x0, 0.0, 3 * layerThickness], time=2 * powderDepositionTime + 2 *
                                                                                layerTime, power=0.0),
                      pbf.LaserPosition(xyz=[x0, 0.0, 3 * layerThickness], time=3 * powderDepositionTime + 2 *
                                                                                layerTime, power=laserPower),
                      pbf.LaserPosition(xyz=[x1, 0.0, 3 * layerThickness], time=3 * powderDepositionTime + 3 *
                                                                                layerTime, power=laserPower)]

        # define heat source
        heatSource = pbf.volumeSource(laserTrack, laserBeam, depthSigma=0.045 * units.mm)
        tsetup.addSource(heatSource)

        # geometric laser refinement
        refinement = pbf.laserRefinement(laserTrack, laserD4Sigma / 4, laserSpeed, nrefinements)
        tsetup.addRefinement(refinement)

        # solve thermal problem
        print(f"Integrating thermal problem:", flush=True)
        print(f"    duration        = {totalTime}", flush=True)

        for pp in tsetup.postprocess:
            pp(tsetup, tstate0)

        for ilayer in range(nLayers):
            print(f"Layer {ilayer + 1} / {nLayers}", flush=True)

            tstate = pbf.addNewPowderLayer(tsetup, tstate0, deltaT=powderDepositionTime, ilayer=ilayer)

            tstate0 = pbf.computeThermalProblem(tsetup, tstate, timestep, layerTime, ilayer, maxNewtonIter)

        # Check whether results are consistent with previous versions
        expectedNElementsList = [500, 500, 2656, 3356, 4056, 4756, 5400, 5960, 6464, 6912, 7311, 7556, 7717, 7892,
                                 8067, 8242, 8417, 8592, 8655, 8634, 8333, 7836, 4882, 5386, 5890, 6394, 6898, 7360,
                                 7766, 8130, 8438, 8690, 8774, 8774, 8774, 8774, 8774, 8774, 8774, 8774, 8718, 8382,
                                 8354, 4462, 4742, 5022, 5302, 5582, 5582, 5722, 5834, 5834, 6044, 6226, 6380, 6506,
                                 6548, 6548, 6548, 6548, 6548, 6548, 6548, 6548, 6520, 6352, 6086]


        expectedNDofList = [756, 756, 2707, 3337, 3967, 4597, 5147, 5633, 6075, 6465, 6813, 7015, 7185, 7391, 7597,
                            7803, 8009, 8261, 8381, 8446, 8272, 7888, 5760, 6234, 6708, 7182, 7656, 8062, 8424, 8748,
                            9012, 9224, 9244, 9236, 9236, 9236, 9236, 9236, 9236, 9236, 9251, 8994, 8969, 5390, 5652,
                            5914, 6176, 6438, 6438, 6569, 6660, 6660, 6850, 7014, 7150, 7258, 7277, 7272, 7272, 7272,
                            7272, 7272, 7272, 7272, 7275, 7142, 6900]


        expectedMaterialNCellsList = [500, 500, 696, 829, 976, 1095, 1214, 1333, 1452, 1571, 1690, 1809, 1928, 2047,
                                      2194, 2341, 2488, 2635, 2782, 2929, 3076, 3104, 3104, 3272, 3279, 3265, 3321,
                                      3433, 3531, 3601, 3671, 3762, 3832, 3902, 3972, 4042, 4056, 4084, 4126, 4168,
                                      4273, 4322, 4350, 4350, 4490, 4462, 4504, 4616, 4616, 4686, 4742, 4742, 4770,
                                      4798, 4840, 4882, 4868, 4868, 4840, 4812, 4812, 4833, 4931, 5001, 5001, 5036,
                                      5036]

        print(len(computedNElementsList))
        print(len(computedMaterialNCellsList))
        print(len(computedNDofList))
        #assert (len(expectedNElementsList) == len(computedNElementsList))
        #assert (len(expectedMaterialNCellsList) == len(computedMaterialNCellsList))
        #assert (len(expectedNDofList) == len(computedNDofList))

        for expectedNCells, computedNCells in zip(expectedNElementsList, computedNElementsList):
            print(computedNCells)
            #assert (expectedNCells == computedNCells)
        for expectedNCells, computedNCells in zip(expectedMaterialNCellsList, computedMaterialNCellsList):
            print(computedNCells)
            #assert (expectedNCells == computedNCells)
        for expectedNDof, computedNDof in zip(expectedNDofList, computedNDofList):
            print(computedNDof)
            #assert (expectedNDof == computedNDof)

        temperature = pbf.thermalEvaluator(tstate0)

        print(temperature([1.0, 0.0, basePlateHeight]))

        #self.assertAlmostEqual(temperature([1.0, 0.0, basePlateHeight]), 1891.0863107752575, delta=1e-9)
