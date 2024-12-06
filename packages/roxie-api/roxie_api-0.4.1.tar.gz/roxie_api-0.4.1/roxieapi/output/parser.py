import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

import pandas as pd

from roxieapi.commons.types import (
    BlockGeometry,
    BlockTopology,
    Brick3DGeometry,
    Coil3DGeometry,
    CoilGeometry,
    DesignVariableResult,
    Geometry,
    GraphPlot,
    HarmonicCoil,
    ObjectiveResult,
    Plot2D,
    Plot3D,
    WedgeGeometry,
)


class TransStepData:
    """Data of a transient step"""

    def __init__(self, id: int, name: str) -> None:
        self.id: int = id
        self.name: str = name
        self.coilData = pd.DataFrame()
        self.meshData = pd.DataFrame()
        self.matrixData = pd.DataFrame()
        # self.irisData = pd.DataFrame()
        self.coilData3D = pd.DataFrame()
        self.brickData3D = pd.DataFrame()
        self.meshData3D = pd.DataFrame()
        self.deviceGraphs: Dict[int, pd.DataFrame] = {}
        self.harmonicCoils: Dict[int, HarmonicCoil] = {}
        self.conductorForces: Optional[pd.DataFrame] = None


@dataclass
class CoilGeomDfs:
    conductors: pd.DataFrame
    strands: pd.DataFrame


@dataclass
class MeshGeomDfs:
    nodes: pd.DataFrame
    elements: pd.DataFrame
    boundaries: pd.DataFrame


