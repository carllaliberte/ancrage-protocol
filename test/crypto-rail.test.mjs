import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { readFileSync, existsSync } from "node:fs";
import { PostQuantumCryptoRail } from "../src/crypto-rail.mjs";

describe("PQC rail — opt-in, never mutates v0", () => {
  it("refuses juge.v0 and flux.v0 and does not fake KEM", () => {
    const off = new PostQuantumCryptoRail({ optIn: false });
    assert.equal(off.encapsulate().code, "OPT_IN_REQUIRED");
    const on = new PostQuantumCryptoRail({ optIn: true });
    const enc = on.encapsulate();
    assert.equal(enc.ok, false);
    assert.equal(enc.code, "PQC_NOT_PRESENT");
    assert.equal(on.write("schema/juge.v0.json").code, "IMMUTABLE_V0");
    assert.equal(on.write("schema/flux.v0.json").code, "IMMUTABLE_V0");
    assert.equal(on.write("README.md").code, "AI_WRITE_DENIED");
    if (existsSync("schema/ancrage.v0.json")) {
      const raw = readFileSync("schema/ancrage.v0.json", "utf8");
      assert.doesNotMatch(raw, /ML-KEM-768/);
    }
  });
});
