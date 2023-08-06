import contur
import yoda
import numpy as np
import scipy.stats
import os
import contur.config.config as cfg
import contur.data.static_db as cdb


def do_ATLAS_2016_I1457605(prediction):
    """ 
    Photon+jet NNLO Calculation from arXiv:1904.01044
    Xuan Chen, Thomas Gehrmann, Nigel Glover, Marius Hoefer, Alexander Huss
    """

    anaObjects = []
    indir = cfg.input_dir

    a_name = "ATLAS_2016_I1457605"
    yoda_name = a_name+".yoda"

    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    splitter = " "
    dataFiles = {a_name+"/d01-x01-y01": indir+"/NNLO-Photons/Fig5/NNLO.Et_gam_bin1_ATLAS.dat",
                 a_name+"/d02-x01-y01": indir+"/NNLO-Photons/Fig5/NNLO.Et_gam_bin2_ATLAS.dat",
                 a_name+"/d03-x01-y01": indir+"/NNLO-Photons/Fig5/NNLO.Et_gam_bin3_ATLAS.dat",
                 a_name+"/d04-x01-y01": indir+"/NNLO-Photons/Fig5/NNLO.Et_gam_bin4_ATLAS.dat"
                 }

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)

    for path, ao in aos.items():
        filename = dataFiles.get(path[5:])
        ao.setPath("/THY/"+path[5:])
        ao.rmAnnotation("ErrorBreakdown")
        cfg.contur_log.debug("Reading {}".format(filename))

        with open(filename, "r+") as f:
            data = f.readlines()  # read the text file
            binNum = 0
            nBins = len(ao.points())
            cfg.contur_log.debug("{} bins".format(nBins))
            for line in data:
                # get a list containing all the entries in a line
                allNums = line.strip().split(splitter)
                # check they're actually numbers
                numberLine = True
                for num in allNums:
                    try:
                        val = float(num)
                    except ValueError:
                        numberLine = False
                        break
                if numberLine:
                    tmplist = [float(allNums[3]), float(allNums[5]), float(allNums[7]), float(
                        allNums[9]), float(allNums[11]), float(allNums[13]), float(allNums[15])]
                    upper = max(tmplist)
                    lower = min(tmplist)
                    uncertainty = (upper - lower)/2000.0
                    mean = (upper + lower)/2000.0
                    if binNum < nBins:
                        point = ao.point(binNum)
                        binNum = binNum + 1
                        point.setY(mean)
                        point.setYErrs(uncertainty, uncertainty)

            ao.setTitle(prediction.short_description)
            #ao.setAnnotation("Title", "NNLO QCD arXiv:1904.01044")
            anaObjects.append(ao)

    yoda.write(anaObjects, a_name+"-Theory.yoda")

def do_ATLAS_2017_I1645627(prediction):

    anaObjects = []
    indir = cfg.input_dir

    # Photon+jet NNLO Calculation from arXiv:1904.01044
    # Xuan Chen, Thomas Gehrmann, Nigel Glover, Marius Hoefer, Alexander Huss
    a_name = "ATLAS_2017_I1645627"
    splitter = " "
    dataFiles = {a_name+"/d01-x01-y01": indir+"/NNLO-Photons/Fig11/NNLO_pt_NNPDF31_hybIso.Et_gam_ATLAS.dat",
                 a_name+"/d02-x01-y01": indir+"/NNLO-Photons/Fig12/NNLO_pt_NNPDF31_hybIso.ptj1_ATLAS.dat",
                 a_name+"/d03-x01-y01": indir+"/NNLO-Photons/Fig14/NNLO_pt_NNPDF31_hybIso.dphi_gam_j1_ATLAS.dat",
                 a_name+"/d04-x01-y01": indir+"/NNLO-Photons/Fig13/NNLO_pt_NNPDF31_hybIso.m_gam_j1_ATLAS.dat",
                 a_name+"/d05-x01-y01": indir+"/NNLO-Photons/Fig15/NNLO_pt_NNPDF31_hybIso.abs_costhetastar_gam_j1_ATLAS.dat"
                 }

    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        filename = dataFiles.get(path[5:])
        ao.setPath("/THY/"+path[5:])
        ao.rmAnnotation("ErrorBreakdown")

        cfg.contur_log.debug("Reading {}".format(filename))

        with open(filename, "r+") as f:
            data = f.readlines()  # read the text file
            binNum = 0
            nBins = len(ao.points())
            cfg.contur_log.debug("nBins= {}".format(nBins))
            for line in data:
                # get a list containing all the entries in a line
                allNums = line.strip().split(splitter)
            # check they're actually numbers
                numberLine = True
                for num in allNums:
                    try:
                        val = float(num)
                    except ValueError:
                        numberLine = False
                        break
                if numberLine:
                    tmplist = [float(allNums[3]), float(allNums[5]), float(allNums[7]), float(
                        allNums[9]), float(allNums[11]), float(allNums[13]), float(allNums[15])]
                    upper = max(tmplist)
                    lower = min(tmplist)
                    uncertainty = (upper - lower)/2000.0
                    mean = (upper + lower)/2000.0
                    if binNum < nBins:
                        point = ao.point(binNum)
                        binNum = binNum + 1
                        point.setY(mean)
                        point.setYErrs(uncertainty, uncertainty)
                        
        ao.setTitle(prediction.short_description)
        anaObjects.append(ao)

    yoda.write(anaObjects, a_name+"-Theory.yoda")

        