class OptData:
    """Data Of an optimization Step"""

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name: str = name

        self.transientGraphs: Dict[int, pd.DataFrame] = {}
        self.step: Dict[int, TransStepData] = {}
        self.designVariables: Dict[int, DesignVariableResult] = {}
        self.objectiveResults: Dict[int, ObjectiveResult] = {}

        self._coilGeometries: Dict[int, CoilGeometry] = {}
        self._coilGeometries3D: Dict[int, Coil3DGeometry] = {}
        self._brickGeometries3D: Dict[int, Brick3DGeometry] = {}
        self._wedgeGeometries3D: Dict[int, WedgeGeometry] = {}
        self._blockGeometries3D: dict[int, BlockGeometry] = {}
        self._meshGeometries: Optional[Geometry] = None
        self._meshGeometries3D: Optional[Geometry] = None

        self._coilGeomdf: CoilGeomDfs = CoilGeomDfs(pd.DataFrame(), pd.DataFrame())
        self._coilGeom3ddf: pd.DataFrame = pd.DataFrame()
        self._brickGeom3ddf: pd.DataFrame = pd.DataFrame()
        self._topologydf: pd.DataFrame = pd.DataFrame()
        self._meshGeomdf: MeshGeomDfs = MeshGeomDfs(
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        )
        self._meshGeom3ddf: MeshGeomDfs = MeshGeomDfs(
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        )

    @property
    def blockTopologies(self) -> Dict[int, BlockTopology]:
        """
        Get block topologies
        """
        return {
            int(block.block_nr): BlockTopology(
                block_nr=block.block_nr,
                block_orig=block.block_origin,
                layer_nr=block.layer_nr,
                first_conductor=block.first_conductor,
                last_conductor=block.last_conductor,
                n_radial=block.n_radial,
                n_azimuthal=block.n_azimuthal,
                first_strand=block.first_strand,
                last_strand=block.last_strand,
                ins_radial=block.ins_radial,
                ins_azimuthal=block.ins_azimuthal,
            )
            for block in self._topologydf.itertuples()
        }

    @property
    def coilGeometries(self) -> Dict[int, CoilGeometry]:
        if not self._coilGeometries:
            self._create_coils_from_df()
        return self._coilGeometries

    @coilGeometries.setter
    def coilGeometries(self, value: Dict[int, CoilGeometry]):
        self._coilGeometries = value

    @property
    def coilGeometries3D(self) -> Dict[int, Coil3DGeometry]:
        if not self._coilGeometries3D:
            self._create_coils3d_from_df()
        return self._coilGeometries3D

    @coilGeometries3D.setter
    def coilGeometries3D(self, value: Dict[int, Coil3DGeometry]):
        self._coilGeometries3D = value

    @property
    def brickGeometries3D(self) -> Dict[int, Brick3DGeometry]:
        if not self._brickGeometries3D:
            self._create_bricks_from_df()
        return self._brickGeometries3D

    @brickGeometries3D.setter
    def brickGeometries3D(self, value: Dict[int, Brick3DGeometry]):
        self._brickGeometries3D = value

    @property
    def wedgeGeometries3D(self) -> Dict[int, WedgeGeometry]:
        if not self._wedgeGeometries3D:
            self._blocks_to_wedges()
        return self._wedgeGeometries3D

    @wedgeGeometries3D.setter
    def wedgeGeometries3D(self, value: Dict[int, WedgeGeometry]):
        self._wedgeGeometries3D = value

    @property
    def blockGeometries3D(self) -> Dict[int, BlockGeometry]:
        return self._blockGeometries3D

    @blockGeometries3D.setter
    def blockGeometries3D(self, value: Dict[int, BlockGeometry]):
        self._blockGeometries3D = value

    @property
    def meshGeometries(self) -> Optional[Geometry]:
        if not self._meshGeometries:
            self._create_mesh_from_df()
            pass
        return self._meshGeometries

    @meshGeometries.setter
    def meshGeometries(self, value: Optional[Geometry]):
        self._meshGeometries = value

    @property
    def meshGeometries3D(self) -> Optional[Geometry]:
        if self._meshGeometries3D is None:
            self._create_mesh3d_from_df()
            pass
        return self._meshGeometries3D

    @meshGeometries3D.setter
    def meshGeometries3D(self, value: Optional[Geometry]):
        self._meshGeometries3D = value

    def _blocks_to_wedges(self) -> None:
        # From given block geometry, generate wedges
        if self._topologydf.empty:
            return

        # Iterate through blocks to establish the blockorder and nr of grouped blocks (by layerid and original blockid)
        block_order: dict[int, dict[int, list[int]]] = {}
        for _, row in self._topologydf.iterrows():
            layer = int(row["layer_nr"])
            block_orig = int(row["block_origin"])
            block_nr = int(row["block_nr"])
            if layer not in block_order:
                block_order[layer] = {}
            if block_orig not in block_order[layer]:
                block_order[layer][block_orig] = []
            block_order[layer][block_orig].append(block_nr)

        # From the generated order extract the list of unique blocklists (each for generating one set of wedges)
        block_ids: dict[int, list[list[int]]] = {}
        for layer in block_order:
            max_len = max(len(blocks) for blocks in block_order[layer].values())
            block_ids[layer] = [[] for _ in range(max_len)]
            for block_orig in block_order[layer]:
                for idx, block_nr in enumerate(block_order[layer][block_orig]):
                    block_ids[layer][idx].append(block_nr)

        wedge_nr = 1
        wedges: dict[int, WedgeGeometry] = {}
        for layer, block_list_list in block_ids.items():
            for block_list in block_list_list:
                # endspacer
                wedges[wedge_nr] = WedgeGeometry(
                    layer,
                    wedge_nr,
                    self.blockGeometries3D[block_list[0]].outer_surface,
                    None,
                    block_list[0],
                    0,
                )
                wedge_nr += 1
                for bl in range(1, len(block_list)):
                    outer = self.blockGeometries3D[block_list[bl - 1]].inner_surface
                    inner = self.blockGeometries3D[block_list[bl]].outer_surface
                    wedges[wedge_nr] = WedgeGeometry(
                        layer,
                        wedge_nr,
                        inner,
                        outer,
                        block_list[bl],
                        block_list[bl - 1],
                    )
                    wedge_nr += 1
                # inner post
                wedges[wedge_nr] = WedgeGeometry(
                    layer,
                    wedge_nr,
                    None,
                    self.blockGeometries3D[block_list[-1]].inner_surface,
                    0,
                    block_list[-1],
                )
                wedge_nr += 1
        self.wedgeGeometries3D = wedges

    def _create_mesh_from_df(self) -> None:
        if self._meshGeomdf.nodes.empty:
            return
        self._meshGeometries = self._meshdf_to_geom(self._meshGeomdf)

    def _create_mesh3d_from_df(self) -> None:
        if self._meshGeom3ddf.nodes.empty:
            return
        self._meshGeometries3D = self._meshdf_to_geom(self._meshGeom3ddf)

    def _meshdf_to_geom(self, df: MeshGeomDfs) -> Geometry:
        nodes = df.nodes.to_numpy()[:, 1:]
        elements = df.elements.to_numpy()[:, 2:]
        elements -= 1  # translate to 0 based index
        elements_list = elements.tolist()
        for nr_elem, lst in zip(df.elements["n_el"], elements_list):
            del lst[nr_elem:]  # Resize lists to match number of elements
        boundaries = {}
        if not df.boundaries.empty:
            for id, grp in df.boundaries.groupby("boundary_id"):
                if grp.empty:
                    continue
                boundaries[id] = grp.to_numpy()[:, 2:]
        return Geometry(nodes, elements_list, boundaries)

    def _create_bricks_from_df(self):
        if self._brickGeom3ddf.empty:
            return
        for idx, grp in self._brickGeom3ddf.groupby("brick_nr"):
            brick_nr = int(idx)
            if grp.empty:
                continue
            nodes = grp.to_numpy()[:, 2:].reshape((-1, 3))
            geom = Geometry(nodes, None, None)
            geom.generate_elements_for_coil_nodes()
            self._brickGeometries3D[brick_nr] = Brick3DGeometry(brick_nr, geom)

    def _create_coils3d_from_df(self):
        if self._coilGeomdf.conductors.empty:
            return
        for idx, grp in self._coilGeom3ddf.groupby("conductor"):
            cond_nr = int(idx)
            if grp.empty:
                continue
            block_info = self._topologydf[
                (self._topologydf.first_conductor <= cond_nr)
                & (self._topologydf.last_conductor >= cond_nr)
            ].iloc[0]
            block_nr = int(block_info.block_nr)
            layer_nr = int(block_info.layer_nr)

            nodes = grp.to_numpy()[:, 2:].reshape((-1, 3))
            geom = Geometry(nodes, None, None)
            geom.generate_elements_for_coil_nodes()

            self._coilGeometries3D[cond_nr] = Coil3DGeometry(
                cond_nr, geom, block_nr, layer_nr
            )

    def _create_coils_from_df(self):
        if self._coilGeomdf.conductors.empty:
            return

        cables = {}
        for _, cond in self._coilGeomdf.conductors.iterrows():
            cable_nr = int(cond["conductor"])
            geom = cond.to_numpy()[1:].reshape((4, 2))
            block_info = self._topologydf[
                (self._topologydf.first_conductor <= cond["conductor"])
                & (self._topologydf.last_conductor >= cond["conductor"])
            ]
            block_nr = block_info.block_nr
            layer_nr = block_info.layer_nr
            first_cond_strand = int(
                (
                    block_info.first_strand
                    + (cond["conductor"] - block_info.first_conductor)
                    * block_info.n_radial
                    * block_info.n_azimuthal
                ).iloc[0]
            )
            last_cond_strand = int(
                (
                    first_cond_strand
                    + (block_info.n_radial * block_info.n_azimuthal)
                    - 1
                ).iloc[0]
            )
            df_strand = self._coilGeomdf.strands
            strands = df_strand[
                (df_strand["strand"] >= first_cond_strand)
                & (df_strand["strand"] <= last_cond_strand)
            ]
            strands_dict = {
                int(st["strand"]): st.to_numpy()[1:].reshape((4, 2))
                for _, st in strands.iterrows()
            }
            cables[cable_nr] = CoilGeometry(
                cable_nr, block_nr, layer_nr, geom, strands_dict
            )
        self._coilGeometries = cables


