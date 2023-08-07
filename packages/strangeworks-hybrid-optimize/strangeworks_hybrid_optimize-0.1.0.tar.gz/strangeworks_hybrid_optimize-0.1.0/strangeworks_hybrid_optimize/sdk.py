import json
from typing import Optional

import dimod
import networkx as nx
import numpy as np
import qiskit
import strangeworks
from strangeworks.core.errors.error import StrangeworksError

import strangeworks_hybrid_optimize.utils as utils


class StrangeworksHybrid:
    """Strangeworks client object."""

    def __init__(self, resource_slug: Optional[str] = " ") -> None:
        self.product_slug = "77a5lhukf"

        try:
            if resource_slug != " " and resource_slug != "":
                self.rsc = strangeworks.resources(slug=resource_slug)[0]
            else:
                rsc_list = strangeworks.resources()
                for rr in range(len(rsc_list)):
                    if rsc_list[rr].product.slug == self.product_slug:
                        self.rsc = rsc_list[rr]
            if self.rsc is None:
                raise StrangeworksError(
                    "Unable to find resource. Please add resource on platform https://portal.strangeworks.com/products"  # noqa: E501
                )
        except Exception as e:
            raise StrangeworksError(
                f"Unable to find resource. Please add resource on platform https://portal.strangeworks.com/products: {e}"  # noqa: E501
            )

        self.backend_list = " "

    def add_sub_resource_credentials(self, resource_slug):
        self.sub_rsc = strangeworks.resources(slug=resource_slug)[0]

        return self.sub_rsc.product.name

    def backends(self):

        all_backends = strangeworks.backends(backend_type_slugs=["sw-qaoa"])

        aws_backends = []
        aws_sim_backends = []
        ibmq_backends = []
        ibm_cloud_backends = []
        ibm_sim_backends = []
        for bb in range(len(all_backends)):
            try:
                arn_str = all_backends[bb].remote_backend_id[0:3]
                # print(arn_str)
                if arn_str == "arn" and all_backends[bb].remote_status != "retired":
                    if (
                        all_backends[bb].name == "SV1"
                        or all_backends[bb].name == "TN1"
                        or all_backends[bb].name == "dm1"
                    ):
                        backend_temp = {
                            "name": all_backends[bb].name,
                            "provider": "AWS_Simulator",
                            "remote_status": all_backends[bb].remote_status,
                            "arn": all_backends[bb].remote_backend_id,
                        }
                        aws_sim_backends.append(backend_temp)
                    else:
                        backend_temp = {
                            "name": all_backends[bb].name,
                            "provider": "AWS",
                            "remote_status": all_backends[bb].remote_status,
                            "arn": all_backends[bb].remote_backend_id,
                        }
                        aws_backends.append(backend_temp)
            except AttributeError:
                None

            try:
                ibm_str = all_backends[bb].name[0:3]
                id_str = all_backends[bb].remote_backend_id[0:3]
                if ibm_str == "ibm":
                    if id_str == "ibm":
                        prov = "IBM_Cloud"
                        backend_temp = {
                            "backend_name": all_backends[bb].name,
                            "provider": prov,
                            "remote_status": all_backends[bb].remote_status,
                        }
                        ibm_cloud_backends.append(backend_temp)
                    else:
                        if all_backends[bb].name == "ibmq_qasm_simulator":
                            prov = "IBM_Simulator"
                            backend_temp = {
                                "backend_name": all_backends[bb].name,
                                "provider": prov,
                                "remote_status": all_backends[bb].remote_status,
                            }
                            ibm_sim_backends.append(backend_temp)
                        else:
                            prov = "IBMQ"
                            backend_temp = {
                                "backend_name": all_backends[bb].name,
                                "provider": prov,
                                "remote_status": all_backends[bb].remote_status,
                            }
                            ibmq_backends.append(backend_temp)
                elif ibm_str == "sim":
                    prov = "IBM_Simulator"
                    backend_temp = {
                        "backend_name": all_backends[bb].name,
                        "provider": prov,
                        "remote_status": all_backends[bb].remote_status,
                    }
                    ibm_sim_backends.append(backend_temp)
            except AttributeError:
                None

        opt_backends = strangeworks.backends(backend_type_slugs=["optimization"])

        self.backend_list = {
            "AWS": aws_backends,
            "AWS_Sim": aws_sim_backends,
            "IBMQ": ibmq_backends,
            "IBM_Cloud": ibm_cloud_backends,
            "IBM_Sim": ibm_sim_backends,
            "Optimization": opt_backends,
        }

        return self.backend_list

    def run(
        self,
        backend,
        problem,
        hybrid_params,
        problem_params,
        backend_sub: Optional[str] = None,
    ):
        """
        Method to submit QAOA problem to backend.

        Parameters:
            backend (str): Backend name for the final QAOA optimization step. Must be a
            gate based device.

            problem:
                Hamiltonian whose ground state we want to find.
                Can be either a networkx graph, a qiskit PauliSumOp operator, a QUBO
                Matrix or a Dwave BinaryQuadraticModel.

            hybrid_params (Dict): Dictionary of hybrid parameters for the problem:
                Nf (int): Size of final vqe
                Ns (int): Number of sub-systems: Upper bound = np.pow(2, Nf)
                Ng (int): Size of sub-systems
                problem_size (int): Number of qubits in the problem
                type_subsystem (str): Type of subsystems to use. Options are:
                    'random', 'weighted_random', 'kernighan_lin_bisection'
                maxiter (int): max number of iteration loops in minimisation
                shotsin (int): number of shots. Number of times quantum circuit is
                    run and measured

            problem_params (Dict): Dictionary of sub problem parameters for the problem
            with two construction choice. 1) the parameters for a StrangeworksQAOA job
            or 2) the parameters for a StrangeworksOptimization job:
                1) StrangeworksQAOA job parameters:
                    shotsin (int): number of shots. Number of times quantum circuit is
                    run and measured
                    maxiter (int): max number of iteration loops in minimisation
                    p (int): Optional. Number of repetitions in qaoa ansatz
                    alpha (float): Optional. Parameter between 0 and 1, which controls
                    the CVar expectation value,
                                    - https://arxiv.org/pdf/1907.04769.pdf
                                    alpha = 1, usual expectation value
                                    alpha < 1, modified expectation value for quantum
                                    simulation with classical outputs
                    theta0 (array): Optional, initial vector of parameters.
                    optimizer (str): Optional, string specifying classical optimizer,
                                    default='COBLYA'.
                    ansatz (str or QuantumCircuit): Optional, Variational circuit
                                                    parametrized with coefficients to
                                                    optimise for the energy
                    ising (bool): Optional, If True then the input problem is treated as
                                        an Ising problem. If False or unspecified, then
                                        the input problem is treated as a QUBO problem.
                    problem_type (str): Optional, If the problem is a quantum encoding
                        of a classical problem (i.e. the solution is one of the basis
                        states) then we can make some simplifications and employ
                        some tricks to make the algorithm potentially more optimal.
                    optimization_level: IBM only. How much optimization to perform on
                        the circuits. Higher levels generate more optimized circuits,
                        at the expense of longer transpilation times. This
                        is based on the ``optimization_level`` parameter in
                        qiskit-terra but may include backend-specific
                        optimization. Default: 1.

                                        * 0: no optimization
                                        * 1: light optimization
                                        * 2: heavy optimization
                                        * 3: even heavier optimization

                    resilience_level: IBM only. How much resilience to build against
                        errors. Higher levels generate more accurate results, at the
                        expense of longer processing times. Default: 1.

                                        * 0: No mitigation.
                                        * 1: Minimal mitigation costs. Mitigate error
                                        associated with readout errors.
                                        * 2: Medium mitigation costs. Typically reduces
                                        bias in estimators but is not guaranteed to be
                                        zero bias. Only applies to estimator.
                                        * 3: Heavy mitigation with layer sampling.
                                        Theoretically expected to deliver zero bias
                                        estimators. Only applies to estimator.
                2) StrangeworksOptimization job parameters:
                    var_type (str): Variable type of the problem. Either 'BINARY' or
                    lagrange_multiplier (float): Lagrange multiplier for the problem.
                    solver (Dict): Dictionary of solver parameters:
                        solver (str): Name of the solver to use. Must be one of the
                            available solvers for the backend.
                        solver_options (Dict): Dictionary of solver options.

        Returns:
            Strangeworks Job object
        """

        if self.backend_list == " ":
            self.backends()

        aws = False
        ibm = False
        backend_sub_id = backend_sub  # For the optimzers
        for nn in range(len(self.backend_list["AWS"])):
            if (
                self.backend_list["AWS"][nn]["name"] == backend
                or self.backend_list["AWS"][nn]["arn"] == backend
            ):
                aws = True
                backend_id = self.backend_list["AWS"][nn]["arn"]
            if (
                self.backend_list["AWS"][nn]["name"] == backend_sub
                or self.backend_list["AWS"][nn]["arn"] == backend_sub
            ):
                aws = True
                backend_sub_id = self.backend_list["AWS"][nn]["arn"]

        for nn in range(len(self.backend_list["IBMQ"])):
            if self.backend_list["IBMQ"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_quantum"
                backend_id = self.backend_list["IBMQ"][nn]["backend_name"]
            if self.backend_list["IBMQ"][nn]["backend_name"] == backend_sub:
                ibm = True
                channel = "ibm_quantum"
                backend_sub_id = self.backend_list["IBMQ"][nn]["backend_name"]

        for nn in range(len(self.backend_list["IBM_Cloud"])):
            if self.backend_list["IBM_Cloud"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_cloud"
                backend_id = self.backend_list["IBM_Cloud"][nn]["backend_name"]
            if self.backend_list["IBM_Cloud"][nn]["backend_name"] == backend_sub:
                ibm = True
                channel = "ibm_cloud"
                backend_sub_id = self.backend_list["IBM_Cloud"][nn]["backend_name"]

        for nn in range(len(self.backend_list["AWS_Sim"])):
            if (
                self.backend_list["AWS_Sim"][nn]["name"] == backend
                or self.backend_list["AWS_Sim"][nn]["arn"] == backend
            ):
                aws = True
                backend_id = self.backend_list["AWS_Sim"][nn]["arn"]
            if (
                self.backend_list["AWS_Sim"][nn]["name"] == backend_sub
                or self.backend_list["AWS_Sim"][nn]["arn"] == backend_sub
            ):
                aws = True
                backend_sub_id = self.backend_list["AWS_Sim"][nn]["arn"]

        for nn in range(len(self.backend_list["IBM_Sim"])):
            if self.backend_list["IBM_Sim"][nn]["backend_name"] == backend:
                ibm = True
                channel = "ibm_quantum"
                backend_id = self.backend_list["IBM_Sim"][nn]["backend_name"]
            if self.backend_list["IBM_Sim"][nn]["backend_name"] == backend_sub:
                ibm = True
                channel = "ibm_quantum"
                backend_sub_id = self.backend_list["IBM_Sim"][nn]["backend_name"]

        if ibm is False and aws is False:
            raise StrangeworksError("Unable to Find Backend")

        # Check which format the problem is specified in and convert to the form which
        # our QUBO solver can accept.
        if type(problem) == nx.classes.graph.Graph:
            H = utils.get_Ham_from_graph(problem)
        elif type(problem) == qiskit.opflow.primitive_ops.pauli_sum_op.PauliSumOp:
            H = utils.get_Ham_from_PauliSumOp(problem)
        elif type(problem) == np.ndarray:
            H = utils.get_Ham_from_QUBO(problem)
        elif (
            type(problem) == dict
            and problem.get("BQM") is not None
            and type(problem.get("BQM"))
            == dimod.binary.binary_quadratic_model.BinaryQuadraticModel
        ):
            QUBO = problem["BQM"].to_numpy_matrix(
                variable_order=problem.get("variable_order")
            )
            H = utils.get_Ham_from_QUBO(QUBO)
        else:
            raise StrangeworksError("Problem not in currently supported format")

        for _, y in H:
            if type(y) is tuple:
                for n in y:
                    if n > (hybrid_params["problem_size"] - 1):
                        raise StrangeworksError(
                            "Specified qubit number is smaller than problem"
                        )
            else:
                if y > (hybrid_params["problem_size"] - 1):
                    raise StrangeworksError(
                        "Specified qubit number is smaller than problem"
                    )

        hybrid_params["H"] = json.dumps(H)
        problem_params["ising"] = (
            json.dumps(problem_params["ising"])
            if problem_params.get("ising")
            else json.dumps(False)
        )
        problem_params["warm_start"] = (
            json.dumps(problem_params["warm_start"])
            if problem_params.get("warm_start")
            else json.dumps(False)
        )

        if aws is True:
            input_params = {
                "provider": "aws",
                "backend": backend_id,
                "backend_sub": backend_sub_id,
                "hyperparams": json.dumps(problem_params),
                "hybrid_params": json.dumps(hybrid_params),
                "resource_slug": self.sub_rsc.slug,
                "product_slug": self.sub_rsc.product.slug,
            }
        elif ibm is True:
            input_params = {
                "provider": "ibm",
                "channel": channel,
                "backend": backend_id,
                "backend_sub": backend_sub_id,
                "hyperparams": json.dumps(problem_params),
                "hybrid_params": json.dumps(hybrid_params),
                "resource_slug": self.sub_rsc.slug,
                "product_slug": self.sub_rsc.product.slug,
            }

        sw_job = strangeworks.execute(self.rsc, input_params, "run_hybrid_job")

        return sw_job

    def get_job(self, sw_job):
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        elif type(sw_job) is str:
            job_slug = sw_job
        else:
            job_slug = sw_job.slug

        status = strangeworks.execute(self.rsc, {"job_slug": job_slug}, "status")

        # from strangeworks.core.client.jobs import Job

        # status["resource"] = {"slug": self.rsc.slug, }
        # Resource(
        #     slug=d.get("slug"),
        #     status=d.get("status"),
        #     name=d.get("name"),
        #     product=Product.from_dict(d.get("product")),
        #     is_deleted=d.get("isDeleted"),
        # )
        # sw_job = Job.from_dict(status)
        return status

    def get_results(self, sw_job, calculate_exact_sol=False, display_results=False):
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
            sw_job = sw_job = strangeworks.jobs(slug=job_slug)[0]
        elif type(sw_job) is str:
            job_slug = sw_job
            sw_job = sw_job = strangeworks.jobs(slug=job_slug)[0]
        else:
            job_slug = sw_job.slug

        if sw_job.status == "COMPLETED" or self.update_status(job_slug) == "COMPLETED":
            result_url = None
            inputs_url = None
            for f in sw_job.files:
                if f.file_name == "result.json":
                    result_url = f.url
                elif f.file_name == "inputs.json":
                    inputs_url = f.url
            if result_url:
                result_file = strangeworks.download_job_files([result_url])[0]
        else:
            return sw_job.status

        if calculate_exact_sol:
            inputs = strangeworks.download_job_files([inputs_url])[0]

            H = json.loads(inputs["H"])
            nqubits = int(inputs["problem_size"])

            try:
                En_exact = utils.get_exact_en(
                    utils.get_graph_from_Ham(H, nqubits),
                    nqubits,
                    ising=json.loads(inputs["ising"]) if inputs.get("ising") else False,
                )
                result_file["En_exact"] = En_exact
            except Exception as e:
                print(f"Error with calculating exact solution: {e}")
                result_file["En_exact"] = f"Error with calculating exact solution: {e}"
        else:
            result_file["En_exact"] = None

        if display_results:
            sol = result_file["sol"]
            En_exact = result_file["En_exact"]
            En_sol = result_file["en_min"]
            En_av = result_file["en"][len(result_file["en"]) - 1]

            print(
                f"The average energy (expectation value) of the final state is {En_av}"
            )
            print(f"The solution found by the algorithm is: {sol}")
            print(f"The energy of the solution found by the algorithm is {En_sol}")
            print(f"The exact optimal energy is {En_exact}")

        return result_file

    def job_list(self):
        job_list = strangeworks.jobs(resource_slugs=self.rsc.slug)

        qaoa_job_list = []
        for jj in range(len(job_list)):
            if job_list[jj].resource.product.slug == self.product_slug:
                if job_list[jj].external_identifier[0:3] == "arn":
                    prov = "AWS"
                else:
                    prov = "IBM"

                status = job_list[jj].status

                temp = {
                    "slug": job_list[jj].slug,
                    "Status": status,
                    "Provider": prov,
                    "resource_slug": job_list[jj].resource.slug,
                }
                qaoa_job_list.append(temp)

        return qaoa_job_list