def do_ATLAS_2012_I1199269(prediction):
    """
         ATLAS 7TeV diphotons, 2gamma NNLO prediction read from paper
         S. Catani, L. Cieri, D. de Florian, G. Ferrera, and M. Grazzini,
         Diphoton production at hadron colliders: a fully-differential QCD calculation at NNLO,
         Phys. Rev. Lett. 108 (2012) 072001, [arXiv:1110.2375].
    """

    anaObjects = []
    indir = cfg.input_dir

    a_name = "ATLAS_2012_I1199269"
    splitter = ", "
    dataFiles = {a_name+"/d01-x01-y01": indir+"/"+a_name+"/2gammaNNLO-Fig5a.txt",
                 a_name+"/d02-x01-y01": indir+"/"+a_name+"/2gammaNNLO-Fig5b.txt",
                 a_name+"/d03-x01-y01": indir+"/"+a_name+"/2gammaNNLO-Fig5c.txt",
                 a_name+"/d04-x01-y01": indir+"/"+a_name+"/2gammaNNLO-Fig5d.txt"
                 }
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        filename = dataFiles.get(path[5:])
        if filename:
            ao.setPath("/THY/"+path[5:])
            ao.rmAnnotation("ErrorBreakdown")

            cfg.contur_log.debug("Reading {}".format(filename))

            with open(filename, "r+") as f:
                data = f.readlines()  # read the text file
                binNum = 0
                nBins = len(ao.points())
                for line in data:
                    # get a list containing all the entries in a line
                    allNums = line.strip().split(splitter)
                    # check they're actually numbers
                    numberLine = True
                    for num in allNums:
                        try:
                            val = float(num)
                        except ValueError:
                            numberLine = False
                            break
                    if numberLine:
                        uncertainty = float(allNums[2])
                        mean = float(allNums[1])
                        if binNum < nBins:
                            point = ao.point(binNum)
                            binNum = binNum + 1
                            point.setY(mean)
                            point.setYErrs(
                                uncertainty, uncertainty)

            ao.setTitle(prediction.short_description)
            anaObjects.append(ao)

    yoda.write(anaObjects, a_name+"-Theory.yoda")

def do_ATLAS_2017_I1591327(prediction):
    """
     ATLAS 8TeV diphotons, Matrix prediction prediction read from
     Predictions for the isolated diphoton production through NNLO in QCD and
     comparison to the 8 TeV ATLAS data
     Bouzid Boussaha, Farida Iddir, Lahouari Semlala arXiv:1803.09176
     2gamma from
     S. Catani, L. Cieri, D. de Florian, G. Ferrera, and M. Grazzini,
     Diphoton production at hadron colliders: a fully-differential QCD calculation at NNLO,
     Phys. Rev. Lett. 108 (2012) 072001, [arXiv:1110.2375].
    """
    anaObjects = []
    indir = cfg.input_dir

    a_name = "ATLAS_2017_I1591327"
    splitter = ", "
    dataFiles = {a_name+"/d02-x01-y01": indir+"/"+a_name+"/Matrix_Mass.txt",
                 a_name+"/d03-x01-y01": indir+"/"+a_name+"/2gammaNNLO_pt.txt"
                 }
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        filename = dataFiles.get(path[5:])
        if filename:
            ao.setPath("/THY/"+path[5:])
            ao.rmAnnotation("ErrorBreakdown")

            with open(filename, "r+") as f:
                data = f.readlines()  # read the text file
                binNum = 0
                nBins = len(ao.points())
                for line in data:
                    # get a list containing all the entries in a line
                    allNums = line.strip().split(splitter)
                    # check they're actually numbers
                    numberLine = True
                    for num in allNums:
                        try:
                            val = float(num)
                        except ValueError:
                            numberLine = False
                            break
                    if numberLine:
                        uncertainty = float(allNums[2])
                        mean = float(allNums[1])
                        if binNum < nBins:
                            point = ao.point(binNum)
                            binNum = binNum + 1
                            point.setY(mean)
                            point.setYErrs(
                                uncertainty, uncertainty)

            if "Matrix" in filename:
                ao.setAnnotation("Title", "1803.09176 (Matrix)")
            else:
                ao.setAnnotation("Title", "2gamma NNLO")

            anaObjects.append(ao)

        yoda.write(anaObjects, a_name+"-Theory.yoda")


def do_ATLAS_2016_I1467454(prediction):
        
    indir = cfg.input_dir

    anaObjects_el = []
    anaObjects_mu = []


    # ATLAS 8TeV HMDY mass distribution
    # Predictions from the paper, taken from the ll theory ratio plot (Born) but applied
    # to the dressed level ee & mm data as mult. factors.
    a_name_mu  = "ATLAS_2016_I1467454:LMODE=MU"
    a_name_el  = "ATLAS_2016_I1467454:LMODE=EL"
    short_name = "ATLAS_2016_I1467454"

    splitter = ", "
    dataFiles = {"d18-x01-y01": indir+"/"+short_name+"/dy1.txt",
                 "d29-x01-y01": indir+"/"+short_name+"/dy1.txt",
                 }
    analysis_mu = cdb.get_analyses(analysisid=a_name_mu,filter=False)[0]
    analysis_el = cdb.get_analyses(analysisid=a_name_el,filter=False)[0]

    # This finds the REF file, which is common to _mu and _el versions.
    yodaf = contur.util.utils.find_ref_file(analysis=analysis_mu)

    for histo, filename in dataFiles.items():

        aos = yoda.read(yodaf, patterns=histo)
        ao = next(iter(aos.values()))  

        mu = ("d29" in histo)
        el = ("d18" in histo)
                
        if mu:
            ao.setPath("/THY/{}/{}".format(a_name_mu,histo))
        elif el:
            ao.setPath("/THY/{}/{}".format(a_name_el,histo))

        ao.rmAnnotation("ErrorBreakdown")

                       
        with open(filename, "r+") as f:
            data = f.readlines()  # read the text file
            binNum = 0
            nBins = len(ao.points())
            for line in data:
                # get a list containing all the entries in a line
                allNums = line.strip().split(splitter)
                # check they're actually numbers
                numberLine = True
                for num in allNums:
                    try:
                        val = float(num)
                    except ValueError:
                        numberLine = False
                        break
                if numberLine:
                    uncertainty = float(allNums[2])
                    mean = float(allNums[1])
                    if binNum < nBins:
                        point = ao.point(binNum)
                        uncertainty = uncertainty*point.y()
                        point.setYErrs(
                            uncertainty, uncertainty)
                        point.setY(point.y()*mean)
                        binNum = binNum + 1

        ao.setTitle(prediction.short_description)

        if el:
            anaObjects_el.append(ao)
        elif mu:
            anaObjects_mu.append(ao)

    yoda.write(anaObjects_el, analysis_el.name+"-Theory.yoda")
    yoda.write(anaObjects_mu, analysis_mu.name+"-Theory.yoda")