class RoxieOutputParser:
    """Roxie output parser class.

    Takes all different Roxie outputs, parses them, and provides a structured output of the results.
    """

    def __init__(self, xml_file: str) -> None:
        from roxieapi.output.xml_parse import _XmlParser

        self.logger = logging.getLogger("RoxieOutputParser")

        self.optimizationGraphs: Dict[
            int, pd.DataFrame
        ] = {}  # Result values on optimization graphs, (id)
        self.opt: Dict[int, OptData] = {}

        self.plots2D: List[Plot2D] = []  # 2D Plots information for device
        self.plots3D: List[Plot3D] = []  # 3D Plots information for device
        self.graphs_device: List[GraphPlot] = []  # Graph information for device
        self.graphs_transient: List[
            GraphPlot
        ] = []  # Plot information for transient plots
        self.graphs_optimization: List[
            GraphPlot
        ] = []  # Plot information for optimization plots

        # General information
        self.roxie_version = ""
        self.roxie_githash = ""
        self.run_date = ""
        self.comment = ""

        _XmlParser.parse_xml(xml_file, self)

    def find_transstep(self, opt_step: int, trans_step: int) -> Optional[TransStepData]:
        if opt_step in self.opt and trans_step in self.opt[opt_step].step:
            return self.opt[opt_step].step[trans_step]
        return None

    def find_optstep(self, opt_step) -> Optional[OptData]:
        return self.opt.get(opt_step, None)

    def get_harmonic_coil(
        self,
        coil_nr: int = 1,
        opt_step: int = 1,
        trans_step: int = 1,
    ) -> Optional[HarmonicCoil]:
        """Return the harmonic coil for given step and coil id, or None if not present

        :param coil_nr: Harmonic Coil Nr, defaults to 1
        :param opt_step: The Optimization Step Nr, defaults to 1
        :param trans_step: The Transient Step Nr, defaults to 1
        :return: The Harmonic coil, or None
        """
        if trans := self.find_transstep(opt_step, trans_step):
            return trans.harmonicCoils.get(coil_nr, None)
        return None

    def get_conductor_forces(
        self, opt_step: int = 1, trans_step: int = 1
    ) -> Optional[pd.DataFrame]:
        """Return Conductor forces for given Step, or None if not present

        :param opt_step: The Optimization step, defaults to 1
        :param trans_step: Transient step, defaults to 1
        :return: The Conductor forces as Dataframe
        """
        if trans := self.find_transstep(opt_step, trans_step):
            return trans.conductorForces
        else:
            return None

    def get_crosssection_plot(self, plot_nr: int = 1) -> Optional[Plot2D]:
        """Return the Crossection 2D plot with number i

        :param plot_nr: The plot_number, defaults to 1
        :return: The Plot2D object, or None
        """
        for pl in self.plots2D:
            if isinstance(pl, Plot2D) and pl.id == plot_nr:
                return pl
        return None

    def get_3d_plot(self, plot_nr: int = 1) -> Optional[Plot3D]:
        """Return the 3D plot with number i
        :param plon_nr: The plot number, defaults to 1
        :return: The Plot3D definition, or None
        """
        for pl in self.plots3D:
            if isinstance(pl, Plot3D) and pl.id == plot_nr:
                return pl
        return None
