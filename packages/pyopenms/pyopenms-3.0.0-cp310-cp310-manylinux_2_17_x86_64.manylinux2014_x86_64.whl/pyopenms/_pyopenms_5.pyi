from __future__ import annotations
from typing import overload, Any, List, Dict, Tuple, Set, Sequence, Union
from pyopenms import *  # pylint: disable=wildcard-import; lgtm(py/polluting-import)
import numpy as _np

from enum import Enum as _PyEnum


def __static_ExperimentalDesign_fromConsensusMap(c: ConsensusMap ) -> ExperimentalDesign:
    """
    Cython signature: ExperimentalDesign fromConsensusMap(ConsensusMap c)
    """
    ...

def __static_ExperimentalDesign_fromFeatureMap(f: FeatureMap ) -> ExperimentalDesign:
    """
    Cython signature: ExperimentalDesign fromFeatureMap(FeatureMap f)
    """
    ...

def __static_ExperimentalDesign_fromIdentifications(proteins: List[ProteinIdentification] ) -> ExperimentalDesign:
    """
    Cython signature: ExperimentalDesign fromIdentifications(libcpp_vector[ProteinIdentification] & proteins)
    """
    ...

def __static_FeatureFinderAlgorithmPicked_getProductName() -> Union[bytes, str, String]:
    """
    Cython signature: String getProductName()
    """
    ...

def __static_LibSVMEncoder_predictPeptideRT(sequences: List[bytes] , svm: SVMWrapper , allowed_characters: Union[bytes, str, String] , maximum_sequence_length: int ) -> List[float]:
    """
    Cython signature: libcpp_vector[double] predictPeptideRT(libcpp_vector[String] sequences, const SVMWrapper & svm, const String & allowed_characters, unsigned int maximum_sequence_length)
    """
    ...

def __static_SpectrumHelper_removePeaks(p: MSChromatogram , pos_start: float , pos_end: float ) -> None:
    """
    Cython signature: void removePeaks(MSChromatogram & p, double pos_start, double pos_end)
    """
    ...

def __static_SpectrumHelper_removePeaks(p: MSSpectrum , pos_start: float , pos_end: float ) -> None:
    """
    Cython signature: void removePeaks(MSSpectrum & p, double pos_start, double pos_end)
    """
    ...

def __static_SpectrumHelper_subtractMinimumIntensity(p: MSChromatogram ) -> None:
    """
    Cython signature: void subtractMinimumIntensity(MSChromatogram & p)
    """
    ...

def __static_SpectrumHelper_subtractMinimumIntensity(p: MSSpectrum ) -> None:
    """
    Cython signature: void subtractMinimumIntensity(MSSpectrum & p)
    """
    ...