def do_CMS_2017_I1467451(prediction):
    """
    CMS 8TeV H->WW pT distribution
     Predictions from the paper
    """
    
    indir = cfg.input_dir
    anaObjects = []

    a_name = "CMS_2017_I1467451"
    splitter = ", "
    dataFiles = {a_name+"/d01-x01-y01": indir +
                 "/"+a_name+"/hpt.txt"}
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        filename = dataFiles.get(path[5:])
        if filename:
            ao.setPath("/THY/"+path[5:])
            ao.rmAnnotation("ErrorBreakdown")

            with open(filename, "r+") as f:
                data = f.readlines()  # read the text file
                binNum = 0
                nBins = len(ao.points())
                for line in data:
                    # get a list containing all the entries in a line
                    allNums = line.strip().split(splitter)
                    # check they're actually numbers
                    numberLine = True
                    for num in allNums:
                        try:
                            val = float(num)
                        except ValueError:
                            numberLine = False
                            break
                    if numberLine:
                        uncertainty = float(allNums[2])
                        mean = float(allNums[1])
                        if binNum < nBins:
                            point = ao.point(binNum)
                            point.setYErrs(
                                uncertainty, uncertainty)
                            point.setY(mean)
                            binNum = binNum + 1

            ao.setTitle(prediction.short_description)

            anaObjects.append(ao)

    yoda.write(anaObjects, a_name+"-Theory.yoda")

def do_ATLAS_2015_I1408516(prediction):
    """
    ATLAS 8TeV Drell-Yan phi* and pT distributions
    Predictions from Bizon et al arXiv:1805.05916
    """
        
    indir = cfg.input_dir

    anaObjects_el = []
    anaObjects_mu = []

    a_name_mu = "ATLAS_2015_I1408516:LMODE=MU"
    a_name_el = "ATLAS_2015_I1408516:LMODE=EL"
    short_name = "ATLAS_2015_I1408516"

    analysis_mu = cdb.get_analyses(analysisid=a_name_mu,filter=False)[0]
    analysis_el = cdb.get_analyses(analysisid=a_name_el,filter=False)[0]

    splitter = " "
    dataFiles = {"d02-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.0_0.8.dat",
                 "d03-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.8_1.6.dat",
                 "d04-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_1.6_2.4.dat",
                 "d05-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.0_0.4.dat",
                 "d06-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.4_0.8.dat",
                 "d07-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.8_1.2.dat",
                 "d08-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_1.2_1.6.dat",
                 "d09-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_1.6_2.0.dat",
                 "d10-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_2.0_2.4.dat",
                 "d11-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.0_0.8.dat",
                 "d12-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.8_1.6.dat",
                 "d13-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_1.6_2.4.dat",
                 "d14-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.0_2.4.dat",
                 "d15-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.0_2.4.dat",
                 "d16-x01-y04": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.0_2.4.dat",
                 "d17-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.0_0.4.dat",
                 "d18-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.4_0.8.dat",
                 "d19-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.8_1.2.dat",
                 "d20-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_1.2_1.6.dat",
                 "d21-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_1.6_2.0.dat",
                 "d22-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_2.0_2.4.dat",
                 "d26-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_46_66_0.0_2.4.dat",
                 "d27-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.0_2.4.dat",
                 "d28-x01-y04": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_116_150_0.0_2.4.dat",
                 
                 "d02-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.0_0.8.dat",
                 "d03-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.8_1.6.dat",
                 "d04-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_1.6_2.4.dat",
                 "d05-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.0_0.4.dat",
                 "d06-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.4_0.8.dat",
                 "d07-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.8_1.2.dat",
                 "d08-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_1.2_1.6.dat",
                 "d09-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_1.6_2.0.dat",
                 "d10-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_2.0_2.4.dat",
                 "d11-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.0_0.8.dat",
                 "d12-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.8_1.6.dat",
                 "d13-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_1.6_2.4.dat",
                 "d14-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_46_66_0.0_2.4.dat",
                 "d15-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_66_116_0.0_2.4.dat",
                 "d16-x01-y01": indir+"/"+short_name+"/phistar/ATLAS_8TeV_phistar_NNLO_N3LL_116_150_0.0_2.4.dat",
                 "d17-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.0_0.4.dat",
                 "d18-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.4_0.8.dat",
                 "d19-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.8_1.2.dat",
                 "d20-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_1.2_1.6.dat",
                 "d21-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_1.6_2.0.dat",
                 "d22-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_2.0_2.4.dat",
                 "d26-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_46_66_0.0_2.4.dat",
                 "d27-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_66_116_0.0_2.4.dat",
                 "d28-x01-y01": indir+"/"+short_name+"/ptz/ATLAS_8TeV_ptz_NNLO_N3LL_116_150_0.0_2.4.dat"
                 }

    # This finds the REF file, which is common to _mu and _el versions.
    f = contur.util.utils.find_ref_file(analysis=analysis_mu)
    aos = yoda.read(f)
    for path, ao in aos.items():
        el = False
        mu = False
        filename = dataFiles.get(ao.name())
        if filename:

            el = ("y01" in path)
            mu = ("y04" in path)
           
            if mu:
                ao.setPath("/THY/{}/{}".format(a_name_mu,ao.name()))
            elif el:
                ao.setPath("/THY/{}/{}".format(a_name_el,ao.name()))
            ao.rmAnnotation("ErrorBreakdown")
                           
            cfg.contur_log.debug("Reading {}".format(filename))

            with open(filename, "r+") as f:
                data = f.readlines()  # read the text file
                binNum = 0
                nBins = len(ao.points())
                # now we want to get the born-to-dressed corrections
                if "y01" in path:
                    # this is an electron plot
                    dpath = path[:len(path)-1]+"2"
                    dplot = aos[dpath]
                elif "y04" in path:
                    # this is a muon plot
                    dpath = path[:len(path)-1]+"5"
                    dplot = aos[dpath]

                bornpath = path[:len(path)-1]+"6"
                bornplot = aos[bornpath]

                for line in data:
                    # get a list containing all the entries in a line
                    allNums = line.strip().split(splitter)
                    # check they're actually numbers
                    numberLine = True
                    for num in allNums:
                        try:
                            val = float(num)
                        except ValueError:
                            numberLine = False
                            break
                    if numberLine:

                        uncertainty = np.abs(
                            (float(allNums[2])-float(allNums[3]))/2.0)
                        mean = float(allNums[1])
                        if binNum < nBins:
                            corr = dplot.point(binNum).y(
                            )/bornplot.point(binNum).y()
                            point = ao.point(binNum)
                            point.setYErrs(
                                uncertainty*corr, uncertainty*corr)
                            point.setY(mean*corr)
                            binNum = binNum + 1

        ao.setTitle(prediction.short_description)

        if el:
            anaObjects_el.append(ao)
        elif mu:
            anaObjects_mu.append(ao)

    yoda.write(anaObjects_el, analysis_el.name+"-Theory.yoda")
    yoda.write(anaObjects_mu, analysis_mu.name+"-Theory.yoda")



