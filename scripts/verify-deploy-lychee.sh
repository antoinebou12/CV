#!/usr/bin/env bash
# Local/CI sanity check: Hugo emits /REPO/blog/...; lychee needs --root-dir and _site/REPO/blog symlink.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
# Default under repo so Windows lychee.exe accepts the path (avoid MSYS-only /tmp).
ROOT="${1:-${REPO_ROOT}/.lychee-deploy-verify}"
REPO="${2:-CV}"
LYCHEE="${LYCHEE:-lychee}"
cleanup() { rm -rf "${ROOT}"; }
if [[ -z "${1:-}" ]]; then
  trap cleanup EXIT
fi

mkdir -p "${ROOT}/blog"
cd "${REPO_ROOT}"
hugo --gc --minify -s hugo -d "${ROOT}/blog" -b "https://antoineboucher.info/${REPO}/blog/"
touch "${ROOT}/favicon.ico"
# Match deploy.yml: published assets under _site root (lychee resolves /REPO/... via symlinks below).
if [[ -f "${REPO_ROOT}/cv-en/resume.pdf" ]] && [[ -f "${REPO_ROOT}/cv-fr/resume.pdf" ]]; then
  mkdir -p "${ROOT}/cv-en" "${ROOT}/cv-fr"
  cp -f "${REPO_ROOT}/cv-en/resume.pdf" "${ROOT}/cv-en/resume.pdf"
  cp -f "${REPO_ROOT}/cv-fr/resume.pdf" "${ROOT}/cv-fr/resume.pdf"
else
  echo "warning: missing cv-en/resume.pdf or cv-fr/resume.pdf; internal /cv-*/ links may fail in lychee (CI deploy requires both)" >&2
fi
if [[ -f "${REPO_ROOT}/letters/en/cover-letter.pdf" ]] && [[ -f "${REPO_ROOT}/letters/fr/cover-letter.pdf" ]]; then
  mkdir -p "${ROOT}/letters/en" "${ROOT}/letters/fr"
  cp -f "${REPO_ROOT}/letters/en/cover-letter.pdf" "${ROOT}/letters/en/cover-letter.pdf"
  cp -f "${REPO_ROOT}/letters/fr/cover-letter.pdf" "${ROOT}/letters/fr/cover-letter.pdf"
fi
for d in css linktree papers; do
  if [[ -d "${REPO_ROOT}/${d}" ]]; then
    cp -r "${REPO_ROOT}/${d}" "${ROOT}/"
  fi
done
mkdir -p "${ROOT}/${REPO}"
ln -sfn "../blog" "${ROOT}/${REPO}/blog"
ln -sfn "../favicon.ico" "${ROOT}/${REPO}/favicon.ico"
for d in cv-en cv-fr letters css linktree papers; do
  if [[ -d "${ROOT}/${d}" ]]; then
    ln -sfn "../${d}" "${ROOT}/${REPO}/${d}"
  fi
done

echo "Running lychee from ${REPO_ROOT} on ${ROOT} (relative paths; required on Windows lychee + OneDrive) ..."
(
  cd "${REPO_ROOT}"
  rel="${ROOT#"${REPO_ROOT}/"}"
  "${LYCHEE}" --no-progress --max-retries 3 --max-concurrency 8 --max-redirects 20 --accept 301,302,303,307,308,403,429,999 --root-dir "./${rel}" "./${rel}"
)
echo "lychee OK"
