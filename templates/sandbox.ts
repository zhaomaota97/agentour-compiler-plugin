// Agentour Platform — sandbox.ts (REQUIRED)
// Must pin justbash(). Without this, eve may probe microsandbox
// and fail to start. This file is non-negotiable.
import { defineSandbox } from "eve/sandbox";
import { justbash } from "eve/sandbox/just-bash";

export default defineSandbox({ backend: justbash() });