def do_ATLAS_2019_I1725190(prediction):
    """
    ATLAS 13 TeV DY Run 2 search
    Fit to SM from the paper.
    """
    anaObjects = []

    a_name = "ATLAS_2019_I1725190"
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    def atlas_fit(mass,muon):

        # return the result of the ATLAS fit to dilepton mass, 13 TeV
        # electron if not muon

        rootS = 13000.0
        mZ = 91.1876
        gammaZ = 2.4952

        x = mass/rootS

        if muon:
            # dimuon channel:
            c = 1.0/3.0
            b = 11.8
            p0 = -7.38
            p1 = -4.132
            p2 = -1.0637
            p3 = -0.1022
        else:
            # electron
            c = 1.0
            b = 1.5
            p0 = -12.38
            p1 = -4.295
            p2 = -0.9191
            p3 = -0.0845

        val = scipy.stats.cauchy.pdf(mass, mZ, gammaZ) * np.power((1-np.power(x,c)),b) * np.power(x, p0 + p1*np.log(x) + p2*np.log(x)**2 + p3*np.log(x)**3)
        return val


    a_muon = 138700
    a_elec = 178000

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():

        if "d01-x01-y01" in path:
            muon = False
            norm = 178000.0
        elif "d02-x01-y01" in path:
            muon = True
            norm = 138700.0
        else:
            continue

        ao.setPath("/THY/"+path[5:])
        ao.rmAnnotation("ErrorBreakdown")

        sum_n = 0
        for point in ao.points():
            mass = point.x()
            point.setY(atlas_fit(mass,muon))
            bw=point.xErrs()[0]*2.0
            sum_n+=point.y()*bw


        norm = 10.*norm/sum_n
        # now another loop to set the normalisation.
        for point in ao.points():
            point.setY(point.y()*norm)
            bw=point.xErrs()[0]*2.0
            # uncertainty set to root of the number of events, then scaled to error on events per ten GeV ie sqrt(n=y*10)/10
            num_events = point.y()*bw/10.0
            uncertainty = 10.0*np.sqrt(num_events)/bw
            point.setYErrs(uncertainty,uncertainty)



        ao.setAnnotation("Title", "fit to data")
        anaObjects.append(ao)

    yoda.write(anaObjects, a_name+"-Theory.yoda")
    
def do_ATLAS_2021_I1852328(prediction):
    """
    ATLAS 13 TeV WW+jet
    the prediction is for the b-veto, so we need to scale it for the difference (taken from the difference in the data)
    y05 multiplied by the ratio y02/y01
    """

    anaObjects = []
    indir = cfg.input_dir

    a_name = "ATLAS_2021_I1852328"
    yoda_name = a_name+".yoda"

    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]

    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)

    for path, ao in aos.items():
        
        if "y05" in path:
            aob = aos[path[:-1]+"2"]
            aoi = aos[path[:-1]+"1"]
            for points in zip(ao.points(),aob.points(),aoi.points()):
                points[0].setY(points[0].y()*points[1].y()/points[2].y())

            ao.setTitle(prediction.short_description)
            ao.setPath(ao.path()[:-1]+"2")
            ao.setPath("/THY/"+ao.path()[5:])
            ao.rmAnnotation("ErrorBreakdown")
            anaObjects.append(ao)


    yoda.write(anaObjects, a_name+"-Theory.yoda")
    
def do_ATLAS_2019_I1764342(prediction):
    """
    ATLAS 13 TeV ll+photons
    There's a version of this in HEPData with no uncertainties. Rerun by Xilin Wang to include scale uncertainties, which 
    are calculated here from the RAW rivet weights output.
    """

    a_name = "ATLAS_2019_I1764342"


    if prediction.id != "B":
        cfg.contur_log.error("Do not know how to make file for {}, prediciton ID {}".format(a_name, prediction.id))
        return
        
    # input raw file.
    relpath = "data/TheoryRaw/{}/{}.yoda".format(a_name,a_name)
    f = cfg.paths.data_path(relpath)
    # output file
    f_out = prediction.file_name

    SCALES = [
      'MUR0.5_MUF0.5_PDF261000', 
      'MUR0.5_MUF1_PDF261000', 
      'MUR1_MUF0.5_PDF261000', 
      'MUR1_MUF1_PDF261000', 
      'MUR1_MUF2_PDF261000', 
      'MUR2_MUF1_PDF261000', 
      'MUR2_MUF2_PDF261000', 
    ]

    #EW_CORRS = [
    #  'MUR1_MUF1_PDF261000_MULTIASSEW', 
    #  'MUR1_MUF1_PDF261000_EXPASSEW', 
    #  'MUR1_MUF1_PDF261000_ASSEW', 
    #]


    OUT = { }
    aos = yoda.read(f)
    for path, ao in aos.items():
        if type(ao) != yoda.core.Histo1D:           # scatter 1D object does not have y value
           continue
        if 'RAW' in path or path.endswith(']'):
            continue
        hname = '/THY' + path
        OUT[hname] = ao.mkScatter()
        OUT[hname].setPath(hname)

        nominal = np.array([ b.sumW()   for b in ao.bins() ])     
        statsSq = np.array([ b.sumW2()  for b in ao.bins() ]) 
        bwidth  = np.array([ b.xMax() - b.xMin()  for b in ao.bins() ])

        scaleup = np.array(nominal)
        scaledn = np.array(nominal)
        for scale in SCALES:
          temp = np.array([ b.sumW() for b in aos['%s[%s]' % (path, scale) ].bins() ])
          scaleup = np.array(list(map(max, zip(scaleup, temp))))
          scaledn = np.array(list(map(min, zip(scaledn, temp))))
        delta_qcd = 0.5 * (scaleup - scaledn)

        delta_total = np.sqrt(statsSq + delta_qcd ** 2) / bwidth

        for i in range(OUT[hname].numPoints()):
          cval = OUT[hname].point(i).y()
          olderr = OUT[hname].point(i).yErrs()[0]
          cfg.contur_log.debug('old: %.1f%%, new: %.1f%%' % (100.*olderr/cval, 100.*delta_total[i]/cval))
          OUT[hname].point(i).setYErrs(delta_total[i])