class AAIndex:
    """
    Cython implementation of _AAIndex

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AAIndex.html>`_
    """
    
    def aliphatic(self, aa: bytes ) -> float:
        """
        Cython signature: double aliphatic(char aa)
        """
        ...
    
    def acidic(self, aa: bytes ) -> float:
        """
        Cython signature: double acidic(char aa)
        """
        ...
    
    def basic(self, aa: bytes ) -> float:
        """
        Cython signature: double basic(char aa)
        """
        ...
    
    def polar(self, aa: bytes ) -> float:
        """
        Cython signature: double polar(char aa)
        """
        ...
    
    def getKHAG800101(self, aa: bytes ) -> float:
        """
        Cython signature: double getKHAG800101(char aa)
        """
        ...
    
    def getVASM830103(self, aa: bytes ) -> float:
        """
        Cython signature: double getVASM830103(char aa)
        """
        ...
    
    def getNADH010106(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010106(char aa)
        """
        ...
    
    def getNADH010107(self, aa: bytes ) -> float:
        """
        Cython signature: double getNADH010107(char aa)
        """
        ...
    
    def getWILM950102(self, aa: bytes ) -> float:
        """
        Cython signature: double getWILM950102(char aa)
        """
        ...
    
    def getROBB760107(self, aa: bytes ) -> float:
        """
        Cython signature: double getROBB760107(char aa)
        """
        ...
    
    def getOOBM850104(self, aa: bytes ) -> float:
        """
        Cython signature: double getOOBM850104(char aa)
        """
        ...
    
    def getFAUJ880111(self, aa: bytes ) -> float:
        """
        Cython signature: double getFAUJ880111(char aa)
        """
        ...
    
    def getFINA770101(self, aa: bytes ) -> float:
        """
        Cython signature: double getFINA770101(char aa)
        """
        ...
    
    def getARGP820102(self, aa: bytes ) -> float:
        """
        Cython signature: double getARGP820102(char aa)
        """
        ...
    
    def calculateGB(self, seq: AASequence , T: float ) -> float:
        """
        Cython signature: double calculateGB(AASequence & seq, double T)
        """
        ... 


class AbsoluteQuantitationStandardsFile:
    """
    Cython implementation of _AbsoluteQuantitationStandardsFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1AbsoluteQuantitationStandardsFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: AbsoluteQuantitationStandardsFile ) -> None:
        """
        Cython signature: void AbsoluteQuantitationStandardsFile(AbsoluteQuantitationStandardsFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , run_concentrations: List[AQS_runConcentration] ) -> None:
        """
        Cython signature: void load(const String & filename, libcpp_vector[AQS_runConcentration] & run_concentrations)
        """
        ... 


class Attachment:
    """
    Cython implementation of _Attachment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::QcMLFile_1_1Attachment.html>`_
    """
    
    name: Union[bytes, str, String]
    
    id: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    cvRef: Union[bytes, str, String]
    
    cvAcc: Union[bytes, str, String]
    
    unitRef: Union[bytes, str, String]
    
    unitAcc: Union[bytes, str, String]
    
    binary: Union[bytes, str, String]
    
    qualityRef: Union[bytes, str, String]
    
    colTypes: List[bytes]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Attachment()
        """
        ...
    
    @overload
    def __init__(self, in_0: Attachment ) -> None:
        """
        Cython signature: void Attachment(Attachment &)
        """
        ...
    
    def toXMLString(self, indentation_level: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String toXMLString(unsigned int indentation_level)
        """
        ...
    
    def toCSVString(self, separator: Union[bytes, str, String] ) -> Union[bytes, str, String]:
        """
        Cython signature: String toCSVString(String separator)
        """
        ...
    
    def __richcmp__(self, other: Attachment, op: int) -> Any:
        ... 


class BoxElement:
    """
    Cython implementation of _BoxElement

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1BoxElement.html>`_
    """
    
    mz: float
    
    c: int
    
    score: float
    
    intens: float
    
    ref_intens: float
    
    RT: float
    
    RT_index: int
    
    MZ_begin: int
    
    MZ_end: int 


class CVMappingTerm:
    """
    Cython implementation of _CVMappingTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CVMappingTerm.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CVMappingTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: CVMappingTerm ) -> None:
        """
        Cython signature: void CVMappingTerm(CVMappingTerm &)
        """
        ...
    
    def setAccession(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccession(String accession)
        Sets the accession string of the term
        """
        ...
    
    def getAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getAccession()
        Returns the accession string of the term
        """
        ...
    
    def setUseTermName(self, use_term_name: bool ) -> None:
        """
        Cython signature: void setUseTermName(bool use_term_name)
        Sets whether the term name should be used, instead of the accession
        """
        ...
    
    def getUseTermName(self) -> bool:
        """
        Cython signature: bool getUseTermName()
        Returns whether the term name should be used, instead of the accession
        """
        ...
    
    def setUseTerm(self, use_term: bool ) -> None:
        """
        Cython signature: void setUseTerm(bool use_term)
        Sets whether the term itself can be used (or only its children)
        """
        ...
    
    def getUseTerm(self) -> bool:
        """
        Cython signature: bool getUseTerm()
        Returns true if the term can be used, false if only children are allowed
        """
        ...
    
    def setTermName(self, term_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermName(String term_name)
        Sets the name of the term
        """
        ...
    
    def getTermName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermName()
        Returns the name of the term
        """
        ...
    
    def setIsRepeatable(self, is_repeatable: bool ) -> None:
        """
        Cython signature: void setIsRepeatable(bool is_repeatable)
        Sets whether this term can be repeated
        """
        ...
    
    def getIsRepeatable(self) -> bool:
        """
        Cython signature: bool getIsRepeatable()
        Returns true if this term can be repeated, false otherwise
        """
        ...
    
    def setAllowChildren(self, allow_children: bool ) -> None:
        """
        Cython signature: void setAllowChildren(bool allow_children)
        Sets whether children of this term are allowed
        """
        ...
    
    def getAllowChildren(self) -> bool:
        """
        Cython signature: bool getAllowChildren()
        Returns true if the children of this term are allowed to be used
        """
        ...
    
    def setCVIdentifierRef(self, cv_identifier_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCVIdentifierRef(String cv_identifier_ref)
        Sets the CV identifier reference string, e.g. UO for unit obo
        """
        ...
    
    def getCVIdentifierRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCVIdentifierRef()
        Returns the CV identifier reference string
        """
        ...
    
    def __richcmp__(self, other: CVMappingTerm, op: int) -> Any:
        ... 


class CompNovoIdentification:
    """
    Cython implementation of _CompNovoIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CompNovoIdentification.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CompNovoIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: CompNovoIdentification ) -> None:
        """
        Cython signature: void CompNovoIdentification(CompNovoIdentification &)
        """
        ...
    
    def getIdentifications(self, ids: List[PeptideIdentification] , in_1: MSExperiment ) -> None:
        """
        Cython signature: void getIdentifications(libcpp_vector[PeptideIdentification] & ids, MSExperiment)
        Performs and returns de novo identifications
        """
        ...
    
    def getIdentification(self, id: PeptideIdentification , cid_spec: MSSpectrum , etd_spec: MSSpectrum ) -> None:
        """
        Cython signature: void getIdentification(PeptideIdentification & id, MSSpectrum cid_spec, MSSpectrum etd_spec)
        Performs and returns de novo identifications
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class CompNovoIonScoringCID:
    """
    Cython implementation of _CompNovoIonScoringCID

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1CompNovoIonScoringCID.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void CompNovoIonScoringCID()
        """
        ...
    
    @overload
    def __init__(self, in_0: CompNovoIonScoringCID ) -> None:
        """
        Cython signature: void CompNovoIonScoringCID(CompNovoIonScoringCID &)
        """
        ... 


class DTA2DFile:
    """
    Cython implementation of _DTA2DFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DTA2DFile.html>`_
      -- Inherits from ['ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DTA2DFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: DTA2DFile ) -> None:
        """
        Cython signature: void DTA2DFile(DTA2DFile &)
        """
        ...
    
    def storeTIC(self, filename: Union[bytes, str, String] , peakmap: MSExperiment ) -> None:
        """
        Cython signature: void storeTIC(String filename, MSExperiment & peakmap)
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , peakmap: MSExperiment ) -> None:
        """
        Cython signature: void store(String filename, MSExperiment & peakmap)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , peakmap: MSExperiment ) -> None:
        """
        Cython signature: void load(String filename, MSExperiment & peakmap)
        """
        ...
    
    def getOptions(self) -> PeakFileOptions:
        """
        Cython signature: PeakFileOptions getOptions()
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class DataProcessing:
    """
    Cython implementation of _DataProcessing

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DataProcessing.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DataProcessing()
        """
        ...
    
    @overload
    def __init__(self, in_0: DataProcessing ) -> None:
        """
        Cython signature: void DataProcessing(DataProcessing &)
        """
        ...
    
    def setProcessingActions(self, in_0: Set[int] ) -> None:
        """
        Cython signature: void setProcessingActions(libcpp_set[ProcessingAction])
        """
        ...
    
    def getProcessingActions(self) -> Set[int]:
        """
        Cython signature: libcpp_set[ProcessingAction] getProcessingActions()
        """
        ...
    
    def getSoftware(self) -> Software:
        """
        Cython signature: Software getSoftware()
        """
        ...
    
    def setSoftware(self, s: Software ) -> None:
        """
        Cython signature: void setSoftware(Software s)
        """
        ...
    
    def getCompletionTime(self) -> DateTime:
        """
        Cython signature: DateTime getCompletionTime()
        """
        ...
    
    def setCompletionTime(self, t: DateTime ) -> None:
        """
        Cython signature: void setCompletionTime(DateTime t)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: DataProcessing, op: int) -> Any:
        ...
    ProcessingAction : __ProcessingAction 


class Date:
    """
    Cython implementation of _Date

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Date.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Date()
        """
        ...
    
    @overload
    def __init__(self, in_0: Date ) -> None:
        """
        Cython signature: void Date(Date &)
        """
        ...
    
    def set(self, date: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void set(const String & date)
        """
        ...
    
    def today(self) -> Date:
        """
        Cython signature: Date today()
        """
        ...
    
    def get(self) -> Union[bytes, str, String]:
        """
        Cython signature: String get()
        """
        ...
    
    def clear(self) -> None:
        """
        Cython signature: void clear()
        """
        ... 


class DeNovoIonScore:
    """
    Cython implementation of _DeNovoIonScore

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1DeNovoIonScore.html>`_
    """
    
    score: float
    
    position: float
    
    index: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void DeNovoIonScore()
        """
        ...
    
    @overload
    def __init__(self, in_0: DeNovoIonScore ) -> None:
        """
        Cython signature: void DeNovoIonScore(DeNovoIonScore)
        """
        ... 


class EnzymaticDigestion:
    """
    Cython implementation of _EnzymaticDigestion

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1EnzymaticDigestion.html>`_

      Class for the enzymatic digestion of proteins
    
      Digestion can be performed using simple regular expressions, e.g. [KR] | [^P] for trypsin.
      Also missed cleavages can be modeled, i.e. adjacent peptides are not cleaved
      due to enzyme malfunction/access restrictions. If n missed cleavages are allowed, all possible resulting
      peptides (cleaved and uncleaved) with up to n missed cleavages are returned.
      Thus no random selection of just n specific missed cleavage sites is performed.
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void EnzymaticDigestion()
        """
        ...
    
    @overload
    def __init__(self, in_0: EnzymaticDigestion ) -> None:
        """
        Cython signature: void EnzymaticDigestion(EnzymaticDigestion &)
        """
        ...
    
    def getMissedCleavages(self) -> int:
        """
        Cython signature: size_t getMissedCleavages()
        Returns the max. number of allowed missed cleavages for the digestion
        """
        ...
    
    def setMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setMissedCleavages(size_t missed_cleavages)
        Sets the max. number of allowed missed cleavages for the digestion (default is 0). This setting is ignored when log model is used
        """
        ...
    
    def countInternalCleavageSites(self, sequence: Union[bytes, str, String] ) -> int:
        """
        Cython signature: size_t countInternalCleavageSites(String sequence)
        Returns the number of internal cleavage sites for this sequence.
        """
        ...
    
    def getEnzymeName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getEnzymeName()
        Returns the enzyme for the digestion
        """
        ...
    
    def setEnzyme(self, enzyme: DigestionEnzyme ) -> None:
        """
        Cython signature: void setEnzyme(DigestionEnzyme * enzyme)
        Sets the enzyme for the digestion
        """
        ...
    
    def getSpecificity(self) -> int:
        """
        Cython signature: Specificity getSpecificity()
        Returns the specificity for the digestion
        """
        ...
    
    def setSpecificity(self, spec: int ) -> None:
        """
        Cython signature: void setSpecificity(Specificity spec)
        Sets the specificity for the digestion (default is SPEC_FULL)
        """
        ...
    
    def getSpecificityByName(self, name: Union[bytes, str, String] ) -> int:
        """
        Cython signature: Specificity getSpecificityByName(String name)
        Returns the specificity by name. Returns SPEC_UNKNOWN if name is not valid
        """
        ...
    
    def digestUnmodified(self, sequence: StringView , output: List[StringView] , min_length: int , max_length: int ) -> int:
        """
        Cython signature: size_t digestUnmodified(StringView sequence, libcpp_vector[StringView] & output, size_t min_length, size_t max_length)
        Performs the enzymatic digestion of an unmodified sequence\n
        By returning only references into the original string this is very fast
        
        
        :param sequence: Sequence to digest
        :param output: Digestion products
        :param min_length: Minimal length of reported products
        :param max_length: Maximal length of reported products (0 = no restriction)
        :return: Number of discarded digestion products (which are not matching length restrictions)
        """
        ...
    
    def isValidProduct(self, sequence: Union[bytes, str, String] , pos: int , length: int , ignore_missed_cleavages: bool ) -> bool:
        """
        Cython signature: bool isValidProduct(String sequence, int pos, int length, bool ignore_missed_cleavages)
        Boolean operator returns true if the peptide fragment starting at position `pos` with length `length` within the sequence `sequence` generated by the current enzyme\n
        Checks if peptide is a valid digestion product of the enzyme, taking into account specificity and the MC flag provided here
        
        
        :param protein: Protein sequence
        :param pep_pos: Starting index of potential peptide
        :param pep_length: Length of potential peptide
        :param ignore_missed_cleavages: Do not compare MC's of potential peptide to the maximum allowed MC's
        :return: True if peptide has correct n/c terminals (according to enzyme, specificity and missed cleavages)
        """
        ...
    Specificity : __Specificity 


class ExperimentalDesign:
    """
    Cython implementation of _ExperimentalDesign

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalDesign.html>`_

    Representation of an experimental design in OpenMS. Instances can be loaded with the ExperimentalDesignFile class
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalDesign()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalDesign ) -> None:
        """
        Cython signature: void ExperimentalDesign(ExperimentalDesign &)
        """
        ...
    
    def getMSFileSection(self) -> List[ExperimentalDesign_MSFileSectionEntry]:
        """
        Cython signature: libcpp_vector[ExperimentalDesign_MSFileSectionEntry] getMSFileSection()
        """
        ...
    
    def setMSFileSection(self, msfile_section: List[ExperimentalDesign_MSFileSectionEntry] ) -> None:
        """
        Cython signature: void setMSFileSection(libcpp_vector[ExperimentalDesign_MSFileSectionEntry] msfile_section)
        """
        ...
    
    def getSampleSection(self) -> ExperimentalDesign_SampleSection:
        """
        Cython signature: ExperimentalDesign_SampleSection getSampleSection()
        Returns the Sample Section of the experimental design file
        """
        ...
    
    def setSampleSection(self, sample_section: ExperimentalDesign_SampleSection ) -> None:
        """
        Cython signature: void setSampleSection(ExperimentalDesign_SampleSection sample_section)
        Sets the Sample Section of the experimental design file
        """
        ...
    
    def getNumberOfSamples(self) -> int:
        """
        Cython signature: unsigned int getNumberOfSamples()
        Returns the number of samples measured (= highest sample index)
        """
        ...
    
    def getNumberOfFractions(self) -> int:
        """
        Cython signature: unsigned int getNumberOfFractions()
        Returns the number of fractions (= highest fraction index)
        """
        ...
    
    def getNumberOfLabels(self) -> int:
        """
        Cython signature: unsigned int getNumberOfLabels()
        Returns the number of labels per file
        """
        ...
    
    def getNumberOfMSFiles(self) -> int:
        """
        Cython signature: unsigned int getNumberOfMSFiles()
        Returns the number of MS files (= fractions * fraction_groups)
        """
        ...
    
    def getNumberOfFractionGroups(self) -> int:
        """
        Cython signature: unsigned int getNumberOfFractionGroups()
        Allows to group fraction ids and source files. Return the number of fraction_groups
        """
        ...
    
    def getSample(self, fraction_group: int , label: int ) -> int:
        """
        Cython signature: unsigned int getSample(unsigned int fraction_group, unsigned int label)
        Returns sample index (depends on fraction_group and label)
        """
        ...
    
    def isFractionated(self) -> bool:
        """
        Cython signature: bool isFractionated()
        Returns whether at least one fraction_group in this experimental design is fractionated
        """
        ...
    
    def sameNrOfMSFilesPerFraction(self) -> bool:
        """
        Cython signature: bool sameNrOfMSFilesPerFraction()
        Returns if each fraction number is associated with the same number of fraction_group
        """
        ...
    
    fromConsensusMap: __static_ExperimentalDesign_fromConsensusMap
    
    fromFeatureMap: __static_ExperimentalDesign_fromFeatureMap
    
    fromIdentifications: __static_ExperimentalDesign_fromIdentifications 


class ExperimentalDesign_MSFileSectionEntry:
    """
    Cython implementation of _ExperimentalDesign_MSFileSectionEntry

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalDesign_MSFileSectionEntry.html>`_
    """
    
    path: bytes
    
    fraction_group: int
    
    fraction: int
    
    label: int
    
    sample: int
    
    def __init__(self) -> None:
        """
        Cython signature: void ExperimentalDesign_MSFileSectionEntry()
        """
        ... 


class ExperimentalDesign_SampleSection:
    """
    Cython implementation of _ExperimentalDesign_SampleSection

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ExperimentalDesign_SampleSection.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ExperimentalDesign_SampleSection()
        """
        ...
    
    @overload
    def __init__(self, in_0: ExperimentalDesign_SampleSection ) -> None:
        """
        Cython signature: void ExperimentalDesign_SampleSection(ExperimentalDesign_SampleSection)
        """
        ...
    
    def getSamples(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSamples()
        Returns a set of all samples that are present in the sample section
        """
        ...
    
    def getFactors(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getFactors()
        Returns a set of all factors (column names) that were defined for the sample section
        """
        ...
    
    def hasSample(self, sample: int ) -> bool:
        """
        Cython signature: bool hasSample(unsigned int sample)
        Checks whether sample section has row for a sample number
        """
        ...
    
    def hasFactor(self, factor: String ) -> bool:
        """
        Cython signature: bool hasFactor(String & factor)
        Checks whether Sample Section has a specific factor (i.e. column name)
        """
        ...
    
    def getFactorValue(self, sample: int , factor: String ) -> Union[bytes, str, String]:
        """
        Cython signature: String getFactorValue(unsigned int sample, String & factor)
        Returns value of factor for given sample and factor name
        """
        ... 


class FeatureFinderAlgorithmPicked:
    """
    Cython implementation of _FeatureFinderAlgorithmPicked

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderAlgorithmPicked.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureFinderAlgorithmPicked()
        """
        ...
    
    def setData(self, input: MSExperiment , output: FeatureMap , ff: FeatureFinder ) -> None:
        """
        Cython signature: void setData(MSExperiment & input, FeatureMap & output, FeatureFinder & ff)
        """
        ...
    
    def run(self) -> None:
        """
        Cython signature: void run()
        """
        ...
    
    def setSeeds(self, seeds: FeatureMap ) -> None:
        """
        Cython signature: void setSeeds(FeatureMap & seeds)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    getProductName: __static_FeatureFinderAlgorithmPicked_getProductName 


class FeatureFinderMultiplexAlgorithm:
    """
    Cython implementation of _FeatureFinderMultiplexAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureFinderMultiplexAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm()
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureFinderMultiplexAlgorithm ) -> None:
        """
        Cython signature: void FeatureFinderMultiplexAlgorithm(FeatureFinderMultiplexAlgorithm &)
        """
        ...
    
    def run(self, exp: MSExperiment , progress: bool ) -> None:
        """
        Cython signature: void run(MSExperiment & exp, bool progress)
        Main method for feature detection
        """
        ...
    
    def getFeatureMap(self) -> FeatureMap:
        """
        Cython signature: FeatureMap getFeatureMap()
        """
        ...
    
    def getConsensusMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getConsensusMap()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithm:
    """
    Cython implementation of _FeatureGroupingAlgorithm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithm.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes in this method
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithmLabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmLabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmLabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmLabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes in this method
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureGroupingAlgorithmUnlabeled:
    """
    Cython implementation of _FeatureGroupingAlgorithmUnlabeled

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureGroupingAlgorithmUnlabeled.html>`_
      -- Inherits from ['FeatureGroupingAlgorithm']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void FeatureGroupingAlgorithmUnlabeled()
        """
        ...
    
    def group(self, maps: List[FeatureMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void group(libcpp_vector[FeatureMap] & maps, ConsensusMap & out)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        """
        ...
    
    def addToGroup(self, map_id: int , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void addToGroup(int map_id, FeatureMap feature_map)
        """
        ...
    
    def setReference(self, map_id: int , map: FeatureMap ) -> None:
        """
        Cython signature: void setReference(int map_id, FeatureMap map)
        """
        ...
    
    def getResultMap(self) -> ConsensusMap:
        """
        Cython signature: ConsensusMap getResultMap()
        """
        ...
    
    def transferSubelements(self, maps: List[ConsensusMap] , out: ConsensusMap ) -> None:
        """
        Cython signature: void transferSubelements(libcpp_vector[ConsensusMap] maps, ConsensusMap & out)
        Transfers subelements (grouped features) from input consensus maps to the result consensus map
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes in this method
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class FeatureHandle:
    """
    Cython implementation of _FeatureHandle

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1FeatureHandle.html>`_
      -- Inherits from ['Peak2D', 'UniqueIdInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void FeatureHandle()
        Representation of a Peak2D, RichPeak2D or Feature
        """
        ...
    
    @overload
    def __init__(self, in_0: FeatureHandle ) -> None:
        """
        Cython signature: void FeatureHandle(FeatureHandle &)
        """
        ...
    
    @overload
    def __init__(self, map_index: int , point: Peak2D , element_index: int ) -> None:
        """
        Cython signature: void FeatureHandle(uint64_t map_index, Peak2D & point, uint64_t element_index)
        """
        ...
    
    def getMapIndex(self) -> int:
        """
        Cython signature: uint64_t getMapIndex()
        Returns the map index
        """
        ...
    
    def setMapIndex(self, i: int ) -> None:
        """
        Cython signature: void setMapIndex(uint64_t i)
        Sets the map index
        """
        ...
    
    def setCharge(self, charge: int ) -> None:
        """
        Cython signature: void setCharge(int charge)
        Sets the charge
        """
        ...
    
    def getCharge(self) -> int:
        """
        Cython signature: int getCharge()
        Returns the charge
        """
        ...
    
    def setWidth(self, width: float ) -> None:
        """
        Cython signature: void setWidth(float width)
        Sets the width (FWHM)
        """
        ...
    
    def getWidth(self) -> float:
        """
        Cython signature: float getWidth()
        Returns the width (FWHM)
        """
        ...
    
    def getIntensity(self) -> float:
        """
        Cython signature: float getIntensity()
        Returns the data point intensity (height)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Returns the m/z coordinate (index 1)
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        Returns the RT coordinate (index 0)
        """
        ...
    
    def setIntensity(self, in_0: float ) -> None:
        """
        Cython signature: void setIntensity(float)
        Returns the data point intensity (height)
        """
        ...
    
    def getUniqueId(self) -> int:
        """
        Cython signature: size_t getUniqueId()
        Returns the unique id
        """
        ...
    
    def clearUniqueId(self) -> int:
        """
        Cython signature: size_t clearUniqueId()
        Clear the unique id. The new unique id will be invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def hasValidUniqueId(self) -> int:
        """
        Cython signature: size_t hasValidUniqueId()
        Returns whether the unique id is valid. Returns 1 if the unique id is valid, 0 otherwise
        """
        ...
    
    def hasInvalidUniqueId(self) -> int:
        """
        Cython signature: size_t hasInvalidUniqueId()
        Returns whether the unique id is invalid. Returns 1 if the unique id is invalid, 0 otherwise
        """
        ...
    
    def setUniqueId(self, rhs: int ) -> None:
        """
        Cython signature: void setUniqueId(uint64_t rhs)
        Assigns a new, valid unique id. Always returns 1
        """
        ...
    
    def ensureUniqueId(self) -> int:
        """
        Cython signature: size_t ensureUniqueId()
        Assigns a valid unique id, but only if the present one is invalid. Returns 1 if the unique id was changed, 0 otherwise
        """
        ...
    
    def isValid(self, unique_id: int ) -> bool:
        """
        Cython signature: bool isValid(uint64_t unique_id)
        Returns true if the unique_id is valid, false otherwise
        """
        ...
    
    def __richcmp__(self, other: FeatureHandle, op: int) -> Any:
        ... 


class HPLC:
    """
    Cython implementation of _HPLC

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1HPLC.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void HPLC()
        Representation of a HPLC experiment
        """
        ...
    
    @overload
    def __init__(self, in_0: HPLC ) -> None:
        """
        Cython signature: void HPLC(HPLC &)
        """
        ...
    
    def getInstrument(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInstrument()
        Returns a reference to the instument name
        """
        ...
    
    def setInstrument(self, instrument: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInstrument(String instrument)
        Sets the instument name
        """
        ...
    
    def getColumn(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getColumn()
        Returns a reference to the column description
        """
        ...
    
    def setColumn(self, column: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setColumn(String column)
        Sets the column description
        """
        ...
    
    def getTemperature(self) -> int:
        """
        Cython signature: int getTemperature()
        Returns the temperature (in degree C)
        """
        ...
    
    def setTemperature(self, temperature: int ) -> None:
        """
        Cython signature: void setTemperature(int temperature)
        Sets the temperature (in degree C)
        """
        ...
    
    def getPressure(self) -> int:
        """
        Cython signature: unsigned int getPressure()
        Returns the pressure (in bar)
        """
        ...
    
    def setPressure(self, pressure: int ) -> None:
        """
        Cython signature: void setPressure(unsigned int pressure)
        Sets the pressure (in bar)
        """
        ...
    
    def getFlux(self) -> int:
        """
        Cython signature: unsigned int getFlux()
        Returns the flux (in microliter/sec)
        """
        ...
    
    def setFlux(self, flux: int ) -> None:
        """
        Cython signature: void setFlux(unsigned int flux)
        Sets the flux (in microliter/sec)
        """
        ...
    
    def getComment(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getComment()
        Returns the comments
        """
        ...
    
    def setComment(self, comment: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setComment(String comment)
        Sets the comments
        """
        ...
    
    def getGradient(self) -> Gradient:
        """
        Cython signature: Gradient getGradient()
        Returns a mutable reference to the used gradient
        """
        ...
    
    def setGradient(self, gradient: Gradient ) -> None:
        """
        Cython signature: void setGradient(Gradient gradient)
        Sets the used gradient
        """
        ... 


class IDRipper:
    """
    Cython implementation of _IDRipper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IDRipper.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void IDRipper()
        Ripping protein/peptide identification according their file origin
        """
        ...
    
    def rip(self, rfis: List[RipFileIdentifier] , rfcs: List[RipFileContent] , proteins: List[ProteinIdentification] , peptides: List[PeptideIdentification] , full_split: bool , split_ident_runs: bool ) -> None:
        """
        Cython signature: void rip(libcpp_vector[RipFileIdentifier] & rfis, libcpp_vector[RipFileContent] & rfcs, libcpp_vector[ProteinIdentification] & proteins, libcpp_vector[PeptideIdentification] & peptides, bool full_split, bool split_ident_runs)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IdentificationRuns:
    """
    Cython implementation of _IdentificationRuns

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1IdentificationRuns.html>`_
    """
    
    def __init__(self, prot_ids: List[ProteinIdentification] ) -> None:
        """
        Cython signature: void IdentificationRuns(libcpp_vector[ProteinIdentification] & prot_ids)
        """
        ... 


class IncludeExcludeTarget:
    """
    Cython implementation of _IncludeExcludeTarget

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IncludeExcludeTarget.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IncludeExcludeTarget()
        This class stores a SRM/MRM transition
        """
        ...
    
    @overload
    def __init__(self, in_0: IncludeExcludeTarget ) -> None:
        """
        Cython signature: void IncludeExcludeTarget(IncludeExcludeTarget &)
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def setPeptideRef(self, peptide_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPeptideRef(const String & peptide_ref)
        """
        ...
    
    def getPeptideRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPeptideRef()
        """
        ...
    
    def setCompoundRef(self, compound_ref: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCompoundRef(const String & compound_ref)
        """
        ...
    
    def getCompoundRef(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCompoundRef()
        """
        ...
    
    def setPrecursorMZ(self, mz: float ) -> None:
        """
        Cython signature: void setPrecursorMZ(double mz)
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        """
        ...
    
    def setPrecursorCVTermList(self, list_: CVTermList ) -> None:
        """
        Cython signature: void setPrecursorCVTermList(CVTermList & list_)
        """
        ...
    
    def addPrecursorCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addPrecursorCVTerm(CVTerm & cv_term)
        """
        ...
    
    def getPrecursorCVTermList(self) -> CVTermList:
        """
        Cython signature: CVTermList getPrecursorCVTermList()
        """
        ...
    
    def setProductMZ(self, mz: float ) -> None:
        """
        Cython signature: void setProductMZ(double mz)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def setProductCVTermList(self, list_: CVTermList ) -> None:
        """
        Cython signature: void setProductCVTermList(CVTermList & list_)
        """
        ...
    
    def addProductCVTerm(self, cv_term: CVTerm ) -> None:
        """
        Cython signature: void addProductCVTerm(CVTerm & cv_term)
        """
        ...
    
    def getProductCVTermList(self) -> CVTermList:
        """
        Cython signature: CVTermList getProductCVTermList()
        """
        ...
    
    def setInterpretations(self, interpretations: List[CVTermList] ) -> None:
        """
        Cython signature: void setInterpretations(libcpp_vector[CVTermList] & interpretations)
        """
        ...
    
    def getInterpretations(self) -> List[CVTermList]:
        """
        Cython signature: libcpp_vector[CVTermList] getInterpretations()
        """
        ...
    
    def addInterpretation(self, interpretation: CVTermList ) -> None:
        """
        Cython signature: void addInterpretation(CVTermList & interpretation)
        """
        ...
    
    def setConfigurations(self, configuration: List[Configuration] ) -> None:
        """
        Cython signature: void setConfigurations(libcpp_vector[Configuration] & configuration)
        """
        ...
    
    def getConfigurations(self) -> List[Configuration]:
        """
        Cython signature: libcpp_vector[Configuration] getConfigurations()
        """
        ...
    
    def addConfiguration(self, configuration: Configuration ) -> None:
        """
        Cython signature: void addConfiguration(Configuration & configuration)
        """
        ...
    
    def setPrediction(self, prediction: CVTermList ) -> None:
        """
        Cython signature: void setPrediction(CVTermList & prediction)
        """
        ...
    
    def addPredictionTerm(self, prediction: CVTerm ) -> None:
        """
        Cython signature: void addPredictionTerm(CVTerm & prediction)
        """
        ...
    
    def getPrediction(self) -> CVTermList:
        """
        Cython signature: CVTermList getPrediction()
        """
        ...
    
    def setRetentionTime(self, rt: RetentionTime ) -> None:
        """
        Cython signature: void setRetentionTime(RetentionTime rt)
        """
        ...
    
    def getRetentionTime(self) -> RetentionTime:
        """
        Cython signature: RetentionTime getRetentionTime()
        """
        ...
    
    def setCVTerms(self, terms: List[CVTerm] ) -> None:
        """
        Cython signature: void setCVTerms(libcpp_vector[CVTerm] & terms)
        """
        ...
    
    def replaceCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void replaceCVTerm(CVTerm & term)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_terms: List[CVTerm] , accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_vector[CVTerm] cv_terms, String accession)
        """
        ...
    
    @overload
    def replaceCVTerms(self, cv_term_map: Dict[bytes,List[CVTerm]] ) -> None:
        """
        Cython signature: void replaceCVTerms(libcpp_map[String,libcpp_vector[CVTerm]] cv_term_map)
        """
        ...
    
    def getCVTerms(self) -> Dict[bytes,List[CVTerm]]:
        """
        Cython signature: libcpp_map[String,libcpp_vector[CVTerm]] getCVTerms()
        """
        ...
    
    def addCVTerm(self, term: CVTerm ) -> None:
        """
        Cython signature: void addCVTerm(CVTerm & term)
        """
        ...
    
    def hasCVTerm(self, accession: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool hasCVTerm(String accession)
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def __richcmp__(self, other: IncludeExcludeTarget, op: int) -> Any:
        ... 


class IndexTriple:
    """
    Cython implementation of _IndexTriple

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IndexTriple.html>`_
    """
    
    feature: int
    
    scan: int
    
    variable: int
    
    rt_probability: float
    
    signal_weight: float
    
    prot_acc: Union[bytes, str, String]
    
    def __init__(self) -> None:
        """
        Cython signature: void IndexTriple()
        """
        ... 


class IntensityBalanceFilter:
    """
    Cython implementation of _IntensityBalanceFilter

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IntensityBalanceFilter.html>`_
      -- Inherits from ['FilterFunctor']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IntensityBalanceFilter()
        It divides the m/z-range into ten regions and sums the intensity in these region
        """
        ...
    
    @overload
    def __init__(self, in_0: IntensityBalanceFilter ) -> None:
        """
        Cython signature: void IntensityBalanceFilter(IntensityBalanceFilter &)
        """
        ...
    
    def apply(self, in_0: MSSpectrum ) -> float:
        """
        Cython signature: double apply(MSSpectrum &)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IsobaricIsotopeCorrector:
    """
    Cython implementation of _IsobaricIsotopeCorrector

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricIsotopeCorrector.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector()
        """
        ...
    
    @overload
    def __init__(self, in_0: IsobaricIsotopeCorrector ) -> None:
        """
        Cython signature: void IsobaricIsotopeCorrector(IsobaricIsotopeCorrector &)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqEightPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: ItraqFourPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTSixPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def correctIsotopicImpurities(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap , quant_method: TMTTenPlexQuantitationMethod ) -> IsobaricQuantifierStatistics:
        """
        Cython signature: IsobaricQuantifierStatistics correctIsotopicImpurities(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out, TMTTenPlexQuantitationMethod * quant_method)
        """
        ... 


class IsobaricQuantifier:
    """
    Cython implementation of _IsobaricQuantifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsobaricQuantifier.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, in_0: IsobaricQuantifier ) -> None:
        """
        Cython signature: void IsobaricQuantifier(IsobaricQuantifier &)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqFourPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqFourPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: ItraqEightPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(ItraqEightPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTSixPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTSixPlexQuantitationMethod * quant_method)
        """
        ...
    
    @overload
    def __init__(self, quant_method: TMTTenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void IsobaricQuantifier(TMTTenPlexQuantitationMethod * quant_method)
        """
        ...
    
    def quantify(self, consensus_map_in: ConsensusMap , consensus_map_out: ConsensusMap ) -> None:
        """
        Cython signature: void quantify(ConsensusMap & consensus_map_in, ConsensusMap & consensus_map_out)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class IsotopeWaveletTransform:
    """
    Cython implementation of _IsotopeWaveletTransform[_Peak1D]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1IsotopeWaveletTransform[_Peak1D].html>`_
    """
    
    @overload
    def __init__(self, min_mz: float , max_mz: float , max_charge: int , max_scan_size: int , hr_data: bool , intenstype: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void IsotopeWaveletTransform(double min_mz, double max_mz, unsigned int max_charge, size_t max_scan_size, bool hr_data, String intenstype)
        """
        ...
    
    @overload
    def __init__(self, in_0: IsotopeWaveletTransform ) -> None:
        """
        Cython signature: void IsotopeWaveletTransform(IsotopeWaveletTransform &)
        """
        ...
    
    def getTransform(self, c_trans: MSSpectrum , c_ref: MSSpectrum , c: int ) -> None:
        """
        Cython signature: void getTransform(MSSpectrum & c_trans, MSSpectrum & c_ref, unsigned int c)
        Computes the isotope wavelet transform of charge state `c`
        
        
        :param c_trans: The transform
        :param c_ref: The reference spectrum
        :param c: The charge state minus 1 (e.g. c=2 means charge state 3) at which you want to compute the transform
        """
        ...
    
    def getTransformHighRes(self, c_trans: MSSpectrum , c_ref: MSSpectrum , c: int ) -> None:
        """
        Cython signature: void getTransformHighRes(MSSpectrum & c_trans, MSSpectrum & c_ref, unsigned int c)
        Computes the isotope wavelet transform of charge state `c`
        
        
        :param c_trans: The transform
        :param c_ref: The reference spectrum
        :param c: The charge state minus 1 (e.g. c=2 means charge state 3) at which you want to compute the transform
        """
        ...
    
    def identifyCharge(self, candidates: MSSpectrum , ref: MSSpectrum , scan_index: int , c: int , ampl_cutoff: float , check_PPMs: bool ) -> None:
        """
        Cython signature: void identifyCharge(MSSpectrum & candidates, MSSpectrum & ref, unsigned int scan_index, unsigned int c, double ampl_cutoff, bool check_PPMs)
        Given an isotope wavelet transformed spectrum 'candidates', this function assigns to every significant
        pattern its corresponding charge state and a score indicating the reliability of the prediction. The result of this
        process is stored internally. Important: Before calling this function, apply updateRanges() to the original map
        
        
        :param candidates: A isotope wavelet transformed spectrum. Entry "number i" in this vector must correspond to the
            charge-"(i-1)"-transform of its mass signal. (This is exactly the output of the function `getTransforms`.)
        :param ref: The reference scan (the untransformed raw data) corresponding to `candidates`
        :param c: The corresponding charge state minus 1 (e.g. c=2 means charge state 3)
        :param scan_index: The index of the scan (w.r.t. to some map) currently under consideration
        :param ampl_cutoff: The thresholding parameter. This parameter is the only (and hence a really important)
            parameter of the isotope wavelet transform. On the basis of `ampl_cutoff` the program tries to distinguish between
            noise and signal. Please note that it is not a "simple" hard thresholding parameter in the sense of drawing a virtual
            line in the spectrum, which is then used as a guillotine cut. Maybe you should play around a bit with this parameter to
            get a feeling about its range. For peptide mass fingerprints on small data sets (like single MALDI-scans e.g.), it
            makes sense to start `ampl_cutoff=0` or even `ampl_cutoff=-1`,
            indicating no thresholding at all. Note that also ampl_cutoff=0 triggers (a moderate) thresholding based on the
            average intensity in the wavelet transform
        :param check_PPMs: If enabled, the algorithm will check each monoisotopic mass candidate for its plausibility
            by computing the ppm difference between this mass and the averagine model
        """
        ...
    
    def initializeScan(self, c_ref: MSSpectrum , c: int ) -> None:
        """
        Cython signature: void initializeScan(MSSpectrum & c_ref, unsigned int c)
        """
        ...
    
    def updateBoxStates(self, map_: MSExperiment , scan_index: int , RT_interleave: int , RT_votes_cutoff: int , front_bound: int , end_bound: int ) -> None:
        """
        Cython signature: void updateBoxStates(MSExperiment & map_, size_t scan_index, unsigned int RT_interleave, unsigned int RT_votes_cutoff, int front_bound, int end_bound)
        A function keeping track of currently open and closed sweep line boxes
        This function is used by the isotope wavelet feature finder and must be called for each processed scan
        
        
        :param map: The original map containing the data set to be analyzed
        :param scan_index: The index of the scan currently under consideration w.r.t. its MS map
            This information is necessary to sweep across the map after each scan has been evaluated
        :param RT_votes_cutoff: See the IsotopeWaveletFF class
        """
        ...
    
    def mapSeeds2Features(self, map_: MSExperiment , RT_votes_cutoff: int ) -> FeatureMap:
        """
        Cython signature: FeatureMap mapSeeds2Features(MSExperiment & map_, unsigned int RT_votes_cutoff)
        Filters the candidates further more and maps the internally used data structures to the OpenMS framework
        
        
        :param map: The original map containing the data set to be analyzed
        :param max_charge: The maximal charge state under consideration
        :param RT_votes_cutoff: See the IsotopeWaveletFF class
        """
        ...
    
    def getLinearInterpolation(self, mz_a: float , intens_a: float , mz_pos: float , mz_b: float , intens_b: float ) -> float:
        """
        Cython signature: double getLinearInterpolation(double mz_a, double intens_a, double mz_pos, double mz_b, double intens_b)
        Computes a linear (intensity) interpolation
        
        
        :param mz_a: The m/z value of the point left to the query
        :param intens_a: The intensity value of the point left to the query
        :param mz_pos: The query point
        :param mz_b: The m/z value of the point right to the query
        :param intens_b: The intensity value of the point left to the query
        """
        ...
    
    def getSigma(self) -> float:
        """
        Cython signature: double getSigma()
        """
        ...
    
    def setSigma(self, sigma: float ) -> None:
        """
        Cython signature: void setSigma(double sigma)
        """
        ...
    
    def computeMinSpacing(self, c_ref: MSSpectrum ) -> None:
        """
        Cython signature: void computeMinSpacing(MSSpectrum & c_ref)
        """
        ...
    
    def getMinSpacing(self) -> float:
        """
        Cython signature: double getMinSpacing()
        """
        ...
    
    def getMaxScanSize(self) -> int:
        """
        Cython signature: size_t getMaxScanSize()
        """
        ... 


class KroenikFile:
    """
    Cython implementation of _KroenikFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1KroenikFile.html>`_

    File adapter for Kroenik (HardKloer sibling) files
    
    The first line is the header and contains the column names:
    File,  First Scan,  Last Scan,  Num of Scans,  Charge,  Monoisotopic Mass,  Base Isotope Peak,  Best Intensity,  Summed Intensity,  First RTime,  Last RTime,  Best RTime,  Best Correlation,  Modifications
    
    Every subsequent line is a feature
    
    All properties in the file are converted to Feature properties, whereas "First Scan", "Last Scan", "Num of Scans" and "Modifications" are stored as
    metavalues with the following names "FirstScan", "LastScan", "NumOfScans" and "AveragineModifications"
    
    The width in m/z of the overall convex hull of each feature is set to 3 Th in lack of a value provided by the Kroenik file
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void KroenikFile()
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void store(String filename, MSSpectrum & spectrum)
        Stores a MSExperiment into a Kroenik file
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , feature_map: FeatureMap ) -> None:
        """
        Cython signature: void load(String filename, FeatureMap & feature_map)
        Loads a Kroenik file into a featureXML
        
        The content of the file is stored in `features`
        
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class LibSVMEncoder:
    """
    Cython implementation of _LibSVMEncoder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1LibSVMEncoder.html>`_

    Serves for encoding sequences into feature vectors
    
    The class can be used to construct composition vectors for
    sequences. Additionally the vectors can be encoded into
    the libsvm format
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LibSVMEncoder()
        """
        ...
    
    @overload
    def __init__(self, in_0: LibSVMEncoder ) -> None:
        """
        Cython signature: void LibSVMEncoder(LibSVMEncoder &)
        """
        ...
    
    predictPeptideRT: __static_LibSVMEncoder_predictPeptideRT 


class LightCompound:
    """
    Cython implementation of _LightCompound

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightCompound.html>`_
    """
    
    rt: float
    
    drift_time: float
    
    charge: int
    
    sequence: bytes
    
    protein_refs: List[bytes]
    
    peptide_group_label: bytes
    
    id: bytes
    
    sum_formula: bytes
    
    compound_name: bytes
    
    modifications: List[LightModification]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightCompound()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightCompound ) -> None:
        """
        Cython signature: void LightCompound(LightCompound &)
        """
        ...
    
    def setDriftTime(self, d: float ) -> None:
        """
        Cython signature: void setDriftTime(double d)
        """
        ...
    
    def getDriftTime(self) -> float:
        """
        Cython signature: double getDriftTime()
        """
        ...
    
    def getChargeState(self) -> int:
        """
        Cython signature: int getChargeState()
        """
        ...
    
    def isPeptide(self) -> bool:
        """
        Cython signature: bool isPeptide()
        """
        ...
    
    def setChargeState(self, ch: int ) -> None:
        """
        Cython signature: void setChargeState(int ch)
        """
        ... 


class LightModification:
    """
    Cython implementation of _LightModification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightModification.html>`_
    """
    
    location: int
    
    unimod_id: int
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightModification()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightModification ) -> None:
        """
        Cython signature: void LightModification(LightModification &)
        """
        ... 


class LightProtein:
    """
    Cython implementation of _LightProtein

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightProtein.html>`_
    """
    
    id: bytes
    
    sequence: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightProtein()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightProtein ) -> None:
        """
        Cython signature: void LightProtein(LightProtein &)
        """
        ... 


class LightTargetedExperiment:
    """
    Cython implementation of _LightTargetedExperiment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTargetedExperiment.html>`_
    """
    
    transitions: List[LightTransition]
    
    compounds: List[LightCompound]
    
    proteins: List[LightProtein]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTargetedExperiment()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTargetedExperiment ) -> None:
        """
        Cython signature: void LightTargetedExperiment(LightTargetedExperiment &)
        """
        ...
    
    def getTransitions(self) -> List[LightTransition]:
        """
        Cython signature: libcpp_vector[LightTransition] getTransitions()
        """
        ...
    
    def getCompounds(self) -> List[LightCompound]:
        """
        Cython signature: libcpp_vector[LightCompound] getCompounds()
        """
        ...
    
    def getProteins(self) -> List[LightProtein]:
        """
        Cython signature: libcpp_vector[LightProtein] getProteins()
        """
        ...
    
    def getCompoundByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getCompoundByRef(libcpp_string & ref)
        """
        ...
    
    def getPeptideByRef(self, ref: bytes ) -> LightCompound:
        """
        Cython signature: LightCompound getPeptideByRef(libcpp_string & ref)
        """
        ... 


class LightTransition:
    """
    Cython implementation of _LightTransition

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1LightTransition.html>`_
    """
    
    transition_name: bytes
    
    peptide_ref: bytes
    
    library_intensity: float
    
    product_mz: float
    
    precursor_mz: float
    
    fragment_charge: int
    
    decoy: bool
    
    detecting_transition: bool
    
    quantifying_transition: bool
    
    identifying_transition: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void LightTransition()
        """
        ...
    
    @overload
    def __init__(self, in_0: LightTransition ) -> None:
        """
        Cython signature: void LightTransition(LightTransition &)
        """
        ...
    
    def getProductChargeState(self) -> int:
        """
        Cython signature: int getProductChargeState()
        """
        ...
    
    def isProductChargeStateSet(self) -> bool:
        """
        Cython signature: bool isProductChargeStateSet()
        """
        ...
    
    def getNativeID(self) -> bytes:
        """
        Cython signature: libcpp_string getNativeID()
        """
        ...
    
    def getPeptideRef(self) -> bytes:
        """
        Cython signature: libcpp_string getPeptideRef()
        """
        ...
    
    def getLibraryIntensity(self) -> float:
        """
        Cython signature: double getLibraryIntensity()
        """
        ...
    
    def setLibraryIntensity(self, l: float ) -> None:
        """
        Cython signature: void setLibraryIntensity(double l)
        """
        ...
    
    def getProductMZ(self) -> float:
        """
        Cython signature: double getProductMZ()
        """
        ...
    
    def getPrecursorMZ(self) -> float:
        """
        Cython signature: double getPrecursorMZ()
        """
        ...
    
    def getCompoundRef(self) -> bytes:
        """
        Cython signature: libcpp_string getCompoundRef()
        """
        ...
    
    def setDetectingTransition(self, d: bool ) -> None:
        """
        Cython signature: void setDetectingTransition(bool d)
        """
        ...
    
    def isDetectingTransition(self) -> bool:
        """
        Cython signature: bool isDetectingTransition()
        """
        ...
    
    def setQuantifyingTransition(self, q: bool ) -> None:
        """
        Cython signature: void setQuantifyingTransition(bool q)
        """
        ...
    
    def isQuantifyingTransition(self) -> bool:
        """
        Cython signature: bool isQuantifyingTransition()
        """
        ...
    
    def setIdentifyingTransition(self, i: bool ) -> None:
        """
        Cython signature: void setIdentifyingTransition(bool i)
        """
        ...
    
    def isIdentifyingTransition(self) -> bool:
        """
        Cython signature: bool isIdentifyingTransition()
        """
        ... 


class MRMMapping:
    """
    Cython implementation of _MRMMapping

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MRMMapping.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MRMMapping()
        """
        ...
    
    def mapExperiment(self, input_chromatograms: MSExperiment , targeted_exp: TargetedExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void mapExperiment(MSExperiment input_chromatograms, TargetedExperiment targeted_exp, MSExperiment & output)
        Maps input chromatograms to assays in a targeted experiment
        
        The output chromatograms are an annotated copy of the input chromatograms
        with native id, precursor information and peptide sequence (if available)
        annotated in the chromatogram files
        
        The algorithm tries to match a given set of chromatograms and targeted
        assays. It iterates through all the chromatograms retrieves one or more
        matching targeted assay for the chromatogram. By default, the algorithm
        assumes that a 1:1 mapping exists. If a chromatogram cannot be mapped
        (does not have a corresponding assay) the algorithm issues a warning, the
        user can specify that the program should abort in such a case (see
        error_on_unmapped)
        
        :note If multiple mapping is enabled (see map_multiple_assays parameter)
        then each mapped assay will get its own chromatogram that contains the
        same raw data but different meta-annotation. This *can* be useful if the
        same transition is used to monitor multiple analytes but may also
        indicate a problem with too wide mapping tolerances
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MapAlignmentAlgorithmSpectrumAlignment:
    """
    Cython implementation of _MapAlignmentAlgorithmSpectrumAlignment

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentAlgorithmSpectrumAlignment.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void MapAlignmentAlgorithmSpectrumAlignment()
        """
        ...
    
    def align(self, in_0: List[MSExperiment] , in_1: List[TransformationDescription] ) -> None:
        """
        Cython signature: void align(libcpp_vector[MSExperiment] &, libcpp_vector[TransformationDescription] &)
        Align peak maps
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class MapAlignmentTransformer:
    """
    Cython implementation of _MapAlignmentTransformer

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MapAlignmentTransformer.html>`_

    This class collects functions for applying retention time transformations to data structures
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MapAlignmentTransformer()
        """
        ...
    
    @overload
    def __init__(self, in_0: MapAlignmentTransformer ) -> None:
        """
        Cython signature: void MapAlignmentTransformer(MapAlignmentTransformer &)
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: MSExperiment , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(MSExperiment &, TransformationDescription &, bool)
        Applies the given transformation to a peak map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: FeatureMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(FeatureMap &, TransformationDescription &, bool)
        Applies the given transformation to a feature map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: ConsensusMap , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(ConsensusMap &, TransformationDescription &, bool)
        Applies the given transformation to a consensus map
        """
        ...
    
    @overload
    def transformRetentionTimes(self, in_0: List[PeptideIdentification] , in_1: TransformationDescription , in_2: bool ) -> None:
        """
        Cython signature: void transformRetentionTimes(libcpp_vector[PeptideIdentification] &, TransformationDescription &, bool)
        Applies the given transformation to peptide identifications
        """
        ... 


class MarkerMower:
    """
    Cython implementation of _MarkerMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MarkerMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MarkerMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: MarkerMower ) -> None:
        """
        Cython signature: void MarkerMower(MarkerMower &)
        """
        ...
    
    def filterSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        Returns the product name
        """
        ...
    
    def insertmarker(self, peak_marker: PeakMarker ) -> None:
        """
        Cython signature: void insertmarker(PeakMarker * peak_marker)
        Insert new Marker (violates the DefaultParamHandler interface)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class MetaInfoDescription:
    """
    Cython implementation of _MetaInfoDescription

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1MetaInfoDescription.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void MetaInfoDescription()
        """
        ...
    
    @overload
    def __init__(self, in_0: MetaInfoDescription ) -> None:
        """
        Cython signature: void MetaInfoDescription(MetaInfoDescription &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name of the peak annotations
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(String name)
        Sets the name of the peak annotations
        """
        ...
    
    def getDataProcessing(self) -> List[DataProcessing]:
        """
        Cython signature: libcpp_vector[shared_ptr[DataProcessing]] getDataProcessing()
        Returns a reference to the description of the applied processing
        """
        ...
    
    def setDataProcessing(self, in_0: List[DataProcessing] ) -> None:
        """
        Cython signature: void setDataProcessing(libcpp_vector[shared_ptr[DataProcessing]])
        Sets the description of the applied processing
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: MetaInfoDescription, op: int) -> Any:
        ... 


class NoiseEstimator:
    """
    Cython implementation of _NoiseEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1NoiseEstimator.html>`_
    """
    
    nr_windows: int
    
    mz_start: float
    
    window_length: float
    
    result_windows_even: List[float]
    
    result_windows_odd: List[float]
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void NoiseEstimator()
        """
        ...
    
    @overload
    def __init__(self, in_0: NoiseEstimator ) -> None:
        """
        Cython signature: void NoiseEstimator(NoiseEstimator &)
        """
        ...
    
    @overload
    def __init__(self, nr_windows_: float , mz_start_: float , win_len_: float ) -> None:
        """
        Cython signature: void NoiseEstimator(double nr_windows_, double mz_start_, double win_len_)
        """
        ...
    
    def get_noise_value(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_value(double mz)
        """
        ...
    
    def get_noise_even(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_even(double mz)
        """
        ...
    
    def get_noise_odd(self, mz: float ) -> float:
        """
        Cython signature: double get_noise_odd(double mz)
        """
        ... 


class OMSSACSVFile:
    """
    Cython implementation of _OMSSACSVFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OMSSACSVFile.html>`_

    File adapter for OMSSACSV files
    
    The files contain the results of the OMSSA algorithm in a comma separated manner. This file adapter is able to
    load the data from such a file into the structures of OpenMS
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OMSSACSVFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: OMSSACSVFile ) -> None:
        """
        Cython signature: void OMSSACSVFile(OMSSACSVFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , protein_identification: ProteinIdentification , id_data: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void load(const String & filename, ProteinIdentification & protein_identification, libcpp_vector[PeptideIdentification] & id_data)
        Loads a OMSSA file
        
        The content of the file is stored in `features`
        
        
        :param filename: The name of the file to read from
        :param protein_identification: The protein ProteinIdentification data
        :param id_data: The peptide ids of the file
        :raises:
          Exception: FileNotFound is thrown if the file could not be opened
        :raises:
          Exception: ParseError is thrown if an error occurs during parsing
        """
        ... 


