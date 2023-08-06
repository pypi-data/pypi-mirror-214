# This file is part of pipe_base.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

"""Module defining a butler like object specialized to a specific quantum.
"""

__all__ = ("ButlerQuantumContext",)

from collections.abc import Sequence
from typing import Any

from lsst.daf.butler import DatasetRef, DimensionUniverse, LimitedButler, Quantum
from lsst.utils.introspection import get_full_type_name
from lsst.utils.logging import PeriodicLogger, getLogger

from .connections import DeferredDatasetRef, InputQuantizedConnection, OutputQuantizedConnection
from .struct import Struct

_LOG = getLogger(__name__)


class ButlerQuantumContext:
    """A Butler-like class specialized for a single quantum.

    Parameters
    ----------
    butler : `lsst.daf.butler.LimitedButler`
        Butler object from/to which datasets will be get/put.
    quantum : `lsst.daf.butler.core.Quantum`
        Quantum object that describes the datasets which will be get/put by a
        single execution of this node in the pipeline graph.

    Notes
    -----
    A ButlerQuantumContext class wraps a standard butler interface and
    specializes it to the context of a given quantum. What this means
    in practice is that the only gets and puts that this class allows
    are DatasetRefs that are contained in the quantum.

    In the future this class will also be used to record provenance on
    what was actually get and put. This is in contrast to what the
    preflight expects to be get and put by looking at the graph before
    execution.
    """

    def __init__(self, butler: LimitedButler, quantum: Quantum):
        self.quantum = quantum
        self.allInputs = set()
        self.allOutputs = set()
        for refs in quantum.inputs.values():
            for ref in refs:
                self.allInputs.add((ref.datasetType, ref.dataId))
        for refs in quantum.outputs.values():
            for ref in refs:
                self.allOutputs.add((ref.datasetType, ref.dataId))
        self.__butler = butler

    def _get(self, ref: DeferredDatasetRef | DatasetRef | None) -> Any:
        # Butler methods below will check for unresolved DatasetRefs and
        # raise appropriately, so no need for us to do that here.
        if isinstance(ref, DeferredDatasetRef):
            self._checkMembership(ref.datasetRef, self.allInputs)
            return self.__butler.getDeferred(ref.datasetRef)
        elif ref is None:
            return None
        else:
            self._checkMembership(ref, self.allInputs)
            return self.__butler.get(ref)

    def _put(self, value: Any, ref: DatasetRef) -> None:
        """Store data in butler"""
        self._checkMembership(ref, self.allOutputs)
        self.__butler.put(value, ref)

    def get(
        self,
        dataset: InputQuantizedConnection
        | list[DatasetRef | None]
        | list[DeferredDatasetRef | None]
        | DatasetRef
        | DeferredDatasetRef
        | None,
    ) -> Any:
        """Fetch data from the butler

        Parameters
        ----------
        dataset
            This argument may either be an `InputQuantizedConnection` which
            describes all the inputs of a quantum, a list of
            `~lsst.daf.butler.DatasetRef`, or a single
            `~lsst.daf.butler.DatasetRef`. The function will get and return
            the corresponding datasets from the butler. If `None` is passed in
            place of a `~lsst.daf.butler.DatasetRef` then the corresponding
            returned object will be `None`.

        Returns
        -------
        return : `object`
            This function returns arbitrary objects fetched from the bulter.
            The structure these objects are returned in depends on the type of
            the input argument. If the input dataset argument is a
            `InputQuantizedConnection`, then the return type will be a
            dictionary with keys corresponding to the attributes of the
            `InputQuantizedConnection` (which in turn are the attribute
            identifiers of the connections). If the input argument is of type
            `list` of `~lsst.daf.butler.DatasetRef` then the return type will
            be a list of objects.  If the input argument is a single
            `~lsst.daf.butler.DatasetRef` then a single object will be
            returned.

        Raises
        ------
        ValueError
            Raised if a `~lsst.daf.butler.DatasetRef` is passed to get that is
            not defined in the quantum object
        """
        # Set up a periodic logger so log messages can be issued if things
        # are taking too long.
        periodic = PeriodicLogger(_LOG)

        if isinstance(dataset, InputQuantizedConnection):
            retVal = {}
            n_connections = len(dataset)
            n_retrieved = 0
            for i, (name, ref) in enumerate(dataset):
                if isinstance(ref, list):
                    val = []
                    n_refs = len(ref)
                    for j, r in enumerate(ref):
                        val.append(self._get(r))
                        n_retrieved += 1
                        periodic.log(
                            "Retrieved %d out of %d datasets for connection '%s' (%d out of %d)",
                            j + 1,
                            n_refs,
                            name,
                            i + 1,
                            n_connections,
                        )
                else:
                    val = self._get(ref)
                    periodic.log(
                        "Retrieved dataset for connection '%s' (%d out of %d)",
                        name,
                        i + 1,
                        n_connections,
                    )
                    n_retrieved += 1
                retVal[name] = val
            if periodic.num_issued > 0:
                # This took long enough that we issued some periodic log
                # messages, so issue a final confirmation message as well.
                _LOG.verbose(
                    "Completed retrieval of %d datasets from %d connections", n_retrieved, n_connections
                )
            return retVal
        elif isinstance(dataset, list):
            n_datasets = len(dataset)
            retrieved = []
            for i, x in enumerate(dataset):
                # Mypy is not sure of the type of x because of the union
                # of lists so complains. Ignoring it is more efficient
                # than adding an isinstance assert.
                retrieved.append(self._get(x))
                periodic.log("Retrieved %d out of %d datasets", i + 1, n_datasets)
            if periodic.num_issued > 0:
                _LOG.verbose("Completed retrieval of %d datasets", n_datasets)
            return retrieved
        elif isinstance(dataset, DatasetRef) or isinstance(dataset, DeferredDatasetRef) or dataset is None:
            return self._get(dataset)
        else:
            raise TypeError(
                f"Dataset argument ({get_full_type_name(dataset)}) is not a type that can be used to get"
            )

    def put(
        self,
        values: Struct | list[Any] | Any,
        dataset: OutputQuantizedConnection | list[DatasetRef] | DatasetRef,
    ) -> None:
        """Put data into the butler.

        Parameters
        ----------
        values : `Struct` or `list` of `object` or `object`
            The data that should be put with the butler. If the type of the
            dataset is `OutputQuantizedConnection` then this argument should be
            a `Struct` with corresponding attribute names. Each attribute
            should then correspond to either a list of object or a single
            object depending of the type of the corresponding attribute on
            dataset. I.e. if ``dataset.calexp`` is
            ``[datasetRef1, datasetRef2]`` then ``values.calexp`` should be
            ``[calexp1, calexp2]``. Like wise if there is a single ref, then
            only a single object need be passed. The same restriction applies
            if dataset is directly a `list` of `~lsst.daf.butler.DatasetRef`
            or a single `~lsst.daf.butler.DatasetRef`.
        dataset
            This argument may either be an `InputQuantizedConnection` which
            describes all the inputs of a quantum, a list of
            `lsst.daf.butler.DatasetRef`, or a single
            `lsst.daf.butler.DatasetRef`. The function will get and return
            the corresponding datasets from the butler.

        Raises
        ------
        ValueError
            Raised if a `~lsst.daf.butler.DatasetRef` is passed to put that is
            not defined in the `~lsst.daf.butler.Quantum` object, or the type
            of values does not match what is expected from the type of dataset.
        """
        if isinstance(dataset, OutputQuantizedConnection):
            if not isinstance(values, Struct):
                raise ValueError(
                    "dataset is a OutputQuantizedConnection, a Struct with corresponding"
                    " attributes must be passed as the values to put"
                )
            for name, refs in dataset:
                valuesAttribute = getattr(values, name)
                if isinstance(refs, list):
                    if len(refs) != len(valuesAttribute):
                        raise ValueError(f"There must be a object to put for every Dataset ref in {name}")
                    for i, ref in enumerate(refs):
                        self._put(valuesAttribute[i], ref)
                else:
                    self._put(valuesAttribute, refs)
        elif isinstance(dataset, list):
            if not isinstance(values, Sequence):
                raise ValueError("Values to put must be a sequence")
            if len(dataset) != len(values):
                raise ValueError("There must be a common number of references and values to put")
            for i, ref in enumerate(dataset):
                self._put(values[i], ref)
        elif isinstance(dataset, DatasetRef):
            self._put(values, dataset)
        else:
            raise TypeError("Dataset argument is not a type that can be used to put")

    def _checkMembership(self, ref: list[DatasetRef] | DatasetRef, inout: set) -> None:
        """Check if a `~lsst.daf.butler.DatasetRef` is part of the input
        `~lsst.daf.butler.Quantum`.

        This function will raise an exception if the `ButlerQuantumContext` is
        used to get/put a `~lsst.daf.butler.DatasetRef` which is not defined
        in the quantum.

        Parameters
        ----------
        ref : `list` [ `~lsst.daf.butler.DatasetRef` ] or \
                `~lsst.daf.butler.DatasetRef`
            Either a `list` or a single `~lsst.daf.butler.DatasetRef` to check
        inout : `set`
            The connection type to check, e.g. either an input or an output.
            This prevents both types needing to be checked for every operation,
            which may be important for Quanta with lots of
            `~lsst.daf.butler.DatasetRef`.
        """
        if not isinstance(ref, list):
            ref = [ref]
        for r in ref:
            if (r.datasetType, r.dataId) not in inout:
                raise ValueError("DatasetRef is not part of the Quantum being processed")

    @property
    def dimensions(self) -> DimensionUniverse:
        """Structure managing all dimensions recognized by this data
        repository (`~lsst.daf.butler.DimensionUniverse`).
        """
        return self.__butler.dimensions