#    yoda.write(OUT, f.replace('.yoda', '_B.yoda'))
    yoda.write(OUT, f_out)

def do_ATLAS_2016_I1494075(prediction, mode_flag):
    """
    ATLAS 8 TeV 4l/2l2nu
    Newly written rivet routine, verified with events generated by Powheg+Pythia 8
    """

    #Two separate files generated but with all histograms on it
    #so for mode 4L, graphs of 2L2NU will be empty and need to be excluded, vice versa.

    a_name = "ATLAS_2016_I1494075"
    mode_analysis = ["_MODE:4L", "_MODE:2L2NU"]

    # input raw file.
    if mode_flag == 1:
        relpath = "data/TheoryRaw/{}/{}-Theory.yoda".format(a_name,a_name + mode_analysis[0])
    if mode_flag == 2:
        relpath = "data/TheoryRaw/{}/{}-Theory.yoda".format(a_name,a_name + mode_analysis[1])
    f = cfg.paths.data_path(relpath)
    # output file
    f_out = prediction.file_name

    #Include 62 weights > <
    SCALES = [
        "_muR5000000E-01_muF5000000E-01_",
        "_muR1000000E+00_muF5000000E-01_",
        "_muR2000000E+00_muF5000000E-01_",
        "_muR5000000E-01_muF1000000E+00_",
        "_muR2000000E+00_muF1000000E+00_",
        "_muR5000000E-01_muF2000000E+00_",
        "_muR1000000E+00_muF2000000E+00_",
        "_muR2000000E+00_muF2000000E+00_",
        "_pdfset_21100_",
        "_pdfset_260000_"
    ]
    pdf_range = list(np.linspace(11001,11052,52,dtype=int))
    pdf_list = ["_pdfset_"+str(i)+"_" for i in pdf_range]
    SCALES = SCALES + pdf_list

    OUT = { }
    histo_4l = ['d02', 'd03' ,'d04', 'd05']
    histo_2l2nu = ['d06', 'd07', 'd08']
    aos = yoda.read(f)
    for path, ao in aos.items():
        #READING only Nominal data
        if type(ao) != yoda.core.Histo1D:           # scatter 1D object does not have y value
            continue
        if 'RAW' in path or path.endswith(']'):
            continue
        if mode_flag == 1:
            if any(histo in path for histo in histo_2l2nu):
                continue
        if mode_flag == 2:
            if any(histo in path for histo in histo_4l):
                continue
        hname = '/THY' + path
        OUT[hname] = ao.mkScatter()
        OUT[hname].setPath(hname)
        #Uncertainty calculation
        nominal = np.array([ b.sumW()   for b in ao.bins() ])     
        statsSq = np.array([ b.sumW2()  for b in ao.bins() ]) 
        bwidth  = np.array([ b.xMax() - b.xMin()  for b in ao.bins() ])

        scaleup = np.array(nominal)
        scaledn = np.array(nominal)
        #For selected ones, calculate uncertainties from the weighted histograms.
        for scale in SCALES: 
            temp = np.array([ b.sumW() for b in aos['%s[%s]' % (path, scale) ].bins() ])
            scaleup = np.array(list(map(max, zip(scaleup, temp))))
            scaledn = np.array(list(map(min, zip(scaledn, temp))))
        delta_qcd = 0.5 * (scaleup - scaledn)

        delta_total = np.sqrt(statsSq + delta_qcd ** 2) / bwidth
        #Writing uncertainties
        for i in range(OUT[hname].numPoints()):
            cval = OUT[hname].point(i).y()
            olderr = OUT[hname].point(i).yErrs()[0]
            cfg.contur_log.debug('old: %.1f%%, new: %.1f%%' % (100.*olderr/cval, 100.*delta_total[i]/cval))
            OUT[hname].point(i).setYErrs(delta_total[i])
    yoda.write(OUT, f_out)

