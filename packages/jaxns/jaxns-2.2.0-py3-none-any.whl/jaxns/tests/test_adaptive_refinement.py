# import tensorflow_probability.substrates.jax as tfp
# from jax import random, numpy as jnp
#
# from jaxns import collect_samples
# from jaxns.internals.log_semiring import LogSpace
# from jaxns.model import Model
# from jaxns.nested_sampler import ApproximateNestedSampler
# from jaxns.prior import PriorModelGen, Prior
# from jaxns.static_uniform import BadUniformSampler
# from jaxns.tests.test_nested_sampler import compute_shrinkage_stats
# from jaxns.types import TerminationCondition
#
# tfpd = tfp.distributions
#
#
# def test_adaptive_refinement():
#     n = 2
#
#     # Prior is uniform in U[0,1]
#     # Likelihood is 1 - x**n
#     # Z = 1 - 1/n+1
#
#     log_Z_true = jnp.log(1. - 1. / (n + 1))
#     print(f"True log(Z): {log_Z_true}")
#
#     def prior_model() -> PriorModelGen:
#         x = yield Prior(tfpd.Uniform(low=0, high=1))
#         return x
#
#     def log_likelihood(x):
#         return (LogSpace(0.) - LogSpace(n * jnp.log(x))).log_abs_val
#
#     def exact_X(L):
#         return (1. - L) ** (1. / n)
#
#     def exact_L(X):
#         return 1. - X ** n
#
#     model = Model(prior_model=prior_model,
#                   log_likelihood=log_likelihood)
#     ns = ApproximateNestedSampler(
#         model=model,
#         num_live_points=50,
#         num_parallel_samplers=1,
#         max_samples=1e6,
#         sampler_chain=[
#             BadUniformSampler(mis_fraction=0., model=model)
#         ]
#     )
#
#     total_state = None
#     for seed in [42, 43, 44]:
#         termination_reason, state = ns(random.PRNGKey(seed),
#                                        term_cond=TerminationCondition(live_evidence_frac=1e-4))
#         termination_reason.block_until_ready()
#         if total_state is None:
#             total_state = state
#         else:
#             total_state = collect_samples(state=total_state, new_reservoir=state.sample_collection.reservoir)
#     results = ns.to_results(total_state, termination_reason)
#     ns.summary(results)
#     ns.plot_diagnostics(results)
#
#     # ensure there is no bug in control flow. X should be same to controlled evaluation
#     log_X_mean, log_X_std = compute_shrinkage_stats(results.num_live_points_per_sample)
#     assert jnp.allclose(results.log_X_mean, log_X_mean)
#
#     # ensure the deviation from the exact shrinkage is correct
#     X_exact = exact_X(jnp.exp(results.log_L_samples))
#
#     rel_diff = jnp.abs(jnp.exp(log_X_mean) - X_exact) / jnp.exp(log_X_std)
#
#     # ensure log_Z is close to truth
#     assert jnp.isclose(results.log_Z_mean, log_Z_true, atol=results.log_Z_uncert * 1.75)
#
#     print("Relative shrinkage errors", jnp.percentile(rel_diff, jnp.asarray([50, 75, 90, 95])))
#     assert jnp.all(jnp.percentile(rel_diff, jnp.asarray([50, 75, 90, 95])) < jnp.asarray([0.9, 1.1, 1.4, 1.5]))
