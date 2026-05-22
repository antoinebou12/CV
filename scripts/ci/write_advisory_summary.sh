#!/usr/bin/env bash
# Append an advisory CI report block to GITHUB_STEP_SUMMARY (or stdout).
# Usage: write_advisory_summary.sh "Title" "tool name" outcome [log_file]
set -euo pipefail

title="$1"
tool="$2"
outcome="$3"
log_file="${4:-}"

summary="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

{
  echo "## ${title} (advisory)"
  echo ""
  echo "| | |"
  echo "|---|---|"
  echo "| Tool | ${tool} |"
  echo "| Step outcome | **${outcome}** |"
  echo "| Blocks CI | No |"
  echo ""
  if [ "${outcome}" = "failure" ]; then
    echo "Issues were found. Review the step log above; this check does not fail the workflow."
  elif [ "${outcome}" = "success" ]; then
    echo "No issues reported."
  else
    echo "Step outcome: ${outcome}."
  fi
  if [ -n "${log_file}" ] && [ -f "${log_file}" ]; then
    echo ""
    echo "<details><summary>Tool output (last 100 lines)</summary>"
    echo ""
    echo '```text'
    tail -n 100 "${log_file}"
    echo '```'
    echo "</details>"
  fi
} >> "${summary}"