def do_ATLAS_2022_I2077570(prediction):
    """
    Z + high transverse momentum jets at ATLAS

    These predictions are read from the SM/data ratio plots in the paper, using https://plotdigitizer.com/app
    and exported at python lists, which are then pasted below as x and y.

    """
    
    anaObjects = []
        
    a_name = "ATLAS_2022_I2077570"
    yoda_name = a_name+".yoda"
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]
    
    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        
        if "d01-x01-y01" in path:
                
            #Sherpa 2.2.11

            x = [10.156653798575688, 9.889135745349547, 9.76490160952038, 30.498700290333964, 30.374548265632335, 30.804482128951026, 50.14329486554741, 50.67833097199977, 52.40775553831339, 70.33245043799708, 70.72420262705239, 70.8579616536655, 90.00570179668998, 91.13316968768103, 89.13622706814118, 111.38924582900106, 110.15667569487634, 110.8542097225487, 129.4095180810344, 129.4095180810344, 130.0305245379251, 150.24841900498166, 148.66236046719254, 150.16244865454348, 171.1159767124084, 171.2688676317169, 171.2688676317169, 189.0406716120921, 190.8274097453646, 190.1872713957786, 219.40569498694043, 218.8037383116178, 218.8037383116178, 259.43051772817546, 258.79037937858953, 259.8604515914942, 309.4687103505892, 308.08333140828347, 306.6596886805869, 369.8261368039261, 369.8261368039261, 368.5553028844106, 450.21974579927667, 449.5127689919478, 448.8438917477549, 550.2675563717522, 550.2675563717522, 548.5286069146545, 649.5699621292532, 649.5699621292532, 649.4935987807264, 778.6547307012299, 778.6547307012299, 778.9986121029829, 1178.1196179577253, 1178.1196179577253, 1177.1546479879544]


            y = [1.127659125977015, 1.5611872044617128, 0.8763102564672531, 0.7807384730007639, 1.344133232051546, 1.0275388602426312, 0.985126984212152, 1.3309327454697224, 0.7812290406872233, 0.9911475527954309, 1.3157696048860543, 0.8137851052919225, 0.9927978531531616, 1.2488741854851748, 0.8539671978850396, 0.9799089537034411, 1.1437141032844267, 0.8827765517844011, 0.9493600007971718, 1.1166435818799625, 0.8712708232568943, 0.9428937054800245, 1.1137894744103791, 0.833184757755377, 0.9341972434695094, 1.1005441468759647, 0.827610299161972, 0.9204613482486347, 1.0950141459791465, 0.816282401420806, 0.9091782914600596, 1.090911390445121, 0.7935380738013088, 0.8885296076761573, 1.0804753294276987, 0.7689648485257295, 0.8772913918401732, 1.0631272463592594, 0.7533115235116056, 0.8722519586298138, 1.061031219267659, 0.7455961968740099, 0.8806360669962159, 1.0646882480678146, 0.7192392981509423, 0.8277440555077338, 1.0330244034428655, 0.6953352378601745, 0.8453596512676959, 1.0607637065761368, 0.6972975086060132, 0.8478573306525851, 1.0614773292575337, 0.6951570238178274, 0.7746289890243143, 1.0178168051626113, 0.6206351931725242]

        elif "d02-x01-y01" in path:

            x = [122.05740486564741, 120.3697679602452, 120.85873672871666, 161.1330237794141, 160.5494465007851, 159.36650126812125, 201.6438998766442, 201.17072178357864, 201.63597065337171, 240.80626584843492, 239.45768795185637, 241.46866096181535, 280.59944558279426, 279.9291890172804, 280.65467906114543, 329.98224149715566, 329.6825575201383, 329.5485062070354, 390.5394816789352, 390.9732169690554, 390.71297579498327, 470.51240772497346, 470.5675734321856, 471.45090245897114, 569.9797019277439, 569.8693705133196, 569.5459666376237, 671.087464323116, 670.6851748415297, 670.8823888562562, 770.4758729199962, 769.8765049659611, 770.1210232357664, 919.4915957010427, 918.9946977092985, 920.0120780491869, 1121.0523157459834, 1121.5017739403706, 1121.4228883344801]
            y = [0.9792379130229375, 1.1702894893466058, 0.8484259380645169, 0.9415147081798104, 1.1658053928945538, 0.8351202425583727, 0.9529192908710987, 1.1806704281252451, 0.8039284219925952, 0.9427331124931889, 1.200896609870624, 0.7858466988530917, 0.940101543465705, 1.21834462873851, 0.7763913955273796, 0.9525293512300688, 1.2499268077848873, 0.7672288610621181, 0.9587189624171064, 1.296910136713425, 0.7742955223117934, 0.9405886538873127, 1.2844333247191997, 0.7457842750033606, 0.9446338064684743, 1.3130907470380717, 0.7277511372541463, 0.9795788484341054, 1.3667998018051148, 0.7303831251212016, 1.012379431793861, 1.419144277248341, 0.7533384655142152, 1.0269031127738109, 1.4824543915119648, 0.7598694309519928, 1.0990838303213883, 1.590164851066931, 0.80144260913598]

        elif "d03-x01-y01" in path:

            x = [0.9945576287097948, 1.9954149085299646, 2.9996322369108097, 3.999241734376777, 4.997315838130568, 0.9972132219175693, 0.9964452500984229, 1.996727032239584, 1.9956068327439864, 2.9960808140622266, 2.996368425420202, 4.002537441582035, 3.9974819708098113, 4.997411525274521, 4.998595516199422]
            y = [0.9588827609638688, 0.9386582795179224, 0.9406627729751338, 1.0445920835716047, 1.2400213905790534, 1.140769869431331, 0.8392731509949976, 1.2878650814349395, 0.736323883036123, 1.477280525241602, 0.6519066088275619, 1.594217604877244, 0.6765412821426946, 1.7152084624384785, 0.7774412656331879]

        elif "d04-x01-y01" in path:
            
            x = [1.0030708335110083, 1.0015835405659756, 1.002147693764862, 2.0042118113185223, 2.0067760639053356, 2.0032117616245584, 3.002762973347398, 3.004506559327706, 3.002762973347398, 4.006724717149343, 4.006904540981488, 4.003416928276185]
            y = [0.8394775356113937, 0.7214062225878145, 0.9952684026894297, 0.9758451327964853, 1.4007210772279557, 0.7298334423527434, 0.9950430055431434, 1.5720597000359018, 0.6739973022052901, 1.2196485508551345, 1.6004059085034754, 0.7776478452303914]

        elif "d05-x01-y01" in path:

            x = [0.1981099646227481, 0.1968218346335153, 0.19819394694410858, 0.4991528975164215, 0.5022051375282706, 0.49660479206975855, 0.7007350137578205, 0.6884143981313091, 0.7018270245725293, 0.8979770006351615, 0.9028491784591844, 0.9061252109033117, 1.0981870045659674, 1.0990268277795712, 1.097122907646037, 1.300217186945971, 1.3027650517556095, 1.3020931931847262, 1.5042629450386242, 1.4994189217464042, 1.5012670140903805, 1.7039969689360464, 1.7017008104534648, 1.6998248042147095, 1.899362949574632, 1.8977949587265392, 1.896534983269109, 2.101616924386914, 2.0992091103252175, 2.098956922724112, 2.301994892960441, 2.303031075985592, 2.298298708272487, 2.502204896891246, 2.502204896891246, 2.500972835328595, 2.6993347469154236, 2.695582734437913, 2.702191108389773, 2.89898502912851, 2.8978646231449745, 2.898816583211741, 3.102218877902338, 3.0977945255798955, 3.1032271470327104, 3.3025131047915286, 3.300160637245341, 3.3036609433957955, 3.7000488372840112, 3.6990689633224654, 3.7008886604976152]
            y = [1.1132034801444348, 1.5989514298587597, 0.7667260369886983, 1.0267562016249987, 1.5473589020580067, 0.7155764597378258, 1.033254501955625, 1.5369222763512216, 0.7258159364892682, 1.0671738528024974, 1.6017572064077643, 0.7591937623085891, 1.030202500745655, 1.5402695779277786, 0.7324618870031883, 0.9401616959886958, 1.3923350939947832, 0.6560577824127058, 1.1019296059770822, 1.6035789304457637, 0.7859252145475625, 0.9805298483941458, 1.4700684733013352, 0.7061243096084735, 0.9441490970704768, 1.395190369315839, 0.6676760326522674, 0.9850096987978566, 1.4722345734115443, 0.7143948352050494, 0.9105745453622399, 1.3297149166876439, 0.6733865832943756, 1.050977177681554, 1.558090828131379, 0.7708120125481507, 0.9002364941331269, 1.2943681397134572, 0.6553686072018602, 0.866858668313806, 1.2120072598199005, 0.6619654820101584, 0.8051743139449037, 0.9573919223926942, 0.6955400337183943, 0.8324472912114295, 1.004061649239856, 0.7405356867108491, 0.9274108969219799, 1.1224094056128224, 0.786319089391821]            

        elif "d06-x01-y01" in path:

            x = [0.05124999922849775, 0.04961444243305227, 0.05164169795365613, 0.15063559725021997, 0.15027327172125413, 0.14867685113277007, 0.2512258329713819, 0.25171549845977287, 0.24988409230174818, 0.3511598428738803, 0.3505037012191026, 0.35068978757091285, 0.4513779058914215, 0.45098620716626314, 0.4494290069486264, 0.550528518343603, 0.549970343452058, 0.5497841729363617, 0.7005471101460069, 0.7005471101460069, 0.699910494512767, 0.900385840918697, 0.8997786826455357, 0.9011986957290925, 1.098775101247752, 1.0973256308041168, 1.0999306714016894, 1.350177173396289, 1.3481400707010305, 1.3495307947522808]
            y = [1.3774071025298116, 1.7032843441336007, 0.9635195174512727, 1.0781527510136306, 1.6241476421736392, 0.7238230916737226, 1.0194639884960686, 1.5483051906852114, 0.7166413897805901, 0.9939390508627559, 1.4774025424694928, 0.6946387056347412, 0.9431179648293557, 1.4190793709947143, 0.6726364145975395, 1.0674943962362202, 1.6026941308092613, 0.7730890398950248, 1.0119163024515045, 1.4892500509075706, 0.7219935640252126, 0.864027256581228, 1.0741273184565296, 0.7136223153627649, 0.8164996348020657, 0.974772252504692, 0.7121587718656858, 0.936485042609047, 1.3484971063272406, 0.6837975553359384]

        else:
            # don't have data for this one.
            continue
            
        ao.rmAnnotation("ErrorBreakdown")
        ao.setPath("/THY/"+path[5:])

        # get rid of some of the spurious precision
        x = list(np.around(np.array(x),4))
        y = list(np.around(np.array(y),4))

        # list of pairs
        points = sorted(zip(x, y))

        # check we have the right number of points"
        nBins = len(ao.points())
        if not nBins == len(points)/3.0:
            cfg.contur_log.error("Mismatched number of points in {}, {} vs {}".format(path,nBins,len(points)/3.0))
            continue
            
        counter=0                
        for point in ao.points():
            # for each x value we have an upper, central and lower value. Get them and order them.
            yvals = sorted([points[counter][1],points[counter+1][1],points[counter+2][1]])

            # central value
            point.setY(point.y()*yvals[1])

            # uncertainty
            uncertainty_up   = (yvals[2]-yvals[1])*point.y()
            uncertainty_down = (yvals[1]-yvals[0])*point.y()                
            point.setYErrs(uncertainty_up, uncertainty_down)

            counter=counter+3


        anaObjects.append(ao)

        
    yoda.write(anaObjects, a_name+"-Theory.yoda")

