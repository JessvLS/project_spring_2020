from __future__ import print_function
import unittest
try:
    unittest.skip
except AttributeError:
    import unittest2 as unittest
import doctest
import os
import commands
import cPickle
from StringIO import StringIO
import subprocess
import sys

try:
    import pysam
except ImportError:
    pysam = None

import vcf
from vcf import model, utils

IS_PYTHON2 = sys.version_info[0] == 2
IS_NOT_PYPY = 'PyPy' not in sys.version

suite = doctest.DocTestSuite(vcf)


def fh(fname, mode='rt'):
    return open(os.path.join(os.path.dirname(__file__), fname), mode)


class TestVcfSpecs(unittest.TestCase):

    def test_vcf_4_0(self):
        reader = vcf.Reader(fh('example-4.0.vcf'))
        self.assertEqual(reader.metadata['fileformat'], 'VCFv4.0')

        # test we can walk the file at least
        for r in reader:

            if r.POS == 1230237:
                assert r.is_monomorphic
            else:
                assert not r.is_monomorphic

            if 'AF' in r.INFO:
                self.assertEqual(type(r.INFO['AF']),  type([]))

            for c in r:
                assert c

                # issue 19, in the example ref the GQ is length 1
                if c.called:
                    self.assertEqual(type(c.data.GQ),  type(1))
                    if 'HQ' in c.data and c.data.HQ is not None:
                        self.assertEqual(type(c.data.HQ),  type([]))



    def test_vcf_4_1(self):
        reader = vcf.Reader(fh('example-4.1.vcf'))
        self.assertEqual(reader.metadata['fileformat'],  'VCFv4.1')

        # contigs were added in vcf4.1
        self.assertEqual(reader.contigs['20'].length, 62435964)

        # test we can walk the file at least
        for r in reader:
            for c in r:
                assert c

    def test_vcf_4_1_sv(self):
        reader = vcf.Reader(fh('example-4.1-sv.vcf'))

        assert 'SVLEN' in reader.infos
        assert 'fileDate' in reader.metadata
        assert 'DEL' in reader.alts

        # test we can walk the file at least
        for r in reader:
            print(r)
            for a in r.ALT:
                print(a)
            for c in r:
                print(c)
                assert c

    def test_vcf_4_1_bnd(self):
        reader = vcf.Reader(fh('example-4.1-bnd.vcf'))

        # test we can walk the file at least
        for r in reader:
            print(r)
            for a in r.ALT:
                print(a)
            if r.ID == "bnd1":
                    self.assertEqual(len(r.ALT), 1)
                    self.assertEqual(r.ALT[0].type, "BND")
                    self.assertEqual(r.ALT[0].chr, "2")
                    self.assertEqual(r.ALT[0].pos, 3)
                    self.assertEqual(r.ALT[0].orientation, False)
                    self.assertEqual(r.ALT[0].remoteOrientation, True)
                    self.assertEqual(r.ALT[0].connectingSequence, "T")
            if r.ID == "bnd4":
                    self.assertEqual(len(r.ALT), 1)
                    self.assertEqual(r.ALT[0].type, "BND")
                    self.assertEqual(r.ALT[0].chr, "1")
                    self.assertEqual(r.ALT[0].pos, 2)
                    self.assertEqual(r.ALT[0].orientation, True)
                    self.assertEqual(r.ALT[0].remoteOrientation, False)
                    self.assertEqual(r.ALT[0].connectingSequence, "G")
            for c in r:
                print(c)
                assert c

    def test_vcf_4_2(self):
        reader = vcf.Reader(fh('example-4.2.vcf'))
        self.assertEqual(reader.metadata['fileformat'],  'VCFv4.2')

        # If INFO contains no Source and Version keys, they should be None.
        self.assertEqual(reader.infos['DP'].source, None)
        self.assertEqual(reader.infos['DP'].version, None)

        # According to spec, INFO Version key is required to be double quoted,
        # but at least SAMtools 1.0 does not quote it. So we want to be
        # forgiving here.
        self.assertEqual(reader.infos['VDB'].source, None)
        self.assertEqual(reader.infos['VDB'].version, '3')

        # test we can walk the file at least
        for r in reader:
            for c in r:
                assert c

    def test_contig_idonly(self):
        """Test VCF inputs with ##contig inputs containing only IDs. produced by bcftools 1.2+
        """
        reader = vcf.Reader(fh("contig_idonly.vcf"))
        for cid, contig in reader.contigs.items():
            if cid == "1":
                assert contig.length is None
            elif cid == "2":
                assert contig.length == 2000
            elif cid == "3":
                assert contig.length == 3000

class TestGatkOutput(unittest.TestCase):

    filename = 'gatk.vcf'

    samples = ['BLANK', 'NA12878', 'NA12891', 'NA12892',
            'NA19238', 'NA19239', 'NA19240']
    formats = ['AD', 'DP', 'GQ', 'GT', 'PL']
    infos = ['AC', 'AF', 'AN', 'BaseQRankSum', 'DB', 'DP', 'DS',
            'Dels', 'FS', 'HRun', 'HaplotypeScore', 'InbreedingCoeff',
            'MQ', 'MQ0', 'MQRankSum', 'QD', 'ReadPosRankSum']

    n_calls = 37

    def setUp(self):
        self.reader = vcf.Reader(fh(self.filename))

    def testSamples(self):
        self.assertEqual(self.reader.samples, self.samples)

    def testFormats(self):
        self.assertEqual(set(self.reader.formats), set(self.formats))

    def testInfos(self):
        self.assertEqual(set(self.reader.infos), set(self.infos))


    def testCalls(self):
        n = 0

        for site in self.reader:
            n += 1
            self.assertEqual(len(site.samples), len(self.samples))


            # check sample name lookup
            for s in self.samples:
                assert site.genotype(s)

            # check ordered access
            self.assertEqual([x.sample for x in site.samples], self.samples)

        self.assertEqual(n,  self.n_calls)
