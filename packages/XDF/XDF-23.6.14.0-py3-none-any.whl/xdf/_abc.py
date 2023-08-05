__all__ = '_XDFABC',


from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty, abstractstaticmethod 
import logging
import os

from arimo.util.date_time import \
    (DATE_COL,
     _T_ORD_COL, _T_DELTA_COL,
     _T_HoY_COL, _T_QoY_COL, _T_MoY_COL, _T_PoY_COL,   # _T_WoY_COL, _T_DoY_COL,
     _T_QoH_COL, _T_MoH_COL, _T_PoH_COL,
     _T_MoQ_COL, _T_PoQ_COL,
     _T_WoM_COL, _T_DoM_COL, _T_PoM_COL,
     _T_DoW_COL, _T_PoW_COL,
     _T_HoD_COL, _T_PoD_COL,
     _T_COMPONENT_AUX_COLS, _T_CAT_AUX_COLS, _T_NUM_AUX_COLS)
from arimo.util import LOCAL_TMP_DIR_PATH, Namespace
from arimo.util.decor import _docstr_settable_property
from arimo.util.log import STDOUT_HANDLER
import arimo.debug


class _XDFABC(ABC):
    # default identity/entity, timestamp & time order columns
    _DEFAULT_I_COL = 'id'

    _DEFAULT_T_COL = 't'
    _DEFAULT_D_COL = DATE_COL

    _T_ORD_COL = _T_ORD_COL

    _T_DELTA_COL = _T_DELTA_COL

    _T_REL_AUX_COLS = _T_ORD_COL, _T_DELTA_COL

    _T_HoY_COL = _T_HoY_COL   # Half of Year
    _T_QoY_COL = _T_QoY_COL   # Quarter of Year
    _T_MoY_COL = _T_MoY_COL   # Month of Year
    # _T_WoY_COL = _T_WoY_COL   # Week of Year
    # _T_DoY_COL = _T_DoY_COL   # Day of Year
    _T_PoY_COL = _T_PoY_COL   # Part/Proportion/Fraction of Year

    _T_QoH_COL = _T_QoH_COL   # Quarter of Half-Year
    _T_MoH_COL = _T_MoH_COL   # Month of Half-Year
    _T_PoH_COL = _T_PoH_COL   # Part/Proportion/Fraction of Half-Year

    _T_MoQ_COL = _T_MoQ_COL   # Month of Quarter
    _T_PoQ_COL = _T_PoQ_COL   # Part/Proportion/Fraction of Quarter

    _T_WoM_COL = _T_WoM_COL   # Week of Month
    _T_DoM_COL = _T_DoM_COL   # Day of Month
    _T_PoM_COL = _T_PoM_COL   # Part/Proportion/Fraction of Month

    _T_DoW_COL = _T_DoW_COL   # Day of Week
    _T_PoW_COL = _T_PoW_COL   # Part/Proportion/Fraction of Week

    _T_HoD_COL = _T_HoD_COL   # Hour of Day
    _T_PoD_COL = _T_PoD_COL   # Part/Proportion/Fraction of Day

    _T_COMPONENT_AUX_COLS = _T_COMPONENT_AUX_COLS

    _T_AUX_COLS = _T_REL_AUX_COLS + _T_COMPONENT_AUX_COLS

    _T_CAT_AUX_COLS = _T_CAT_AUX_COLS

    _T_NUM_AUX_COLS = _T_NUM_AUX_COLS

    # repr sample size
    _DEFAULT_REPR_SAMPLE_SIZE = 10 ** 6

    # default profiling settings
    _DEFAULT_MIN_NON_NULL_PROPORTION = .32
    _DEFAULT_OUTLIER_TAIL_PROPORTION = 1e-3   # 0.1% each tail
    _DEFAULT_MAX_N_CATS = 12   # Month of Year is probably most numerous-category cat var
    _DEFAULT_MIN_PROPORTION_BY_MAX_N_CATS = .9

    # NULL-filling
    _NULL_FILL_SQL_STATEMENT_FILE_NAME = 'nullFillSQLStatement.json'

    # prep col prefixes / suffix
    _NULL_FILL_PREFIX = '__NullFill__'

    _CAT_IDX_PREFIX = '__CatIdx__'
    _OHE_PREFIX = '__OHE__'

    _STD_SCL_PREFIX = '__StdScl__'
    _MAX_ABS_SCL_PREFIX = '__MaxAbsScl__'

    _MIN_MAX_SCL_PREFIX = '__MinMaxScl__'

    _PREP_SUFFIX = '__'

    _CAT_ORIG_TO_PREP_COL_MAP_FILE_NAME = 'catOrigToPrepColMap.json'
    _NUM_ORIG_TO_PREP_COL_MAP_FILE_NAME = 'numOrigToPrepColMap.json'

    _PREP_SQL_STATEMENT_FILE_NAME = 'prepSQLStatement.json'

    # temp dir
    _TMP_DIR_PATH = \
        os.path.join(
            LOCAL_TMP_DIR_PATH,
            '.arimo/df')

    # data prep cache
    _PREP_CACHE = {}

    # **********************
    # PYTHON DEFAULT METHODS
    # __repr__
    # __short_repr__
    # __str__
    # __unicode__

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def __short_repr__(self):
        raise NotImplementedError

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)

    # **********************
    # LOGGERS
    # class_logger
    # class_stdout_logger
    # logger
    # stdout_logger

    @classmethod
    def class_logger(cls, *handlers, **kwargs):
        logger = logging.getLogger(name='{}'.format(cls.__name__))

        level = kwargs.get('level')

        if level is None:
            level = logging.DEBUG \
                if arimo.debug.ON \
                else logging.INFO

        logger.setLevel(level)

        if kwargs.get('verbose'):
            handlers += (STDOUT_HANDLER,)

        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @classmethod
    def class_stdout_logger(cls):
        return cls.class_logger(
            level=logging.DEBUG,
            verbose=True)

    def logger(self, *handlers, **kwargs):
        logger = logging.getLogger(name=self.__short_repr__)

        level = kwargs.get('level')

        if level is None:
            level = logging.DEBUG \
                if arimo.debug.ON \
                else logging.INFO

        logger.setLevel(level)

        if kwargs.get('verbose'):
            handlers += (STDOUT_HANDLER,)

        for handler in handlers:
            logger.addHandler(handler)

        return logger

    @property
    def stdout_logger(self):
        return self.logger(
            level=logging.DEBUG,
            verbose=True)

    # **********
    # IO METHODS
    # load / read
    # save / write

    @classmethod
    @abstractmethod
    def load(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def read(cls, *args, **kwargs):
        return cls.load(*args, **kwargs)

    @abstractmethod
    def save(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    # ***************
    # CACHING METHODS
    # _emptyCache
    # _inheritCache

    @abstractmethod
    def _emptyCache(self):
        raise NotImplementedError

    @abstractmethod
    def _inheritCache(self):
        raise NotImplementedError

    # *************************
    # KEY (SETTABLE) PROPERTIES
    # _assignReprSample
    # reprSampleSize
    # reprSample
    # minNonNullProportion
    # outlierTailProportion
    # maxNCats
    # minProportionByMaxNCats

    @abstractmethod
    def _assignReprSample(self):
        raise NotImplementedError

    @property
    @_docstr_settable_property
    def reprSampleSize(self):
        """
        *Approximate* number of rows to sample for profiling purposes *(int, default = 1,000,000)*
        """
        if self._cache.reprSample is None:
            self._assignReprSample()
        return self._reprSampleSize

    @reprSampleSize.setter
    def reprSampleSize(self, reprSampleSize):
        self._reprSampleSize = reprSampleSize
        self._assignReprSample()

    @property
    def reprSample(self):
        """
        Sub-sampled ``XDF`` according to ``.reprSampleSize`` attribute
        """
        if self._cache.reprSample is None:
            self._assignReprSample()
        return self._cache.reprSample

    @property
    @_docstr_settable_property
    def minNonNullProportion(self):
        """
        Minimum proportion of non-``NULL`` values in each column to qualify it as a valid feature
            to use in downstream data analyses *(float between 0 and 1, default = .32)*
        """
        return self._minNonNullProportion.default

    @minNonNullProportion.setter
    def minNonNullProportion(self, minNonNullProportion):
        if minNonNullProportion != self._minNonNullProportion.default:
            self._minNonNullProportion.default = minNonNullProportion
            self._cache.suffNonNull = {}

    @property
    @_docstr_settable_property
    def outlierTailProportion(self):
        """
        Proportion in each tail end of each numerical column's distribution to exclude
            when computing outlier-resistant statistics *(float between 0 and .1, default = .005)*
        """
        return self._outlierTailProportion.default

    @outlierTailProportion.setter
    def outlierTailProportion(self, outlierTailProportion):
        self._outlierTailProportion.default = outlierTailProportion

    @property
    @_docstr_settable_property
    def maxNCats(self):
        """
        Maximum number of categorical levels to consider for each possible categorical column *(int, default = 12)*
        """
        return self._maxNCats.default

    @maxNCats.setter
    def maxNCats(self, maxNCats):
        self._maxNCats.default = maxNCats

    @property
    @_docstr_settable_property
    def minProportionByMaxNCats(self):
        """
        Minimum total proportion accounted for by the most common ``maxNCats`` of each possible categorical column
            to consider the column truly categorical *(float between 0 and 1, default = .9)*
        """
        return self._minProportionByMaxNCats.default

    @minProportionByMaxNCats.setter
    def minProportionByMaxNCats(self, minProportionByMaxNCats):
        self._minProportionByMaxNCats.default = minProportionByMaxNCats

    # *********************
    # ROWS, COLUMNS & TYPES
    # __len__ / nRows / nrow
    # nCols / ncol
    # shape / dim
    # colNames / colnames / names
    # types / type / typeIsNum / typeIsComplex

    def __len__(self):
        """
        Number of rows
        """
        return self.nRows

    @property
    @abstractmethod
    def nRows(self):
        raise NotImplementedError

    @nRows.deleter
    def nRows(self):
        self._cache.nRows = None

    @property
    def nrow(self):   # R style
        """
        Alias for ``.__len__()``: number of rows
        """
        return self.nRows

    @nrow.deleter
    def nrow(self):
        self._cache.nRows = None

    @property
    def nCols(self):
        # Number of columns
        return len(self.columns)

    @property
    def ncol(self):   # R style
        """
        Number of columns
        """
        return self.nCols

    @property
    def shape(self):
        """
        Tuple (number of rows, number of columns)
        """
        return self.nRows, self.nCols

    @property
    def dim(self):   # R style
        """
        Alias for ``.shape``: tuple (number of rows, number of columns)
        """
        return self.shape

    @property
    def colNames (self):   # R style
        # Alias for ``.columns``: `list` of column names
        return self.columns

    @property
    def colnames(self):   # R style
        """
        Alias for ``.columns``: `list` of column names
        """
        return self.columns

    @property
    def names(self):   # R style
        # Alias for ``.columns``: `list` of column names
        return self.columns

    @property
    @abstractmethod
    def types(self):
        raise NotImplementedError

    @abstractmethod
    def type(self, col):
        raise NotImplementedError

    @abstractmethod
    def typeIsBool(self, col):
        raise NotImplementedError

    @abstractmethod
    def typeIsNum(self, col):
        raise NotImplementedError

    @abstractmethod
    def typeIsComplex(self, col):
        raise NotImplementedError

    # *************
    # COLUMN GROUPS
    # indexCols
    # tRelAuxCols
    # tComponentAuxCols
    # tAuxCols
    # possibleFeatureTAuxCols
    # possibleCatTAuxCols
    # possibleNumTAuxCols
    # contentCols
    # possibleFeatureContentCols
    # possibleCatContentCols
    # possibleNumContentCols
    # possibleFeatureCols
    # possibleCatCols
    # possibleNumCols

    @property
    @abstractmethod
    def indexCols(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def tRelAuxCols(self):
        raise NotImplementedError

    @property
    def tComponentAuxCols(self):
        return tuple(tComponentAuxCol for tComponentAuxCol in self._T_COMPONENT_AUX_COLS
                     if tComponentAuxCol in self.columns)

    @property
    def tAuxCols(self):
        return self.tRelAuxCols + self.tComponentAuxCols

    @property
    def possibleFeatureTAuxCols(self):
        return ((self._T_DELTA_COL,)
                if self.hasTS
                else ()) + \
               self.tComponentAuxCols

    @property
    def possibleCatTAuxCols(self):
        return tuple(tComponentAuxCol for tComponentAuxCol in self.tComponentAuxCols
                     if tComponentAuxCol in self._T_CAT_AUX_COLS)

    @property
    def possibleNumTAuxCols(self):
        return ((self._T_DELTA_COL,)
                if self.hasTS
                else ()) + \
               tuple(tComponentAuxCol for tComponentAuxCol in self.tComponentAuxCols
                     if tComponentAuxCol in self._T_NUM_AUX_COLS)

    @property
    def contentCols(self):
        return tuple(
            col for col in self.columns
            if col not in (self.indexCols + self._T_AUX_COLS))

    @property
    @abstractmethod
    def possibleFeatureContentCols(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def possibleCatContentCols(self):
        raise NotImplementedError

    @property
    def possibleNumContentCols(self):
        return tuple(
            col for col in self.contentCols
            if self.typeIsNum(col))

    @property
    def possibleFeatureCols(self):
        return self.possibleFeatureTAuxCols + self.possibleFeatureContentCols

    @property
    def possibleCatCols(self):
        return self.possibleCatTAuxCols + self.possibleCatContentCols

    @property
    def possibleNumCols(self):
        return self.possibleNumTAuxCols + self.possibleNumContentCols

    # ****************
    # COLUMN PROFILING
    # count
    # nonNullProportion
    # suffNonNull
    # distinct / unique
    # quantile
    # sampleStat / sampleMedian
    # outlierRstStat / outlierRstMin / outlierRstMax / outlierRstMedian
    # profile

    @abstractmethod
    def count(self, *cols, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def nonNullProportion(self, *cols, **kwargs):
        raise NotImplementedError

    def suffNonNull(self, *cols, **kwargs):
        """
        Check whether the columns has at least ``.minNonNullProportion`` of non-``NULL`` values

        Return:
            - If 1 column name is given, return ``True``/``False``

            - If multiple column names are given, return a {``col``: ``True`` or ``False``} *dict*

            - If no column names are given, return a {``col``: ``True`` or ``False``} *dict* for all columns

        Args:
            *cols (str): column names

            **kwargs:
        """
        if not cols:
            cols = self.contentCols

        if len(cols) > 1:
            return Namespace(**
                {col: self.suffNonNull(col, **kwargs)
                 for col in cols})

        else:
            col = cols[0]

            minNonNullProportion = self._minNonNullProportion[col]

            outdatedSuffNonNullProportionThreshold = False

            if col in self._cache.suffNonNullProportionThreshold:
                if self._cache.suffNonNullProportionThreshold[col] != minNonNullProportion:
                    outdatedSuffNonNullProportionThreshold = True
                    self._cache.suffNonNullProportionThreshold[col] = minNonNullProportion

            else:
                self._cache.suffNonNullProportionThreshold[col] = minNonNullProportion

            if (col not in self._cache.suffNonNull) or outdatedSuffNonNullProportionThreshold:
                self._cache.suffNonNull[col] = \
                    (self.nonNullProportion(col) >=
                     self._cache.suffNonNullProportionThreshold[col])

            return self._cache.suffNonNull[col]

    @abstractmethod
    def distinct(self, *cols, **kwargs):
        raise NotImplementedError

    def unique(self, *cols, **kwargs):
        return self.distinct(*cols, **kwargs)

    @abstractmethod
    def quantile(self, *cols, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def sampleStat(self, *cols, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def outlierRstStat(self, *cols, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def profile(self, *cols, **kwargs):
        raise NotImplementedError

    # *********
    # DATA PREP
    # fillna
    # prep

    @abstractmethod
    def fillna(self, *cols, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def prep(self, *cols, **kwargs):
        raise NotImplementedError

    # *******************************
    # SAMPLING / ITERATIVE GENERATION

    @abstractmethod
    def sample(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def gen(self, *args, **kwargs):
        raise NotImplementedError
