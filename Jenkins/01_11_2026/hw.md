***********************************************************


Capstone Objectives

Synthesize all concepts learned in Hours 1–8 by provisioning and executing a self-healing parallel processing engine named lesson7-capstone-pipeline.
Laboratory Specifications

	Provisioning: Deployed headlessly via Groovy using /scriptText.
    
	Parameters:
	SERVICE_COUNT: String parameter (Default: 3).
	SIMULATE_FAILURE: String parameter (Default: false).
	Execution Logic (set -euo pipefail):
	Process Cleanup Trap: Bind an EXIT trap to kill lingering background subshell PIDs.
	Parallel Processing: Launch ${SERVICE_COUNT} background subshell workers in parallel.
	Transient Retries: Each worker attempts service synchronization using a retry loop (3 attempts maximum). If SIMULATE_FAILURE=true, worker 2 exceeds its retry limit.
	Timeout Watchdog: Run a parallel watchdog process to ensure no subshell exceeds a 5-second runtime window.
	Fallback Routing: If any worker subshell fails completely, trigger a global fallback recovery routine that writes an emergency status file (./build_out/emergency.json) and flags the build appropriately.
REST Workspace Verification: Query and display the generated status manifest over HTTP via /ws/.




Extension Challenge: Multithreaded Log Aggregator & Health Auditing

•	Prerequisites: Completion of Lesson 7 Capstone (lesson7-capstone-pipeline).
•	Objective: Provision an independent auditing job named lesson7-audit-aggregator that launches parallel worker processes, captures individual stdout/stderr log files in real-time, generates an aggregated MD5 integrity audit manifest, and exposes all outputs over the REST API.

Challenge Requirements
1.	Job Setup:
o	Job Name: lesson7-audit-aggregator
o	Type: FreeStyleProject
o	Parameters:
	WORKER_COUNT: String parameter (Default: 4)
	SIMULATE_LATENCY: String parameter (Default: true)
2.	Execution Script (set -euo pipefail):
o	Signal Handler Trap: Register an EXIT signal trap that executes cleanup() to kill any dangling subshell PIDs stored in a Bash array.
o	Parallel Execution & File Redirection: Spawns ${WORKER_COUNT} parallel subshells. Each worker:
	Writes stdout logs directly to ./logs/worker_${ID}.log.
	Simulates work (if SIMULATE_LATENCY=true, sleeps for a random duration between 1 and 3 seconds).
	Writes an individual status JSON payload to ./logs/worker_${ID}.json:
JSON
{
  "worker_id": "<ID>",
  "pid": "<PID>",
  "status": "COMPLETED"
}
o	Synchronization & Failure Gate:
	Use a wait loop across all stored PIDs to confirm clean completion.
	If any subshell fails, log the failing PID to stderr and flag the pipeline.
o	Aggregated Manifest Generation:
	Merge all individual JSON payloads into a single runtime manifest: ./build_out/audit_summary.json.
	Compute an MD5 checksum of ./build_out/audit_summary.json and save it to ./build_out/audit_summary.json.md5.
o	Console Output: Print the aggregated summary manifest and the MD5 hash digest.