def do_CMS_2021_I1866118(prediction):
    """
    Z + high transverse momentum jets at ATLAS

    These predictions are read from the SM/data ratio plots in the paper, using https://plotdigitizer.com/app
    and exported at python lists, which are then pasted below as x and y.

    """
    
    anaObjects = []
        
    a_name = "CMS_2021_I1866118"
    yoda_name = a_name+".yoda"
    analysis = cdb.get_analyses(analysisid=a_name,filter=False)[0]
    
    f = contur.util.utils.find_ref_file(analysis)
    aos = yoda.read(f)
    for path, ao in aos.items():
        
        if "d01-x01-y01" in path:
                
            #Sherpa 2.2.11

            x = [0.15827338129496404, 0.15827338129496404, 0.16084275436793422, 0.47173689619732784, 0.47430626927029806, 0.47173689619732784, 0.7826310380267214, 0.7852004110996917, 0.7852004110996917, 1.0960945529290853, 1.0986639260020556, 1.093525179856115, 1.4121274409044193, 1.4121274409044193, 1.409558067831449, 1.725590955806783, 1.723021582733813, 1.725590955806783, 2.039054470709147, 2.036485097636177, 2.036485097636177, 2.352517985611511, 2.355087358684481, 2.355087358684481, 2.6659815005138747, 2.6659815005138747, 2.663412127440904, 2.9820143884892087, 2.979445015416238, 2.979445015416238]
            y = [1.005263157894737, 0.9394736842105265, 1.0710526315789475, 1.0026315789473685, 0.936842105263158, 1.0710526315789475, 0.9947368421052633, 0.9263157894736843, 1.0657894736842106, 0.9763157894736844, 0.9052631578947369, 1.0421052631578949, 0.9421052631578949, 0.868421052631579, 1.0210526315789474, 0.9684210526315791, 0.8842105263157896, 1.0447368421052632, 0.9894736842105264, 0.9105263157894737, 1.0710526315789475, 1.005263157894737, 0.936842105263158, 1.073684210526316, 1.0157894736842108, 0.9605263157894738, 1.0710526315789475, 1.1184210526315792, 1.0605263157894738, 1.1763157894736844]
        
        elif "d02-x01-y01" in path:

            x = [0.05039999999999997, 0.05039999999999997, 0.04959999999999998, 0.1496, 0.1504, 0.1496, 0.24960000000000002, 0.24960000000000002, 0.24960000000000002, 0.35040000000000004, 0.34800000000000003, 0.35120000000000007, 0.4488000000000001, 0.4488000000000001, 0.4504000000000001, 0.5496000000000001, 0.5488000000000001, 0.5488000000000001, 0.6496000000000001, 0.6496000000000001, 0.6488, 0.7496, 0.7496, 0.7496, 0.8496000000000001, 0.8512000000000002, 0.8496000000000001, 0.9496000000000002, 0.9504000000000001, 0.9496000000000002]
            y = [1.2262886597938145, 1.290721649484536, 1.1670103092783504, 1.1, 1.154123711340206, 1.0484536082474227, 1.0278350515463917, 1.0819587628865979, 0.9711340206185567, 1.0097938144329897, 1.0716494845360824, 0.9479381443298969, 0.9582474226804123, 1.0278350515463917, 0.8886597938144329, 0.9582474226804123, 1.0355670103092782, 0.8809278350515464, 0.9711340206185567, 1.0458762886597937, 0.8809278350515464, 0.9891752577319588, 1.0639175257731959, 0.9092783505154639, 1.0252577319587628, 1.0948453608247424, 0.9530927835051546, 1.0716494845360824, 1.1309278350515464, 1.002061855670103]

        elif "d03-x01-y01" in path:

            x = [0.15920651068158698, 0.16174974567650047, 0.15920651068158698, 0.4694811800610376, 0.4694811800610376, 0.4669379450661241, 0.7848423194303153, 0.7848423194303153, 0.7848423194303153, 1.100203458799593, 1.100203458799593, 1.100203458799593, 1.4155645981688707, 1.4130213631739572, 1.4079348931841302, 1.7258392675483216, 1.7309257375381486, 1.7258392675483216, 2.041200406917599, 2.046286876907426, 2.0437436419125126, 2.3540183112919637, 2.356561546286877, 2.35147507629705, 2.666836215666328, 2.6693794506612414, 2.664292980671414, 2.979654120040692, 2.9821973550356056, 2.979654120040692]
            y = [0.9125, 0.9828125, 0.8421875, 0.896875, 0.9776041666666666, 0.8239583333333333, 0.9828125, 1.0739583333333333, 0.896875, 0.8864583333333333, 0.9671875, 0.8135416666666666, 0.9697916666666666, 1.0635416666666666, 0.8734375, 0.9463541666666666, 1.0322916666666666, 0.8578125, 0.975, 1.0635416666666666, 0.88125, 0.9671875, 1.0583333333333333, 0.8682291666666666, 0.9932291666666666, 1.084375, 0.9072916666666666, 1.1208333333333331, 1.2067708333333331, 1.0375]

        elif "d04-x01-y01" in path:
            
            x = [0.04939271255060729, 0.04777327935222672, 0.04939271255060729, 0.14898785425101216, 0.15060728744939272, 0.14979757085020243, 0.2493927125506073, 0.25020242914979757, 0.24858299595141703, 0.3489878542510122, 0.34817813765182193, 0.3473684210526316, 0.4493927125506073, 0.44858299595141704, 0.44858299595141704, 0.5489878542510123, 0.5489878542510123, 0.5497975708502025, 0.6493927125506074, 0.6493927125506074, 0.6485829959514171, 0.7489878542510122, 0.7506072874493928, 0.7449392712550609, 0.8485829959514171, 0.8485829959514171, 0.8469635627530365, 0.9489878542510122, 0.9481781376518219, 0.9497975708502024]
            y = [1.2458333333333331, 1.3291666666666666, 1.1598958333333331, 1.1364583333333331, 1.2276041666666666, 1.0479166666666666, 1.0036458333333333, 1.0947916666666666, 0.9151041666666666, 1.0114583333333333, 1.1078125, 0.9098958333333333, 0.9151041666666666, 1.00625, 0.8239583333333333, 0.9411458333333333, 1.0348958333333333, 0.85, 0.88125, 0.9645833333333333, 0.7979166666666666, 0.94375, 1.0348958333333333, 0.85, 0.9463541666666666, 1.0296875, 0.8630208333333333, 0.9125, 0.9828125, 0.8395833333333333]

        elif "d05-x01-y01" in path:

            x = [0.04959128065395094, 0.04877384196185283, 0.04877384196185283, 0.14850136239782016, 0.14931880108991827, 0.15013623978201635, 0.2474114441416894, 0.2506811989100818, 0.24904632152588557, 0.3471389645776567, 0.34959128065395095, 0.3479564032697548, 0.4493188010899183, 0.4501362397820164, 0.4501362397820164, 0.5498637602179837, 0.5498637602179837, 0.5490463215258856, 0.649591280653951, 0.6512261580381472, 0.648773841961853, 0.7501362397820164, 0.7501362397820164, 0.7493188010899183, 0.8498637602179837, 0.8490463215258857, 0.8490463215258857, 0.9504087193460491, 0.9520435967302454, 0.949591280653951]
            y = [1.0934036939313985, 1.1778364116094986, 1.0089709762532981, 1.024802110817942, 1.1118733509234828, 0.9271767810026386, 1.0775725593667547, 1.1804749340369391, 0.9773087071240105, 1.0696569920844325, 1.1646437994722953, 0.9641160949868073, 1.0617414248021109, 1.1620052770448548, 0.9641160949868073, 1.0749340369393139, 1.1699208443271767, 0.9799472295514511, 1.0828496042216358, 1.1699208443271767, 0.9957783641160949, 1.067018469656992, 1.146174142480211, 0.9852242744063324, 1.0696569920844325, 1.1329815303430077, 0.9984168865435357, 1.0116094986807387, 1.096042216358839, 0.9192612137203167]   
     
        else:
            # don't have data for this one.
            continue
            
        ao.rmAnnotation("ErrorBreakdown")
        ao.setPath("/THY/"+path[5:])

        # get rid of some of the spurious precision
        x = list(np.around(np.array(x),4))
        y = list(np.around(np.array(y),4))

        # list of pairs
        points = sorted(zip(x, y))

        # check we have the right number of points"
        nBins = len(ao.points())
        if not nBins == len(points)/3.0:
            cfg.contur_log.error("Mismatched number of points in {}, {} vs {}".format(path,nBins,len(points)/3.0))
            continue
            
        counter=0                
        for point in ao.points():
            # for each x value we have an upper, central and lower value. Get them and order them.
            yvals = sorted([points[counter][1],points[counter+1][1],points[counter+2][1]])

            # central value
            point.setY(point.y()*yvals[1])

            # uncertainty
            uncertainty_up   = (yvals[2]-yvals[1])*point.y()
            uncertainty_down = (yvals[1]-yvals[0])*point.y()                
            point.setYErrs(uncertainty_up, uncertainty_down)

            counter=counter+3


        anaObjects.append(ao)

        
    yoda.write(anaObjects, a_name+"-Theory.yoda")