class OSBinaryDataArray:
    """
    Cython implementation of _OSBinaryDataArray

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSBinaryDataArray.html>`_
    """
    
    data: List[float]
    
    description: bytes
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSBinaryDataArray()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSBinaryDataArray ) -> None:
        """
        Cython signature: void OSBinaryDataArray(OSBinaryDataArray &)
        """
        ... 


class OSChromatogram:
    """
    Cython implementation of _OSChromatogram

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSChromatogram.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSChromatogram()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSChromatogram ) -> None:
        """
        Cython signature: void OSChromatogram(OSChromatogram &)
        """
        ... 


class OSSpectrum:
    """
    Cython implementation of _OSSpectrum

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenSwath_1_1OSSpectrum.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OSSpectrum()
        """
        ...
    
    @overload
    def __init__(self, in_0: OSSpectrum ) -> None:
        """
        Cython signature: void OSSpectrum(OSSpectrum &)
        """
        ... 


class OSWFile:
    """
    Cython implementation of _OSWFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OSWFile.html>`_

    This class serves for reading in and writing OpenSWATH OSW files
    
    See OpenSwathOSWWriter for more functionality
    
    The reader and writer returns data in a format suitable for PercolatorAdapter.
    OSW files have a flexible data structure. They contain all peptide query
    parameters of TraML/PQP files with the detected and quantified features of
    OpenSwathWorkflow (feature, feature_ms1, feature_ms2 & feature_transition)
    
    The OSWFile reader extracts the feature information from the OSW file for
    each level (MS1, MS2 & transition) separately and generates Percolator input
    files. For each of the three Percolator reports, OSWFile writer adds a table
    (score_ms1, score_ms2, score_transition) with the respective confidence metrics.
    These tables can be mapped to the corresponding feature tables, are very similar
    to PyProphet results and can thus be used interchangeably
    """
    
    @overload
    def __init__(self, filename: Union[bytes, str] ) -> None:
        """
        Cython signature: void OSWFile(const libcpp_utf8_string filename)
        """
        ...
    
    @overload
    def __init__(self, in_0: OSWFile ) -> None:
        """
        Cython signature: void OSWFile(OSWFile &)
        """
        ... 


class OpenSwathDataAccessHelper:
    """
    Cython implementation of _OpenSwathDataAccessHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1OpenSwathDataAccessHelper.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper()
        """
        ...
    
    @overload
    def __init__(self, in_0: OpenSwathDataAccessHelper ) -> None:
        """
        Cython signature: void OpenSwathDataAccessHelper(OpenSwathDataAccessHelper &)
        """
        ...
    
    def convertToOpenMSSpectrum(self, sptr: OSSpectrum , spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void convertToOpenMSSpectrum(shared_ptr[OSSpectrum] sptr, MSSpectrum & spectrum)
        Converts a SpectrumPtr to an OpenMS Spectrum
        """
        ...
    
    def convertToOpenMSChromatogram(self, cptr: OSChromatogram , chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogram(shared_ptr[OSChromatogram] cptr, MSChromatogram & chromatogram)
        Converts a ChromatogramPtr to an OpenMS Chromatogram
        """
        ...
    
    def convertToOpenMSChromatogramFilter(self, chromatogram: MSChromatogram , cptr: OSChromatogram , rt_min: float , rt_max: float ) -> None:
        """
        Cython signature: void convertToOpenMSChromatogramFilter(MSChromatogram & chromatogram, shared_ptr[OSChromatogram] cptr, double rt_min, double rt_max)
        """
        ...
    
    def convertTargetedExp(self, transition_exp_: TargetedExperiment , transition_exp: LightTargetedExperiment ) -> None:
        """
        Cython signature: void convertTargetedExp(TargetedExperiment & transition_exp_, LightTargetedExperiment & transition_exp)
        Converts from the OpenMS TargetedExperiment to the OpenMs LightTargetedExperiment
        """
        ...
    
    def convertPeptideToAASequence(self, peptide: LightCompound , aa_sequence: AASequence ) -> None:
        """
        Cython signature: void convertPeptideToAASequence(LightCompound & peptide, AASequence & aa_sequence)
        Converts from the LightCompound to an OpenMS AASequence (with correct modifications)
        """
        ...
    
    def convertTargetedCompound(self, pep: Peptide , p: LightCompound ) -> None:
        """
        Cython signature: void convertTargetedCompound(Peptide pep, LightCompound & p)
        Converts from the OpenMS TargetedExperiment Peptide to the LightTargetedExperiment Peptide
        """
        ... 


class PSLPFormulation:
    """
    Cython implementation of _PSLPFormulation

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PSLPFormulation.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PSLPFormulation()
        """
        ...
    
    @overload
    def __init__(self, in_0: PSLPFormulation ) -> None:
        """
        Cython signature: void PSLPFormulation(PSLPFormulation &)
        """
        ...
    
    def createAndSolveILPForKnownLCMSMapFeatureBased(self, features: FeatureMap , experiment: MSExperiment , variable_indices: List[IndexTriple] , mass_ranges: List[List[List[int, int]]] , charges_set: Set[int] , ms2_spectra_per_rt_bin: int , solution_indices: List[int] ) -> None:
        """
        Cython signature: void createAndSolveILPForKnownLCMSMapFeatureBased(FeatureMap & features, MSExperiment & experiment, libcpp_vector[IndexTriple] & variable_indices, libcpp_vector[libcpp_vector[libcpp_pair[size_t,size_t]]] & mass_ranges, libcpp_set[int] & charges_set, unsigned int ms2_spectra_per_rt_bin, libcpp_vector[int] & solution_indices)
        Encode ILP formulation for a given LC-MS map, but unknown protein sample
        
        
        :param features: FeatureMap with all possible precursors
        :param experiment: Input raw data
        :param variable_indices: Assignment of feature indices and ILP variables
        :param mass_ranges: Feature borders as indices in the raw data
        :param charges_set: Allowed charge states
        :param ms2_spectra_per_rt_bin: Allowed number of precursors per rt bin
        :param solution_indices: Indices of ILP variables that are in the optimal solution
        """
        ...
    
    def createAndSolveILPForInclusionListCreation(self, preprocessing: PrecursorIonSelectionPreprocessing , ms2_spectra_per_rt_bin: int , max_list_size: int , precursors: FeatureMap , solve_ILP: bool ) -> None:
        """
        Cython signature: void createAndSolveILPForInclusionListCreation(PrecursorIonSelectionPreprocessing & preprocessing, unsigned int ms2_spectra_per_rt_bin, unsigned int max_list_size, FeatureMap & precursors, bool solve_ILP)
        Find a set of precursors, so that the protein coverage is maximal and that the number of precursors per bin is not exceeded
        """
        ...
    
    def updateStepSizeConstraint(self, iteration: int , step_size: int ) -> None:
        """
        Cython signature: void updateStepSizeConstraint(size_t iteration, unsigned int step_size)
        """
        ...
    
    def updateRTConstraintsForSequentialILP(self, rt_index: int , ms2_spectra_per_rt_bin: int , max_rt_index: int ) -> None:
        """
        Cython signature: void updateRTConstraintsForSequentialILP(size_t & rt_index, unsigned int ms2_spectra_per_rt_bin, size_t max_rt_index)
        """
        ...
    
    def solveILP(self, solution_indices: List[int] ) -> None:
        """
        Cython signature: void solveILP(libcpp_vector[int] & solution_indices)
        Solve the ILP
        """
        ...
    
    def setLPSolver(self, solver: int ) -> None:
        """
        Cython signature: void setLPSolver(SOLVER solver)
        """
        ...
    
    def getLPSolver(self) -> int:
        """
        Cython signature: SOLVER getLPSolver()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class ParamValue:
    """
    Cython implementation of _ParamValue

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ParamValue.html>`_

    Class to hold strings, numeric values, vectors of strings and vectors of numeric values using the stl types
    
    - To choose one of these types, just use the appropriate constructor
    - Automatic conversion is supported and throws Exceptions in case of invalid conversions
    - An empty object is created with the default constructor
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ParamValue()
        """
        ...
    
    @overload
    def __init__(self, in_0: ParamValue ) -> None:
        """
        Cython signature: void ParamValue(ParamValue &)
        """
        ...
    
    @overload
    def __init__(self, in_0: bytes ) -> None:
        """
        Cython signature: void ParamValue(char *)
        """
        ...
    
    @overload
    def __init__(self, in_0: Union[bytes, str] ) -> None:
        """
        Cython signature: void ParamValue(const libcpp_utf8_string &)
        """
        ...
    
    @overload
    def __init__(self, in_0: int ) -> None:
        """
        Cython signature: void ParamValue(int)
        """
        ...
    
    @overload
    def __init__(self, in_0: float ) -> None:
        """
        Cython signature: void ParamValue(double)
        """
        ...
    
    @overload
    def __init__(self, in_0: List[Union[bytes, str]] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[libcpp_utf8_string])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[int] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[int])
        """
        ...
    
    @overload
    def __init__(self, in_0: List[float] ) -> None:
        """
        Cython signature: void ParamValue(libcpp_vector[double])
        """
        ...
    
    def toStringVector(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[libcpp_string] toStringVector()
        Explicitly convert ParamValue to string vector
        """
        ...
    
    def toDoubleVector(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] toDoubleVector()
        Explicitly convert ParamValue to DoubleList
        """
        ...
    
    def toIntVector(self) -> List[int]:
        """
        Cython signature: libcpp_vector[int] toIntVector()
        Explicitly convert ParamValue to IntList
        """
        ...
    
    def toBool(self) -> bool:
        """
        Cython signature: bool toBool()
        Converts the strings 'true' and 'false' to a bool
        """
        ...
    
    def valueType(self) -> int:
        """
        Cython signature: ValueType valueType()
        """
        ...
    
    def isEmpty(self) -> int:
        """
        Cython signature: int isEmpty()
        Test if the value is empty
        """
        ... 


class PeakMarker:
    """
    Cython implementation of _PeakMarker

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakMarker.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakMarker()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakMarker ) -> None:
        """
        Cython signature: void PeakMarker(PeakMarker &)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        Returns the product name
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class PeakPickerSH:
    """
    Cython implementation of _PeakPickerSH

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakPickerSH.html>`_
      -- Inherits from ['DefaultParamHandler', 'ProgressLogger']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakPickerSH()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakPickerSH ) -> None:
        """
        Cython signature: void PeakPickerSH(PeakPickerSH &)
        """
        ...
    
    def pick(self, input_: MSSpectrum , output: MSSpectrum , fWindowWidth: float ) -> None:
        """
        Cython signature: void pick(MSSpectrum & input_, MSSpectrum & output, float fWindowWidth)
        Applies the peak-picking algorithm to one spectrum
        """
        ...
    
    def pickExperiment(self, input_: MSExperiment , output: MSExperiment ) -> None:
        """
        Cython signature: void pickExperiment(MSExperiment & input_, MSExperiment & output)
        Applies the peak-picking algorithm to a map (MSExperiment)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class PeakTypeEstimator:
    """
    Cython implementation of _PeakTypeEstimator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeakTypeEstimator.html>`_

    Estimates if the data of a spectrum is raw data or peak data
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeakTypeEstimator()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeakTypeEstimator ) -> None:
        """
        Cython signature: void PeakTypeEstimator(PeakTypeEstimator &)
        """
        ... 


class PeptideIdentification:
    """
    Cython implementation of _PeptideIdentification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1PeptideIdentification.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void PeptideIdentification()
        """
        ...
    
    @overload
    def __init__(self, in_0: PeptideIdentification ) -> None:
        """
        Cython signature: void PeptideIdentification(PeptideIdentification &)
        """
        ...
    
    def getHits(self) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getHits()
        Returns the peptide hits as const
        """
        ...
    
    def insertHit(self, in_0: PeptideHit ) -> None:
        """
        Cython signature: void insertHit(PeptideHit)
        Appends a peptide hit
        """
        ...
    
    def setHits(self, in_0: List[PeptideHit] ) -> None:
        """
        Cython signature: void setHits(libcpp_vector[PeptideHit])
        Sets the peptide hits
        """
        ...
    
    def getSignificanceThreshold(self) -> float:
        """
        Cython signature: double getSignificanceThreshold()
        Returns the peptide significance threshold value
        """
        ...
    
    def setSignificanceThreshold(self, value: float ) -> None:
        """
        Cython signature: void setSignificanceThreshold(double value)
        Setting of the peptide significance threshold value
        """
        ...
    
    def getScoreType(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getScoreType()
        """
        ...
    
    def setScoreType(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setScoreType(String)
        """
        ...
    
    def isHigherScoreBetter(self) -> bool:
        """
        Cython signature: bool isHigherScoreBetter()
        """
        ...
    
    def setHigherScoreBetter(self, in_0: bool ) -> None:
        """
        Cython signature: void setHigherScoreBetter(bool)
        """
        ...
    
    def getIdentifier(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getIdentifier()
        """
        ...
    
    def setIdentifier(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setIdentifier(String)
        """
        ...
    
    def hasMZ(self) -> bool:
        """
        Cython signature: bool hasMZ()
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        """
        ...
    
    def hasRT(self) -> bool:
        """
        Cython signature: bool hasRT()
        """
        ...
    
    def getRT(self) -> float:
        """
        Cython signature: double getRT()
        """
        ...
    
    def setRT(self, in_0: float ) -> None:
        """
        Cython signature: void setRT(double)
        """
        ...
    
    def getBaseName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getBaseName()
        """
        ...
    
    def setBaseName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setBaseName(String)
        """
        ...
    
    def getExperimentLabel(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getExperimentLabel()
        """
        ...
    
    def setExperimentLabel(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setExperimentLabel(String)
        """
        ...
    
    def assignRanks(self) -> None:
        """
        Cython signature: void assignRanks()
        """
        ...
    
    def sort(self) -> None:
        """
        Cython signature: void sort()
        """
        ...
    
    def sortByRank(self) -> None:
        """
        Cython signature: void sortByRank()
        """
        ...
    
    def empty(self) -> bool:
        """
        Cython signature: bool empty()
        """
        ...
    
    def getReferencingHits(self, in_0: List[PeptideHit] , in_1: Set[bytes] ) -> List[PeptideHit]:
        """
        Cython signature: libcpp_vector[PeptideHit] getReferencingHits(libcpp_vector[PeptideHit], libcpp_set[String] &)
        Returns all peptide hits which reference to a given protein accession (i.e. filter by protein accession)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: PeptideIdentification, op: int) -> Any:
        ... 


class Product:
    """
    Cython implementation of _Product

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Product.html>`_

    This class describes the product isolation window for special scan types, such as MRM
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Product()
        """
        ...
    
    @overload
    def __init__(self, in_0: Product ) -> None:
        """
        Cython signature: void Product(Product &)
        """
        ...
    
    def getMZ(self) -> float:
        """
        Cython signature: double getMZ()
        Returns the target m/z
        """
        ...
    
    def setMZ(self, in_0: float ) -> None:
        """
        Cython signature: void setMZ(double)
        Sets the target m/z
        """
        ...
    
    def getIsolationWindowLowerOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowLowerOffset()
        Returns the lower offset from the target m/z
        """
        ...
    
    def setIsolationWindowLowerOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowLowerOffset(double bound)
        Sets the lower offset from the target m/z
        """
        ...
    
    def getIsolationWindowUpperOffset(self) -> float:
        """
        Cython signature: double getIsolationWindowUpperOffset()
        Returns the upper offset from the target m/z
        """
        ...
    
    def setIsolationWindowUpperOffset(self, bound: float ) -> None:
        """
        Cython signature: void setIsolationWindowUpperOffset(double bound)
        Sets the upper offset from the target m/z
        """
        ...
    
    def __richcmp__(self, other: Product, op: int) -> Any:
        ... 


class ProteinInference:
    """
    Cython implementation of _ProteinInference

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ProteinInference.html>`_

    [experimental class] given a peptide quantitation, infer corresponding protein quantities
    
    Infers protein ratios from peptide ratios (currently using unique peptides only).
    Use the IDMapper class to add protein and peptide information to a
    quantitative ConsensusMap prior to this step
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ProteinInference()
        """
        ...
    
    @overload
    def __init__(self, in_0: ProteinInference ) -> None:
        """
        Cython signature: void ProteinInference(ProteinInference &)
        """
        ...
    
    def infer(self, consensus_map: ConsensusMap , reference_map: int ) -> None:
        """
        Cython signature: void infer(ConsensusMap & consensus_map, unsigned int reference_map)
        Given a peptide quantitation, infer corresponding protein quantities
        
        Infers protein ratios from peptide ratios (currently using unique peptides only).
        Use the IDMapper class to add protein and peptide information to a
        quantitative ConsensusMap prior to this step
        
        
        :param consensus_map: Peptide quantitation with ProteinIdentifications attached, where protein quantitation will be attached
        :param reference_map: Index of (iTRAQ) reference channel within the consensus map
        """
        ... 


class QTClusterFinder:
    """
    Cython implementation of _QTClusterFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1QTClusterFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void QTClusterFinder()
        """
        ...
    
    @overload
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    @overload
    def run(self, input_maps: List[FeatureMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[FeatureMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        Returns the name of the product
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes here
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class RansacModelLinear:
    """
    Cython implementation of _RansacModelLinear

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Math_1_1RansacModelLinear.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void RansacModelLinear()
        """
        ...
    
    @overload
    def __init__(self, in_0: RansacModelLinear ) -> None:
        """
        Cython signature: void RansacModelLinear(RansacModelLinear &)
        """
        ... 


class ResidueModification:
    """
    Cython implementation of _ResidueModification

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ResidueModification.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ResidueModification()
        """
        ...
    
    @overload
    def __init__(self, in_0: ResidueModification ) -> None:
        """
        Cython signature: void ResidueModification(ResidueModification &)
        """
        ...
    
    def setId(self, id_: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setId(const String & id_)
        Sets the identifier of the modification
        """
        ...
    
    def getId(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getId()
        Returns the identifier of the modification
        """
        ...
    
    def setFullId(self, full_id: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFullId(const String & full_id)
        Sets the full identifier (Unimod Accession + origin, if available)
        """
        ...
    
    def getFullId(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFullId()
        """
        ...
    
    def getUniModRecordId(self) -> int:
        """
        Cython signature: int getUniModRecordId()
        Gets the unimod record id
        """
        ...
    
    def setUniModRecordId(self, id_: int ) -> None:
        """
        Cython signature: void setUniModRecordId(int id_)
        Sets the unimod record id
        """
        ...
    
    def getUniModAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getUniModAccession()
        Returns the unimod accession if available
        """
        ...
    
    def setPSIMODAccession(self, id_: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setPSIMODAccession(const String & id_)
        Sets the MOD-XXXXX accession of PSI-MOD
        """
        ...
    
    def getPSIMODAccession(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getPSIMODAccession()
        Returns the PSI-MOD accession if available
        """
        ...
    
    def setFullName(self, full_name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFullName(const String & full_name)
        Sets the full name of the modification; must NOT contain the origin (or . for terminals!)
        """
        ...
    
    def getFullName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFullName()
        Returns the full name of the modification
        """
        ...
    
    def setName(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String & name)
        Sets the name of modification
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the PSI-MS-label if available; e.g. Mascot uses this name
        """
        ...
    
    @overload
    def setTermSpecificity(self, term_spec: int ) -> None:
        """
        Cython signature: void setTermSpecificity(TermSpecificity term_spec)
        Sets the term specificity
        """
        ...
    
    @overload
    def setTermSpecificity(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTermSpecificity(const String & name)
        Sets the terminal specificity using a name
        """
        ...
    
    def getTermSpecificity(self) -> int:
        """
        Cython signature: TermSpecificity getTermSpecificity()
        Returns terminal specificity
        """
        ...
    
    def getTermSpecificityName(self, in_0: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getTermSpecificityName(TermSpecificity)
        Returns the name of the terminal specificity
        """
        ...
    
    def setOrigin(self, origin: bytes ) -> None:
        """
        Cython signature: void setOrigin(char origin)
        Sets the origin (i.e. modified amino acid)
        """
        ...
    
    def getOrigin(self) -> bytes:
        """
        Cython signature: char getOrigin()
        Returns the origin (i.e. modified amino acid)
        """
        ...
    
    @overload
    def setSourceClassification(self, classification: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setSourceClassification(const String & classification)
        Classification as defined by the PSI-MOD
        """
        ...
    
    @overload
    def setSourceClassification(self, classification: int ) -> None:
        """
        Cython signature: void setSourceClassification(SourceClassification classification)
        Sets the source classification
        """
        ...
    
    def getSourceClassification(self) -> int:
        """
        Cython signature: SourceClassification getSourceClassification()
        Returns the source classification, if none was set, it is unspecific
        """
        ...
    
    def getSourceClassificationName(self, classification: int ) -> Union[bytes, str, String]:
        """
        Cython signature: String getSourceClassificationName(SourceClassification classification)
        Returns the classification
        """
        ...
    
    def setAverageMass(self, mass: float ) -> None:
        """
        Cython signature: void setAverageMass(double mass)
        Sets the average mass
        """
        ...
    
    def getAverageMass(self) -> float:
        """
        Cython signature: double getAverageMass()
        Returns the average mass if set
        """
        ...
    
    def setMonoMass(self, mass: float ) -> None:
        """
        Cython signature: void setMonoMass(double mass)
        Sets the monoisotopic mass (this must include the weight of the residue itself!)
        """
        ...
    
    def getMonoMass(self) -> float:
        """
        Cython signature: double getMonoMass()
        Return the monoisotopic mass, or 0.0 if not set
        """
        ...
    
    def setDiffAverageMass(self, mass: float ) -> None:
        """
        Cython signature: void setDiffAverageMass(double mass)
        Sets the difference average mass
        """
        ...
    
    def getDiffAverageMass(self) -> float:
        """
        Cython signature: double getDiffAverageMass()
        Returns the difference average mass, or 0.0 if not set
        """
        ...
    
    def setDiffMonoMass(self, mass: float ) -> None:
        """
        Cython signature: void setDiffMonoMass(double mass)
        Sets the difference monoisotopic mass
        """
        ...
    
    def getDiffMonoMass(self) -> float:
        """
        Cython signature: double getDiffMonoMass()
        Returns the diff monoisotopic mass, or 0.0 if not set
        """
        ...
    
    def setFormula(self, composition: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setFormula(const String & composition)
        Sets the formula (no masses will be changed)
        """
        ...
    
    def getFormula(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getFormula()
        Returns the chemical formula if set
        """
        ...
    
    def setDiffFormula(self, diff_formula: EmpiricalFormula ) -> None:
        """
        Cython signature: void setDiffFormula(EmpiricalFormula & diff_formula)
        Sets diff formula (no masses will be changed)
        """
        ...
    
    def getDiffFormula(self) -> EmpiricalFormula:
        """
        Cython signature: EmpiricalFormula getDiffFormula()
        Returns the diff formula if one was set
        """
        ...
    
    def setSynonyms(self, synonyms: Set[bytes] ) -> None:
        """
        Cython signature: void setSynonyms(libcpp_set[String] & synonyms)
        Sets the synonyms of that modification
        """
        ...
    
    def addSynonym(self, synonym: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void addSynonym(const String & synonym)
        Adds a synonym to the unique list
        """
        ...
    
    def getSynonyms(self) -> Set[bytes]:
        """
        Cython signature: libcpp_set[String] getSynonyms()
        Returns the set of synonyms
        """
        ...
    
    def setNeutralLossDiffFormulas(self, diff_formulas: List[EmpiricalFormula] ) -> None:
        """
        Cython signature: void setNeutralLossDiffFormulas(libcpp_vector[EmpiricalFormula] & diff_formulas)
        Sets the neutral loss formula
        """
        ...
    
    def getNeutralLossDiffFormulas(self) -> List[EmpiricalFormula]:
        """
        Cython signature: libcpp_vector[EmpiricalFormula] getNeutralLossDiffFormulas()
        Returns the neutral loss diff formula (if available)
        """
        ...
    
    def setNeutralLossMonoMasses(self, mono_masses: List[float] ) -> None:
        """
        Cython signature: void setNeutralLossMonoMasses(libcpp_vector[double] mono_masses)
        Sets the neutral loss mono weight
        """
        ...
    
    def getNeutralLossMonoMasses(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getNeutralLossMonoMasses()
        Returns the neutral loss mono weight
        """
        ...
    
    def setNeutralLossAverageMasses(self, average_masses: List[float] ) -> None:
        """
        Cython signature: void setNeutralLossAverageMasses(libcpp_vector[double] average_masses)
        Sets the neutral loss average weight
        """
        ...
    
    def getNeutralLossAverageMasses(self) -> List[float]:
        """
        Cython signature: libcpp_vector[double] getNeutralLossAverageMasses()
        Returns the neutral loss average weight
        """
        ...
    
    def hasNeutralLoss(self) -> bool:
        """
        Cython signature: bool hasNeutralLoss()
        Returns true if a neutral loss formula is set
        """
        ...
    
    def isUserDefined(self) -> bool:
        """
        Cython signature: bool isUserDefined()
        Returns true if it is a user-defined modification (empty id)
        """
        ...
    
    def __richcmp__(self, other: ResidueModification, op: int) -> Any:
        ...
    SourceClassification : __SourceClassification
    TermSpecificity : __TermSpecificity 


class RipFileContent:
    """
    Cython implementation of _RipFileContent

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileContent.html>`_
    """
    
    def __init__(self, prot_idents: List[ProteinIdentification] , pep_idents: List[PeptideIdentification] ) -> None:
        """
        Cython signature: void RipFileContent(libcpp_vector[ProteinIdentification] & prot_idents, libcpp_vector[PeptideIdentification] & pep_idents)
        """
        ...
    
    def getProteinIdentifications(self) -> List[ProteinIdentification]:
        """
        Cython signature: libcpp_vector[ProteinIdentification] getProteinIdentifications()
        """
        ...
    
    def getPeptideIdentifications(self) -> List[PeptideIdentification]:
        """
        Cython signature: libcpp_vector[PeptideIdentification] getPeptideIdentifications()
        """
        ... 


class RipFileIdentifier:
    """
    Cython implementation of _RipFileIdentifier

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::IDRipper_1_1RipFileIdentifier.html>`_
    """
    
    def __init__(self, id_runs: IdentificationRuns , pep_id: PeptideIdentification , file_origin_map: Dict[Union[bytes, str, String], int] , origin_annotation_fmt: int , split_ident_runs: bool ) -> None:
        """
        Cython signature: void RipFileIdentifier(IdentificationRuns & id_runs, PeptideIdentification & pep_id, libcpp_map[String,unsigned int] & file_origin_map, OriginAnnotationFormat origin_annotation_fmt, bool split_ident_runs)
        """
        ...
    
    def getIdentRunIdx(self) -> int:
        """
        Cython signature: unsigned int getIdentRunIdx()
        """
        ...
    
    def getFileOriginIdx(self) -> int:
        """
        Cython signature: unsigned int getFileOriginIdx()
        """
        ...
    
    def getOriginFullname(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOriginFullname()
        """
        ...
    
    def getOutputBasename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputBasename()
        """
        ... 


class ScanWindow:
    """
    Cython implementation of _ScanWindow

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1ScanWindow.html>`_
      -- Inherits from ['MetaInfoInterface']
    """
    
    begin: float
    
    end: float
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void ScanWindow()
        """
        ...
    
    @overload
    def __init__(self, in_0: ScanWindow ) -> None:
        """
        Cython signature: void ScanWindow(ScanWindow &)
        """
        ...
    
    def isMetaEmpty(self) -> bool:
        """
        Cython signature: bool isMetaEmpty()
        Returns if the MetaInfo is empty
        """
        ...
    
    def clearMetaInfo(self) -> None:
        """
        Cython signature: void clearMetaInfo()
        Removes all meta values
        """
        ...
    
    def metaRegistry(self) -> MetaInfoRegistry:
        """
        Cython signature: MetaInfoRegistry metaRegistry()
        Returns a reference to the MetaInfoRegistry
        """
        ...
    
    def getKeys(self, keys: List[bytes] ) -> None:
        """
        Cython signature: void getKeys(libcpp_vector[String] & keys)
        Fills the given vector with a list of all keys for which a value is set
        """
        ...
    
    def getMetaValue(self, in_0: Union[bytes, str, String] ) -> Union[int, float, bytes, str, List[int], List[float], List[bytes]]:
        """
        Cython signature: DataValue getMetaValue(String)
        Returns the value corresponding to a string, or
        """
        ...
    
    def setMetaValue(self, in_0: Union[bytes, str, String] , in_1: Union[int, float, bytes, str, List[int], List[float], List[bytes]] ) -> None:
        """
        Cython signature: void setMetaValue(String, DataValue)
        Sets the DataValue corresponding to a name
        """
        ...
    
    def metaValueExists(self, in_0: Union[bytes, str, String] ) -> bool:
        """
        Cython signature: bool metaValueExists(String)
        Returns whether an entry with the given name exists
        """
        ...
    
    def removeMetaValue(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void removeMetaValue(String)
        Removes the DataValue corresponding to `name` if it exists
        """
        ...
    
    def __richcmp__(self, other: ScanWindow, op: int) -> Any:
        ... 


class SemanticValidator:
    """
    Cython implementation of _SemanticValidator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator.html>`_
    """
    
    def __init__(self, mapping: CVMappings , cv: ControlledVocabulary ) -> None:
        """
        Cython signature: void SemanticValidator(CVMappings mapping, ControlledVocabulary cv)
        """
        ...
    
    def validate(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool validate(String filename, StringList errors, StringList warnings)
        """
        ...
    
    def locateTerm(self, path: Union[bytes, str, String] , parsed_term: SemanticValidator_CVTerm ) -> bool:
        """
        Cython signature: bool locateTerm(String path, SemanticValidator_CVTerm & parsed_term)
        Checks if a CVTerm is allowed in a given path
        """
        ...
    
    def setTag(self, tag: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTag(String tag)
        Sets the CV parameter tag name (default 'cvParam')
        """
        ...
    
    def setAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setAccessionAttribute(String accession)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'accession')
        """
        ...
    
    def setNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setNameAttribute(String name)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'name')
        """
        ...
    
    def setValueAttribute(self, value: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setValueAttribute(String value)
        Sets the name of the attribute for accessions in the CV parameter tag name (default 'value')
        """
        ...
    
    def setCheckTermValueTypes(self, check: bool ) -> None:
        """
        Cython signature: void setCheckTermValueTypes(bool check)
        Sets if CV term value types should be check (enabled by default)
        """
        ...
    
    def setCheckUnits(self, check: bool ) -> None:
        """
        Cython signature: void setCheckUnits(bool check)
        Sets if CV term units should be check (disabled by default)
        """
        ...
    
    def setUnitAccessionAttribute(self, accession: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitAccessionAttribute(String accession)
        Sets the name of the unit accession attribute (default 'unitAccession')
        """
        ...
    
    def setUnitNameAttribute(self, name: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setUnitNameAttribute(String name)
        Sets the name of the unit name attribute (default 'unitName')
        """
        ... 


class SemanticValidator_CVTerm:
    """
    Cython implementation of _SemanticValidator_CVTerm

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS::Internal_1_1SemanticValidator_CVTerm.html>`_
    """
    
    accession: Union[bytes, str, String]
    
    name: Union[bytes, str, String]
    
    value: Union[bytes, str, String]
    
    has_value: bool
    
    unit_accession: Union[bytes, str, String]
    
    has_unit_accession: bool
    
    unit_name: Union[bytes, str, String]
    
    has_unit_name: bool
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm()
        """
        ...
    
    @overload
    def __init__(self, in_0: SemanticValidator_CVTerm ) -> None:
        """
        Cython signature: void SemanticValidator_CVTerm(SemanticValidator_CVTerm &)
        """
        ... 


class SignalToNoiseEstimatorMeanIterative:
    """
    Cython implementation of _SignalToNoiseEstimatorMeanIterative[_MSSpectrum]

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMeanIterative[_MSSpectrum].html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative()
        """
        ...
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMeanIterative ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMeanIterative(SignalToNoiseEstimatorMeanIterative &)
        """
        ...
    
    def init(self, c: MSSpectrum ) -> None:
        """
        Cython signature: void init(MSSpectrum & c)
        """
        ...
    
    def getSignalToNoise(self, index: int ) -> float:
        """
        Cython signature: double getSignalToNoise(size_t index)
        """
        ...
    IntensityThresholdCalculation : __IntensityThresholdCalculation 


class SignalToNoiseEstimatorMedianRapid:
    """
    Cython implementation of _SignalToNoiseEstimatorMedianRapid

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SignalToNoiseEstimatorMedianRapid.html>`_
    """
    
    @overload
    def __init__(self, in_0: SignalToNoiseEstimatorMedianRapid ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedianRapid(SignalToNoiseEstimatorMedianRapid &)
        """
        ...
    
    @overload
    def __init__(self, window_length: float ) -> None:
        """
        Cython signature: void SignalToNoiseEstimatorMedianRapid(double window_length)
        """
        ...
    
    @overload
    def estimateNoise(self, in_0: _Interfaces_Spectrum ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(shared_ptr[_Interfaces_Spectrum])
        """
        ...
    
    @overload
    def estimateNoise(self, in_0: _Interfaces_Chromatogram ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(shared_ptr[_Interfaces_Chromatogram])
        """
        ...
    
    @overload
    def estimateNoise(self, mz_array: List[float] , int_array: List[float] ) -> NoiseEstimator:
        """
        Cython signature: NoiseEstimator estimateNoise(libcpp_vector[double] mz_array, libcpp_vector[double] int_array)
        """
        ... 


class SpectrumAccessSqMass:
    """
    Cython implementation of _SpectrumAccessSqMass

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SpectrumAccessSqMass.html>`_
      -- Inherits from ['ISpectrumAccess']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass()
        """
        ...
    
    @overload
    def __init__(self, in_0: SpectrumAccessSqMass ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass(SpectrumAccessSqMass &)
        """
        ...
    
    @overload
    def __init__(self, in_0: MzMLSqliteHandler , indices: List[int] ) -> None:
        """
        Cython signature: void SpectrumAccessSqMass(MzMLSqliteHandler, libcpp_vector[int] indices)
        """
        ...
    
    def getSpectrumById(self, id_: int ) -> OSSpectrum:
        """
        Cython signature: shared_ptr[OSSpectrum] getSpectrumById(int id_)
        Returns a pointer to a spectrum at the given string id
        """
        ...
    
    def getSpectraByRT(self, RT: float , deltaRT: float ) -> List[int]:
        """
        Cython signature: libcpp_vector[size_t] getSpectraByRT(double RT, double deltaRT)
        Returns a vector of ids of spectra that are within RT +/- deltaRT
        """
        ...
    
    def getNrSpectra(self) -> int:
        """
        Cython signature: size_t getNrSpectra()
        Returns the number of spectra available
        """
        ...
    
    def getChromatogramById(self, id_: int ) -> OSChromatogram:
        """
        Cython signature: shared_ptr[OSChromatogram] getChromatogramById(int id_)
        Returns a pointer to a chromatogram at the given id
        """
        ...
    
    def getNrChromatograms(self) -> int:
        """
        Cython signature: size_t getNrChromatograms()
        Returns the number of chromatograms available
        """
        ...
    
    def getChromatogramNativeID(self, id_: int ) -> str:
        """
        Cython signature: libcpp_utf8_output_string getChromatogramNativeID(int id_)
        """
        ... 


class SpectrumHelper:
    """
    Cython implementation of _SpectrumHelper

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/class_1_1SpectrumHelper.html>`_
    """
    
    removePeaks: __static_SpectrumHelper_removePeaks
    
    removePeaks: __static_SpectrumHelper_removePeaks
    
    subtractMinimumIntensity: __static_SpectrumHelper_subtractMinimumIntensity
    
    subtractMinimumIntensity: __static_SpectrumHelper_subtractMinimumIntensity 


class SplineInterpolatedPeaks:
    """
    Cython implementation of _SplineInterpolatedPeaks

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineInterpolatedPeaks.html>`_
    """
    
    @overload
    def __init__(self, mz: List[float] , intensity: List[float] ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(libcpp_vector[double] mz, libcpp_vector[double] intensity)
        """
        ...
    
    @overload
    def __init__(self, raw_spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSSpectrum raw_spectrum)
        """
        ...
    
    @overload
    def __init__(self, raw_chromatogram: MSChromatogram ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(MSChromatogram raw_chromatogram)
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineInterpolatedPeaks ) -> None:
        """
        Cython signature: void SplineInterpolatedPeaks(SplineInterpolatedPeaks &)
        """
        ...
    
    def getPosMin(self) -> float:
        """
        Cython signature: double getPosMin()
        """
        ...
    
    def getPosMax(self) -> float:
        """
        Cython signature: double getPosMax()
        """
        ...
    
    def size(self) -> int:
        """
        Cython signature: int size()
        """
        ...
    
    def getNavigator(self, scaling: float ) -> SplineSpectrum_Navigator:
        """
        Cython signature: SplineSpectrum_Navigator getNavigator(double scaling)
        """
        ... 


class SplineSpectrum_Navigator:
    """
    Cython implementation of _SplineSpectrum_Navigator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1SplineSpectrum_Navigator.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator()
        """
        ...
    
    @overload
    def __init__(self, in_0: SplineSpectrum_Navigator ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(SplineSpectrum_Navigator)
        """
        ...
    
    @overload
    def __init__(self, packages: List[SplinePackage] , posMax: float , scaling: float ) -> None:
        """
        Cython signature: void SplineSpectrum_Navigator(libcpp_vector[SplinePackage] * packages, double posMax, double scaling)
        """
        ...
    
    def eval(self, pos: float ) -> float:
        """
        Cython signature: double eval(double pos)
        """
        ...
    
    def getNextPos(self, pos: float ) -> float:
        """
        Cython signature: double getNextPos(double pos)
        """
        ... 


class StablePairFinder:
    """
    Cython implementation of _StablePairFinder

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1StablePairFinder.html>`_
      -- Inherits from ['BaseGroupFinder']
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void StablePairFinder()
        """
        ...
    
    def run(self, input_maps: List[ConsensusMap] , result_map: ConsensusMap ) -> None:
        """
        Cython signature: void run(libcpp_vector[ConsensusMap] & input_maps, ConsensusMap & result_map)
        """
        ...
    
    def getProductName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getProductName()
        """
        ...
    
    def registerChildren(self) -> None:
        """
        Cython signature: void registerChildren()
        Register all derived classes here
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ...
    
    def setLogType(self, in_0: int ) -> None:
        """
        Cython signature: void setLogType(LogType)
        Sets the progress log that should be used. The default type is NONE!
        """
        ...
    
    def getLogType(self) -> int:
        """
        Cython signature: LogType getLogType()
        Returns the type of progress log being used
        """
        ...
    
    def startProgress(self, begin: int , end: int , label: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void startProgress(ptrdiff_t begin, ptrdiff_t end, String label)
        """
        ...
    
    def setProgress(self, value: int ) -> None:
        """
        Cython signature: void setProgress(ptrdiff_t value)
        Sets the current progress
        """
        ...
    
    def endProgress(self) -> None:
        """
        Cython signature: void endProgress()
        Ends the progress display
        """
        ...
    
    def nextProgress(self) -> None:
        """
        Cython signature: void nextProgress()
        Increment progress by 1 (according to range begin-end)
        """
        ... 


class TMTEighteenPlexQuantitationMethod:
    """
    Cython implementation of _TMTEighteenPlexQuantitationMethod

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TMTEighteenPlexQuantitationMethod.html>`_
      -- Inherits from ['IsobaricQuantitationMethod']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod()
        """
        ...
    
    @overload
    def __init__(self, in_0: TMTEighteenPlexQuantitationMethod ) -> None:
        """
        Cython signature: void TMTEighteenPlexQuantitationMethod(TMTEighteenPlexQuantitationMethod &)
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        """
        ...
    
    def getChannelInformation(self) -> List[IsobaricChannelInformation]:
        """
        Cython signature: libcpp_vector[IsobaricChannelInformation] getChannelInformation()
        """
        ...
    
    def getNumberOfChannels(self) -> int:
        """
        Cython signature: size_t getNumberOfChannels()
        """
        ...
    
    def getIsotopeCorrectionMatrix(self) -> MatrixDouble:
        """
        Cython signature: MatrixDouble getIsotopeCorrectionMatrix()
        """
        ...
    
    def getReferenceChannel(self) -> int:
        """
        Cython signature: size_t getReferenceChannel()
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class Tagging:
    """
    Cython implementation of _Tagging

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1Tagging.html>`_

    Meta information about tagging of a sample e.g. ICAT labeling
    
    Holds information about the mass difference between light and heavy tag
    All other relevant information is provided by Modification
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void Tagging()
        """
        ...
    
    @overload
    def __init__(self, in_0: Tagging ) -> None:
        """
        Cython signature: void Tagging(Tagging &)
        """
        ...
    
    def getMassShift(self) -> float:
        """
        Cython signature: double getMassShift()
        Returns the mass difference between light and heavy variant (default is 0.0)
        """
        ...
    
    def setMassShift(self, mass_shift: float ) -> None:
        """
        Cython signature: void setMassShift(double mass_shift)
        Sets the mass difference between light and heavy variant
        """
        ...
    
    def getVariant(self) -> int:
        """
        Cython signature: IsotopeVariant getVariant()
        Returns the isotope variant of the tag (default is LIGHT)
        """
        ...
    
    def setVariant(self, variant: int ) -> None:
        """
        Cython signature: void setVariant(IsotopeVariant variant)
        Sets the isotope variant of the tag
        """
        ... 


class TheoreticalSpectrumGenerator:
    """
    Cython implementation of _TheoreticalSpectrumGenerator

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TheoreticalSpectrumGenerator.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator()
        """
        ...
    
    @overload
    def __init__(self, in_0: TheoreticalSpectrumGenerator ) -> None:
        """
        Cython signature: void TheoreticalSpectrumGenerator(TheoreticalSpectrumGenerator &)
        """
        ...
    
    def getSpectrum(self, spec: MSSpectrum , peptide: AASequence , min_charge: int , max_charge: int ) -> None:
        """
        Cython signature: void getSpectrum(MSSpectrum & spec, AASequence & peptide, int min_charge, int max_charge)
        Generates a spectrum for a peptide sequence, with the ion types that are set in the tool parameters. If precursor_charge is set to 0 max_charge + 1 will be used
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class TraMLFile:
    """
    Cython implementation of _TraMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TraMLFile.html>`_
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TraMLFile()
        """
        ...
    
    @overload
    def __init__(self, in_0: TraMLFile ) -> None:
        """
        Cython signature: void TraMLFile(TraMLFile &)
        """
        ...
    
    def load(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void load(String filename, TargetedExperiment & id)
        Loads a map from a TraML file
        """
        ...
    
    def store(self, filename: Union[bytes, str, String] , id: TargetedExperiment ) -> None:
        """
        Cython signature: void store(String filename, TargetedExperiment & id)
        Stores a map in a TraML file
        """
        ...
    
    def isSemanticallyValid(self, filename: Union[bytes, str, String] , errors: List[bytes] , warnings: List[bytes] ) -> bool:
        """
        Cython signature: bool isSemanticallyValid(String filename, StringList & errors, StringList & warnings)
        Checks if a file is valid with respect to the mapping file and the controlled vocabulary
        
        :param filename: File name of the file to be checked
        :param errors: Errors during the validation are returned in this output parameter
        :param warnings: Warnings during the validation are returned in this output parameter
        """
        ... 


class TransformationModelInterpolated:
    """
    Cython implementation of _TransformationModelInterpolated

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationModelInterpolated.html>`_
      -- Inherits from ['TransformationModel']
    """
    
    def __init__(self, data: List[TM_DataPoint] , params: Param ) -> None:
        """
        Cython signature: void TransformationModelInterpolated(libcpp_vector[TM_DataPoint] & data, Param & params)
        """
        ...
    
    def getDefaultParameters(self, in_0: Param ) -> None:
        """
        Cython signature: void getDefaultParameters(Param &)
        Gets the default parameters
        """
        ...
    
    def evaluate(self, value: float ) -> float:
        """
        Cython signature: double evaluate(double value)
        Evaluate the interpolation model at the given value
        
        :param value: The position where the interpolation should be evaluated
        :returns: The interpolated value
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        """
        ...
    
    def weightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void weightData(libcpp_vector[TM_DataPoint] & data)
        Weight the data by the given weight function
        """
        ...
    
    def checkValidWeight(self, weight: Union[bytes, str, String] , valid_weights: List[bytes] ) -> bool:
        """
        Cython signature: bool checkValidWeight(const String & weight, libcpp_vector[String] & valid_weights)
        Check for a valid weighting function string
        """
        ...
    
    def weightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double weightDatum(double & datum, const String & weight)
        Weight the data according to the weighting function
        """
        ...
    
    def unWeightDatum(self, datum: float , weight: Union[bytes, str, String] ) -> float:
        """
        Cython signature: double unWeightDatum(double & datum, const String & weight)
        Apply the reverse of the weighting function to the data
        """
        ...
    
    def getValidXWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidXWeights()
        Returns a list of valid x weight function stringss
        """
        ...
    
    def getValidYWeights(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getValidYWeights()
        Returns a list of valid y weight function strings
        """
        ...
    
    def unWeightData(self, data: List[TM_DataPoint] ) -> None:
        """
        Cython signature: void unWeightData(libcpp_vector[TM_DataPoint] & data)
        Unweight the data by the given weight function
        """
        ...
    
    def checkDatumRange(self, datum: float , datum_min: float , datum_max: float ) -> float:
        """
        Cython signature: double checkDatumRange(const double & datum, const double & datum_min, const double & datum_max)
        Check that the datum is within the valid min and max bounds
        """
        ... 


class TransformationXMLFile:
    """
    Cython implementation of _TransformationXMLFile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TransformationXMLFile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void TransformationXMLFile()
        """
        ...
    
    def load(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription , fit_model: bool ) -> None:
        """
        Cython signature: void load(String, TransformationDescription &, bool fit_model)
        """
        ...
    
    def store(self, in_0: Union[bytes, str, String] , in_1: TransformationDescription ) -> None:
        """
        Cython signature: void store(String, TransformationDescription)
        """
        ... 


class TwoDOptimization:
    """
    Cython implementation of _TwoDOptimization

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1TwoDOptimization.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void TwoDOptimization()
        """
        ...
    
    @overload
    def __init__(self, in_0: TwoDOptimization ) -> None:
        """
        Cython signature: void TwoDOptimization(TwoDOptimization &)
        """
        ...
    
    def getMZTolerance(self) -> float:
        """
        Cython signature: double getMZTolerance()
        Returns the matching epsilon
        """
        ...
    
    def setMZTolerance(self, tolerance_mz: float ) -> None:
        """
        Cython signature: void setMZTolerance(double tolerance_mz)
        Sets the matching epsilon
        """
        ...
    
    def getMaxPeakDistance(self) -> float:
        """
        Cython signature: double getMaxPeakDistance()
        Returns the maximal peak distance in a cluster
        """
        ...
    
    def setMaxPeakDistance(self, max_peak_distance: float ) -> None:
        """
        Cython signature: void setMaxPeakDistance(double max_peak_distance)
        Sets the maximal peak distance in a cluster
        """
        ...
    
    def getMaxIterations(self) -> int:
        """
        Cython signature: unsigned int getMaxIterations()
        Returns the maximal number of iterations
        """
        ...
    
    def setMaxIterations(self, max_iteration: int ) -> None:
        """
        Cython signature: void setMaxIterations(unsigned int max_iteration)
        Sets the maximal number of iterations
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class WindowMower:
    """
    Cython implementation of _WindowMower

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1WindowMower.html>`_
      -- Inherits from ['DefaultParamHandler']
    """
    
    @overload
    def __init__(self, ) -> None:
        """
        Cython signature: void WindowMower()
        """
        ...
    
    @overload
    def __init__(self, in_0: WindowMower ) -> None:
        """
        Cython signature: void WindowMower(WindowMower &)
        """
        ...
    
    def filterPeakSpectrumForTopNInSlidingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInSlidingWindow(MSSpectrum & spectrum)
        Sliding window version (slower)
        """
        ...
    
    def filterPeakSpectrumForTopNInJumpingWindow(self, spectrum: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrumForTopNInJumpingWindow(MSSpectrum & spectrum)
        Jumping window version (faster)
        """
        ...
    
    def filterPeakSpectrum(self, spec: MSSpectrum ) -> None:
        """
        Cython signature: void filterPeakSpectrum(MSSpectrum & spec)
        """
        ...
    
    def filterPeakMap(self, exp: MSExperiment ) -> None:
        """
        Cython signature: void filterPeakMap(MSExperiment & exp)
        """
        ...
    
    def getSubsections(self) -> List[bytes]:
        """
        Cython signature: libcpp_vector[String] getSubsections()
        """
        ...
    
    def setParameters(self, param: Param ) -> None:
        """
        Cython signature: void setParameters(Param & param)
        Sets the parameters
        """
        ...
    
    def getParameters(self) -> Param:
        """
        Cython signature: Param getParameters()
        Returns the parameters
        """
        ...
    
    def getDefaults(self) -> Param:
        """
        Cython signature: Param getDefaults()
        Returns the default parameters
        """
        ...
    
    def getName(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getName()
        Returns the name
        """
        ...
    
    def setName(self, in_0: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setName(const String &)
        Sets the name
        """
        ... 


class XTandemInfile:
    """
    Cython implementation of _XTandemInfile

    Original C++ documentation is available `here <http://www.openms.de/current_doxygen/html/classOpenMS_1_1XTandemInfile.html>`_
    """
    
    def __init__(self) -> None:
        """
        Cython signature: void XTandemInfile()
        """
        ...
    
    def setFragmentMassTolerance(self, tolerance: float ) -> None:
        """
        Cython signature: void setFragmentMassTolerance(double tolerance)
        """
        ...
    
    def getFragmentMassTolerance(self) -> float:
        """
        Cython signature: double getFragmentMassTolerance()
        """
        ...
    
    def setPrecursorMassTolerancePlus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassTolerancePlus(double tol)
        """
        ...
    
    def getPrecursorMassTolerancePlus(self) -> float:
        """
        Cython signature: double getPrecursorMassTolerancePlus()
        """
        ...
    
    def setPrecursorMassToleranceMinus(self, tol: float ) -> None:
        """
        Cython signature: void setPrecursorMassToleranceMinus(double tol)
        """
        ...
    
    def getPrecursorMassToleranceMinus(self) -> float:
        """
        Cython signature: double getPrecursorMassToleranceMinus()
        """
        ...
    
    def setPrecursorErrorType(self, mono_isotopic: int ) -> None:
        """
        Cython signature: void setPrecursorErrorType(MassType mono_isotopic)
        """
        ...
    
    def getPrecursorErrorType(self) -> int:
        """
        Cython signature: MassType getPrecursorErrorType()
        """
        ...
    
    def setFragmentMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setFragmentMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getFragmentMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getFragmentMassErrorUnit()
        """
        ...
    
    def setPrecursorMassErrorUnit(self, unit: int ) -> None:
        """
        Cython signature: void setPrecursorMassErrorUnit(ErrorUnit unit)
        """
        ...
    
    def getPrecursorMassErrorUnit(self) -> int:
        """
        Cython signature: ErrorUnit getPrecursorMassErrorUnit()
        """
        ...
    
    def setNumberOfThreads(self, threads: int ) -> None:
        """
        Cython signature: void setNumberOfThreads(unsigned int threads)
        """
        ...
    
    def getNumberOfThreads(self) -> int:
        """
        Cython signature: unsigned int getNumberOfThreads()
        """
        ...
    
    def setModifications(self, mods: ModificationDefinitionsSet ) -> None:
        """
        Cython signature: void setModifications(ModificationDefinitionsSet & mods)
        """
        ...
    
    def getModifications(self) -> ModificationDefinitionsSet:
        """
        Cython signature: ModificationDefinitionsSet getModifications()
        """
        ...
    
    def setOutputFilename(self, output: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputFilename(const String & output)
        """
        ...
    
    def getOutputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputFilename()
        """
        ...
    
    def setInputFilename(self, input_file: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setInputFilename(const String & input_file)
        """
        ...
    
    def getInputFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getInputFilename()
        """
        ...
    
    def setTaxonomyFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxonomyFilename(const String & filename)
        """
        ...
    
    def getTaxonomyFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxonomyFilename()
        """
        ...
    
    def setDefaultParametersFilename(self, filename: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setDefaultParametersFilename(const String & filename)
        """
        ...
    
    def getDefaultParametersFilename(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getDefaultParametersFilename()
        """
        ...
    
    def setTaxon(self, taxon: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setTaxon(const String & taxon)
        """
        ...
    
    def getTaxon(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getTaxon()
        """
        ...
    
    def setMaxPrecursorCharge(self, max_charge: int ) -> None:
        """
        Cython signature: void setMaxPrecursorCharge(int max_charge)
        """
        ...
    
    def getMaxPrecursorCharge(self) -> int:
        """
        Cython signature: int getMaxPrecursorCharge()
        """
        ...
    
    def setNumberOfMissedCleavages(self, missed_cleavages: int ) -> None:
        """
        Cython signature: void setNumberOfMissedCleavages(unsigned int missed_cleavages)
        """
        ...
    
    def getNumberOfMissedCleavages(self) -> int:
        """
        Cython signature: unsigned int getNumberOfMissedCleavages()
        """
        ...
    
    def setOutputResults(self, result: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setOutputResults(String result)
        """
        ...
    
    def getOutputResults(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getOutputResults()
        """
        ...
    
    def setMaxValidEValue(self, value: float ) -> None:
        """
        Cython signature: void setMaxValidEValue(double value)
        """
        ...
    
    def getMaxValidEValue(self) -> float:
        """
        Cython signature: double getMaxValidEValue()
        """
        ...
    
    def setSemiCleavage(self, semi_cleavage: bool ) -> None:
        """
        Cython signature: void setSemiCleavage(bool semi_cleavage)
        """
        ...
    
    def setAllowIsotopeError(self, allow_isotope_error: bool ) -> None:
        """
        Cython signature: void setAllowIsotopeError(bool allow_isotope_error)
        """
        ...
    
    def write(self, filename: Union[bytes, str, String] , ignore_member_parameters: bool , force_default_mods: bool ) -> None:
        """
        Cython signature: void write(String filename, bool ignore_member_parameters, bool force_default_mods)
        """
        ...
    
    def setCleavageSite(self, cleavage_site: Union[bytes, str, String] ) -> None:
        """
        Cython signature: void setCleavageSite(String cleavage_site)
        """
        ...
    
    def getCleavageSite(self) -> Union[bytes, str, String]:
        """
        Cython signature: String getCleavageSite()
        """
        ...
    ErrorUnit : __ErrorUnit
    MassType : __MassType 


class __ErrorUnit:
    None
    DALTONS : int
    PPM : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __IntensityThresholdCalculation:
    None
    MANUAL : int
    AUTOMAXBYSTDEV : int
    AUTOMAXBYPERCENT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class IsotopeVariant:
    None
    LIGHT : int
    HEAVY : int
    SIZE_OF_ISOTOPEVARIANT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __MassType:
    None
    MONOISOTOPIC : int
    AVERAGE : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class OriginAnnotationFormat:
    None
    FILE_ORIGIN : int
    MAP_INDEX : int
    ID_MERGE_INDEX : int
    UNKNOWN_OAF : int
    SIZE_OF_ORIGIN_ANNOTATION_FORMAT : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __ProcessingAction:
    None
    DATA_PROCESSING : int
    CHARGE_DECONVOLUTION : int
    DEISOTOPING : int
    SMOOTHING : int
    CHARGE_CALCULATION : int
    PRECURSOR_RECALCULATION : int
    BASELINE_REDUCTION : int
    PEAK_PICKING : int
    ALIGNMENT : int
    CALIBRATION : int
    NORMALIZATION : int
    FILTERING : int
    QUANTITATION : int
    FEATURE_GROUPING : int
    IDENTIFICATION_MAPPING : int
    FORMAT_CONVERSION : int
    CONVERSION_MZDATA : int
    CONVERSION_MZML : int
    CONVERSION_MZXML : int
    CONVERSION_DTA : int
    IDENTIFICATION : int
    SIZE_OF_PROCESSINGACTION : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __SourceClassification:
    None
    ARTIFACT : int
    HYPOTHETICAL : int
    NATURAL : int
    POSTTRANSLATIONAL : int
    MULTIPLE : int
    CHEMICAL_DERIVATIVE : int
    ISOTOPIC_LABEL : int
    PRETRANSLATIONAL : int
    OTHER_GLYCOSYLATION : int
    NLINKED_GLYCOSYLATION : int
    AA_SUBSTITUTION : int
    OTHER : int
    NONSTANDARD_RESIDUE : int
    COTRANSLATIONAL : int
    OLINKED_GLYCOSYLATION : int
    UNKNOWN : int
    NUMBER_OF_SOURCE_CLASSIFICATIONS : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __Specificity:
    None
    SPEC_NONE : int
    SPEC_SEMI : int
    SPEC_FULL : int
    SPEC_UNKNOWN : int
    SPEC_NOCTERM : int
    SPEC_NONTERM : int
    SIZE_OF_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class __TermSpecificity:
    None
    ANYWHERE : int
    C_TERM : int
    N_TERM : int
    PROTEIN_C_TERM : int
    PROTEIN_N_TERM : int
    NUMBER_OF_TERM_SPECIFICITY : int

    def getMapping(self) -> Dict[int, str]:
       ... 


class ValueType:
    None
    STRING_VALUE : int
    INT_VALUE : int
    DOUBLE_VALUE : int
    STRING_LIST : int
    INT_LIST : int
    DOUBLE_LIST : int
    EMPTY_VALUE : int

    def getMapping(self) -> Dict[int, str]:
       ... 

