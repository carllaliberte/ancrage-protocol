/**
 * ML-KEM-768 is Opt-In and not present in this tree.
 * Never writes juge.v0.json or flux.v0.json.
 * Never claims a FIPS 203 encapsulation without an implementation.
 */
const FORBIDDEN = /(^|\/)(juge|flux)\.v0\.json$/;

export class PostQuantumCryptoRail {
  constructor({ optIn = false } = {}) {
    this.optIn = optIn === true;
  }

  encapsulate() {
    if (!this.optIn) {
      return {
        ok: false,
        code: "OPT_IN_REQUIRED",
        kem: null,
        write: "DENIED",
      };
    }
    return {
      ok: false,
      code: "PQC_NOT_PRESENT",
      kem: "ML-KEM-768",
      hold: "HUMAN — no local FIPS 203 module",
      write: "DENIED",
    };
  }

  write(path) {
    const p = String(path || "").replace(/\0/g, "");
    if (/(juge|flux)\.v0\.json/i.test(p)) {
      return { ok: false, code: "IMMUTABLE_V0", path: p, write: "DENIED" };
    }
    return { ok: false, code: "AI_WRITE_DENIED", path: p, write: "DENIED" };
  }
}
